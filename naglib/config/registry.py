import os
#import host, servicegroup, command, servicedependency, serviceescalation, servicecluster, service
from naglib.config.host import Host, HostTemplate
from naglib.config.service import *
from naglib.config.servicegroup import *
from naglib.config.serviceescalation import *
from naglib.config.command import *
import naglib.utils as utils
import shutil

from sets import Set
from collections import defaultdict

class Registry(object):
    __metaclass__ = utils.Singleton

    PATHS = dict(host_templates = 'templates/host',
                 hosts = 'hosts',
                 service_templates = 'templates/service',
                 services = 'services',
                 service_groups = 'service_groups',
                 service_dependencies = 'service_dependencies',
                 service_escalations = 'service_escalations',
                 service_clusters = 'service_clusters',
                 commands = 'commands',
                 )

    TYPES = (
        ('host_templates', HostTemplate),
        ('service_templates', ServiceTemplate),
        ('hosts', Host),
        ('services', Service),
        ('service_clusters', ServiceCluster),
        ('service_groups', ServiceGroup),
        ('service_dependencies', ServiceDependency),
        ('service_escalations', ServiceEscalation),
        ('commands', Command),
    )

    PREFIX = 'fixtures'
    OUTPUT_DIR = 'build'

    def __new__(cls):
        return object.__new__(cls)

    def __init__(self):
        self.hosts = dict()
        self.host_templates = dict()
        self.services = dict()
        self.service_templates = dict()
        self.service_groups = dict()
        self.service_dependencies = dict()
        self.service_escalations = dict()
        self.service_clusters = dict()
        self.commands = dict()
        self.lazy_service_clusters = dict()

    def register(self, obj, warn=True):
        registry = getattr(self, self.class2attr(obj.__class__))
        if registry.get(obj.identity, None):
            if warn:
                print "WARN: attempting to register %s(%s) again" % (obj.__class__.__name__,
                                                                    obj.identity)
            return

        registry[obj.identity] = obj

    def class2attr(self, obj):
        return utils.pluralize(utils.underscoreize(obj.__name__))

    def resolve_template(self, cls, name):
        attr_name = self.class2attr(cls)
        registry = getattr(self, attr_name)

        if registry.get(name, None):
            return registry.get(name, None)
        else:
            tpl = cls.from_file(self, self.path_for(attr_name, "%s.cfg" % name))
            self.register(tpl, warn=False)
            return tpl

    def resolve_all(self):
        for kind, cls in self.TYPES:
            path =  os.path.join(self.PREFIX, self.PATHS[kind])
            for cur_dir, subdirs, files in os.walk(path):
                for f in files:
                    cls.from_file(self, os.path.join(cur_dir, f))

    def validate_all(self):
        for attr, cls in self.TYPES:
            if not all([o.validate_params() for o in getattr(self, attr).values()]):
                raise Exception("failed validation")

        #return all([h.validate_params() for h in self.hosts.values()]) and\
        #    all([s.validate_params() for s in self.services.values()])


    def path_for(self, kind, name):
        path = os.path.join(self.PREFIX, self.PATHS[kind])
        f = utils.find(path, name)
        if not f:
            raise Exception("could not find path for %s in %s" % (name, path))

        if len(f) > 1:
            print "Warning, we found 2 paths for %s, we are using %s" % (name, f[0])

        return f[0]


    def hosts_by_group(self, group):
        return [h for h in self.hosts.values() if h.use == group]

    def write_all(self):
        if os.path.isdir(self.OUTPUT_DIR):
            shutil.rmtree(self.OUTPUT_DIR)

        os.mkdir(self.OUTPUT_DIR)

        self._write('host_templates', self.host_templates)
        self._write('service_templates', self.service_templates)
        self._write('hosts', self.hosts)
        self._write('services', self.services)
        self._write('service_groups', self.service_groups)
        self._write('service_dependencies', self.service_dependencies)
        self._write('service_escalations', self.service_escalations)
        self._write('service_clusters', self.service_clusters)
        self._write('commands', self.commands)

    def _write(self, kind, data):
        os.mkdir(os.path.join(self.OUTPUT_DIR, kind)) # e.g. build/hosts

        for d in filter(None, Set(map(os.path.dirname, data.keys()))):
            os.makedirs(os.path.join(self.OUTPUT_DIR, kind, d)) # e.g. build/hosts/datacenter1

        for name, obj in data.iteritems():
            cfg_file = "%s.cfg" % obj.identity

            if obj._registry_prefix:
                path = os.path.join(self.OUTPUT_DIR, kind, obj._registry_prefix)
            else:
                path = os.path.join(self.OUTPUT_DIR, kind)

            if not os.path.exists(path):
                os.makedirs(path)
            with open(os.path.join(path, cfg_file), 'w') as fd:
                fd.write(obj.render())


    def generate_servicegroups(self):
        """For service 'foobar' running in datacenters datacenter1, and datacenter2, with a parent
        service 'foo' create the following service groups:
            foobar.datacenter1: foobar service only in dc1
            foobar.datacenter2: foobar service only in dc2
            foobar: foobar service in all datacenters
            foo.datacenter1: [foo, foobar] service in dc1
            foo.datacenter2: [foo, foobar] service in dc2
            foo: [foo, foobar] services
        """

        self._sg = defaultdict(list)
        for s in self.services.values():
            ss = s.template
            while ss != None:
                if not ss.service_description:
                    break
                k =  "%s.%s" % (ss.service_description, s.host._datacenter)
                self._sg[k].append(s)
                self._sg[ss.service_description].append(s)
                ss = ss.template

        for s, members in self._sg.iteritems():
            m = ','.join(["%s,%s" % (ss.host_name, ss.service_description) for ss in members])
            ServiceGroup(servicegroup_name=s, members=m, registry=self)

    def generate_clusters(self):
        """A cluster is basically a check of a service group. However, a cluster check only checks
        the services that comprise the cluster, not the inherited services. Given the services: foo,
        foobar, where foobar inherits from foo, a cluster check of foo will only check foo, not
        foobar."""

        sc = defaultdict(list)

        for s in self.services.values():
            k = "%s.%s" % (s.service_description, s.host._datacenter)
            sc[k].append(s)
            sc[s.service_description].append(s)

        for cluster_identity, cluster in self.lazy_service_clusters.iteritems():
            for sg, services in sc.iteritems():
                if sg.startswith(cluster_identity):
                    self.generate_cluster(sg, cluster.kwargs, services)

    def generate_cluster(self, cluster_name, cluster_config, services):
        ch = Host(use='cluster',
                  host_name="vip-%s" % cluster_name,
                  registry_prefix='cluster',
                  registry=self,
                  qualified=True,
                  address='127.0.0.1')

        cluster_config['host'] = ch
        cluster = ServiceCluster(services[0],
                                 cluster_name,
                                 registry=self,
                                 **cluster_config)

        chk = ["$SERVICESTATEID:%s:%s$" % (s.host_name, s.service_description) for s in services]
        chk_str = ','.join(chk)

        Command(command_name=cluster.check_command,
                command_line="$USER1$/check_cluster -l '%(service)s' -d %(chk_str)s -w @%(warn)d: -c @%(crit)d:" % {
                    'service': cluster.service_description,
                    'chk_str': chk_str,
                    'warn': max(int(int(cluster.warn_threshold)/100.0*len(chk)), 1),
                    'crit': max(int(int(cluster.crit_threshold)/100.0*len(chk)), 2),
                },
                registry=self,)
