from enum import Enum, auto

from asylum.init import Rc


class Service(object):

    class Protocol(Enum):
        http = auto()
        tcp  = auto()

    def __init__(self):
        self.name = None
        self.container = None
        self.command = None

    @classmethod
    def from_config(cls, config):
        return cls()

    @classmethod
    def install(cls, jail):
        pass


class HttpService(Service):

    def __init__(self):
        super(HttpService, self).__init__()
        self.protocol = self.Protocol.http
        self.path = None
        self.host = None
        self.port = None

    def create(self):
        pass


class InitTemplate(object):

    TEMPLATE = '''
#!/bin/sh

# PROVIDE: {$SERVICE}
# REQUIRE: LOGIN
# KEYWORD: shutdown

. /etc/rc.subr

name="{$SERVICE}"
rcvar=${name}_enable
{$SERVICE}_chdir="/home/{$SERVICE}"
pidfile="/var/run/${name}.pid"
command="/usr/sbin/daemon"
command_args=" -f -P ${pidfile} -u {$SERVICE} -r /usr/local/bin/${name}"
load_rc_config $name
run_rc_command "$1"
'''

    @classmethod
    def render(cls, name):
        return cls.TEMPLATE.replace('{$SERVICE}', name)


class ScriptTemplate(object):

    TEMPLATE = '''
#!/bin/sh
exec {$COMMAND}
'''

    @classmethod
    def render(cls, command):
        return cls.TEMPLATE.replace('{$COMMAND}', command)
