
import os

from fabric import Connection
from invoke import Responder

host = '123.209.117.198'
port = 2024
user = 'debian'
password = 'N00B2828'

CWD = os.getcwd()
ctx = Connection(host=host, port=port, user=user, connect_timeout=3, connect_kwargs={'password': password})

file = f"{CWD}/.env"
print(file)
directory = '/data/rubix-wires/config'

out = ctx.put(file, directory)
print(out.__dict__)


sudo_pass = Responder(
    pattern=r'\[sudo\] password for debian:',
    response='N00B2828\n',
)
ctx.run('sudo rm /data/rubix-wires/config/.env', pty=True, watchers=[sudo_pass])
