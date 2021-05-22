#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PyQt5 - QMainWindow with menubar
Author: niftycode
Date created: March 15th, 2020
"""

import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication,
    QWidget, QAction, qApp)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Create a new widget object (window)
        widget = QWidget()
        self.setCentralWidget(widget)
        self.title = 'Qt5-MainWindow with menubar'
        self.left = 300
        self.top = 300
        self.width = 450
        self.height = 300

        self.create_actions()
        self.init_ui()

    def create_actions(self):

        # Add a quit action
        self.quit_action = QAction('&Quit', self)
        self.quit_action.setShortcut('Ctrl+Q')
        self.quit_action.setStatusTip('Exit this application.')
        self.quit_action.triggered.connect(qApp.quit)

    def create_menubar(self):
        # Create menubar
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        self.file_menu.addAction(self.quit_action)

    def init_ui(self):

        # Create menus
        self.file_menu = self.menuBar().addMenu('&File')
        self.create_menubar()

        # Set basic window layout
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())