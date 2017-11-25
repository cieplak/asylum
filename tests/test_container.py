from unittest import TestCase

from asylum.container import Container

from tests import get_fixture_path


class TestContainer(TestCase):

    def test_load_asylum_file(self):
        path = get_fixture_path('helloworld')
        Container.build(path)
