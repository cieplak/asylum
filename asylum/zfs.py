from asylum.console import Console


class Zfs(Console):

    @classmethod
    def create_pool(cls, device, name):
        cmd = ' '.join(['zpool', 'create', name, device])
        return cls.run(cmd)

    @classmethod
    def create_directory(cls, pool_path, filesystem_path):
        cmd = ' '.join(['zfs', 'create', '-o', 'mountpoint={}'.format(filesystem_path), pool_path])
        return cls.run(cmd)

    @classmethod
    def create(cls, pool_path):
        cmd = ' '.join(['zfs', 'create', pool_path])
        return cls.run(cmd)

    @classmethod
    def snapshot(cls, pool_path, version):
        cmd = ' '.join(['zfs', 'snapshot', '{}@{}'.format(pool_path, version)])
        return cls.run(cmd)

    @classmethod
    def clone(cls, snapshot, destination):
        cmd = ' '.join(['zfs', 'clone', snapshot, destination])
        return cls.run(cmd)
