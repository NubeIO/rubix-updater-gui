import logging
from app.core.logger import LoggerSetup
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
        self.parent.action_remote_update_connect.pressed.connect(self._update_rubix)
        self.parent.action_remote_ping_host.pressed.connect(self._ping_host)
        self.parent.action_remote_clear_console.pressed.connect(self._clear_console)
        # tab options
        self.parent.setting_remote_update_type.currentText()
        # tab logger
        RubixUpdateLogger(self.parent)

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
