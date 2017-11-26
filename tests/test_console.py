from unittest import TestCase

from asylum.console import Console


class TestConsole(TestCase):

    def test_run(self):
        Console.run('echo foo bar')
        Console.run('ls /tmp')
        Console.run('ls /absent')
        Console.run('ls /')
        print('******')
