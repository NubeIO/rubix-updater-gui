import time

from dearpygui.core import show_logger
from fabric import task

from src.common_ssh.ssh import SSHConnection
from src.common_ui.logs import Common
from src.linux_commands.commands import LinuxCommands


@task
def deploy_rubix_update(ctx, **kwargs):
    delete_all_dirs = kwargs.get('delete_all_dirs')
    install_rubix_plat = kwargs.get('install_rubix_plat')
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
        # if install_rubix_plat == 0 and delete_all_dirs == 1:
        #     install_wires_plat(c)


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
    print(1111111)
    print(exe)
    print(111111)
    token = LinuxCommands.clean_token(exe)
    Common.log(f"LOG: @func clean_token {token}")
    version = "v1.6.8"
    Common.log(f"LOG: >>>>>>>>>>> INSTALL RUBIX SERVICE >>>>>>>>>>> ")
    exe = SSHConnection.run_command(ctx, LinuxCommands.install_rubix_service(token, version))
    Common.log(f"LOG: @func install_rubix_service {exe}")


@task
def install_wires_plat(ctx):
    Common.log(f"LOG: >>>>>>>>>>> INSTALL RUBIX PLATFORM UI >>>>>>>>>>> ")
    time.sleep(5)
    exe = SSHConnection.run_command(ctx, LinuxCommands.get_rubix_service_token())
    token = LinuxCommands.clean_token(exe)
    Common.log(f"LOG: @func clean_token {token}")
    service = "RUBIX_PLAT"
    version = "v1.7.0"
    Common.log(f"LOG: >>>>>>>>>>> INSTALL RUBIX PLATFORM DOWNLOAD >>>>>>>>>>> ")
    exe = SSHConnection.run_command(ctx, LinuxCommands.download_rubix_service_app(token, service, version))
    Common.log(f"LOG: @func download_rubix_service_app {exe}")
    Common.log(f"LOG: >>>>>>>>>>> INSTALL RUBIX PLATFORM INSTALL >>>>>>>>>>> ")
    exe = SSHConnection.run_command(ctx, LinuxCommands.install_rubix_service_app(token, service, version))
    Common.log(f"LOG: @func install_rubix_service_app {exe}")
    time.sleep(2)
    Common.log(f"LOG: >>>>>>>>>>> INSTALL RUBIX PLATFORM RESTART >>>>>>>>>>> ")
    exe = SSHConnection.run_command(ctx, LinuxCommands.service_command("restart", "nubeio-wires-plat"))
    Common.log(f"LOG: @func service_command {exe}")
    Common.log(f"LOG: >>>>>>>>>>> INSTALL RUBIX PLATFORM STATUS >>>>>>>>>>> ")
    time.sleep(10)
    exe = SSHConnection.run_command(ctx, LinuxCommands.service_command("status", "nubeio-wires-plat"))
    Common.log(f"LOG: @func service_command {exe}")
    time.sleep(2)
    if True:
        SSHConnection.run_command(ctx, LinuxCommands.reboot_host())

