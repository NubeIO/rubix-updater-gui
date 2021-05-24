# import githubdl
from fabric import Connection

POINT_SERVER_PATH = "./config-files/point-server/point-server/config.json"
BACNET_SERVER_PATH = "./config-files/bacnet-server/bacnet-server"

githubdl.dl_dir("https://github.com/NubeIO/rubix-pi-image", "config-files/point-server",
                github_token="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")

# import os
# # POINT_SERVER_PATH = "./config-files/point-server/point-server"
# arr = os.listdir(POINT_SERVER_PATH)
file = POINT_SERVER_PATH
HOME_DIR = '/home/pi'
file ="/home/aidan/code/py-nube/rubix-updater-gui/r-c-loraraw_subnet-1_v0.2.bin"

from fabric import Connection
host = '192.168.15.189'
port = 22
user = 'pi'
password = 'N00BRCRC'
c = Connection(host=host, port=port, user=user, connect_kwargs={'password': password})
c.put(file, HOME_DIR)
# c.run('stty -F /dev/ttyAMA0 38400 -cstopb -parenb && cat /dev/ttyAMA0')
c.run('ls')
