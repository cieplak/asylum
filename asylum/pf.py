from asylum import config
from asylum.init import Rc


class Pf(object):

    FILE = '/etc/pf.conf'

    @classmethod
    def converge(cls):
        text = ConfigTemplate.render(
            jail_iface=config.network['interface'],
            public_ip=config.network['public_ip'])
        with open(cls.FILE, 'w') as fd:
            fd.write(text)
        Rc.reload('pf')


class ConfigTemplate(object):

    TEMPLATE = '''
PUBLIC_IP="{$PUBLIC_IP}"
JAIL_CIDR="{$JAIL_CIDR}"

scrub in all
nat pass on {$JAIL_IFACE} from $JAIL_CIDR to any -> $PUBLIC_IP
'''

    @classmethod
    def render(cls, jail_iface, public_ip, jail_cidr='10.0.0.0/24'):
        return (cls.TEMPLATE
                .replace('{$PUBLIC_IP}', public_ip)
                .replace('{$JAIL_IFACE}', jail_iface)
                .replace('{$JAIL_CIDR}', jail_cidr))
