from dearpygui.core import *
from dearpygui.simple import *


def theme_callback(sender, data):
    set_theme(sender)


with window("Main Window"):
    add_text("these is a basic menu, it does not use context managers from dearpygui.simple which are recomended.")
    add_menu_bar("MenuBar")

    add_menu("Themes")
    add_menu_item("Dark", callback=theme_callback)
    add_menu_item("Light", callback=theme_callback)
    add_menu_item("Classic", callback=theme_callback)
    add_menu_item("Dark 2", callback=theme_callback)
    add_menu_item("Grey", callback=theme_callback)
    add_menu_item("Dark Grey", callback=theme_callback)
    add_menu_item("Cherry", callback=theme_callback)
    add_menu_item("Purple", callback=theme_callback)
    add_menu_item("Gold", callback=theme_callback)
    add_menu_item("Red", callback=theme_callback)
    end()
    end()


start_dearpygui(primary_window="Main Window")
