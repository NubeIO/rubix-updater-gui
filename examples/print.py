from dearpygui.core import *
from dearpygui.simple import *


def print_me(sender, data):
    log_debug(f"Menu Item: {sender}")


show_logger()

with window("Tutorial"):

    with menu_bar("Main Menu Bar"):

        with menu("File"):

            add_menu_item("Save", callback=print_me)
            add_menu_item("Save As", callback=print_me)

            with menu("Settings"):

                add_menu_item("Setting 1", callback=print_me)
                add_menu_item("Setting 2", callback=print_me)

        add_menu_item("Help", callback=print_me)

        with menu("Widget Items"):

            add_checkbox("Pick Me", callback=print_me)
            add_button("Press Me", callback=print_me)
            add_color_picker4("Color Me", callback=print_me)

start_dearpygui()