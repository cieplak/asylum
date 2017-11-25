import subprocess


class Zfs(object):

    @classmethod
    def create_pool(cls, device, name):
        cmd = ['zpool', 'create', name, device]
        return subprocess.run(cmd)

    @classmethod
    def create_directory(cls, pool_path, filesystem_path):
        cmd = ['zfs', 'create', '-o', 'mountpoint={}'.format(filesystem_path), pool_path]
        return subprocess.run(cmd)

    @classmethod
    def create(cls, pool_path):
        cmd = ['zfs', 'create', pool_path]
        return subprocess.run(cmd)

    @classmethod
    def snapshot(cls, pool_path, version):
        cmd = ['zfs', 'snapshot', '{}@{}'.format(pool_path, version)]
        return subprocess.run(cmd)

    @classmethod
    def clone(cls, snapshot, destination):
        cmd = ['zfs', 'clone', snapshot, destination]
        return subprocess.run(cmd)
