
all: bootstrap install setup

bootstrap:
	pkg install -y python3 py36-pip py36-sqlite3

install:
	python3 setup.py install

setup:
	asylum init
