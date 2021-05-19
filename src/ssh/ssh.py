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

    def list_all(self,
                 limit: int = 100
                 ):
        """
        list all gateways
        :param organizationID:
        :param limit:
        :return:
        """

        return self.host
