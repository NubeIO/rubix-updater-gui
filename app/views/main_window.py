import logging
import traceback

import sys
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QMainWindow, qApp

from app.controllers import (
    MainWindowController,

    ScratchPadController,
)
from app.generated.MainWindow_ui import Ui_MainWindow
from app.settings.app_settings import app


class MainWindow(QMainWindow, Ui_MainWindow):
    """Main Window."""

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        # Initialise controllers
        self.main_controller = MainWindowController(self, app)
        self.scratch_pad_controller = ScratchPadController(self, app)
        sys.excepthook = MainWindow.log_uncaught_exceptions



    @staticmethod
    def log_uncaught_exceptions(cls, exc, tb) -> None:
        logging.critical("".join(traceback.format_tb(tb)))
        logging.critical("{0}: {1}".format(cls, exc))

    def closeEvent(self, event: QCloseEvent):
        logging.info("Received close event")
        event.accept()
        # self.main_controller.shutdown()
        try:
            qApp.exit(0)
        except:
            pass