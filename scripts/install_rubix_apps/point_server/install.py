import argparse
import logging
import sys

logging.basicConfig(level=logging.INFO)
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
SERVICE = "POINT_SERVER"
VERSION = "latest"

CONFIG_FILE = {
    'service': SERVICE,
    "data": {
        "drivers": {
            "generic": True,
            "modbus_rtu": False,
            "modbus_tcp": False
        },
        "services": {
            "mqtt": True,
            "histories": True,
            "cleaner": False,
            "history_sync_influxdb": False,
            "history_sync_postgres": True
        },
        "influx": {
            "host": "0.0.0.0",
            "port": 8086,
            "database": "db",
            "username": "username",
            "password": "password",
            "ssl": False,
            "verify_ssl": False,
            "timeout": 5,
            "retries": 3,
            "timer": 5,
            "path": "",
            "measurement": "points",
            "attempt_reconnect_secs": 5
        },
        "postgres": {
            "host": "0.0.0.0",
            "port": 5432,
            "dbname": "db",
            "user": "user",
            "password": "password",
            "ssl_mode": "allow",
            "connect_timeout": 5,
            "timer": 5,
            "table_prefix": "tbl",
            "attempt_reconnect_secs": 5
        },
        "mqtt": [
            {
                "enabled": True,
                "name": "rubix-points",
                "host": "0.0.0.0",
                "port": 1883,
                "authentication": True,
                "username": "admin",
                "password": "N00BMQTT",
                "keepalive": 60,
                "qos": 1,
                "attempt_reconnect_on_unavailable": True,
                "attempt_reconnect_secs": 5,
                "timeout": 10,
                "retain_clear_interval": 10,
                "publish_value": True,
                "topic": "rubix/points/value",
                "listen": True,
                "listen_topic": "rubix/points/listen",
                "publish_debug": True,
                "debug_topic": "rubix/points/debug"
            }
        ]
    }
}

if __name__ == "__main__":
    host = IP
    payload = {"username": "admin", "password": "N00BWires"}
    access_token = RubixApi.get_rubix_service_token(host)
    body = CONFIG_FILE
    app = SERVICE
    version = VERSION
    print(access_token)
    if access_token != False:
        add_config = RubixApi.rubix_add_config_file(host, access_token, body)
        print(" add_config file", add_config)
        if add_config != False:
            app = RubixApi.install_rubix_app(host, access_token, app, version)
            print(" install_rubix_app", app)
        else:
            sys.exit("FAILED to get install_rubix_app")
    else:
        sys.exit("FAILED to get token")
