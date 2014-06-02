import csv
import re

from naglib.config import *

class ReClassifer(object):
    def __init__(self, registry, config, **kwargs):
        self.global_config = config
        self.registry = registry
        self.config = self.global_config[self.__class__.__name__]
        self.hosts = []

        if not self.config.get('csv'):
            raise Exception("require a csv file to parse")

        self.load_csv(self.config['csv'])
        self.configure_hosts()
        self.configure_services()

    def load_csv(self, csv_file):
        with open(csv_file, 'r') as fd:
            dialect = csv.Sniffer().sniff(fd.read(1024))
            fd.seek(0)
            csvr = csv.reader(fd, dialect)
            self.hosts = list(csvr)

    def configure_hosts(self):
        for host in self.hosts:
            kwargs = self._host_args(host)
            Host(registry=self.registry,
                 **kwargs)

    def configure_services(self):
        for rule in self.config['rules']:
            field = rule['field']
            cre = re.compile(rule['re'])
            for host in self.hosts:
                if cre.search(host[field]):
                    for check in rule['checks']:
                        kwargs = self._host_args(host)

                        host = self.registry.hosts[Host.identity_for(**kwargs)]

                        Service(registry=self.registry,
                                use=check,
                                host=host)

    def _host_args(self, host):
        kwargs=dict()
        for field, pos in self.config['host_mappings'].iteritems():
            kwargs[field] = host[pos]
        return kwargs
