import sys

from app.core.rubix_service_api import RubixApi

IP = "120.157.111.164"
RS_PORT = 1616
SERVICE = "LORA_RAW"
VERSION = "latest"

host = IP
payload = {"username": "admin", "password": "N00BWires"}
access_token = RubixApi.get_rubix_service_token(host, port=1616)
print(access_token)


