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
        # bios
        self.bios_url = None
        self.bios_dir = None
        self.bios_version = None
        # rubix-service
        self.rubix_service_version = None
        # stm 32
        self.stm_version = None
        # build repo
        self.rubix_build_repo = None
        # wires_plat_settings
        self.wires_plat_settings = None

    def load_config(self):
        CWD = os.getcwd()
        key_connection = "connection"
        key_bios = "bios"
        key_rubix_service = "rubix_service"
        key_stm32 = "rubix_stm_32"
        key_rubix_build_repo = "rubix_build_repo"
        key_wires_plat_settings = "wires_plat_settings"
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
        # bios
        bios_url = "bios_url"
        bios_dir = "bios_dir"
        bios_version = "bios_version"
        # rubix-service
        rubix_service_version = "rubix_service_version"
        # stm32
        stm_version = "stm_version"
        # builds repo
        rubix_build_repo = "rubix_build_repo"
        # wires plat settings
        wires_plat_settings = "wires_plat_settings"

        with open(file) as json_file:
            data = json.load(json_file)
            for p in data[key_connection]:
                if p == host:
                    self.host = data[key_connection].get(host)
                if p == port:
                    self.port = data[key_connection].get(port)
                if p == user:
                    self.user = data[key_connection].get(user)
                if p == password:
                    self.password = data[key_connection].get(password)
                if p == git_token:
                    self.git_token = data[key_connection].get(git_token)
                if p == rubix_bios_user:
                    self.rubix_bios_user = data[key_connection].get(rubix_bios_user)
                if p == rubix_bios_password:
                    self.rubix_bios_password = data[key_connection].get(rubix_bios_password)
                if p == rubix_bios_port:
                    self.rubix_bios_port = data[key_connection].get(rubix_bios_port)
                if p == rubix_service_user:
                    self.rubix_service_user = data[key_connection].get(rubix_service_user)
                if p == rubix_service_password:
                    self.rubix_service_password = data[key_connection].get(rubix_service_password)
                if p == rubix_service_port:
                    self.rubix_service_port = data[key_connection].get(rubix_service_port)
            for b in data[key_bios]:
                if b == bios_url:
                    self.bios_url = data[key_bios].get(bios_url)
                if b == bios_dir:
                    self.bios_dir = data[key_bios].get(bios_dir)
                if b == bios_version:
                    self.bios_version = data[key_bios].get(bios_version)
            for rs in data[key_rubix_service]:
                if rs == rubix_service_version:
                    self.rubix_service_version = data[key_rubix_service].get(rubix_service_version)
            for stm in data[key_stm32]:
                if stm == stm_version:
                    self.stm_version = data[key_stm32].get(stm_version)
            for br in data[key_rubix_build_repo]:
                if br == rubix_build_repo:
                    self.rubix_build_repo = data[key_rubix_build_repo].get(rubix_build_repo)
            # wires plat
            self.wires_plat_settings = data[key_wires_plat_settings]

    def get_host(self):
        return self.host

    def get_port(self):
        return self.port

    def get_user(self):
        return self.user

    def get_password(self):
        return self.password

    def get_git_token(self):
        return self.git_token

    def get_rubix_bios_user(self):
        return self.rubix_bios_user

    def get_rubix_bios_password(self):
        return self.rubix_bios_password

    def get_rubix_bios_port(self):
        return self.rubix_bios_port

    def get_rubix_service_user(self):
        return self.rubix_service_user

    def get_rubix_service_password(self):
        return self.rubix_service_password

    def get_rubix_service_port(self):
        return self.rubix_service_port

    # bios
    def get_bios_url(self):
        return self.bios_url

    def get_bios_dir(self):
        return self.bios_dir

    def get_bios_version(self):
        return self.bios_version

    # rubix_service
    def get_rubix_service_version(self):
        return self.rubix_service_version

    # stm 32
    def get_stm_version(self):
        return self.stm_version

    # build repo
    def get_rubix_build_repo(self):
        return self.rubix_build_repo

    # wires plat settings
    def get_wires_plat_settings(self):
        return self.wires_plat_settings
