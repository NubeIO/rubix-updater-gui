from dearpygui.core import *
from dearpygui.simple import *
import os


class MyClass:

    def openFile(self, sender, data):
        open_file_dialog(callback=self.csvUser)
        # ensures only csvs are searched

    def csvUser(self, sender, data):
        filename = os.sep.join(data)
        for i in open(filename, "rt"):
            print(i)


myhandler = MyClass()

with window("Open a csv"):
    add_button("Open", callback=myhandler.openFile)

start_dearpygui()
