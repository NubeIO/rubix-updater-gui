import logging
import requests
from time import sleep

logging.basicConfig(level=logging.INFO)


class RubixApi:

    @staticmethod
    def ping_app(host, token, app, **kwargs):
        port = kwargs.get('port') or 1616
        url = f"http://{host}:{port}/{app}/api/system/ping"
        if app == "RUBIX_BIOS":
            url = f"http://{host}:1615/api/system/ping"
        elif app == "RUBIX_SERVICE":
            url = f"http://{host}:{port}/api/system/ping"
        req = requests.get(url,
                           headers={'Content-Type': 'application/json',
                                    'Authorization': 'Bearer {}'.format(token)})
        if req.json():
            logging.info(f"PING SERVICE PASS:  {req.status_code}")
            return True
        else:
            logging.info(f"PING SERVICE FAIL:', {req.status_code}")

    @staticmethod
    def bios_get_token(host, **kwargs):
        port = kwargs.get('port') or 1615
        url = f"http://{host}:{port}/api/users/login"
        payload = {"username": "admin", "password": "N00BWires"}
        try:
            result = requests.post(url, json=payload)
            logging.info(f"Add get bios status {result.status_code}")
            if result.status_code == 200:
                token = result.json().get('access_token')
                logging.info(f"PASS get bios token: {result.status_code}")
                return token
        except:
            logging.info(f"ERROR get bios token")
            return False

    @staticmethod
    def bios_add_git_token(host, access_token, github_token, **kwargs):
        port = kwargs.get('port') or 1615
        url = f"http://{host}:{port}/api/service/token"
        github_token = {"token": github_token}
        result = requests.put(url,
                              headers={'Content-Type': 'application/json',
                                       'Authorization': 'Bearer {}'.format(access_token)}, json=github_token)
        logging.info(f"bios_add_git_token status code {result.status_code}")
        if result.status_code == 200:
            return True
        else:
            return False

    @staticmethod
    def install_rubix_service(host, access_token, **kwargs):
        port = kwargs.get('port') or 1615

        url = f"http://{host}:{port}/api/service/upgrade"
        body = {"version": "latest"}
        result = requests.put(url,
                              headers={'Content-Type': 'application/json',
                                       'Authorization': 'Bearer {}'.format(access_token)}, json=body)
        logging.info(f"install_rubix_service status code {result.status_code}")
        if result.status_code == 200:
            return True
        else:
            return False

    @staticmethod
    def get_rubix_service_token(host, **kwargs):
        port = kwargs.get('port') or 1616
        username = kwargs.get('username') or 'admin'
        password = kwargs.get('password') or 'N00BWires'
        url = f"http://{host}:{port}/api/users/login"
        payload = {"username": username, "password": password}
        logging.info(f"get_rubix_service_token status code {url}")
        sleep(5)
        try:
            result = requests.post(url, json=payload)
            logging.info(f"get_rubix_service_token status code {result.status_code}")
            if result.status_code == 200:
                return result.json().get('access_token')
        except:
            logging.info(f"FAILED get_rubix_service_token")
            return False

    @staticmethod
    def rubix_add_git_token(host, access_token, github_token, **kwargs):
        port = kwargs.get('port') or 1616
        url = f"http://{host}:{port}/api/app/token"
        github_token = {"token": github_token}
        result = requests.put(url,
                              headers={'Content-Type': 'application/json',
                                       'Authorization': 'Bearer {}'.format(access_token)}, json=github_token)
        logging.info(f"rubix_add_git_token status code {result.status_code} github_token:{github_token}")
        if result.status_code == 200:
            return True
        else:
            return False

    @staticmethod
    def rubix_add_config_file(host, access_token, body, **kwargs):
        port = kwargs.get('port') or 1616
        url = f"http://{host}:{port}/api/app/config/config"
        result = requests.put(url,
                              headers={'Content-Type': 'application/json',
                                       'Authorization': 'Bearer {}'.format(access_token)}, json=body)

        if result.status_code == 200:
            logging.info(f"ADD CONFIG PASS: status code {result.status_code}")
            return True
        else:
            logging.info(f"ADD CONFIG FAIL: status code {result.status_code}")
            return False

    @staticmethod
    def rubix_update_plat(host, access_token, body, **kwargs):
        port = kwargs.get('port') or 1616
        url = f"http://{host}:{port}/api/wires/plat"
        result = requests.put(url,
                              headers={'Content-Type': 'application/json',
                                       'Authorization': 'Bearer {}'.format(access_token)}, json=body)
        logging.info(f"rubix_update_plat status code {result.status_code}")
        if result.status_code == 200:
            return result.json()
        else:
            return False

    @staticmethod
    def rubix_add_droplets(host, access_token, body, **kwargs):
        port = kwargs.get('port') or 1616
        url = f"http://{host}:{port}/lora/api/lora/devices"
        result = requests.post(url,
                               headers={'Content-Type': 'application/json',
                                        'Authorization': 'Bearer {}'.format(access_token)}, json=body)
        logging.info(f"rubix_add_droplets status code {result.status_code}")
        if result.status_code == 200:
            return result.json()
        else:
            return False

    @staticmethod
    def start_stop_app(host, access_token, action, service, **kwargs):
        port = kwargs.get('port') or 1616
        url = f"http://{host}:{port}/api/app/control"
        action = action.upper()
        service = service.upper()
        payload = [{"action": action, "service": service}]
        result = requests.post(url,
                               headers={'Content-Type': 'application/json',
                                        'Authorization': 'Bearer {}'.format(access_token)}, json=payload)
        logging.info(
            f"start_stop_app: {url} service: {service} action {action}  body: {payload} status code: {result.status_code} status_code:{result.status_code} res:{result.text}")
        if result.status_code == 200:
            return True
        else:
            return False

    @staticmethod
    def download_rubix_app(host, token, app, version, **kwargs):
        port = kwargs.get('port') or 1616
        payload = [{"service": app, "version": version}]
        access_token = token
        download_url = f"http://{host}:{port}/api/app/download"
        result = requests.post(download_url,
                               headers={'Content-Type': 'application/json',
                                        'Authorization': 'Bearer {}'.format(access_token)},
                               json=payload)
        logging.info(f"DOWNLOAD APP: status code {result.status_code}")
        if result.status_code != 200:
            logging.info(f"DOWNLOAD APP: FAILED to download", result.json())
            return False
        else:
            logging.info(f"DOWNLOAD APP: Download process has been started, and waiting for it's completion...")
            return True

    @staticmethod
    def check_state_download_rubix_app(host, token, app, version, **kwargs):
        port = kwargs.get('port') or 1616
        payload = [{"service": app, "version": version}]
        access_token = token
        download_state_url = f"http://{host}:{port}/api/app/download_state"
        download_state = requests.get(download_state_url,
                                      headers={'Content-Type': 'application/json',
                                               'Authorization': 'Bearer {}'.format(access_token)},
                                      json=payload)
        logging.info(f"CHECK DOWNLOAD STATE:', {download_state.json()}")
        if download_state.json().get('state') == 'DOWNLOADED':
            logging.info(f"CHECK DOWNLOAD STATE: Download completed...")
            return True
        else:
            logging.info(f"CHECK DOWNLOAD STATE:', {download_state.json()}")

    @staticmethod
    def manual_install_rubix_app(host, token, app, version, **kwargs):
        port = kwargs.get('port') or 1616
        payload = [{"service": app, "version": version}]
        access_token = token
        install_url = f"http://{host}:{port}/api/app/install"
        result = requests.post(install_url,
                               headers={'Content-Type': 'application/json',
                                        'Authorization': 'Bearer {}'.format(access_token)},
                               json=payload)
        if result.status_code != 200:
            logging.debug(f"INSTALL APP FAIL:Failed to install', {result.json()}")
        else:
            logging.info(f"INSTALL APP PASS: Install completed...service {app}")
            return True

    @staticmethod
    def delete_state_download_rubix_app(host, token, app, version, **kwargs):
        port = kwargs.get('port') or 1616
        payload = [{"service": app, "version": version}]
        access_token = token
        download_state_url = f"http://{host}:{port}/api/app/download_state"
        logging.info(f"DOWNLOAD STATE: Clearing download state...")
        result = requests.delete(download_state_url,
                                 headers={'Content-Type': 'application/json',
                                          'Authorization': 'Bearer {}'.format(access_token)},
                                 json=payload)
        logging.info(f"DOWNLOAD STATE: Download state is cleared.....{result.status_code}")

    @staticmethod
    def install_rubix_app(host, token, app, version, **kwargs):
        port = kwargs.get('port') or 1616
        payload = [{"service": app, "version": version}]
        access_token = token
        download_url = f"http://{host}:{port}/api/app/download"
        download_state_url = f"http://{host}:{port}/api/app/download_state"
        install_url = f"http://{host}:{port}/api/app/install"
        result = requests.post(download_url,
                               headers={'Content-Type': 'application/json',
                                        'Authorization': 'Bearer {}'.format(access_token)},
                               json=payload)
        logging.info(f"DOWNLOAD APP: status code {result.status_code}")
        if result.status_code != 200:
            logging.info(f"DOWNLOAD APP: FAILED to download", result.json())
            logging.info(f"DOWNLOAD APP: Clearing download state...")

            requests.delete(download_state_url,
                            headers={'Content-Type': 'application/json',
                                     'Authorization': '{}'.format(access_token)},
                            json=payload)
            logging.info(f"DOWNLOAD APP: state is cleared....")
        else:
            logging.info(f"DOWNLOAD APP: Download process has been started, and waiting for it's completion...")
            while True:
                sleep(1.5)
                download_state = requests.get(download_state_url,
                                              headers={'Content-Type': 'application/json',
                                                       'Authorization': 'Bearer {}'.format(access_token)},
                                              json=payload)

                logging.info(f"DOWNLOAD STATE:', {download_state.json()}")
                if download_state.json().get('state') == 'DOWNLOADED':
                    break
            logging.info(f"DOWNLOAD STATE: Download completed...")
            logging.info(f"DOWNLOAD STATE: Clearing download state...")
            requests.delete(download_state_url,
                            headers={'Content-Type': 'application/json',
                                     'Authorization': 'Bearer {}'.format(access_token)},
                            json=payload)
            logging.info(f"DOWNLOAD STATE: Download state is cleared.....")
            result = requests.post(install_url,
                                   headers={'Content-Type': 'application/json',
                                            'Authorization': 'Bearer {}'.format(access_token)},
                                   json=payload)
            if result.status_code != 200:
                logging.debug(f"DOWNLOAD APP FAIL:Failed to install', {result.json()}")
            else:
                logging.info(f"DOWNLOAD APP PASS: Install completed...service {app}")
                return True

    @staticmethod
    def add_point_server_network(host, access_token, **kwargs):
        port = kwargs.get('port') or 1616
        name = kwargs.get('name') or "net-1"
        enable = kwargs.get('enable') or True
        history_enable = kwargs.get('history_enable') or True
        url = f"http://{host}:{port}/api/generic/network"
        net = {
            "name": name,
            "enable": enable,
            "history_enable": history_enable
        }
        result = requests.post(url,
                               headers={'Content-Type': 'application/json',
                                        'Authorization': 'Bearer {}'.format(access_token)}, json=net)
        logging.info(f"add_point_server_network status code {result.status_code}")
        if result.status_code == 200:
            return result.json()
        else:
            return False

    @staticmethod
    def add_point_server_device(host, access_token, **kwargs):
        port = kwargs.get('port') or 1616
        name = kwargs.get('name') or "dev-1"
        network_uuid = kwargs.get('network_uuid') or "dev-1"
        enable = kwargs.get('enable') or True
        history_enable = kwargs.get('history_enable') or True
        url = f"http://{host}:{port}/api/generic/devices"
        dev = {
            "name": name,
            "enable": enable,
            "network_uuid": network_uuid,
            "history_enable": history_enable
        }
        result = requests.post(url,
                               headers={'Content-Type': 'application/json',
                                        'Authorization': 'Bearer {}'.format(access_token)}, json=dev)
        logging.info(f"add_point_server_device status code {result.status_code}")
        if result.status_code == 200:
            return result.json()
        else:
            return False
