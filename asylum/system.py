from asylum import config
from asylum import sqlite
from asylum.console import Console
from asylum.init import Rc
from asylum.pf import Pf
from asylum.pkg import Pkg
from asylum.nginx import Nginx
from asylum.zfs import Zfs


class System(Console):

    def __init__(self):
        self.config = config.AsylumConf.load()
        self.jail_path = config.jails['path']
        self.base_uname = config.base['uname']
        self.base_url = config.base['url']
        self.nginx = Nginx()
        self.sqlite = sqlite
        sqlite.init(config.db['path'])

    @classmethod
    def bootstrap(cls):
        config.AsylumConf.bootstrap()
        sqlite.init(config.db['path'])
        sqlite.create_new_database()
        Pkg.install('nginx sqlite3 rsync')
        Rc.set('nginx_enable=YES')
        Rc.set('jail_enable=YES')
        Rc.set('pf_enable=YES')
        Rc.converge()
        system = cls()
        system.create_jail_directory()
        system.configure_network()
        system.build_base_jail()

    def create_jail_directory(self):
        path = config.jails['path']
        pool = config.zpool['zpath']
        dev = config.zpool['device']
        Zfs.create_pool(dev, pool)
        jail_pool = config.jails['zpool']
        jail_dir = config.jails['path']
        Zfs.create_directory(jail_pool, jail_dir)

    def build_base_jail(self, name='base'):
        Zfs.create('pool/jails/{}'.format(name))
        self.run(' '.join(['fetch', self.base_url, '-o', '/tmp/base.txz']))
        jail_path = '{}/{}'.format(self.jail_path, name)
        self.run(' '.join(['tar', '-xvf', '/tmp/base.txz', '-C', jail_path]))
        uname = 'UNAME_r={}'.format(self.base_uname)
        self.run(' '.join(['env', uname, 'freebsd-update', '-b', jail_path, 'fetch install']))
        self.run(' '.join(['env', uname, 'freebsd-update', '-b', jail_path, 'IDS']))
        self.run('cp /etc/resolv.conf {}/etc/resolv.conf'.format(jail_path))
        config.base['']
        Zfs.snapshot('pool/jails/base', '0.0.1')
        sqlite.Jail.save()

    def configure_network(self):
        Pf.converge()
