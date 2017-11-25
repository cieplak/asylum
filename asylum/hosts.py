from asylum import sqlite


class Hosts(object):

    FILE = '/etc/hosts'

    @classmethod
    def register(cls, name, address):
        sqlite.Host.save(name=name, address=address)

    @classmethod
    def converge(cls):
        hosts = sqlite.Host.query.all()
        with open(cls.FILE) as fd:
            fd.write(ConfigTemplate.render(hosts))


class Host(object):

    def __init__(self, domain, address):
        self.domain = domain
        self.address = address


class ConfigTemplate(object):

    TEMPLATE = '''
::1          localhost
127.0.0.1    localhost
{}
'''
    @classmethod
    def render(cls, hosts):
        cfg = '\n'.join('{}\t{}'.format(h.address, h.domain) for h in hosts)
        return cls.TEMPLATE.format(cfg)
