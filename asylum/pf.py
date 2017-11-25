
from asylum.init import Rc


class Pf(object):

    @classmethod
    def converge(cls):
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
                .replace('{JAIL_IFACE}', jail_iface)
                .replace('{$JAIL_CIDR}', jail_cidr))
