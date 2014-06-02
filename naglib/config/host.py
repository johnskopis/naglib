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

        self.props.update(self.get_hostname(host_name, network_site, **kwargs))
        self._registry_prefix = self._datacenter

        super(Host, self).__init__(registry=registry, **kwargs)

    @staticmethod
    def get_hostname(host_name = None, network_site = None, **kwargs):
        if network_site:
            _datacenter = network_site
        else:
            _datacenter = kwargs.get('use', 'generic-host')

        if kwargs.get('qualified', False):
            host_name = host_name
        else:
            host = host_name.split('.')[0]
            host_name = "%s.%s" % (host, _datacenter)

        if kwargs.get('alias', None):
            alias = kwargs['alias']
        else:
            alias = host_name

        return dict(host_name=host_name,
                    alias=alias,
                    _datacenter=_datacenter)

    @staticmethod
    def identity_for(**kwargs):
        host_config = Host.get_hostname(**kwargs)
        return host_config['host_name']

    @property
    def identity(self):
        return self.host_name

class HostTemplate(BaseTemplate):
    PARAMS = Host.PARAMS + ('name','register')
    TYPE = 'host'
    TEMPLATE_CLASS = 'host.HostTemplate'

