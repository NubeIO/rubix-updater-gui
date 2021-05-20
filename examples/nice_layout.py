import dearpygui.core as dpg
import dearpygui.simple as sdpg
from dearpygui.core import show_logger, log, clear_log, set_log_level, get_value, mvTRACE, log_debug


class FileZipApp:
    def __init__(self):
        self.files_list = None

    def store_data(self, sender, data):
        custom_data = {
            "Radio Button": dpg.get_value("Radio Button"),
            "Checkbox": dpg.get_value("Checkbox"),
            "Text Input": dpg.get_value("Text Input"),
        }
        dpg.add_data("stored_data", custom_data)

    def print_data(self, sender, data):
        show_logger()

        log("trace message")
        log_debug("debug message")
        log(dpg.get_value("Checkbox"))

    def show(self):
        """Start the gui."""
        with sdpg.window("Main Window"):
            show_logger()
            dpg.set_theme("Light")
            dpg.set_main_window_size(550, 500)
            dpg.set_main_window_resizable(False)
            dpg.add_spacing()
            dpg.set_main_window_title("Rubix Service Factory Reset")

            dpg.add_spacing()
            dpg.add_text("File Zip App")
            dpg.add_spacing()
            dpg.add_text("Select files to zip by adding them to the table", bullet=True, tip="MY TIP")
            dpg.add_text("Set the output directory", bullet=True)
            dpg.add_text("Click on the table to remove a file", bullet=True)
            dpg.add_text("Click on the zip files button to zip all the files", bullet=True)
            dpg.add_text("If you do not choose a directory, it will by default be"
                         "the same directory from where you've run this script.", bullet=True)
            dpg.add_spacing()
            dpg.add_separator()
            dpg.add_checkbox("Checkbox")
            dpg.add_spacing(count=5)
            # dpg.add_button("Store Data", callback=self.store_data)
            dpg.add_button("Run", callback=self.print_data)

            dpg.start_dearpygui(primary_window="Main Window")


if __name__ == '__main__':
    file_zip_app = FileZipApp()
    file_zip_app.show()
