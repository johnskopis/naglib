#!/usr/bin/env python
from base import *

""" A representation of a nagios service dependency"""

class Command(BaseObject):
    TYPE = 'command'
    TEMPLATE_CLASS = None
    PARAMS = (
        'command_name',
        'command_line'
    )

    REQUIRED_PARAMS = PARAMS

    @property
    def identity(self):
        return self.command_name
