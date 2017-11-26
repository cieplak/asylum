import subprocess
from subprocess import PIPE
import sys

import colorful


class Console(object):

    @classmethod
    def show_ok(cls, msg=None):
        text = str(colorful.bold_green('*** OK ***'))
        if msg:
            text += '\n' + msg
        cls.stdout(text)

    @classmethod
    def show_warn(cls, msg=None):
        text = str(colorful.bold_yellow('*** WARNING ***'))
        if msg:
            text += '\n' + msg
        cls.stderr(text)

    @classmethod
    def show_err(cls, msg=None):
        text = str(colorful.bold_red('*** ERROR ***'))
        if msg:
            text += '\n' + msg
        cls.stderr(text)

    @classmethod
    def show_debug(cls, msg=None):
        text = '*** DEBUG ***'
        if msg:
            text += '\n' + msg
        cls.stderr(text)

    @classmethod
    def show_cmd(cls, msg):
        text = 'COMMAND: ( ' + msg + ' ) '
        cls.stdout(text.ljust(70, '.'))

    @classmethod
    def stdout(cls, msg=''):
        print(msg)

    @classmethod
    def stderr(cls, msg=''):
        print(msg, file=sys.stderr)

    @classmethod
    def run(cls, cmd):
        cls.show_cmd(cmd)
        output = subprocess.run(cmd.split(), stdout=PIPE, stderr=PIPE, universal_newlines=True)
        if output.returncode:
            cls.stdout(str(colorful.red(output.stdout)))
            cls.stdout(str(colorful.red(output.stderr)))
            return output
        cls.stdout(str(colorful.green(output.stderr)))
        cls.stdout(str(colorful.green(output.stdout)))
        return output
