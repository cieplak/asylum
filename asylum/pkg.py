from asylum.console import Console


class Pkg(Console):

    @classmethod
    def install(cls, pkg_name):
        cmd = ' '.join(['pkg', 'install', '-y', pkg_name])
        return cls.run(cmd)
