from enum import Enum, auto
import subprocess

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

    @classmethod
    def create(cls, name):
        Zfs.clone('pool/jails/basejail@0.0.1', 'pool/jails/{}'.format(name))

    def enable(self):
        cmd = ['service', 'jail', 'enable', self.name]
        return subprocess.run(cmd)

    def start(self):
        cmd = ['service', 'jail', 'start', self.name]
        return subprocess.run(cmd)

    def stop(self):
        cmd = ['service', 'jail', 'stop', self.name]
        return subprocess.run(cmd)

    def create_user(self, name, shell='/bin/csh'):
        home = '/home/{}'.format(name)
        subprocess.run(['mdkir', home])
        cmd = ['pw', 'useradd', '-n', name, '-s', shell, '-w', 'no', '-d', home]
        subprocess.run(cmd)
        subprocess.run(['chown', '-R', '{user}:{user}'.format(user=name), home])

    def install_file(self, src, dst):
        cmd = ['cp', src, dst]
        return subprocess.run(cmd)


class File(object):
    pass
