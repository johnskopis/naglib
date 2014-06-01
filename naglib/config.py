#!/usr/bin/env python
import registry
import sys
import utils

""" The base class for all of the nagios configuration objects """

class ConfigurationException(Exception):
    pass

class BaseObject(object):
    TYPE = 'base'
    PARAMS = ()
    REQUIRED_PARAMS = ()
    TEMPLATE_CLASS = None

    @classmethod
    def from_file(cls, path):
        cfg = utils.read_template_file(path)
        return cls(**cfg)

    def __init__(self, template = None, **kwargs):
        if not self.__dict__.get('props', None):
            self.props = dict()
        self.template = template

        use = kwargs.get('use', None)
        if use:
            # TODO(JS): fix
            module_name, class_name = self.TEMPLATE_CLASS.split('.')
            module_name = "naglib.%s" % module_name
            cls = getattr(sys.modules[module_name], class_name)
            self.template = registry.Registry().resolve_template(cls, use)

        for k, v in kwargs.iteritems():
            if k in self.PARAMS or k.startswith('_'):
                key = k
            else:
                key = "_%s" % k

            if not self.props.get(key, None):
                self.props[key] = v

        registry.Registry().register(self)

    def validate_params(self):
        print "validating %s(%s)" % (self.TYPE, self.identity)
        for p in self.REQUIRED_PARAMS:
            if not getattr(self, p):
                raise ConfigurationException("%s Missing required param %s" % (self,p))

        return True

    def __getattr__(self, k):
        if self.__dict__.get(k, None):
            return self.__dict__[k]

        if self.props.get(k, None):
            return self.props[k]

        if self.template:
            tpl_attr = getattr(self.template, k, None)
            if tpl_attr:
                return tpl_attr


    def render(self):
        out = "define %s { \n" % self.TYPE
        out += "\n".join([self._flatten(k, v) for k,v in self.props.iteritems()])
        out += "\n}\n"
        return out

    def _flatten(self, k, v):
        if isinstance(v, list):
            return "\n".join(["  %s %s" % (k, vv) for vv in v])
        else:
            return "  %s %s" % (k, v)



class BaseTemplate(BaseObject):
    PARAMS = ()

    @property
    def identity(self):
        return self.name

