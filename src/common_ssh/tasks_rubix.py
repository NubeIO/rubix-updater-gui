import json
import time

from dearpygui.core import show_logger
from fabric import task

from src.common_ssh.ssh import SSHConnection
from src.common_ui.logs import Common
from src.linux_commands.commands import LinuxCommands


@task
def deploy_rubix_update(ctx, **kwargs):
    delete_all_dirs = kwargs.get('delete_all_dirs')
    with ctx as c:
        show_logger()
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
def command_ls(ctx):
    exe = SSHConnection.run_command(ctx, LinuxCommands.command_ls(LinuxCommands.get_path_data()))
    Common.log(f"LOG: @func command_ls {exe}")


@task
def delete_home_dir(ctx):
    exe = SSHConnection.run_command(ctx, LinuxCommands.delete_home_dir())
    Common.log(f"LOG: @func delete_home_dir {exe}")


@task
def delete_data_dir(ctx):
    exe = SSHConnection.run_command(ctx, LinuxCommands.delete_data_dir())
    Common.log(f"LOG: @func delete_data_dir {exe}")


@task
def delete_data_dir(ctx):
    exe = SSHConnection.run_command(ctx, LinuxCommands.delete_data_dir())
    Common.log(f"LOG: @func delete_data_dir {exe}")


@task
def mk_dir_data(ctx):
    exe = SSHConnection.run_command(ctx, LinuxCommands.make_data_dir())
    Common.log(f"LOG: @func mk_dir_data {exe}")


@task
def install_bios(ctx):
    Common.log(f"LOG: >>>>>>>>>>> INSTALL BIOS >>>>>>>>>>> ")
    exe = SSHConnection.run_command(ctx, LinuxCommands.download_bios())
    Common.log(f"LOG: @func install_bios {exe}")
    Common.log(f"LOG: INSTALL BIOS -> unzip")
    exe = SSHConnection.run_command(ctx, LinuxCommands.unzip_bios())
    Common.log(f"LOG: @func install_bios {exe}")
    Common.log(f"LOG: INSTALL BIOS -> run install")
    exe = SSHConnection.run_command(ctx, LinuxCommands.install_bios())
    Common.log(f"LOG: @func install_bios {exe}")
    time.sleep(5)
    exe = SSHConnection.run_command(ctx, LinuxCommands.get_bios_token())
    token = LinuxCommands.clean_token(exe)
    Common.log(f"LOG: @func clean_token {token}")
    version = "latest"
    Common.log(f"LOG: >>>>>>>>>>> INSTALL RUBIX SERVICE >>>>>>>>>>> ")
    exe = SSHConnection.run_command(ctx, LinuxCommands.install_rubix_service(token, version))
    Common.log(f"LOG: @func install_rubix_service {exe}")


@task
def install_wires_plat(ctx):
    Common.log(f"LOG: >>>>>>>>>>> INSTALL RUBIX PLATFORM UI >>>>>>>>>>> ")
    exe = SSHConnection.run_command(ctx, LinuxCommands.get_rubix_service_token())
    token = LinuxCommands.clean_token(exe)
    Common.log(f"LOG: @func clean_token {token}")
    service = "RUBIX_PLAT"
    git_token = "478aadf6e6e392a98e34b2925dec7d56438cc6d6"
    version = "v1.7.1"
    # version = "latest"
    Common.log(f"LOG: >>>>>>>>>>> INSTALL RUBIX PLATFORM ADD GITHUB TOKEN >>>>>>>>>>> ")
    exe = SSHConnection.run_command(ctx, LinuxCommands.add_rubix_service_github_token(token, git_token))
    Common.log(f"LOG: @func add_rubix_service_github_token {exe}")

    Common.log(f"LOG: >>>>>>>>>>> INSTALL RUBIX PLATFORM DOWNLOAD >>>>>>>>>>> ")
    exe = SSHConnection.run_command(ctx, LinuxCommands.download_rubix_service_app(token, service, version))
    Common.log(f"LOG: @func download_rubix_service_app {exe}")
    time.sleep(5)
    Common.log(f"LOG: >>>>>>>>>>> INSTALL RUBIX PLATFORM CHECK DOWNLOAD STATUS >>>>>>>>>>> ")
    max_checks = 20
    time.sleep(2)
    i = 1
    while i < max_checks:
        aa = SSHConnection.run_command(ctx, LinuxCommands.get_state_download_rubix_service_app(token))
        time.sleep(3)
        Common.log(f"LOG: >>>>>>>>>>> CHECK DOWNLOAD STATUS  >>>>>>>>>>> ")
        tt = json.loads(aa)
        if isinstance(tt, list):
            Common.log(f"LOG: >>>>>>>>>>> DOWNLOADED WIRES-PLAT-COMPLETED >>>>>>>>>>> ")
            ttt = tt[0].get('download')
            if ttt:
                SSHConnection.run_command(ctx, LinuxCommands.delete_state_download_rubix_service_app(token))
                Common.log(f"LOG: >>>>>>>>>>> DOWNLOADED WIRES-PLAT-COMPLETED DELETED DOWNLOAD>>>>>>>>>>> ")
                break
        i += 1

    Common.log(f"LOG: >>>>>>>>>>> INSTALL RUBIX PLATFORM INSTALL >>>>>>>>>>> ")
    exe = SSHConnection.run_command(ctx, LinuxCommands.install_rubix_service_app(token, service, version))
    Common.log(f"LOG: @func install_rubix_service_app {exe}")
    time.sleep(8)
    exe = SSHConnection.run_command(ctx, LinuxCommands.service_command("status", "nubeio-wires-plat"))
    Common.log(f"LOG: @func service_command {exe}")
