import os

from asylum import sqlite
from asylum.console import Console


class Rc(Console):

    PATH = '/etc/rc.conf'

    @classmethod
    def enable(cls, name):
        cmd = ' '.join(['service', name, 'enable'])
        return cls.run(cmd)

    @classmethod
    def start(cls, name):
        cmd = ' '.join(['service', name, 'start'])
        return cls.run(cmd)

    @classmethod
    def stop(cls, name):
        cmd = ' '.join(['service', name, 'stop'])
        return cls.run(cmd)

    @classmethod
    def restart(cls, name):
        cmd = ' '.join(['service', name, 'restart'])
        return cls.run(cmd)

    @classmethod
    def reload(cls, name):
        cmd = ' '.join(['service', name, 'reload'])
        return cls.run(cmd)

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
        try:
            sqlite.Session.commit()
        except Exception as exc:
            Console.show_warn('/etc/rc.conf already has ' + value)
            sqlite.Session.rollback()

    @classmethod
    def converge(cls):
        values = [r.value for r in sqlite.RcSetting.query]
        text = '\n'.join(values)
        os.rename(cls.PATH, cls.PATH + '.bak')
        with open(cls.PATH, 'w') as fd:
            fd.write(text)
