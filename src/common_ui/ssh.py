from dearpygui.core import add_input_text, add_text, add_spacing, add_separator, set_main_window_title, \
    set_main_window_resizable, set_main_window_size, set_theme, get_value, set_global_font_scale, \
    set_style_window_padding


class CommonTheme:
    def __init__(self):
        set_theme("Dark")
        set_global_font_scale(1.25)
        set_style_window_padding(30, 30)
        set_main_window_size(540, 720)
        set_main_window_resizable(False)
        add_spacing()
        set_main_window_title("Rubix Service Factory Reset")


class CommonHost:
    def __init__(self):
        add_text("IP ADDRESS")
        add_spacing(count=2)
        add_input_text("host##inputtext", default_value="192.168.15.189")
        add_input_text("port##inputtext", default_value="22")
        add_input_text("user##inputtext", default_value="pi")
        add_input_text("password##inputtext", default_value="N00BRCRC", password=True)
        add_separator()
        add_spacing(count=2)

    @staticmethod
    def get_host():
        return get_value("host##inputtext")

    @staticmethod
    def get_port():
        return get_value("port##inputtext")

    @staticmethod
    def get_user():
        return get_value("user##inputtext")

    @staticmethod
    def get_password():
        return get_value("password##inputtext")

