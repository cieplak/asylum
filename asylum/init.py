import os
import subprocess

from asylum import sqlite


class Rc(object):

    PATH = '/etc/rc.conf'

    @classmethod
    def enable(cls, name):
        cmd = ['service', name, 'enable']
        return subprocess.run(cmd)

    @classmethod
    def start(cls, name):
        cmd = ['service', name, 'start']
        return subprocess.run(cmd)

    @classmethod
    def stop(cls, name):
        cmd = ['service', name, 'stop']
        return subprocess.run(cmd)

    @classmethod
    def restart(cls, name):
        cmd = ['service', name, 'restart']
        return subprocess.run(cmd)

    @classmethod
    def reload(cls, name):
        cmd = ['service', name, 'reload']
        return subprocess.run(cmd)

    @classmethod
    def bootstrap(cls):
        with open(cls.PATH) as fd:
            current_settings = fd.read().split('\n')
        for setting in current_settings:
            sqlite.Session.add(sqlite.RcSetting(value=setting))
        sqlite.Session.commit()

    @classmethod
    def set(cls, value):
        sqlite.Session.add(sqlite.RcSetting(value=value))
        sqlite.Session.commit()

    @classmethod
    def converge(cls):
        values = [r.value for r in sqlite.RcSetting.query]
        text = '\n'.join(values)
        os.rename(cls.PATH, cls.PATH + '.bak')
        with open(cls.PATH, 'w') as fd:
            fd.write(text)
