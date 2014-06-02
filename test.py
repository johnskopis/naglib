#!/usr/bin/env python

from naglib.config import *
from naglib.config.registry import Registry

print "creating the registry"
r = Registry()
print "resolving"
r.resolve_all()

print "adding some hosts"
for dc in ('datacenter1', 'datacenter2'):
    for i in xrange(2):
        h = Host(host_name="host%.2d" % i,
                 registry=r,
                alias="host%.2d" % i,
                address="127.0.0.%d" % i,
                use=dc,)

print "adding a service"
for h in r.hosts.values():
    s = Service(host=h, use='test-service', registry=r,)
    if h.use == 'datacenter1':
        s = Service(host=h, use='test-service-test', registry=r,)

r.validate_all()
r.generate_servicegroups()
r.generate_clusters()
r.write_all()
