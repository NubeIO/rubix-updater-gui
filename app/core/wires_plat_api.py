import requests
from config.load_config import get_config_wires_plat_settings

_get_config_wires_plat_settings = get_config_wires_plat_settings()


class WiresPlatApi:

    @staticmethod
    def get_token(host, **kwargs):
        port = kwargs.get('port') or 1414
        url = f"http://{host}:{port}/api/auth/login"
        print()
        payload = {"name": "admin", "password": "N00BWires"}
        try:
            result = requests.post(url, json=payload)
            print(result.status_code)
            if result.status_code == 201:
                return result.json().get("token")
        except:
            print(f"ERROR: get bios token")
            return False

    @staticmethod
    def put_settings(host, access_token, body, **kwargs):
        port = kwargs.get('port') or 1414
        url = f"http://{host}:{port}/api/setting"
        print("add config file", body)
        print("url", url)
        result = requests.put(url,
                              headers={'Content-Type': 'application/json',
                                       'Authorization': 'Bearer {}'.format(access_token)}, json=body)
        print(result.status_code)
        print(result.text)
        if result.status_code == 200:
            return True
        else:
            return False

    @staticmethod
    def put_bios_user(host, access_token, body, **kwargs):
        port = kwargs.get('port') or 1414
        service = kwargs.get('service') or 'rubixBios'
        url = f"http://{host}:{port}/api/system-service-auth/{service}"
        print("body", body)
        print("url", url)
        print("access_token", access_token)
        result = requests.post(url,
                               headers={'Content-Type': 'application/json',
                                        'Authorization': 'Bearer {}'.format(access_token)}, json=body)
        print(result.status_code)
        print(result.text)
        if result.status_code == 200:
            return True
        else:
            return False


url = "120.157.111.164"  # 165.227.72.56
token = WiresPlatApi.get_token(url)

# _body = _get_config_wires_plat_settings.get('get_wires_plat_settings')

# WiresPlatApi.put_settings(url, token, _body)

service = "rubixService"  # rubixBios rubixService
_body = {"username": "admin", "password": "N00BWires"}
# token = WiresPlatApi.get_token("165.227.72.56")
WiresPlatApi.put_bios_user(url, token, _body, service=service)

# wires-plat auth for rubix-service
# {"username":"admin","password":"admin"}
## POST
## http://165.227.72.56:1414/api/system-service-auth/rubixService
## bios
## POST
## Request URL: http://165.227.72.56:1414/api/system-service-auth/rubixBios
