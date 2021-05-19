from fabric import Connection, task


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
        """
        list all gateways
        :param organizationID:
        :param limit:
        :return:
        """
        print(self.host)
        connection = Connection(host=self.host, port=self.port, user=self.user,
                                connect_kwargs={'password': self.password})
        return connection
