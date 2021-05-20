from fabric import Connection

from src.common_ui.logs import Common
from src.common_ui.ssh import CommonHost


class SSHConnection:
    def __init__(self,
                 host='192.168.15.10',
                 port=22,
                 user='pi',
                 password=None
                 ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def connect(self):
        connection = Connection(host=self.host, port=self.port, user=self.user,
                                connect_kwargs={'password': self.password})
        return connection

    @staticmethod
    def connection():
        cx = SSHConnection(
            host=CommonHost.get_host(),
            port=22,
            user=CommonHost.get_user(),
            password=CommonHost.get_password()
        )
        return cx

    @staticmethod
    def run_command(ctx, command):
        if not Common.ping():
            Common.log(f"ERROR: failed to ping @func _run {CommonHost.get_host()}")
            return
        try:
            out = ctx.run(command)
            return out.__dict__.get('stdout')
        except:
            print(f"ERROR: {command}")

