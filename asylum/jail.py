from enum import Enum, auto
import os
import subprocess

from asylum import config
from asylum import sqlite
from asylum.hosts import Hosts
from asylum.zfs import Zfs


class Jail(object):

    class State(Enum):
        stopped = auto()
        running = auto()
        enabled = auto()

    def __init__(self):
        self.name = None
        self.version = None
        self.path = None
        self.state = None
        self.user = None
        self.domain = None
        self.address = None
        self.interface = None

    @classmethod
    def new(cls, name):
        jail = Jail()
        zpool = config.jails['zpool']
        path = os.path.join(config.jails['path'], name)
        base_snapshot = config.base['snapshot']
        interface = config.network['interface']
        Zfs.clone(base_snapshot, '{}/{}'.format(zpool, name))
        record = sqlite.Jail.save(
            name=name,
            path=path,
            base=base_snapshot,
            interface=interface,
        )
        cidr = config.network['cidr']
        record.address = cidr.replace('*', record.id)
        record.session.commit()
        return jail

    def enable(self):
        cmd = ['service', 'jail', 'enable', self.name]
        return subprocess.run(cmd)

    def start(self):
        cmd = ['service', 'jail', 'start', self.name]
        return subprocess.run(cmd)

    def stop(self):
        cmd = ['service', 'jail', 'stop', self.name]
        return subprocess.run(cmd)

    def install_file(self, src, dst=None):
        cmd = ['cp', src, self.user.home]
        return subprocess.run(cmd)

    def install_package(self, *pkgs):
        pass

    def install_service(self, service):
        pass

    def register_host(self):
        Hosts.register(self.domain, self.address)


class User(object):

    def __init__(self):
        self.name = None
        self.shell = None
        self.home = None

    def create(self, name, shell='/bin/csh'):
        home = '/home/{}'.format(name)
        subprocess.run(['mdkir', home])
        cmd = ['pw', 'useradd', '-n', name, '-s', shell, '-w', 'no', '-d', home]
        subprocess.run(cmd)
        subprocess.run(['chown', '-R', '{user}:{user}'.format(user=name), home])


class File(object):
    pass


class JailConfig(object):

    TEMPLATE = '''
# /etc/jail.conf

exec.start = "/bin/sh /etc/rc";
exec.stop = "/bin/sh /etc/rc.shutdown";
exec.clean;
mount.devfs;

path = "/usr/local/jails/$name";

{$JAILS}
'''

    JAIL = '''
{$NAME} {
    host.hostname = "{$NAME}.local";
    interface     = "{$IFACE}";
    ip4.addr      = {$ADDRESS};
}
'''

    @classmethod
    def render(cls, jails):
        jails_cfg = ''.join(cls.render_jail_config(j) for j in jails)
        return cls.TEMPLATE.replace('{$JAILS}', jails_cfg)

    @classmethod
    def render_jail_config(cls, jail):
        return (cls.JAIL
                .replace('{$NAME}', jail.name)
                .replace('{$IFACE}', jail.iface)
                .replace('{$ADDRESS}', jail.address))
