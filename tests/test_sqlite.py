from unittest import TestCase

from asylum import sqlite


class TestSqlite(TestCase):

    def setUp(self):
        sqlite.init('sqlite://')

    def test_init(self):
        print('ok')
