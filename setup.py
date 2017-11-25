#!/usr/bin/env python
from setuptools import setup


requirements = [
    'click',
    'colorful',
    'ipdb',
    'ipython',
    'nose',
    'prompt_toolkit',
    'pycryptodome',
    'sqlalchemy',
    'toml',
]

setup(
    name='asylum',
    version='0.0.1',
    url='https://www.github.com/cieplak/asylum',
    description='container platform for FreeBSD jails',
    packages=['asylum'],
    include_package_data=True,
    install_requires=requirements,
    tests_require=['nose'],
    scripts=['bin/asylum'],
)
