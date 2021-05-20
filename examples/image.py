from dearpygui.core import *
from dearpygui.simple import *

# please update the image directory argument with a path to an image on your computer for this example
with window("Tutorial"):
    add_drawing("Drawing_1", width=700, height=700)

# draw_image("Drawing_1", 'SpriteMapExample.png', [0, 400], pmax=[200, 600], uv_min=[0, 0], uv_max=[1, 1], tag="image")
# draw_image("Drawing_1", 'SpriteMapExample.png', [400, 300], pmax=[600, 500], uv_min=[0, 0], uv_max=[0.5, 0.5])
draw_image("Drawing_1", '/home/aidan/code/python/nube/rubix-updater-gui/nube_logo.png', [0, 0], pmax=[700, 700])

start_dearpygui()