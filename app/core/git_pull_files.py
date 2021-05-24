import os

import githubdl

GIT_TOKEN = "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"
RUBIX_IMAGE_REPO = "https://github.com/NubeIO/rubix-pi-image"

POINT_SERVER_CONFIG = "config-files/point-server"
STM_FLASH_SCRIPT = "scripts/rubix"

POINT_SERVER_PATH = "./config-files/point-server/point-server/config.json"
BACNET_SERVER_PATH = "./config-files/bacnet-server/bacnet-server"
#
githubdl.dl_dir(RUBIX_IMAGE_REPO, STM_FLASH_SCRIPT,
                github_token=GIT_TOKEN)

HOME_DIR = '/home/pi'

from fabric import Connection

host = '192.168.15.189'
port = 22
user = 'pi'
password = 'N00BRCRC'
c = Connection(host=host, port=port, user=user, connect_kwargs={'password': password})


def unpack_stm(path):
    cwd = os.getcwd()
    file = f"{cwd}/{path}/rubix/stm-flasher.py"

    c.put(file, HOME_DIR)
    # c.run('stty -F /dev/ttyAMA0 38400 -cstopb -parenb && cat /dev/ttyAMA0')
    c.run('ls')
    print(file)
    # f = open("demofile.txt", "r")


unpack_stm(STM_FLASH_SCRIPT)
