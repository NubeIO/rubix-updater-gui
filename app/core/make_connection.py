from fabric import Connection


class SSHConnection:
    def __init__(self,
                 host='192.168.15.10',
                 port=22,
                 user='pi',
                 connect_timeout=10,
                 password=None
                 ):
        self.host = host
        self.port = port
        self.user = user
        self.connect_timeout = connect_timeout
        self.password = password

    def connect(self):
        connection = Connection(host=self.host,
                                port=self.port,
                                user=self.user,
                                connect_timeout=self.connect_timeout,
                                connect_kwargs={'password': self.password})
        try:
            connection.run('pwd')
            return connection
        except:
            print(333333, "An exception occurred")
            return False

    @staticmethod
    def run_command(ctx, command):
        print("run_command")
        try:
            out = ctx.run(command)
            print("run_command 2")
            return out.__dict__.get('stdout')
        except:
            print("run_command ERROR")
            return f"ERROR: {command}"

    @staticmethod
    def run_sftp(ctx, file, directory):
        try:
            out = ctx.put(file, directory)
            return out.__dict__.get('stdout')
        except:
            return f"ERROR: file transfer {directory}"

    @staticmethod
    def run_command_sudo(ctx, command, **kwargs):
        pty = kwargs.get('pty')
        watchers = kwargs.get('watchers')
        try:
            out = ctx.run(command, pty=pty, watchers=watchers)
            print("run_command 2")
            return out.__dict__.get('stdout')
        except:
            print("run_command ERROR")
            return f"ERROR: {command}"
