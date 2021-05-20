import dearpygui.core as dpg
import dearpygui.simple as sdpg
from dearpygui.core import add_drawing, draw_image

from src.common_ssh.tasks_rubix import deploy_rubix_update

from src.common_ui.make_connection import MakeConnection
from src.common_ui.ssh import CommonHost, CommonTheme


class FileZipApp:
    def __init__(self):
        self.files_list = None

    def run_setup(self, sender, data):
        enable = dpg.get_value("enable")
        delete_all_dirs = dpg.get_value("delete_all_dirs")

        if enable:
            cx = MakeConnection().get_connection().connect()
            deploy_rubix_update(cx,
                                delete_all_dirs=delete_all_dirs
                                )

    def show(self):
        """Start the gui."""
        with sdpg.window("Main Window"):
            add_drawing("logo", width=520, height=290)  # create some space for the image
            # draw_image("logo", "/home/aidan/code/python/nube/rubix-updater-gui/nube_logo.png", [0, 240])


            CommonTheme()
            CommonHost()

            dpg.add_checkbox("enable", label="Enable")
            # dpg.add_checkbox("delete_all_dirs", label="Wipe All Data")

            dpg.add_text("File Zip App")
            dpg.add_radio_button("delete_all_dirs", items=["Wipe All Data", "Wipe All Data & Reinstall Rubix "
                                                                            "Bios/Service"])

            dpg.add_text("Please enter an SMS message of your choice to check if it's spam or not",
                         color=[232, 163, 33])
            dpg.add_button("Run", callback=self.run_setup)

            dpg.start_dearpygui(primary_window="Main Window")






if __name__ == '__main__':
    file_zip_app = FileZipApp()
    file_zip_app.show()
