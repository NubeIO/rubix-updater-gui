from config.config import Config

file = None
# file = '/home/aidan/code/py-nube/rubix-updater-gui'

c = Config()
c.load_config(file=file)


def get_config_host():
    return {
        "get_host": c.get_host(),
        "get_port": c.get_port(),
        "get_user": c.get_user(),
        "get_password": c.get_password(),
        "get_git_token": c.get_git_token()
    }


def get_config_bios():
    return {
        c.get_git_token.__name__: c.get_git_token(),
        c.get_rubix_bios_user.__name__: c.get_rubix_bios_user(),
        c.get_rubix_bios_password.__name__: c.get_rubix_bios_password(),
        c.get_rubix_bios_port.__name__: c.get_rubix_bios_port(),
    }


def get_config_rubix_service():
    return {
        c.get_rubix_service_user.__name__: c.get_rubix_service_user(),
        c.get_rubix_service_password.__name__: c.get_rubix_service_password(),
        c.get_rubix_service_port.__name__: c.get_rubix_service_port()
    }


def get_config_stm():
    return {
        c.get_stm_version.__name__: c.get_stm_version()
    }


def get_config_rubix_build_repo():
    return {
        c.get_rubix_build_repo.__name__: c.get_rubix_build_repo()
    }


def get_config_wires_plat_settings():
    return {
        c.get_wires_plat_settings.__name__: c.get_wires_plat_settings()
    }


def get_config_wires_plat_user():
    return {
        c.get_wires_plat_user.__name__: c.get_wires_plat_user(),
        c.get_wires_plat_password.__name__: c.get_wires_plat_password()
    }


def get_lora_raw_config():
    return {
        c.get_lora_raw_config.__name__: c.get_lora_raw_config()
    }


def get_point_server_config():
    return {
        c.get_point_server_config.__name__: c.get_point_server_config()
    }
