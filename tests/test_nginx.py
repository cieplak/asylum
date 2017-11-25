from unittest import TestCase

from asylum import nginx
from asylum.service import HttpService


class TestNginx(TestCase):

    def test_config(self):
        self.maxDiff = None
        http_service_a = HttpService()
        http_service_b = HttpService()
        http_service_a.host = 'a.local'
        http_service_b.host = 'b.local'
        http_service_a.port = '3001'
        http_service_b.port = '3002'
        http_service_a.path = '/a'
        http_service_b.path = '/b'
        config = nginx.ConfigTemplate.render(*[http_service_a, http_service_b])
        expected_config = '''
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

        location /a {
            rewrite        /a/(.*) /$1 break;
            rewrite        /a      /   break;
            proxy_pass     http://a.local:3001;
            proxy_redirect off;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $remote_addr;
        }

        location /b {
            rewrite        /b/(.*) /$1 break;
            rewrite        /b      /   break;
            proxy_pass     http://b.local:3002;
            proxy_redirect off;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $remote_addr;
        }

    }

}
'''
        self.assertEqual(config, expected_config)
