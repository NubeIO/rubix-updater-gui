import json
import logging
import time
from fabric import task
from app.core.commands import LinuxCommands
from app.core.make_connection import SSHConnection


@task
def deploy_rubix_update(ctx, **kwargs):
    delete_all_dirs = kwargs.get('delete_all_dirs')
    with ctx as c:
        if delete_all_dirs == 0:
            delete_home_dir(c)
            delete_data_dir(c)
        elif delete_all_dirs == 1:
            delete_home_dir(c)
            delete_data_dir(c)
            mk_dir_data(c)
            command_ls(c)
            install_bios(c)
            time.sleep(5)
            install_wires_plat(c)

@task
def file_transfer_stm(ctx, file, directory):
    exe = SSHConnection.run_sftp(ctx, file, directory)
    logging.info(f"LOG: @func file_transfer_stm {exe}")




@task
def command_ls(ctx):
    exe = SSHConnection.run_command(ctx, LinuxCommands.command_ls("/home/pi"))
    logging.info(f"LOG: @func command_ls {exe}")


@task
def delete_home_dir(ctx):
    exe = SSHConnection.run_command(ctx, LinuxCommands.delete_home_dir())
    logging.debug(f"LOG: @func delete_home_dir {exe}")


@task
def delete_data_dir(ctx):
    exe = SSHConnection.run_command(ctx, LinuxCommands.delete_data_dir())
    logging.debug(f"LOG: @func delete_data_dir {exe}")


@task
def delete_data_dir(ctx):
    exe = SSHConnection.run_command(ctx, LinuxCommands.delete_data_dir())
    logging.debug(f"LOG: @func delete_data_dir {exe}")


@task
def mk_dir_data(ctx):
    exe = SSHConnection.run_command(ctx, LinuxCommands.make_data_dir())
    logging.debug(f"LOG: @func mk_dir_data {exe}")


@task
def install_bios(ctx):
    logging.debug(f"LOG: >>>>>>>>>>> INSTALL BIOS >>>>>>>>>>> ")
    exe = SSHConnection.run_command(ctx, LinuxCommands.download_bios())
    logging.debug(f"LOG: @func install_bios {exe}")
    logging.debug(f"LOG: INSTALL BIOS -> unzip")
    exe = SSHConnection.run_command(ctx, LinuxCommands.unzip_bios())
    logging.debug(f"LOG: @func install_bios {exe}")
    logging.debug(f"LOG: INSTALL BIOS -> run install")
    exe = SSHConnection.run_command(ctx, LinuxCommands.install_bios())
    logging.debug(f"LOG: @func install_bios {exe}")
    time.sleep(5)
    exe = SSHConnection.run_command(ctx, LinuxCommands.get_bios_token())
    token = LinuxCommands.clean_token(exe)
    logging.debug(f"LOG: @func clean_token {token}")
    # version = "latest"
    version = "v1.7.0"
    logging.debug(f"LOG: >>>>>>>>>>> INSTALL RUBIX SERVICE >>>>>>>>>>> ")
    exe = SSHConnection.run_command(ctx, LinuxCommands.install_rubix_service(token, version))
    logging.debug(f"LOG: @func install_rubix_service {exe}")


@task
def install_wires_plat(ctx):
    logging.debug(f"LOG: >>>>>>>>>>> INSTALL RUBIX PLATFORM UI >>>>>>>>>>> ")
    exe = SSHConnection.run_command(ctx, LinuxCommands.get_rubix_service_token())
    token = LinuxCommands.clean_token(exe)
    logging.debug(f"LOG: @func clean_token {token}")
    service = "RUBIX_PLAT"
    git_token = "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"
    version = "v1.7.1"
    # version = "latest"
    logging.debug(f"LOG: >>>>>>>>>>> INSTALL RUBIX PLATFORM ADD GITHUB TOKEN >>>>>>>>>>> ")
    exe = SSHConnection.run_command(ctx, LinuxCommands.add_rubix_service_github_token(token, git_token))
    logging.debug(f"LOG: @func add_rubix_service_github_token {exe}")

    logging.debug(f"LOG: >>>>>>>>>>> INSTALL RUBIX PLATFORM DOWNLOAD >>>>>>>>>>> ")
    exe = SSHConnection.run_command(ctx, LinuxCommands.download_rubix_service_app(token, service, version))
    logging.debug(f"LOG: @func download_rubix_service_app {exe}")
    time.sleep(5)
    logging.debug(f"LOG: >>>>>>>>>>> INSTALL RUBIX PLATFORM CHECK DOWNLOAD STATUS >>>>>>>>>>> ")
    max_checks = 20
    time.sleep(2)
    i = 1
    while i < max_checks:
        aa = SSHConnection.run_command(ctx, LinuxCommands.get_state_download_rubix_service_app(token))
        time.sleep(3)
        logging.debug(f"LOG: >>>>>>>>>>> CHECK DOWNLOAD STATUS  >>>>>>>>>>> ")
        tt = json.loads(aa)
        tt = tt.get('services')
        if isinstance(tt, list):
            logging.debug(f"LOG: >>>>>>>>>>> DOWNLOADED WIRES-PLAT-COMPLETED >>>>>>>>>>> ")
            ttt = tt[0].get('download')
            if ttt:
                SSHConnection.run_command(ctx, LinuxCommands.delete_state_download_rubix_service_app(token))
                logging.debug(f"LOG: >>>>>>>>>>> DOWNLOADED WIRES-PLAT-COMPLETED DELETED DOWNLOAD>>>>>>>>>>> ")
                break
        i += 1

    logging.debug(f"LOG: >>>>>>>>>>> INSTALL RUBIX PLATFORM INSTALL >>>>>>>>>>> ")
    exe = SSHConnection.run_command(ctx, LinuxCommands.install_rubix_service_app(token, service, version))
    logging.debug(f"LOG: @func install_rubix_service_app {exe}")
    time.sleep(8)
    exe = SSHConnection.run_command(ctx, LinuxCommands.service_command("status", "nubeio-wires-plat"))
    logging.debug(f"LOG: @func service_command {exe}")
