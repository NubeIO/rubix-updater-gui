import argparse
import logging
logging.basicConfig(level=logging.INFO)
from app.core.wires_plat_api import WiresPlatApi
from config.load_config import get_config_host, get_config_rubix_service, get_config_wires_plat_settings, \
    get_config_bios, get_config_wires_plat_user

_get_config_wires_plat_settings = get_config_wires_plat_settings()
_host_settings = get_config_host()
_rubix_settings = get_config_rubix_service()
_bios_settings = get_config_bios()
_config_wires_plat_user = get_config_wires_plat_user()

IP = None
RS_PORT = None
wires_plat_user = _config_wires_plat_user.get('get_wires_plat_user')
wires_plat_password = _config_wires_plat_user.get('get_wires_plat_password')

rubix_bios_user = _bios_settings.get('get_rubix_bios_user')
rubix_bios_password = _bios_settings.get('get_rubix_bios_password')

parser = argparse.ArgumentParser()
parser.add_argument('-ip', '--ip', type=str, help="override config ip address")
parser.add_argument('-port', '--port', type=str, help="override config port number")
args = parser.parse_args()

if args.ip is None:
    IP = _host_settings.get('get_host')
else:
    IP = args.ip

if args.port is None:
    RS_PORT = _rubix_settings.get('get_rubix_service_port')
else:
    RS_PORT = args.port

url = IP
print(f"url {url}")
token = WiresPlatApi.get_token(url, name=wires_plat_user, password=wires_plat_password)

_body = _get_config_wires_plat_settings.get('get_wires_plat_settings')
put_settings = WiresPlatApi.put_settings(url, token, _body)
if put_settings:
    print(f"PASS: Add settings")
else:
    print(f"FAIL: Add settings")

service = "rubixBios"  # rubixBios rubixService
_body = {"username": rubix_bios_user, "password": rubix_bios_password}
put_user_bios = WiresPlatApi.put_bios_user(url, token, _body, service=service)
if put_user_bios:
    print(f"PASS: Add bios user Ok")
else:
    print(f"FAIL: Add bios user Fail")

_body = {"username": rubix_bios_user, "password": rubix_bios_password}
service = "rubixService"  # rubixBios rubixService
put_user_rubix = WiresPlatApi.put_bios_user(url, token, _body, service=service)
if put_user_rubix:
    print(f"PASS: Add rubix service user Ok")
else:
    print(f"FAIL: Add rubix service user Fail")
