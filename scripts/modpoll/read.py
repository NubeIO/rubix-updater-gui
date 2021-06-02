from fabric import Connection
from app.core.commands import LinuxCommands
from app.core.make_connection import SSHConnection

host = '120.157.111.164'
port = 2022
user = 'pi'
password = 'N00BRCRC'


ctx = Connection(host=host, port=port, user=user, connect_timeout=3, connect_kwargs={'password': password})
run_for = 5
baud_rate = 9600
serial_port = "ttyRS485-1"
device_address = 1
point_address = 1
count = 1
point_type = 3
data_type = "float"
delay = 2

# -t 0          Discrete output (coil) data type
# -t 1          Discrete input data type
# -t 3          16-bit input register data type
# -t 4          16-bit output (holding) register data type (default)
a = f"timeout {run_for} modpoll -m rtu -p none -b {baud_rate}" \
                                                           f"-a {device_address} -t {point_type}:{data_type} " \
                                                           f"-r {point_address} -c{count} -l {delay} /dev/{serial_port}"

SSHConnection.run_command(ctx, LinuxCommands.command_blank(f"timeout {run_for} modpoll -m rtu -p none -b {baud_rate} "
                                                           f"-a {device_address} -t {point_type}:{data_type} "
                                                           f"-r {point_address} -c{count} -l {delay} /dev/{serial_port}"))