import githubdl
from fabric import Connection

POINT_SERVER_PATH = "./config-files/point-server/point-server/config.json"
BACNET_SERVER_PATH = "./config-files/bacnet-server/bacnet-server"

githubdl.dl_dir("https://github.com/NubeIO/rubix-pi-image", "config-files/point-server",
                github_token="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")

# import os
# # POINT_SERVER_PATH = "./config-files/point-server/point-server"
# arr = os.listdir(POINT_SERVER_PATH)
file = POINT_SERVER_PATH


host = '192.168.15.189'
port = 22
user = 'pi'
password = 'N00BRCRC'
c = Connection(host=host, port=port, user=user, connect_kwargs={'password': password})
c.put(file, '/home/pi')
c.run('sudo mv config.json /data/point-server/config/config.json')

