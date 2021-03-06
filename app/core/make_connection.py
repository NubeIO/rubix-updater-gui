import logging
from fabric import Connection

from config.config import Config


class SSHConnection:
    def __init__(self,
                 host=None,
                 port=None,
                 user=None,
                 connect_timeout=10,
                 password=None,
                 use_config=None
                 ):
        self.host = host
        self.port = port
        self.user = user
        self.connect_timeout = connect_timeout
        self.password = password
        self.use_config = use_config

    def connect(self):
        from config.load_config import get_config_host
        _host_settings = get_config_host()
        host = _host_settings.get('get_host')
        port = _host_settings.get('get_port')
        user = _host_settings.get('get_user')
        password = _host_settings.get('get_password')
        if self.use_config:
            c = Config()
            c.load_config()
            connection = Connection(host=host,
                                    port=port,
                                    user=user,
                                    connect_timeout=self.connect_timeout,
                                    connect_kwargs={'password': password})
            logging.info(f"CONNECTED with host:{host} port:{port} user:{user}")
        else:
            connection = Connection(host=self.host,
                                    port=self.port,
                                    user=self.user,
                                    connect_timeout=self.connect_timeout,
                                    connect_kwargs={'password': self.password})
            logging.info(f"CONNECTED with host:{self.host} port:{self.port} user:{self.user}")
        try:
            connection.run('pwd')
            return connection
        except:
            logging.info(f"DEAD host:{self.host} port:{self.port} user:{self.user}")
            return False

    @staticmethod
    def run_command(ctx, command):
        try:
            out = ctx.run(command)
            return out.__dict__.get('stdout')
        except:
            return f"ERROR: {command}"

    @staticmethod
    def run_sftp(ctx, file, directory):
        try:
            out = ctx.put(file, directory)
            return out.__dict__.get('stdout')
        except:
            return f"ERROR: file transfer: file {file} dir: {directory}"

    @staticmethod
    def run_command_sudo(ctx, command, **kwargs):
        pty = kwargs.get('pty')
        watchers = kwargs.get('watchers')
        try:
            out = ctx.run(command, pty=pty, watchers=watchers)
            return out.__dict__.get('stdout')
        except:
            return f"ERROR: {command}"
