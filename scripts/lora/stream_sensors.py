from fabric import Connection
from app.core.commands import LinuxCommands
from app.core.make_connection import SSHConnection

host = '120.157.111.164'
port = 2022
user = 'pi'
password = 'N00BRCRC'

ctx = Connection(host=host, port=port, user=user, connect_timeout=3, connect_kwargs={'password': password})
run_for = 5
baud_rate = 38400
serial_port = "ttyAMA0"
# stty -F /dev/ttyAMA0 38400 -cstopb -parenb && cat /dev/ttyAMA0
# timeout 5 stty -F /dev/ttyAMA0 38400 -cstopb -parenb && timeout 5  cat /dev/ttyAMA0
SSHConnection.run_command(ctx, LinuxCommands.command_blank(f"timeout {run_for} stty -F /dev/{serial_port} {baud_rate} "
                                                           f"-cstopb -parenb && timeout {run_for} cat /dev/{serial_port}"))
