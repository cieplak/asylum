import subprocess


class Pkg(object):

    @classmethod
    def install(cls, pkg_name):
        cmd = ['pkg', 'install', '-y', pkg_name]
        return subprocess.run(cmd)
