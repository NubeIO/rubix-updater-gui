import json


class LinuxCommands:

    @classmethod
    def clean_token(cls, res):
        t = json.loads(res)
        t = t.get('access_token')
        return t

    @classmethod
    def get_path_data(cls):
        return f"/data"

    @classmethod
    def command_ls(cls, path):
        return f"ls -l {path}"

    @classmethod
    def download_bios(cls):
        return f"wget https://github.com/NubeIO/rubix-bios/releases/download/v1.4.0/rubix-bios-1.4.0-7fa0370a.armv7.zip"

    @classmethod
    def unzip_bios(cls):
        return f"unzip rubix-bios-1.4.0-7fa0370a.armv7.zip"

    @classmethod
    def install_bios(cls):
        return f"sudo ./rubix-bios -p 1615 -g /data/rubix-bios -d data -c config -a apps --prod --install --auth"

    @classmethod
    def get_bios_token(cls):
        return r"""curl -X POST http://localhost:1615/api/users/login -H "Content-Type: application/json" -d '{"username":
        "admin", "password": "N00BWires"}'"""

    @classmethod
    def install_rubix_service(cls, token, version):
        url = f"""curl -X PUT http://localhost:1615/api/service/upgrade -H "Content-Type: application/json" -H "Authorization: {token}" -d '{{"version": "{version}"}}'"""
        return url

    @classmethod
    def get_rubix_service_token(cls):
        return r"""curl -X POST http://localhost:1616/api/users/login -H "Content-Type: application/json" -d '{"username":
        "admin", "password": "N00BWires"}'"""

    @classmethod
    def download_rubix_service_app(cls, token, service, version):
        download = f"""curl -X POST http://localhost:1616/api/app/download -H "Content-Type: application/json" -H "Authorization: {token}" -d '{{"service": "{service}", "version": "{version}"}}'"""
        return download

    @classmethod
    def install_rubix_service_app(cls, token, service, version):
        download = f"""curl -X POST http://localhost:1616/api/app/install -H "Content-Type: application/json" -H "Authorization: {token}" -d '{{"service": "{service}", "version": "{version}"}}'"""
        return download

    @classmethod
    def service_command(cls, command, service):
        return f"sudo systemctl {command} {service}.service "

    @classmethod
    def make_data_dir(cls):
        return f"sudo mkdir /data"

    @classmethod
    def make_dir_service_config(cls, service):
        return f"sudo mkdir -p /data/{service}/config"

    @classmethod
    def download_config_file(cls, service):
        return f"curl -OL https://raw.githubusercontent.com/NubeIO/rubix-pi-image/main/config-files/{service}/config.json"

    @classmethod
    def move_config_file(cls, service):
        return f"sudo mv config.json /data/{service}/config/config.json"

    @classmethod
    def delete_home_dir(cls):
        return f"sudo rm -r *"

    @classmethod
    def delete_data_dir(cls):
        return f"sudo rm -r /data"

    @classmethod
    def reboot_host(cls):
        return f"sudo reboot"
