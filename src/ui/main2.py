import json
import time
from fabric import Connection, task

host = '192.168.15.1'
port = 22
user = 'pi'
password = 'N00BRCRC'
connection = Connection(host=host, port=port, user=user, connect_kwargs={'password': password})


def _download_bios(command, service):
    return f"sudo systemctl {command} {service}.service "


def _service(command, service):
    return f"sudo systemctl {command} {service}.service "


def _make_dir_config(service):
    return f"sudo mkdir -p /data/{service}/config"


def _download_config_file(service):
    return f"curl -OL https://raw.githubusercontent.com/NubeIO/rubix-pi-image/main/config-files/{service}/config.json"


def _move_config_file(service):
    return f"sudo mv config.json /data/{service}/config/config.json"


def _delete_home_dir():
    return f"sudo rm -r *"


def _delete_data_dir():
    return f"sudo rm -r /home/data"


def _run(ctx, command):
    try:
        ctx.run(command)
    except:
        print(f"ERROR: {command}")


@task
def clone_repo(ctx):
    print("Cloning repository . . .")
    ctx.run("sudo rm -r *")
    ctx.run("sudo rm -r /data")
    ctx.run("wget https://github.com/NubeIO/rubix-bios/releases/download/v1.4.0/rubix-bios-1.4.0-7fa0370a.armv7.zip")
    print("unzip")
    ctx.run("unzip rubix-bios-1.4.0-7fa0370a.armv7.zip")
    print("install bios")
    ctx.run("sudo ./rubix-bios -p 1615 -g /data/rubix-bios -d data -c config -a apps --prod --install --auth")
    time.sleep(5)
    print("install rubix get password")
    token = ctx.run(
        r"""curl -X POST http://localhost:1615/api/users/login -H "Content-Type: application/json" -d '{"username":
        "admin", "password": "N00BWires"}'""")
    # print(type(token))
    token = token.__dict__.get('stdout')
    t = json.loads(token)
    t = t.get('access_token')
    version = "v1.6.8"
    print('token:', t)
    url = f"""curl -X PUT http://localhost:1615/api/service/upgrade -H "Content-Type: application/json" -H "Authorization: {t}" -d '{{"version": "{version}"}}'"""
    print('url:', url)
    ctx.run(url)
    time.sleep(5)
    print("install rubix UI")
    token = ctx.run(
        r"""curl -X POST http://localhost:1616/api/users/login -H "Content-Type: application/json" -d '{"username":
        "admin", "password": "N00BWires"}'""")
    # print(type(token))
    token = token.__dict__.get('stdout')
    t = json.loads(token)
    t = t.get('access_token')
    version = "v1.7.0"
    service = 'RUBIX_PLAT'
    download = f"""curl -X POST http://localhost:1616/api/app/download -H "Content-Type: application/json" -H "Authorization: {t}" -d '{{"service": "{service}", "version": "{version}"}}'"""
    print('download UI:', url)
    ctx.run(download)
    time.sleep(2)
    install = f"""curl -X POST http://localhost:1616/api/app/install -H "Content-Type: application/json" -H "Authorization: {t}" -d '{{"service": "{service}", "version": "{version}"}}'"""
    print('install UI:', url)
    ctx.run(install)
    time.sleep(5)
    ctx.run(_service('restart', 'nubeio-wires-plat'))
    time.sleep(5)
    ctx.run(_service('status', 'nubeio-wires-plat'))
    # time.sleep(2)
    # ctx.run(install)


@task
def mk_dirs(ctx):
    ctx.run('sudo mkdir -p /data/point-server/config')
    ctx.run(
        'curl -OL https://raw.githubusercontent.com/NubeIO/rubix-pi-image/main/config-files/point-server/config.json')
    ctx.run('sudo mv config.json /data/point-server/config/config.json')


@task
def list_services(ctx):
    _run(ctx, 'ls /etc/systemd/system/ | grep -e nube')
    _run(ctx, 'ls /lib/systemd/system/ | grep -e nube')


@task
def deploy(conn):
    with conn as c:
        list_services(c)
        # mk_dirs(c)


deploy(connection)
