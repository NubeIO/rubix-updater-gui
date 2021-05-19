from dearpygui.core import *
from dearpygui.simple import *

with window("Tutorial"):
    add_text("Right Click Me")
    add_button("Button 1", enabled=True, label="Press me")
    # at a later time, change the item's configuration
    configure_item("Button 1", enabled=False, label="New Label")

    with popup("Right Click Me", "Popup ID", modal=True):
        add_button("Close", callback=lambda: close_popup("Popup ID"))

start_dearpygui()
