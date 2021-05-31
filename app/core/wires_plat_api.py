import requests
from config.load_config import get_config_wires_plat_settings
import logging
logging.basicConfig(level=logging.INFO)
_get_config_wires_plat_settings = get_config_wires_plat_settings()


class WiresPlatApi:

    @staticmethod
    def get_token(host, **kwargs):
        port = kwargs.get('port') or 1414
        url = f"http://{host}:{port}/api/auth/login"
        name = kwargs.get('name')
        password = kwargs.get('password')
        payload = {"name": name, "password": password}
        try:
            result = requests.post(url, json=payload)
            print(result.status_code)
            if result.status_code == 201:
                return result.json().get("token")
        except:
            return False

    @staticmethod
    def put_settings(host, access_token, body, **kwargs):
        port = kwargs.get('port') or 1414
        url = f"http://{host}:{port}/api/setting"
        result = requests.put(url,
                              headers={'Content-Type': 'application/json',
                                       'Authorization': 'Bearer {}'.format(access_token)}, json=body)

        if result.status_code == 201:
            return True
        else:
            return False

    @staticmethod
    def put_bios_user(host, access_token, body, **kwargs):
        port = kwargs.get('port') or 1414
        service = kwargs.get('service') or 'rubixBios'
        url = f"http://{host}:{port}/api/system-service-auth/{service}"
        result = requests.post(url,
                               headers={'Content-Type': 'application/json',
                                        'Authorization': 'Bearer {}'.format(access_token)}, json=body)

        if result.status_code == 201:
            return True
        else:
            return False



