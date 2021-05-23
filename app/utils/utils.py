import re
import platform
import subprocess


class Utils:

    @staticmethod
    def is_ip(ip):
        return re.match(r'^\d{1,255}[.]\d{1,255}[.]\d{1,255}[.]\d{1,255}$', ip)

    @classmethod
    def ping(cls, host) -> bool:
        try:
            output = subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower(
            ) == "windows" else 'c', host), shell=True, universal_newlines=True)
            if 'unreachable' in output:
                return False
            else:
                return True
        except Exception:
            return False
