#!/usr/bin/env python

import naglib.registry as registry
from naglib.host import Host
from naglib.service import Service
from naglib.servicegroup import ServiceGroup
from naglib.command import Command

from collections import defaultdict

print "creating the registry"
r = registry.Registry()
print "resolving"
r.resolve_all()

print "adding some hosts"
for dc in ('datacenter1', 'datacenter2'):
    for i in xrange(2):
        h = Host(host_name="host%.2d" % i,
                alias="host%.2d" % i,
                address="127.0.0.%d" % i,
                use=dc,)

print "adding a service"
for h in r.hosts.values():
    s = Service(host=h, use='test-service',)
    if h.use == 'datacenter1':
        s = Service(host=h, use='test-service-test',)

r.validate_all()
r.generate_servicegroups()
r.generate_clusters()
r.write_all()
