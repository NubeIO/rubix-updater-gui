import sys
from PyQt5 import QtWidgets,QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *

# https://github.com/ahmetcevdetbulbul/pyQt5-exercises

class Window(QtWidgets.QWidget):
    def __init__(self):

        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.text_area = QtWidgets.QLabel("haven't been clicked")
        self.button = QtWidgets.QPushButton("Click")
        self.count = 0
        self.setWindowTitle("Just Click")
        self.setGeometry(100,200,400,200)
        self.label = QLabel(self)
        self.pixmap = QPixmap('firstphoto.jpg')
        self.label.setPixmap(self.pixmap)
        self.label.resize(self.pixmap.width(),self.pixmap.height())
        self.text_area.setStyleSheet("color: red;")
        v_box = QtWidgets.QVBoxLayout()

        v_box.addWidget(self.text_area)
        v_box.addWidget(self.button)
        v_box.addStretch()

        h_box = QtWidgets.QHBoxLayout()

        h_box.addStretch()
        h_box.addLayout(v_box)
        h_box.addStretch()

        self.setLayout(h_box)

        self.button.clicked.connect(self.click)

        self.show()

    def click(self):
        self.count += 1
        print(222222)
        self.text_area.setText(str(self.count) + " time clicked")




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window1 = Window()



    sys.exit(app.exec_())

