import logging

from app.core.logger import LoggerSetup


class RubixUpdate:
    def __init__(self, parent):
        self.parent = parent
        # tab Host connection
        self.parent.setting_remote_update_host.text()
        self.parent.setting_remote_update_port.text()
        self.parent.setting_remote_update_user.text()
        self.parent.setting_remote_update_password.text()


class RubixUpdateOptions:
    def __init__(self, parent):
        self.parent = parent
        self.parent.setting_remote_update_password.text()


class RubixUpdateLogger:
    def __init__(self, parent):
        self.parent = parent
        LoggerSetup(self.parent)


class ScratchPadController:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        # tab host connection
        RubixUpdate(self.parent)
        action_remote_update_connect = self.parent.action_remote_update_connect.pressed.connect(self.on_success)
        # tab options
        RubixUpdateOptions(self.parent)
        # tab options
        RubixUpdateLogger(self.parent)

        self.parent.statusBar.showMessage("Hello")

    def on_success(self):
        shost = self.parent.setting_remote_update_user.text()
        logging.debug(shost)
        print(shost)
        print(22222)
