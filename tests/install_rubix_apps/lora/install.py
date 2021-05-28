import sys

from app.core.rubix_service_api import RubixApi

IP = '123.210.200.78'
RS_PORT = 1616
SERVICE = "LORA_RAW"
VERSION = "latest"

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

