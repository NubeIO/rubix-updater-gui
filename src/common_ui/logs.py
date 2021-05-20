from dearpygui.core import log_debug
from src.common_ui.ssh import CommonHost
from src.utils.functions import Utils


class Common:

    @staticmethod
    def log(data):
        log_debug(data)

    @staticmethod
    def ping():
        ping = Utils.ping(CommonHost.get_host())
        Common.log(f"ERROR: failed to @func _ping {CommonHost.get_host()}")
        if ping:
            Common.log(f"LOG: @func _ping {CommonHost.get_host()}")
            return True
        else:
            Common.log(f"ERROR: failed to @func _ping {CommonHost.get_host()}")
            return False

