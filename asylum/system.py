import subprocess

from asylum import config
from asylum import sqlite
from asylum.init import Rc
from asylum.pf import Pf
from asylum.pkg import Pkg
from asylum.nginx import Nginx
from asylum.zfs import Zfs


class System(object):

    def __init__(self):
        self.jail_path = config.jails['path']
        self.base_uname = config.base['uname']
        self.base_url = config.base['url']
        self.nginx = Nginx()
        self.sqlite = sqlite

    @classmethod
    def bootstrap(cls):
        config.AsylumConf.bootstrap()
        Pkg.install('nginx sqlite3')
        Rc.set('nginx_enable=YES')
        Rc.set('jail_enable=YES')
        Rc.converge()
        system = cls()
        system.create_jail_directory()
        system.configure_network()
        system.build_base_jail()

    def create_jail_directory(self):
        path = config.jails['path']
        pass

    def build_base_jail(self, name='base'):
        Zfs.create('pool/jails/{}'.format(name))
        subprocess.run(['fetch', self.base_url, '-o', '/tmp/base.txz'])
        jail_path = '{}/{}'.format(self.jail_path, name)
        subprocess.run(['tar', '-xvf', '/tmp/base.txz', '-C', jail_path])
        uname = 'UNAME_r={}'.format(self.base_uname)
        subprocess.run(['env', uname, 'freebsd-update', '-b', jail_path, 'fetch', 'install'])
        subprocess.run(['env', uname, 'freebsd-update', '-b', jail_path, 'IDS'])
        subprocess.run(['cp', '/etc/resolv.conf', '{}/etc/resolv.conf'.format(jail_path)])
        sqlite.Jail.save()

    def configure_network(self):
        Pf.converge()
