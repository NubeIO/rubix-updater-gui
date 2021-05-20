from src.common_ui.ssh import CommonHost


class MakeConnection:

    @staticmethod
    def get_connection():
        from src.common_ssh.ssh import SSHConnection
        cx = SSHConnection(
            host=CommonHost.get_host(),
            port=22,
            user=CommonHost.get_user(),
            password=CommonHost.get_password()
        )
        return cx
