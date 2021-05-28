import json
import logging
import time
from fabric import task
from app.core.commands import LinuxCommands
from app.core.make_connection import SSHConnection
from app.core.rubix_service_api import RubixApi


@task
def deploy_rubix_update(ctx, **kwargs):
    with ctx as c:
        delete_data_dir(c)
        mk_dir_data(c)
        delete_rubix_dirs(c)
        command_ls(c)
        install_bios(c)
        return "install completed"


@task
def deploy_rubix_service_update(ctx, **kwargs):
    delete_all_dirs = kwargs.get('delete_all_dirs')
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


@task
def delete_data_dir(ctx):
    exe = SSHConnection.run_command(ctx, LinuxCommands.delete_data_dir())
    logging.info(f"LOG: @func delete_data_dir {exe}")


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


@task
def install_rubix_service(ctx, host, github_token, **kwargs):
    rubix_username = kwargs.get('rubix_username')
    rubix_password = kwargs.get('rubix_password')
    rubix_bios_port = kwargs.get('rubix_bios_port')
    rubix_service_port = kwargs.get('rubix_service_port')
    print(22222, rubix_username, rubix_password, rubix_bios_port, rubix_service_port)
    bios_token = RubixApi.bios_get_token(host)
    print(22222, bios_token)
    RubixApi.bios_add_git_token(host, bios_token, github_token)
    RubixApi.install_rubix_service(host, bios_token)
    rubix_token = RubixApi.get_rubix_service_token(host)
    RubixApi.rubix_add_git_token(host, rubix_token, github_token)
    RubixApi.install_wires_plat(host, rubix_token)


@task
def install_wires_plat(ctx):
    logging.info(f"LOG: >>>>>>>>>>> INSTALL RUBIX PLATFORM UI >>>>>>>>>>> ")
    exe = SSHConnection.run_command(ctx, LinuxCommands.get_rubix_service_token())
    token = LinuxCommands.clean_token(exe)
    logging.info(f"LOG: @func clean_token {token}")
    service = "RUBIX_PLAT"
    # git_token = "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"
    version = "v1.7.1"
    # version = "latest"

    logging.info(f"LOG: >>>>>>>>>>> INSTALL RUBIX PLATFORM DOWNLOAD >>>>>>>>>>> ")
    exe = SSHConnection.run_command(ctx, LinuxCommands.download_rubix_service_app(token, service, version))
    logging.info(f"LOG: @func download_rubix_service_app {exe}")
    time.sleep(5)
    logging.info(f"LOG: >>>>>>>>>>> INSTALL RUBIX PLATFORM CHECK DOWNLOAD STATUS >>>>>>>>>>> ")
    max_checks = 20
    time.sleep(2)
    i = 1
    while i < max_checks:
        aa = SSHConnection.run_command(ctx, LinuxCommands.get_state_download_rubix_service_app(token))
        time.sleep(3)
        logging.info(f"LOG: >>>>>>>>>>> CHECK DOWNLOAD STATUS  >>>>>>>>>>> ")
        tt = json.loads(aa)
        tt = tt.get('services')
        if isinstance(tt, list):
            logging.info(f"LOG: >>>>>>>>>>> DOWNLOADED WIRES-PLAT-COMPLETED >>>>>>>>>>> ")
            ttt = tt[0].get('download')
            if ttt:
                SSHConnection.run_command(ctx, LinuxCommands.delete_state_download_rubix_service_app(token))
                logging.info(f"LOG: >>>>>>>>>>> DOWNLOADED WIRES-PLAT-COMPLETED DELETED DOWNLOAD>>>>>>>>>>> ")
                break
        i += 1

    logging.info(f"LOG: >>>>>>>>>>> INSTALL RUBIX PLATFORM INSTALL >>>>>>>>>>> ")
    exe = SSHConnection.run_command(ctx, LinuxCommands.install_rubix_service_app(token, service, version))
    logging.info(f"LOG: @func install_rubix_service_app {exe}")
    time.sleep(8)
    exe = SSHConnection.run_command(ctx, LinuxCommands.service_command("restart", "nubeio-wires-plat"))
    logging.info(f"LOG: @func service_command {exe}")
