import json
import time
from fabric import Connection, task

from src.common_ssh.ssh import SSHConnection
from src.linux_commands.commands import LinuxCommands

host = '192.168.15.189'
port = 22
user = 'pi'
password = 'N00BRCRC'
connection = Connection(host=host, port=port, user=user, connect_kwargs={'password': password})


def get_nested(dict_, *keys, default=None):
    if not isinstance(dict_, dict):
        return default
    elem = dict_.get(keys[0], default)
    if len(keys) == 1:
        return elem
    return get_nested(elem, *keys[1:], default=default)

def _run(ctx, command):
    try:
        return ctx.run(command)
    except:
        print(f"ERROR: {command}")


@task
def list_services(ctx):
    _run(ctx, 'ls /etc/systemd/system/ | grep -e nube')
    _run(ctx, 'ls /lib/systemd/system/ | grep -e nube')


@task
def mk_dirs(ctx):
    # ctx.run('sudo rm -r /data/point-server/config')
    ctx.run('sudo mkdir -p /data/point-server/config')
    ctx.run(
        'curl -OL https://raw.githubusercontent.com/NubeIO/rubix-pi-image/main/config-files/point-server/config.json')
    ctx.run('sudo mv config.json /data/point-server/config/config.json')




@task
def deploy(conn):
    with conn as c:
        mk_dirs(c)


# @task
# def deploy(conn):
#     with conn as c:
#         list_services(c)
#         exe = _run(c, LinuxCommands.get_rubix_service_token())
#         print(type(exe))
#         token = exe.__dict__.get('stdout')
#         t = json.loads(token)
#         t = t.get('access_token')
#         service = "RUBIX_PLAT"
#         version = "v1.7.1"
#         # print(1111, LinuxCommands.download_rubix_service_app(t, service, version))
#         # print(22222, LinuxCommands.get_state_download_rubix_service_app(t))
#         _run(c, LinuxCommands.download_rubix_service_app(t, service, version))
#         max_checks = 100
#         down_load_state = 10
#         time.sleep(2)
#         i = 1
#         print(555555555)
#         while i < max_checks:
#             aa = _run(c, LinuxCommands.get_state_download_rubix_service_app(t))
#             time.sleep(2)
#             print(aa, 6666666)
#             bb = aa.__dict__.get('stdout')
#
#             tt = json.loads(bb)
#             tt = tt.get('services')
#             # tt = tt.get('download')
#             print(tt, 5555555555)
#             if isinstance(tt, list):
#                 ttt = tt[0].get('download')
#                 print(5555, ttt)
#                 if ttt:
#                     _run(c, LinuxCommands.delete_state_download_rubix_service_app(t))
#                     break
#             i += 1
#
#         # state = exe.__dict__.get('message')
#         # print(222222, state)
#         print("DONE")


deploy(connection)
