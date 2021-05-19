from src.ssh.ssh import SSHConnection
from src.ssh.test_settings import TestSettings
from fabric import task

from src.utils.functions import Utils

settings = TestSettings()

cx = SSHConnection(
    host=settings.host,
    port=settings.port,
    user=settings.user,
    password=settings.password
)


def _run(ctx, command):
    if Utils.ping(settings.host) == False:
        print()
        raise Exception(f"ERROR: failed to ping {settings.host}")


    try:
        ctx.run(command)
    except:
        print(f"ERROR: {command}")


@task
def list_services(ctx):
    _run(ctx, 'ls -l')
    # _run(ctx, 'ls /lib/systemd/system/ | grep -e nube')


@task
def deploy(conn):
    with conn as c:
        list_services(c)
        # mk_dirs(c)


deploy(cx.connect())
