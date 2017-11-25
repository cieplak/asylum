import os

import toml
from asylum.jail import Jail
from asylum.service import Service


class Container(object):

    def __init__(self):
        self.jail = Jail()
        self.service = Service()
        self.files = []
        self.packages = []

    @classmethod
    def build(cls, config_directory=os.getcwd()):
        container = Container()
        config = Config.parse(config_directory)
        container.name = config.name
        container.version = config.version
        container.service = Service.from_config(config.service)
        container.files = [File(**f) for f in config.files]
        container.packages = config.packages
        container.jail = Jail.create(container.name)
        # container.jail.install_packages(container.packages)
        # container.jail.install_services(*[container.service])

    def enable(self):
        self.jail.enable()

    def run(self):
        self.jail.run()

    def attach(self):
        self.jail.attach()


class Config(object):

    FILE = 'asylum.toml'

    CONTAINER_SETTINGS = {
        'name':     str,
        'version':  str,
        'packages': list,
        'files':    list,
        'service':  dict,
    }

    SERVICE_SETTINGS = {
        'protocol': str,
        'path':     str,
        'port':     str,
        'command':  str,
    }

    def __init__(self):
        self.name = None
        self.version = None
        self.files = []
        self.packages = []
        self.service = None

    @classmethod
    def parse(cls, directory):
        path_to_file = os.path.join(directory, cls.FILE)
        settings = toml.load(path_to_file).get('container')
        cls.validate(settings)
        config = Config()
        config.name     = settings['name']
        config.version  = settings['version']
        config.packages = settings['packages']
        config.files    = settings['files']
        config.service  = settings['service']
        return config

    @classmethod
    def validate(cls, settings):
        for key in settings:
            try:
                assert(key in cls.CONTAINER_SETTINGS)
                assert(type(settings[key]) == cls.CONTAINER_SETTINGS[key])
            except AssertionError:
                raise Exception('Unknown value `{}` in asylum file'.format(key))


class File(object):

    def __init__(self, src, dst=None):
        self.src = os.path.join(os.getcwd(), src)
        self.dst = dst
