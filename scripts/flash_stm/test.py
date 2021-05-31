# import githubdl
# from fabric import Connection
#
# POINT_SERVER_PATH = "./config-files/point-server/point-server/config.json"
# BACNET_SERVER_PATH = "./config-files/bacnet-server/bacnet-server"
#
# githubdl.dl_dir("https://github.com/NubeIO/rubix-pi-image", "config-files/point-server",
#                 github_token="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")
#
# # import os
# # # POINT_SERVER_PATH = "./config-files/point-server/point-server"
# # arr = os.listdir(POINT_SERVER_PATH)
#
# HOME_DIR = '/home/pi'
# file ="/home/aidan/code/py-nube/rubix-updater-gui/r-c-loraraw_subnet-1_v0.2.bin"
import json
import time

from fabric import Connection, Config
from invoke import Responder
import getpass
from app.core.commands import LinuxCommands
from app.core.make_connection import SSHConnection

host = '192.168.15.249'
port = 22
user = 'debian'
password = 'N00B2828'

#
# stty -F /dev/ttyAMA0 38400 -cstopb -parenb && cat /dev/ttyAMA0"
try:
    # sudo_pass = getpass.getpass("N00B2828")
    # print(sudo_pass)

    # from fabric import Connection, Config
    #
    # config = Config(overrides={'sudo': {'user': 'debian'}})
    # c = Connection(host=host, port=port, config=config,  connect_kwargs={'password': password})
    #
    # c.sudo('whoami')
    # config = Config(overrides={'sudo': {'password': sudo_pass}})
    #
    ctx = Connection(host=host, port=port, user=user, connect_timeout=3, connect_kwargs={'password': password})
    # c = Connection(host, config=config)
    # c.sudo('whoami', hide='stderr')
    # exe = SSHConnection.run_command(N00Bctx, LinuxCommands.command_blank("sudo pwd", pty=True))
    # iface = ''.join(exe.split())[8:]
    # ctx.run('sudo pwd', pty=True)
    sudopass = Responder(
        pattern=r'\[sudo\] N00B2828:',
        response='N00B2828\n',
    )
    # print(sudopass.response)
    ctx.run("sudo pwd", pty=True, watchers=[sudopass])


    # const setIP = `sudo connmanctl config ${iface} --ipv4 manual ${ipAddress} ${subnetMask} ${gateway} --nameservers 8.8.8.8
    # new_ip = f"sudo connmanctl config ${iface} --ipv4 manual {ipAddress} {subnetMask} {gateway} --nameservers 8.8.8.8"
    # print(iface)

except:
    print("An exception occurred")

# def do1():
#     SSHConnection.run_command(ctx, LinuxCommands.command_blank( "timeout 5 stty -F /dev/ttyAMA0 38400 -cstopb -parenb && cat /dev/ttyAMA0"))
#     time.sleep(10)
#     return
#
#
