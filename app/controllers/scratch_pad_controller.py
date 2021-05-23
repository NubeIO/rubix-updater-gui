import logging
from app.core.logger import LoggerSetup
from app.core.make_connection import SSHConnection
from app.core.tasks_rubix import command_ls
from app.utils.utils import Utils


class RubixUpdateLogger:
    def __init__(self, parent):
        self.parent = parent
        LoggerSetup(self.parent)


class ScratchPadController:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app

        # tab host connection
        self.parent.action_remote_update_connect.pressed.connect(self._connect)
        self.parent.action_remote_ping_host.pressed.connect(self._ping_host)
        self.parent.action_remote_clear_console.pressed.connect(self._clear_console)
        # tab options
        self.parent.setting_remote_update_type.currentText()
        # tab logger
        RubixUpdateLogger(self.parent)
        # make connection

    def _connect(self):
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
        command_ls(cx)

    def _update_rubix(self):
        ip = self.parent.setting_remote_update_host.text()
        ping = Utils.ping(ip)
        if ping:
            msg = f"device on ip: {ip} is connected"
            self.parent.statusBar.showMessage(msg)
            logging.info(msg)
            logging.info("------ Connect and start updates ------")
        else:
            msg = f"device on ip: {ip} is dead"
            self.parent.statusBar.showMessage(msg)
            logging.debug(msg)

    def _clear_console(self):
        print("ADD LATER")

    def _ping_host(self):
        ip = self.parent.setting_remote_update_host.text()
        res = Utils.ping(ip)
        if res:
            msg = f"device on ip: {ip} is connected"
            self.parent.statusBar.showMessage(msg)
            logging.debug(msg)
        else:
            msg = f"device on ip: {ip} is dead"
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
