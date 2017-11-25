from pathlib import Path

import toml


zpool = dict(
    name=None,
    device=None,
)

jails = dict(
    zpool=None,
    path=None,
)

base = dict(
    uname=None,
    url=None,
    snapshot=None,
)

db = dict(
    path=None,
)

network = dict(
    public_address=None,
    interface=None,
    cidr=None,
)


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
        global zpool, jails, base, db, network
        settings = toml.load(path)
        zpool = settings.get('zpool')
        jails = settings.get('jails')
        base = settings.get('base')
        db = settings.get('db')
        network = settings.get('network')
