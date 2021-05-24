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

from fabric import Connection

from app.core.commands import LinuxCommands
from app.core.make_connection import SSHConnection

host = '192.168.15.189'
port = 22
user = 'pi'
password = 'N00BRCRC'
ctx = Connection(host=host, port=port, user=user, connect_kwargs={'password': password})
# c.put(file, HOME_DIR)
# # c.run('stty -F /dev/ttyAMA0 38400 -cstopb -parenb && cat /dev/ttyAMA0')
# c.run('ls')

github_token = ""

exe = SSHConnection.run_command(ctx, LinuxCommands.get_rubix_service_token())
print(4444, exe)
token = LinuxCommands.clean_token(exe)
print(4444, token)
service = "RUBIX_PLAT"
# git_token = "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"
version = "v1.7.1"
# version = "latest"
exe = SSHConnection.run_command(ctx, LinuxCommands.add_rubix_service_github_token(token, github_token))
print(55555, exe)

import requests



time.sleep(5)
max_checks = 20
time.sleep(2)
i = 1
while i < max_checks:
    aa = SSHConnection.run_command(ctx, LinuxCommands.get_state_download_rubix_service_app(token))
    time.sleep(3)
    print(44444, type(aa))
    tt = json.loads(aa)
    tt = tt.get('services')
    if isinstance(tt, list):
        ttt = tt[0].get('download')
        if ttt:
            SSHConnection.run_command(ctx, LinuxCommands.delete_state_download_rubix_service_app(token))
            break
    i += 1
