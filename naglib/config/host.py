#!/usr/bin/env python

from naglib.config.base import *

""" A representation of a nagios host"""

class Host(BaseObject):
    TYPE = 'host'
    TEMPLATE_CLASS = 'host.HostTemplate'
    PARAMS = (
        'use',
        '2d_coords',
        '3d_coords',
        'action_url',
        'active_checks_enabled',
        'address',
        'alias',
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
        'hostgroups',
        'icon_image',
        'icon_image_alt',
        'initial_state',
        'low_flap_threshold',
        'max_check_attempts',
        'notes',
        'notes_url',
        'notification_interval',
        'notification_options',
        'notification_period',
        'notifications_enabled',
        'obsess_over_host',
        'parents',
        'passive_checks_enabled',
        'process_perf_data',
        'retain_nonstatus_information',
        'retain_status_information',
        'retry_interval',
        'stalking_options',
        'statusmap_image',
        'vrml_image',
    )

    REQUIRED_PARAMS = (
        'address',
        'host_name',
        'alias',
        'max_check_attempts',
        'notification_interval',
        'notification_period',
    )

    def __init__(self, host_name, network_site = None, registry=None, **kwargs):
        self.props = dict()
        self.network_site = network_site

        if self.network_site:
            self.props['_datacenter'] = self.network_site
        else:
            self.props['_datacenter'] = kwargs.get('use', 'default')


        if kwargs.get('qualified', False):
            del kwargs['qualified']
            self.props['host_name'] = host_name
            self.props['alias'] = host_name
        else:
            host = host_name.split('.')[0]

            self.props['host_name'] = "%s.%s" % (host, self._datacenter)
            self.props['alias'] = self.props['host_name']

            self._registry_prefix = self._datacenter

        super(Host, self).__init__(registry=registry, **kwargs)


    @property
    def identity(self):
        return self.host_name

class HostTemplate(BaseTemplate):
    PARAMS = Host.PARAMS + ('name','register')
    TYPE = 'host'
    TEMPLATE_CLASS = 'host.HostTemplate'

