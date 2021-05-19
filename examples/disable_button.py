from dearpygui.core import *
from dearpygui.simple import *


def theme_callback(sender, data):
    configure_item("Button 1", enabled=False, label="New Label")
    # set_theme(sender)


with window("Main Window"):
    add_text("these is a basic menu, it does not use context managers from dearpygui.simple which are recomended.")
    add_button("Button 1", enabled=True, label="Press me", callback=theme_callback)


start_dearpygui(primary_window="Main Window")
