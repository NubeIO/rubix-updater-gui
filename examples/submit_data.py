from dearpygui.core import *
from dearpygui.simple import *


def store_data(sender, data):
    custom_data = {
        "Radio Button": get_value("Radio Button"),
        "Checkbox": get_value("Checkbox"),
        "Text Input": get_value("Text Input"),
    }
    add_data("stored_data", custom_data)
    # print(sender, data)
    # print(custom_data)


def print_data(sender, data):
    print(type(get_data("stored_data")))
    print(get_data("stored_data").get("Checkbox"))


with window("Aidans"):
    set_theme("Light")
    set_main_window_size(550, 650)
    set_main_window_resizable(False)
    add_spacing()
    add_radio_button("Radio Button", items=["item1", "item2"])
    add_checkbox("Checkbox")
    add_input_text("Text Input")
    add_button("Store Data", callback=store_data)
    add_button("Print Data", callback=print_data)

    # start_dearpygui()

start_dearpygui(primary_window="Main Window")
