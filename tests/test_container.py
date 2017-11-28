from unittest import TestCase

from asylum.container import Container
from asylum.system import System

from tests import get_fixture_path


class TestContainer(TestCase):

    def test_load_asylum_file(self):
        system = System()
        sqlite.init('sqlite://')
        system.sqlite.create_nefw_database()

        path = get_fixture_path('helloworld')
        Container.build(path)
