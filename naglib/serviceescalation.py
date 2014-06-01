#!/usr/bin/env python
import config

""" A representation of a nagios service escalation"""

class ServiceEscalation(config.BaseObject):
    TYPE = 'serviceescalation'
    TEMPLATE_CLASS = None
    PARAMS = (
        'host_name',
        'hostgroup_name',
        'service_description',
        'contacts',
        'contact_groups',
        'first_notification',
        'last_notification',
        'notification_interval',
        'escalation_period',
        'escalation_options',
    )


    @property
    def identity(self):
        return "%s/%s/%s_%s" % (
            self.service_description,
            self.host_name,
            self.contact_groups,
            self.first_notification,)

