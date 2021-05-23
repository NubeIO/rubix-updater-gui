import re


class Utils:

    @staticmethod
    def is_ip(ip):
        return re.match(r'^\d{1,255}[.]\d{1,255}[.]\d{1,255}[.]\d{1,255}$', ip)
