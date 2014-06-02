#!/usr/bin/env python
#import re
#import registry
import json
from naglib.config.base import BaseObject, BaseTemplate
from naglib.config.servicedependency import ServiceDependency
from naglib.config.serviceescalation  import ServiceEscalation

""" A representation of a nagios service"""

class Service(BaseObject):
    TYPE = 'service'
    TEMPLATE_CLASS  = 'service.ServiceTemplate'
    PARAMS = (
        'use',
        'action_url',
        'active_checks_enabled',
        'check_command',
        'check_freshness',
        'check_interval',
        'check_period',
        'contact_groups',
        'contacts',
        'display_name',
        'event_handler',
        'event_handler_enabled',
        'first_notification_delay',
        'flap_detection_enabled',
        'flap_detection_options',
        'freshness_threshold',
        'high_flap_threshold',
        'host_name',
        'hostgroup_name',
        'icon_image',
        'icon_image_alt',
        'initial_state',
        'is_volatile',
        'low_flap_threshold',
        'max_check_attempts',
        'notes',
        'notes_url',
        'notification_interval',
        'notification_options',
        'notification_period',
        'notifications_enabled',
        'obsess_over_service',
        'passive_checks_enabled',
        'process_perf_data',
        'retain_nonstatus_information',
        'retain_status_information',
        'retry_interval',
        'service_description',
        'servicegroups',
        'stalking_options',
    )

    REQUIRED_PARAMS = (
        'host_name',
        'service_description',
        'check_command',
        'max_check_attempts',
        'check_interval',
        'retry_interval',
        'check_period',
        'notification_interval',
        'notification_period',
    )


    def __init__(self, host = None, registry = None, **kwargs):
        if not self.__dict__.get('props', None):
            self.props = dict()
        self.host = host

        if self.host:
            self.props['host_name'] = self.host.host_name

        self._registry_prefix = None

        super(Service, self).__init__(registry=registry, **kwargs)

        if self._depends_on:
            if not isinstance(self._depends_on, list):
                deps = [self._depends_on]
            else:
                deps = self._depends_on

            for dep in deps:
                sd = self.load_json(dep)
                if sd:
                    if sd['host_name'] == "":
                        sd["host_name"] = self.host_name
                    sd['dependent_host_name'] = self.host_name
                    sd['dependent_service_description'] = self.service_description
                    ServiceDependency(registry=registry, **sd)

        if self._escalates_to:
            if not isinstance(self._escalates_to, list):
                escalations = [self._escalates_to]
            else:
                escalations = self._escalates_to

            for e in escalations:
                es = self.load_json(e)
                if es:
                    es['host_name'] = self.host_name
                    es['service_description'] = self.service_description
                    if not es.get('notification_interval', None):
                        es['notification_interval'] = self.check_interval
                    ServiceEscalation(registry=registry, **es)

        if self._cluster_config and not self.__class__.__name__ == 'ServiceCluster':
            if not isinstance(self._cluster_config, list):
                clusters = [self._cluster_config]
            else:
                clusters = self._cluster_config

            for c in clusters:
                sc = self.load_json(c)
                LazyServiceCluster(self.service_description, registry=registry, **sc)


    def load_json(self, s):
        j = dict()
        jj = dict()

        params = dict()
        if getattr(self, 'host', None):
            params.update(self.host.props)
        params.update(self.props)

        try:
            j = json.loads("{%s}" % s)
        except:
            print "ERROR occured parsing %s for %s" % (s, self.service_description)

        for k, v in j.iteritems():
            jj[k] = str(v) % params

        return jj


    def __getattr__(self, k):
        # This is a bit of a smell and is actually probably not even required
        sup = super(Service, self).__getattr__(k)
        if sup:
            return sup
        else:
            return getattr(self.host, k, None)

    @property
    def identity(self):
        return "%s/%s" % (self.service_description, self.host.identity)


class ServiceTemplate(BaseTemplate):
    TYPE = 'service'
    PARAMS = Service.PARAMS + ('name','register')
    TEMPLATE_CLASS  = 'service.ServiceTemplate'


class ServiceCluster(Service):
    """ A representation of a nagios service cluster"""
    def __init__(self, service, cluster_name, **kwargs):
        self.props = dict()
        self._registry_prefix = None

        if kwargs.get('props', None):
            self.props.update(kwargs['props'])
            del kwargs['props']

        self.warn_threshold = kwargs.get('warn', 10)
        self.crit_threshold = kwargs.get('crit', 20)
        self.cluster = "cluster_%s" % cluster_name


        self.props['host_name'] = "vip-%s" % self.cluster
        self.props['service_description'] = self.cluster
        self.props['check_command'] = "check_%s" % self.cluster

        super(ServiceCluster, self).__init__(**kwargs)

    @property
    def identity(self):
        return self.cluster


class LazyServiceCluster(object):
    """ We defer creation of the service cluster until all of the services are defined. """
    def __init__(self, service, registry=None, **kwargs):
        self.clustergroup = service
        self.kwargs = kwargs
        registry.register(self, warn=False)

    @property
    def identity(self):
        return self.clustergroup
