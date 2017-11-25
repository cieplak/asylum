import os


def get_fixture_path(fixture_path):
    test_directory = os.path.dirname(__file__)
    return os.path.join(test_directory, 'fixtures', fixture_path)
