import logging
from fabric import task
from app.core.commands import LinuxCommands
from app.core.make_connection import SSHConnection
from app.core.rubix_service_api import RubixApi
from app.core.wires_plat_api import WiresPlatApi
from config.load_config import get_config_host, get_config_rubix_service, get_config_wires_plat_settings, \
    get_config_bios, get_config_wires_plat_user, get_point_server_config, get_lora_raw_config

logging.basicConfig(level=logging.INFO)

_get_config_wires_plat_settings = get_config_wires_plat_settings()
_bios_settings = get_config_bios()
_config_wires_plat_user = get_config_wires_plat_user()

IP = None
RS_PORT = None
wires_plat_user = _config_wires_plat_user.get('get_wires_plat_user')
wires_plat_password = _config_wires_plat_user.get('get_wires_plat_password')
_host_settings = get_config_host()
_rubix_settings = get_config_rubix_service()
_lora_config = get_lora_raw_config()
_point_server = get_point_server_config()

rubix_bios_user = _bios_settings.get('get_rubix_bios_user')
rubix_bios_password = _bios_settings.get('get_rubix_bios_password')
rubix_service_user = _rubix_settings.get('get_rubix_service_user')
rubix_service_password = _rubix_settings.get('get_rubix_service_password')
lora_config = _lora_config.get('get_lora_raw_config')
point_server_config = _point_server.get('get_point_server_config')


@task
def deploy_rubix_update(ctx):
    with ctx as c:
        delete_data_dir(c)
        mk_dir_data(c)
        delete_rubix_dirs(c)
        install_bios(c)
        return "install completed"


@task
def deploy_rubix_service_update(ctx, **kwargs):
    host = kwargs.get('host')
    github_token = kwargs.get('github_token')
    rubix_username = kwargs.get('rubix_username')
    rubix_password = kwargs.get('rubix_password')
    rubix_bios_port = kwargs.get('rubix_bios_port')
    rubix_service_port = kwargs.get('rubix_service_port')
    with ctx as c:
        install_rubix_service(c, host,
                              github_token,
                              rubix_username=rubix_username,
                              rubix_password=rubix_password,
                              rubix_bios_port=rubix_bios_port,
                              rubix_service_port=rubix_service_port
                              )
        return "install completed"


@task
def file_transfer_stm(ctx, file, directory):
    exe = SSHConnection.run_sftp(ctx, file, directory)
    logging.info(f"LOG: @func transfer stm file {exe}")
    exe = SSHConnection.run_command(ctx, LinuxCommands.install_dfu())
    logging.info(f"LOG: @func install_dfu {exe}")


@task
def file_transfer_stm_build(ctx, file, directory):
    exe = SSHConnection.run_sftp(ctx, file, directory)
    logging.info(f"LOG: @func transfer stm file {exe}")
    exe = SSHConnection.run_command(ctx, LinuxCommands.run_stm_file())
    logging.info(f"LOG: @func run_stm_file {exe}")
    return exe

@task
def task_command_blank(ctx, command):
    exe = SSHConnection.run_command(ctx, LinuxCommands.command_blank(command))
    logging.info(f"LOG: @func command_blank {exe}")
    return exe

@task
def command_ls(ctx):
    exe = SSHConnection.run_command(ctx, LinuxCommands.command_ls("/home"))
    logging.info(f"LOG: @func command_ls {exe}")
    return exe


@task
def reboot_host(ctx):
    exe = SSHConnection.run_command(ctx, LinuxCommands.reboot_host())
    logging.info(f"LOG: @func reboot_host {exe}")
    return exe


@task
def delete_rubix_dirs(ctx):
    exe = SSHConnection.run_command(ctx, LinuxCommands.delete_rubix_dirs())
    logging.info(f"LOG: @func delete_rubix_dirs {exe}")
    return exe


@task
def delete_data_dir(ctx):
    exe = SSHConnection.run_command(ctx, LinuxCommands.delete_data_dir())
    logging.info(f"LOG: @func delete_data_dir {exe}")
    return exe


@task
def mk_dir_data(ctx):
    exe = SSHConnection.run_command(ctx, LinuxCommands.make_data_dir())
    logging.info(f"LOG: @func mk_dir_data {exe}")
    exe = SSHConnection.run_command(ctx, LinuxCommands.chown_data_dir())
    logging.info(f"LOG: @func chown_data_dir {exe}")
    exe = SSHConnection.run_command(ctx, LinuxCommands.make_rubix_service_dir())
    logging.info(f"LOG: @func make_rubix_service_dir {exe}")
    exe = SSHConnection.run_command(ctx, LinuxCommands.make_rubix_service_dir_config())
    logging.info(f"LOG: @func make_rubix_service_dir_config {exe}")
    exe = SSHConnection.run_command(ctx, LinuxCommands.chown_data_dir())
    logging.info(f"LOG: @func chown_data_dir {exe}")
    # mkdir point-server
    exe = SSHConnection.run_command(ctx, LinuxCommands.make_dir_service_config("point-server"))
    logging.info(f"LOG: @func mkdir point-server {exe}")
    # make lora-raw
    exe = SSHConnection.run_command(ctx, LinuxCommands.make_dir_service_config("lora-raw"))
    logging.info(f"LOG: @func mkdir lora-raw {exe}")
    exe = SSHConnection.run_command(ctx, LinuxCommands.chown_data_dir())
    logging.info(f"LOG: @func chown_data_dir {exe}")
    return exe


@task
def install_bios(ctx):
    logging.info(f"LOG: >>>>>>>>>>> INSTALL BIOS >>>>>>>>>>> ")
    exe = SSHConnection.run_command(ctx, LinuxCommands.download_bios())
    logging.info(f"LOG: @func install_bios {exe}")
    logging.info(f"LOG: INSTALL BIOS -> unzip")
    exe = SSHConnection.run_command(ctx, LinuxCommands.unzip_bios())
    logging.info(f"LOG: @func install_bios {exe}")
    logging.info(f"LOG: INSTALL BIOS -> run install")
    exe = SSHConnection.run_command(ctx, LinuxCommands.install_bios())
    logging.info(f"LOG: @func install_bios {exe}")
    return exe


@task
def install_rubix_service(ctx, host, github_token, **kwargs):
    bios_token = RubixApi.bios_get_token(host)
    RubixApi.bios_add_git_token(host, bios_token, github_token)
    RubixApi.install_rubix_service(host, bios_token)
    rubix_token = RubixApi.get_rubix_service_token(host)
    RubixApi.rubix_add_git_token(host, rubix_token, github_token)
    app = "RUBIX_PLAT"
    version = "latest"
    RubixApi.install_rubix_app(host, rubix_token, app, version)


def _add_rubix_users_and_settings(url):
    token = WiresPlatApi.get_token(url, name=wires_plat_user, password=wires_plat_password)
    _body = _get_config_wires_plat_settings.get('get_wires_plat_settings')
    put_settings = WiresPlatApi.put_settings(url, token, _body)
    if put_settings:
        print(f"PASS: Add settings")
    else:
        print(f"FAIL: Add settings")

    service = "rubixBios"  # rubixBios rubixService
    _body = {"username": rubix_bios_user, "password": rubix_bios_password}
    put_user_bios = WiresPlatApi.put_bios_user(url, token, _body, service=service)
    if put_user_bios:
        print(f"PASS: Add bios user Ok")
    else:
        print(f"FAIL: Add bios user Fail")

    _body = {"username": rubix_bios_user, "password": rubix_bios_password}
    service = "rubixService"  # rubixBios rubixService
    put_user_rubix = WiresPlatApi.put_bios_user(url, token, _body, service=service)
    if put_user_rubix:
        print(f"PASS: Add rubix service user Ok")
    else:
        print(f"FAIL: Add rubix service user Fail")


def _app_status(host, action, app, response):
    if response:
        logging.info(f"PASS: start | stop | restart app: {app} action: {action} host: {host}")
    else:
        logging.info(f"FAIL: start | stop | restart app: {app} action: {action} host: {host}")


def _select_config(app):
    if app == "LORA_RAW":
        return lora_config


def install_rubix_app(host, version, app, add_config, action, **kwargs):
    username = rubix_service_user
    password = rubix_service_password
    if action == "RUBIX_PLAT_ADD_CREDENTIALS":
        url = f"{host}"
        _add_rubix_users_and_settings(url)
    else:
        access_token = RubixApi.get_rubix_service_token(host, username=username, password=password)
        if access_token != False:
            if action == "START":
                response = RubixApi.start_stop_app(host, access_token, action, app)
                _app_status(host, action, app, response)
            elif action == "STOP":
                response = RubixApi.start_stop_app(host, access_token, action, app)
                _app_status(host, action, app, response)
            elif action == "RESTART":
                response = RubixApi.start_stop_app(host, access_token, action, app)
                _app_status(host, action, app, response)
            elif action == "STATUS":
                response = RubixApi.start_stop_app(host, access_token, action, app)
                _app_status(host, action, app, response)
            elif action == "INSTALL":
                if add_config:
                    config_file = _select_config(app)
                    config = RubixApi.rubix_add_config_file(host, access_token, config_file)
                    if config:
                        logging.info(f"PASS: Add config file service: {app}")
                        logging.info(f"try and instll app: {app}")
                        RubixApi.install_rubix_app(host, access_token, app, version)
                    else:
                        logging.info(f"FAIL: Add config file service: {app}")
                else:
                    RubixApi.install_rubix_app(host, access_token, app, version)
