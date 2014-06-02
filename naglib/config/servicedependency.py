#!/usr/bin/env python
from base import *

""" A representation of a nagios service dependency"""

class ServiceDependency(BaseObject):
    TYPE = 'servicedependency'
    TEMPLATE_CLASS = None
    PARAMS = (
        'dependent_host_name',
        'dependent_hostgroup_name',
        'servicegroup_name'
        'dependent_servicegroup_name',
        'dependent_service_description',
        'host_name',
        'hostgroup_name',
        'service_description',
        'inherits_parent',
        'execution_failure_criteria',
        'notification_failure_criteria',
        'dependency_period',
    )

    @property
    def identity(self):
        return "%s/%s/%s/%s" % (
            self.service_description,
            self.host_name,
            self.dependent_service_description,
            self.dependent_host_name,)
