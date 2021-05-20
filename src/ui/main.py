import dearpygui.core as dpg
import dearpygui.simple as sdpg
from src.common_ssh.tasks_rubix import deploy_rubix_update

from src.common_ui.make_connection import MakeConnection
from src.common_ui.ssh import CommonHost, CommonTheme


class FileZipApp:
    def __init__(self):
        self.files_list = None

    def run_setup(self, sender, data):
        enable = dpg.get_value("enable")
        delete_all_dirs = dpg.get_value("delete_all_dirs")
        install_rubix_plat = dpg.get_value("install_rubix_plat")
        if enable:
            cx = MakeConnection().get_connection().connect()
            deploy_rubix_update(cx,
                                delete_all_dirs=delete_all_dirs,
                                install_rubix_plat=install_rubix_plat
                                )

    def show(self):
        """Start the gui."""
        with sdpg.window("Main Window"):
            CommonTheme()
            CommonHost()

            dpg.add_checkbox("enable", label="Enable")
            # dpg.add_checkbox("delete_all_dirs", label="Wipe All Data")

            dpg.add_text("File Zip App")
            dpg.add_radio_button("delete_all_dirs", items=["Wipe All Data", "Wipe All Data & Reinstall Rubix "
                                                                            "Bios/Service"])
            dpg.add_checkbox("install_rubix_plat", label="install rubix service")


            dpg.add_button("Run", callback=self.run_setup)
            dpg.start_dearpygui(primary_window="Main Window")


if __name__ == '__main__':
    file_zip_app = FileZipApp()
    file_zip_app.show()
