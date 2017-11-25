import subprocess

from asylum.pkg import Pkg
from asylum.zfs import Zfs


class System(object):

    def __init__(self):
        self.jail_path = '/usr/local/jails'
        self.base_uname = '11.1-RELEASE'
        self.base_url = 'ftp://ftp.freebsd.org/pub/FreeBSD/releases/amd64/amd64/11.1-RELEASE/base.txz'
        self.nginx = None
        self.sqlite = None

    @classmethod
    def bootstrap(cls):
        Pkg.install('nginx sqlite3')

    def create_jail_directory(self):
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
