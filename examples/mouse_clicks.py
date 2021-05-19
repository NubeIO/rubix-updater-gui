from dearpygui.core import *
from dearpygui.simple import *


def main_callback(sender, data):
    set_value("Mouse Position", str(get_mouse_pos()))
    set_value("A key Down", is_key_down(mvKey_A))
    set_value("A key Pressed", is_key_pressed(mvKey_A))
    set_value("A key Released", is_key_released(mvKey_A))
    set_value("Left Mouse Dragging", is_mouse_button_dragging(mvMouseButton_Left, 10))
    set_value("Left Mouse Clicked", is_mouse_button_clicked(mvMouseButton_Left))
    set_value("Left Mouse Double Clicked", is_mouse_button_double_clicked(mvMouseButton_Left))
    set_value("Shift + Left Mouse Clicked", is_key_down(mvKey_Shift) and is_mouse_button_clicked(mvMouseButton_Left))


with window("Tutorial"):
    add_label_text("A key Down", color=[0, 200, 255])
    add_label_text("A key Pressed", color=[0, 200, 255])
    add_label_text("A key Released", color=[0, 200, 255])
    add_spacing()
    add_label_text("Mouse Position", color=[0, 200, 255])
    add_label_text("Left Mouse Clicked", color=[0, 200, 255])
    add_label_text("Left Mouse Dragging", color=[0, 200, 255])
    add_label_text("Left Mouse Double Clicked", color=[0, 200, 255])
    add_label_text("Shift + Left Mouse Clicked", color=[0, 200, 255])

set_render_callback(main_callback)

start_dearpygui()
