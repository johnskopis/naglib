#!/usr/bin/env python
from base import *

""" A representation of a nagios host"""

class ServiceGroup(BaseObject):
    TYPE = 'servicegroup'
    TEMPLATE_CLASS = None
    PARAMS = (
        'servicegroup_name',
        'alias',
        'members',
        'servicegroup_members',
        'notes',
        'notes_url',
        'action_url',
    )

    REQUIRED_PARAMS = (
        'servicegroup_name',
        'members',
    )


    @property
    def identity(self):
        return self.servicegroup_name
