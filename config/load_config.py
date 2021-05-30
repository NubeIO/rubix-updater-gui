from config.config import Config

c = Config()
c.load_config()


def get_config_host():
    return {
        c.get_host.__name__: c.get_host(),
        c.get_port.__name__: c.get_port(),
        c.get_user.__name__: c.get_user(),
        c.get_password.__name__: c.get_password(),
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
        c.get_rubix_service_port.__name__: c.get_rubix_service_port(),
        c.get_rubix_bios_port.__name__: c.get_rubix_bios_port(),
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
