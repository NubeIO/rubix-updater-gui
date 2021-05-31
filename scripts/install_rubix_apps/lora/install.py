import logging
logging.basicConfig(level=logging.INFO)
import sys
import argparse
from app.core.rubix_service_api import RubixApi
from config.load_config import get_config_host, get_config_rubix_service

_host_settings = get_config_host()
_rubix_settings = get_config_rubix_service()

IP = None
RS_PORT = None


rubix_service_user = _rubix_settings.get('get_rubix_service_user')
rubix_service_password = _rubix_settings.get('get_rubix_service_password')

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



SERVICE = "LORA_RAW"
VERSION = "latest"

print(f"{IP}:{RS_PORT}")

CONFIG_FILE = {
    'service': SERVICE,
    "data": {
        "mqtt": {
            "enabled": True,
            "name": 'lora-raw-mqtt',
            "host": '0.0.0.0',
            "port": 1883,
            "authentication": True,
            "username": 'admin',
            "password": 'N00BMQTT',
            "keepalive": 60,
            "qos": 1,
            "attempt_reconnect_on_unavailable": True,
            "attempt_reconnect_secs": 5,
            "timeout": 10,
            "retain_clear_interval": 10,
            "publish_value": True,
            "topic": 'rubix/lora_raw/value',
            "publish_raw": True,
            "raw_topic": 'rubix/lora_raw/raw',
            "publish_debug": False,
            "debug_topic": 'rubix/lora_raw/debug'
        },
        "serial": {
            "enabled": True,
            "port": '/dev/ttyAMA0',
            "baud_rate": 38400,
            "stop_bits": 1,
            "parity": 'N',
            "byte_size": 8,
            "timeout": 5
        }
    }
}

if __name__ == "__main__":
    host = IP
    payload = {"username": rubix_service_user, "password": rubix_service_password}
    access_token = RubixApi.get_rubix_service_token(host)
    body = CONFIG_FILE
    app = SERVICE
    version = VERSION
    if access_token != False:
        add_config = RubixApi.rubix_add_config_file(host, access_token, body)
        if add_config:
            print(f"PASS: Add config file")
        else:
            print(f"FAIL: Add config file")
        if add_config != False:
            app = RubixApi.install_rubix_app(host, access_token, app, version)
            if app:
                print(f"PASS: install rubix app")
            else:
                print(f"FAIL: install rubix app")
        else:
            sys.exit("FAILED to get install_rubix_app")
    else:
        sys.exit("FAILED to get token")
