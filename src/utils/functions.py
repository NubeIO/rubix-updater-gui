import platform
import subprocess


#
#
class Utils:

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


# import subprocess
# import platform


print(Utils.ping("192.168.15.100"))
