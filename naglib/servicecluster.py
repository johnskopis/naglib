#!/usr/bin/env python
import config
import registry

from service import Service

""" A representation of a nagios service cluster"""

class ServiceCluster(Service):
    def __init__(self, service, cluster_name, **kwargs):
        self.props = dict()
        self._registry_prefix = None

        if kwargs.get('props', None):
            self.props.update(kwargs['props'])
            del kwargs['props']

        #if kwargs.get('host', None):
        #    del kwargs['host']

        self.warn_threshold = kwargs.get('warn', 10)
        self.crit_threshold = kwargs.get('crit', 20)
        self.cluster = "cluster_%s" % cluster_name


        self.props['host_name'] = "vip-%s" % self.cluster
        self.props['service_description'] = self.cluster
        self.props['check_command'] = "check_%s" % self.cluster

        super(ServiceCluster, self).__init__(**kwargs)


        print self.props

    @property
    def identity(self):
        return self.cluster


class LazyServiceCluster(object):
    def __init__(self, service, **kwargs):
        self.clustergroup = service
        self.kwargs = kwargs
        registry.Registry().register(self, warn=False)

    @property
    def identity(self):
        return self.clustergroup
