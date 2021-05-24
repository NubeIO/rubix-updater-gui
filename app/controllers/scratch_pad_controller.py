import logging
import os
from time import sleep

import githubdl
from datetime import datetime
from app.core.logger import LoggerSetup
from app.core.make_connection import SSHConnection
from app.core.tasks_rubix import file_transfer_stm, file_transfer_stm_build, deploy_rubix_update
from app.utils.utils import Utils

RUBIX_IMAGE_REPO = "https://github.com/NubeIO/rubix-pi-image"
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
        # self.parent.action_remote_update_connect.pressed.connect(self._connect)
        self.parent.action_remote_ping_host.pressed.connect(self._ping_host)
        self.parent.action_remote_clear_console.pressed.connect(self._clear_console)
        # flash lora
        self.parent.action_lora_reflash.pressed.connect(self._lora_reflash)
        # update rubix
        self.parent.action_remote_update.pressed.connect(self._update_rubix)

        # make connection




    def _connection(self):
        host = self.parent.setting_remote_update_host.text()
        port = self.parent.setting_remote_update_port.text()
        user = self.parent.setting_remote_update_user.text()
        password = self.parent.setting_remote_update_password.text()
        logging.info(f"try and connect with host:{host} port:{port} user:{user}")
        cx = SSHConnection(
            host=host,
            port=port,
            user=user,
            password=password
        ).connect()
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
        else:
            msg = f"device on ip: {ip} is dead"
            self.parent.statusBar.showMessage(msg)
            logging.debug(msg)

    def _clear_console(self):
        print("ADD LATER")

    def _ping_host(self):
        ip = self.parent.setting_remote_update_host.text()
        res = Utils.ping(ip)
        dt = datetime.now()
        time = dt.strftime("%d-%b-%Y (%H:%M:%S)")
        if res:
            msg = f"device on ip: {ip} is connected {time}"
            self.parent.statusBar.showMessage(msg)
            logging.warning("1212123132")
            logging.warning(msg)
            self._ping_host2()
        else:
            msg = f"device on ip: {ip} is dead {time}"
            self.parent.statusBar.showMessage(msg)
            logging.debug(msg)

    def _ping_host2(self):
        ip = self.parent.setting_remote_update_host.text()
        res = Utils.ping(ip)
        dt = datetime.now()
        time = dt.strftime("%d-%b-%Y (%H:%M:%S)")
        if res:
            msg = f"device on ip: {ip} is connected {time}"
            self.parent.statusBar.showMessage(msg)
            logging.warning("_ping_host2")
            # sleep(5)
            logging.warning(msg)
        else:
            msg = f"device on ip: {ip} is dead {time}"
            self.parent.statusBar.showMessage(msg)
            logging.debug(msg)

    def _update_options(self):
        op = self.parent.setting_remote_update_type.currentText()
        op_service = "install rubix service"
        op_service_bios = "install bios & rubix service"
        if op == op_service:
            print(op)
        elif op == op_service_bios:
            print(op)
