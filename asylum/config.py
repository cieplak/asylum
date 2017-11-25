from pathlib import Path

import toml


class AsylumConf(object):

    PATH = '/root/asylumrc'

    KEYS = [
        'zpool'
    ]

    @classmethod
    def bootstrap(cls):
        Path(cls.PATH).touch()

    @classmethod
    def load(cls, path=PATH):
        settings = toml.load(path)
