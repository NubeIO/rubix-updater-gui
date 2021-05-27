import logging
import os
from time import sleep

import githubdl
from datetime import datetime

from invoke import Responder

from app.core.commands import LinuxCommands
from app.core.logger import LoggerSetup
from app.core.make_connection import SSHConnection
from app.core.tasks_rubix import file_transfer_stm, file_transfer_stm_build, deploy_rubix_update, command_ls, \
    deploy_rubix_service_update, reboot_host
from app.utils.utils import Utils

RUBIX_IMAGE_REPO = "https://github.com/NubeIO/rubix-pi-image"
RUBIX_SERVICE_CONFIG = "config-files/rubix-apps"
RUBIX_SERVICE_DIR = '/data/rubix-service/config'
POINT_SERVER_CONFIG = "config-files/point-server"
STM_FLASH_SCRIPT = "scripts/rubix"
STM_FLASH_BUILD = "builds"
POINT_SERVER_PATH = "./config-files/point-server/point-server/config.json"
BACNET_SERVER_PATH = "./config-files/bacnet-server/bacnet-server"
HOME_DIR = '/home/pi'
CWD = os.getcwd()


class RubixUpdateLogger:
    def __init__(self, parent):
        self.parent = parent
        LoggerSetup(self.parent)


class ScratchPadController:
    def __init__(self, parent, app):

        self.parent = parent
        RubixUpdateLogger(self.parent)
        self.app = app
        # tab host connection
        self.parent.action_remote_update_connect.pressed.connect(self._check_rc_connection)
        self.parent.action_remote_ping_host.pressed.connect(self._ping_host)

        # update rubix bios
        self.parent.action_remote_update.pressed.connect(self._update_rubix)
        self.parent.action_remote_update.setEnabled(False)

        # update rubix service
        self.parent.action_remote_rubix_service.pressed.connect(self._update_rubix_service)
        self.parent.action_remote_rubix_service.setEnabled(False)

        # flash lora
        self.parent.action_lora_reflash.pressed.connect(self._lora_reflash)

        # check bbb connection
        self.parent.bbb_host_check_connection.pressed.connect(self.check_bbb_connection)
        # update bbb ip
        self.parent.run_update_bbb_ip.setEnabled(False)
        self.parent.run_update_bbb_ip.pressed.connect(self.run_update_bbb_ip)
        # rubix_reboot
        self.parent.rubix_reboot.pressed.connect(self._reboot_rubix)

    def _connection(self):
        host = self.parent.setting_remote_update_host.text()
        port = self.parent.setting_remote_update_port.text()
        user = self.parent.setting_remote_update_user.text()
        password = self.parent.setting_remote_update_password.text()
        logging.info(f"try and connect with host:{host} port:{port} user:{user}")
        time = self._time_stamp()
        cx = SSHConnection(
            host=host,
            port=port,
            user=user,
            connect_timeout=5,
            password=password
        ).connect()
        if not cx:
            msg = f"device on ip: {host} is DEAD {time}"
            self.parent.statusBar.showMessage(msg)
            return False
        else:
            msg = f"device on ip: {host} is connected {time}"
            self.parent.statusBar.showMessage(msg)
            return cx

    def _check_rc_connection(self):
        cx = self._connection()
        if not cx:
            self.parent.action_remote_update.setEnabled(False)
            self.parent.action_remote_rubix_service.setEnabled(False)
        else:
            self.parent.action_remote_update.setEnabled(True)
            self.parent.action_remote_rubix_service.setEnabled(True)

    def _connection_bbb(self):
        host = self.parent.bbb_host.text()
        port = self.parent.bbb_port.text()
        user = self.parent.bbb_user.text()
        password = self.parent.bbb_password.text()
        time = self._time_stamp()
        logging.info(f"try and connect with host:{host} port:{port} user:{user}")
        cx = SSHConnection(
            host=host,
            port=port,
            user=user,
            connect_timeout=5,
            password=password
        ).connect()
        if not cx:
            msg = f"device on ip: {host} is DEAD {time}"
            self.parent.statusBar.showMessage(msg)
            return False
        else:
            msg = f"device on ip: {host} is connected {time}"
            self.parent.statusBar.showMessage(msg)
            return cx

    def _connection_status(self):
        cx = self._connection()
        ip = self.parent.setting_remote_update_host.text()
        time = self._time_stamp()
        if not cx:
            msg = f"device on ip: {ip} is DEAD {time}"
            self.parent.statusBar.showMessage(msg)
            return False
        else:
            msg = f"device on ip: {ip} is cnnected {time}"
            self.parent.statusBar.showMessage(msg)
            return cx

    def _lora_reflash(self):
        cx = self._connection()

        github_token = self.parent.github_token.text()
        githubdl.dl_dir(RUBIX_IMAGE_REPO, STM_FLASH_SCRIPT,
                        github_token=github_token)
        file_stm_script = f"{CWD}/{STM_FLASH_SCRIPT}/rubix/stm-flasher.py"
        self.parent.statusBar.showMessage(f"LOG: DOWNLOAD STM SCRIPT")
        githubdl.dl_dir(RUBIX_IMAGE_REPO, STM_FLASH_BUILD,
                        github_token=github_token)
        file_stm_bin = f"{CWD}/{STM_FLASH_BUILD}/r-c-loraraw_subnet-1_v0.2.bin"
        file_transfer_stm(cx, file_stm_script, HOME_DIR)
        self.parent.statusBar.showMessage(f"LOG: START STM INSTALL")
        file_transfer_stm_build(cx, file_stm_bin, HOME_DIR)

    def _update_rubix(self):
        cx = self._connection()
        ip = self.parent.setting_remote_update_host.text()
        rubix_username = self.parent.rubix_username.text()
        rubix_password = self.parent.rubix_password.text()
        rubix_bios_port = self.parent.rubix_bios_port.text()
        rubix_service_port = self.parent.rubix_service_port.text()
        github_token = self.parent.github_token.text()
        ping = Utils.ping(ip)
        if ping:
            msg = f"device on ip: {ip} is connected"
            self.parent.statusBar.showMessage(msg)
            logging.info(msg)
            logging.info("------ Connect and start updates ------")
            deploy_rubix_update(cx,
                                host=ip,
                                github_token=github_token,
                                rubix_username=rubix_username,
                                rubix_password=rubix_password,
                                rubix_bios_port=rubix_bios_port,
                                rubix_service_port=rubix_service_port
                                )
            msg = f"install completed"
            logging.debug(msg)
            return msg
        else:
            msg = f"device on ip: {ip} is dead"
            self.parent.statusBar.showMessage(msg)
            logging.debug(msg)
            return msg

    def _reboot_rubix(self):
        cx = self._connection()
        ip = self.parent.setting_remote_update_host.text()
        # rubix_username = self.parent.rubix_username.text()
        # rubix_password = self.parent.rubix_password.text()
        # rubix_bios_port = self.parent.rubix_bios_port.text()
        # rubix_service_port = self.parent.rubix_service_port.text()
        ping = Utils.ping(ip)

        if ping:
            msg = f"device on ip: {ip} is connected"
            self.parent.statusBar.showMessage(msg)
            logging.info(msg)
            logging.info("------ Connect and start updates ------")
            reboot_host(cx)
            msg = f"install completed"
            logging.debug(msg)
            return msg
        else:
            msg = f"device on ip: {ip} is dead"
            self.parent.statusBar.showMessage(msg)
            logging.debug(msg)
            return msg

    def _update_rubix_service(self):
        cx = self._connection()
        ip = self.parent.setting_remote_update_host.text()
        rubix_username = self.parent.rubix_username.text()
        rubix_password = self.parent.rubix_password.text()
        rubix_bios_port = self.parent.rubix_bios_port.text()
        rubix_service_port = self.parent.rubix_service_port.text()
        ping = Utils.ping(ip)

        github_token = self.parent.github_token.text()
        githubdl.dl_dir(RUBIX_IMAGE_REPO, RUBIX_SERVICE_CONFIG,
                        github_token=github_token)
        file = f"{CWD}/{RUBIX_SERVICE_CONFIG}/rubix-apps/app.json"
        print(file, 33333333333)
        exe = cx.put(file, RUBIX_SERVICE_DIR)
        # exe = SSHConnection.run_sftp(cx, file, RUBIX_SERVICE_DIR)
        print(exe, 44444444)
        if ping:
            msg = f"device on ip: {ip} is connected"
            self.parent.statusBar.showMessage(msg)
            logging.info(msg)
            logging.info("------ Connect and start updates ------")
            deploy_rubix_service_update(cx,
                                        host=ip,
                                        github_token=github_token,
                                        rubix_username=rubix_username,
                                        rubix_password=rubix_password,
                                        rubix_bios_port=rubix_bios_port,
                                        rubix_service_port=rubix_service_port
                                        )
            msg = f"install completed"
            logging.debug(msg)
            return msg
        else:
            msg = f"device on ip: {ip} is dead"
            self.parent.statusBar.showMessage(msg)
            logging.debug(msg)
            return msg

    def check_bbb_connection(self):
        cx = self._connection_bbb()
        if not cx:
            self.parent.run_update_bbb_ip.setEnabled(False)
        else:
            self.parent.run_update_bbb_ip.setEnabled(True)

    def run_update_bbb_ip(self):
        cx = self._connection_bbb()
        bbb_new_ip = self.parent.bbb_new_ip.text()
        bbb_new_mask = self.parent.bbb_new_mask.text()
        bbb_new_router = self.parent.bbb_new_router.text()

        sudo_pass = Responder(
            pattern=r'\[sudo\] password for debian:',
            response='N00B2828\n',
        )

        # exe = cx.run()
        exe = SSHConnection.run_command(cx, LinuxCommands.command_blank("connmanctl services"))
        iface = ''.join(exe.split())[8:]
        print(iface)
        new_ip = f"sudo connmanctl config {iface} --ipv4 manual {bbb_new_ip} {bbb_new_mask} {bbb_new_router} --nameservers 8.8.8.8"
        print(new_ip)
        # new_ip = "sudo pwd"
        print(new_ip)
        cx.run(new_ip, pty=True, watchers=[sudo_pass])
        new_ip = "sudo pwd"
        print(new_ip)
        cx.run(new_ip, pty=True, watchers=[sudo_pass])

    def _clear_console(self):
        print("ADD LATER")

    def _time_stamp(self):
        dt = datetime.now()
        time = dt.strftime("%d-%b-%Y (%H:%M:%S)")
        return time

    def _ping_host(self):
        ip = self.parent.setting_remote_update_host.text()
        cx = self._connection_status()
        time = self._time_stamp()
        print(cx, 666666666)
        if not cx:
            msg = f"device on ip: {ip} is DEAD {time}"
            logging.info(msg)
        else:
            exe = command_ls(cx)
            if "ERROR" in exe:
                msg = f"device on ip: {ip} is DEAD {time}"
                self.parent.statusBar.showMessage(msg)
            else:
                msg = f"device on ip: {ip} is connected {time}"
                self.parent.statusBar.showMessage(msg)

    def _update_options(self):
        op = self.parent.setting_remote_update_type.currentText()
        op_service = "install rubix service"
        op_service_bios = "install bios & rubix service"
        if op == op_service:
            print(op)
        elif op == op_service_bios:
            print(op)
