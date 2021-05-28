import json
import os


class Config:
    def __init__(self):
        self.host = None
        self.port = None
        self.user = None
        self.password = None
        self.git_token = None
        self.rubix_bios_user = None
        self.rubix_bios_password = None
        self.rubix_bios_port = None
        self.rubix_service_user = None
        self.rubix_service_password = None
        self.rubix_service_port = None

    def get_host(self):
        return self.host

    def load_config(self):
        CWD = os.getcwd()
        key = "connection"
        file = f"{CWD}/config.json"
        host = 'host'
        port = 'port'
        user = 'user'
        password = 'password'
        git_token = 'git_token'
        rubix_bios_user = "rubix_bios_user"
        rubix_bios_password = "rubix_bios_password"
        rubix_bios_port = "rubix_bios_port"
        rubix_service_user = "rubix_service_user"
        rubix_service_password = "rubix_service_password"
        rubix_service_port = "rubix_service_port"
        with open(file) as json_file:
            data = json.load(json_file)
            for p in data[key]:
                if p == host:
                    self.host = p
                if p == port:
                    self.port = p
                if p == user:
                    self.user = p
                if p == password:
                    self.password = p
                if p == git_token:
                    self.git_token = p
                if p == rubix_bios_user:
                    self.rubix_bios_user = p
                if p == rubix_bios_password:
                    self.rubix_bios_password = p
                if p == rubix_bios_port:
                    self.rubix_bios_port = p
                if p == rubix_service_user:
                    self.rubix_service_user = p
                if p == rubix_service_password:
                    self.rubix_service_password = p
                if p == rubix_service_port:
                    self.rubix_service_port = p




