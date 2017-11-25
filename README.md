# asylum

Container platform implemented with FreeBSD jails

## Installation

Install asylum on a FreeBSD host
```
git clone https://github.com/cieplak/asylum.git
cd asylum
su
make
```

## Simple Usage

Let's provision a very simple web service.

Example asylum file:

```toml
# asylum.toml

[container]
name     = "helloworld"
version  = "0.0.1"
packages = ["python36"]
files    = [
    {src = "files/foo"},
    {src = "files/bar"}
]

[container.service]
protocol = "http"
path     = "/greetings"
port     = "8000"
command  = "python3 -m http.server"


```

Build the container:
```
asylum build
```

Start the container
```
asylum run helloworld
```

Test the container from the localhost
```
$ fetch http://helloworld.local:8000/things/foo
$ fetch http://helloworld.local:8000/things/bar
```

Test the container from a remote host
```
$ curl http://<server IP address>/things/foo
$ curl http://<server IP address>/things/bar
```

## Advanced Usage

Example asylum file (kitchen sink):
```toml
# asylum.toml

name      = "complex_container"
prototype = "base_container"

[[services]]
name     = "postgresql"
protocol = "tcp"
port     = "5432"

[[services]]
name     = "schema1.postgREST"
protocol = "http"
path     = "/schema1"
port     = "3001"
command  = "/usr/local/bin/postgrest /usr/local/etc/schema1.conf"

[[services]]
name     = "schema2.postgREST"
protocol = "http"
path     = "/schema2"
port     = "3002"
command  = "/usr/local/bin/postgrest /usr/local/etc/schema2.conf"

[[services]]
name     = "schema3.postgREST"
protocol = "http"
path     = "/schema3"
port     = "3003"
command  = "/usr/local/bin/postgrest /usr/local/etc/schema3.conf"

packages = ["postgresql10-server"]

[[files]]
src = "files/schema1.conf"
dst = "/usr/local/etc/schema1.conf"

[[files]]
src = "files/schema2.conf"
dst = "/usr/local/etc/schema2.conf"

[[files]]
src = "files/schema3.conf"
dst = "/usr/local/etc/schema3.conf"

bootstrap = [
  {csh = "fetch postgrest-v0.4.3.0-freebsd.tar.xz -o /tmp/postgrest.txz"},
  {csh = "tar -xvf /tmp/postgrest.txz"}
  {csh = "cp /tmp/postgrest /usr/local/bin/."}
]

```

Build a container
```
asylum build
```

Ship a container to another asylum host over HTTPS or SSH
```
asylum ship https://<asylum server IP address>
asylum ship ssh://<host in ~/.ssh/config>
```
