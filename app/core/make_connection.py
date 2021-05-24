from fabric import Connection

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
    def run_command(ctx, command):
        try:
            out = ctx.run(command)
            return out.__dict__.get('stdout')
        except:
            print(f"ERROR: {command}")

    @staticmethod
    def run_sftp(ctx, file, directory):
        try:
            out = ctx.put(file, directory)
            return out.__dict__.get('stdout')
        except:
            print(f"ERROR: file transfer {directory}")


