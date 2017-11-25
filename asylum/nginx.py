from asylum.init import Rc
from asylum.pkg import Pkg


class Nginx(object):

    @classmethod
    def install(cls):
        Pkg.install('nginx')

    @classmethod
    def enable(cls):
        Rc.enable('nginx')

    @classmethod
    def register_service(self, http_service):
        pass

    @classmethod
    def reload(self):
        pass


class ConfigTemplate(object):

    FILE_TEMPLATE = '''
worker_processes  1;

events {
    worker_connections  1024;
}

http {

    include       mime.types;
    default_type  application/octet-stream;
    keepalive_timeout  65;

    server {
        listen       8080;
        server_name  localhost;
{$LOCATIONS}

    }

}
'''

    LOCATION_TEMPLATE = '''
        location {$PATH} {
            rewrite        {$PATH}/(.*) /$1 break;
            rewrite        {$PATH}      /   break;
            proxy_pass     http://{$HOST}:{$PORT};
            proxy_redirect off;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $remote_addr;
        }'''

    @classmethod
    def render(cls, *http_services):
        locations = '\n'.join(
            cls.render_location(svc.path, svc.host, svc.port)
            for svc in http_services
        )
        return cls.FILE_TEMPLATE.replace('{$LOCATIONS}', locations)

    @classmethod
    def render_location(cls, path, host, port):
        return (cls.LOCATION_TEMPLATE
                .replace('{$PATH}', path)
                .replace('{$HOST}', host)
                .replace('{$PORT}', port))
