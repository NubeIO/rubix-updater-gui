import os
import re
import socket
import threading
import sys
import time

import qdarkstyle
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget, QListWidget, QPushButton, QLineEdit, QPlainTextEdit, \
    QVBoxLayout

import logging


class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(False)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)


class chat_window(QWidget):

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        x = event.globalX()
        y = event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x - x_w, y - y_w)

    def __init__(self, parent=None):
        super(chat_window, self).__init__(parent)
        self.setWindowTitle('Rubix Compute Flashing Tool')

        self.setGeometry(400, 400, 800, 600)
        # self.setWindowFlag(Qt.FramelessWindowHint) ## hide the frame
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        self.sendBtn = QPushButton('Send')
        self.sendBtn.setDisabled(True)
        self.discBtn = QPushButton('Disconnect')
        self.discBtn.setDisabled(True)
        self.textbox = QLineEdit('')
        # self.label = QPlainTextEdit('')
        # self.label.setReadOnly(True)
        self.ip_bar = QLineEdit('IP')
        self.q_btn = QPushButton('Exit')
        self.connBtn = QPushButton('Connect')
        self.host = QPushButton('Host')
        self.port = QLineEdit('Port')
        self.name_bar = QLineEdit('Name')
        self.repeat = 0
        self.coding = 1
        self.coded = ''

        layout = QGridLayout()
        log_box = QTextEditLogger(self)

        log_box.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(log_box)
        logging.getLogger().setLevel(logging.DEBUG)

        layout.addWidget(self.sendBtn, 4, 7, 1, 1)
        layout.addWidget(self.discBtn, 1, 6, 1, 1)
        layout.addWidget(self.textbox, 4, 0, 1, 4)
        # layout.addWidget(self.label, 3, 0, 1, 0)  # console

        layout.addWidget(self.q_btn, 1, 7, 1, 1)
        layout.addWidget(self.connBtn, 1, 5, 1, 1)
        # layout.addWidget(self.host, 1, 0, 1, 1)
        layout.addWidget(self.name_bar, 1, 1, 1, 1)
        self.name_bar.setText("pi")
        layout.addWidget(self.ip_bar, 1, 2, 1, 1)
        self.ip_bar.setText("0.0.0.0")
        layout.addWidget(self.port, 1, 3, 1, 1)
        self.port.setText("22")
        layout.addWidget(log_box.widget, 3, 0, 1, 0)

        self.host.clicked.connect(self.startServer)
        self.connBtn.clicked.connect(self.connect)
        self.sendBtn.clicked.connect(self.send_msg)
        self.discBtn.clicked.connect(self.disconnect)
        self.q_btn.clicked.connect(self.exit)

        self._button = QPushButton(self)
        self._button.setText('Test Me')
        layout.addWidget(self._button)
        self._button.clicked.connect(self.test)

        self.setLayout(layout)

    def test(self):
        print(111111)
        # QTextEditLogger(self).clear()
        logging.debug('damn, a bug')
        # logging.info('something to remember')
        # logging.warning('that\'s not right')
        # logging.error('foobar')

    def disconnect(self):
        self.sendBtn.setDisabled(True)
        self.connBtn.setDisabled(False)
        self.discBtn.setDisabled(True)
        self.name_bar.setDisabled(False)
        self.ip_bar.setDisabled(False)

    def send_msg(self):
        message = self.textbox.text()
        name = self.name_bar.text()
        self.client.send_msg_manual(name + ": " + message)
        self.textbox.setText("")

    def exit(self):
        os._exit(1)

    def is_ip(self, ip):
        return re.match(r'^\d{1,255}[.]\d{1,255}[.]\d{1,255}[.]\d{1,255}$', ip)

    def connect(self):
        print(111111)
        try:
            ip = self.ip_bar.text()
            if self.is_ip(ip) is None:
                text = "Invalid IP.\n"
                logging.error(text)

            else:
                # self.start_timer()
                # self.client.connect(ip)
                # disbale the buttons when connected
                self.sendBtn.setDisabled(False)
                self.connBtn.setDisabled(True)
                self.discBtn.setDisabled(False)
                self.name_bar.setDisabled(True)
                self.ip_bar.setDisabled(True)

        except (ConnectionRefusedError, TimeoutError):
            text = self.label.toPlainText()
            text += "No Connection found.\n"
            self.label.setPlainText(text)

    def startServer(self):
        self.connBtn.setDisabled(True)
        self.sendBtn.setDisabled(True)
        self.host.setDisabled(True)

    def refresh_state(self):
        print("refresh_state")
        if self.client.log != self.label.toPlainText():
            self.label.setPlainText(self.client.log)

    # def start_timer(self):
    #     self.timer.start(140)


if __name__ == '__main__':
    if '-s' not in sys.argv:
        app = QApplication(sys.argv)
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        window = chat_window()
        window.show()
        app.exec()
    else:
        try:
            print(222222)
            # client = Client()
            # client.terminal = True
            # client.connect(sys.argv[len(sys.argv) - 1])
        except ConnectionRefusedError:
            print("Failed to connect.")
