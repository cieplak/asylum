import os
from pathlib import Path

import toml


zpool = dict(
    zpath=None,
    device=None,
)

jails = dict(
    zpath=None,
    path=None,
)

base = dict(
    uname=None,
    url=None,
    zpath=None,
    version=None,
)

db = dict(
    path=None,
)

network = dict(
    public_ip=None,
    interface=None,
    cidr=None,
)


class AsylumConf(object):

    PATH = os.path.expanduser('~/.asylumrc')

    KEYS = [
        'zpool'
    ]

    @classmethod
    def bootstrap(cls):
        Path(cls.PATH).touch()

    @classmethod
    def load(cls, path=None):
        if not path:
            path = cls.PATH
        global zpool, jails, base, db, network
        settings = toml.load(path)
        zpool = settings.get('zpool')
        jails = settings.get('jails')
        base = settings.get('base')
        db = settings.get('db')
        db['path'] = os.path.expanduser(db['path'])

        network = settings.get('network')
