import requests
from time import sleep


class RubixApi:

    @staticmethod
    def bios_get_token(host):
        url = f"http://{host}:1615/api/users/login"
        payload = {"username": "admin", "password": "N00BWires"}
        sleep(1)
        while True:
            sleep(1)
            try:
                result = requests.post(url, json=payload)
                print(result.status_code)
                if result.status_code == 200:
                    return result.json().get('access_token')
            except:
                print(f"ERROR: get bios token")

    @staticmethod
    def bios_add_git_token(host, access_token, github_token):
        url = f"http://{host}:1615/api/service/token"
        github_token = {"token": github_token}
        result = requests.put(url,
                              headers={'Content-Type': 'application/json',
                                       'Authorization': '{}'.format(access_token)}, json=github_token)
        if result.status_code == 200:
            return True
        else:
            return False

    @staticmethod
    def install_rubix_service(host, access_token):
        url = f"http://{host}:1615/api/service/upgrade"
        body = {"version": "latest"}
        result = requests.put(url,
                              headers={'Content-Type': 'application/json',
                                       'Authorization': '{}'.format(access_token)}, json=body)
        if result.status_code == 200:
            return True
        else:
            return False

    @staticmethod
    def get_rubix_service_token(host):
        url = f"http://{host}:1616/api/users/login"
        payload = {"username": "admin", "password": "N00BWires"}
        sleep(2)
        while True:
            sleep(1)
            try:
                result = requests.post(url, json=payload)
                print(result.status_code)
                if result.status_code == 200:
                    return result.json().get('access_token')
                #
            except:
                print(f"ERROR: 1616/api/system/ping")

    @staticmethod
    def rubix_add_git_token(host, access_token, github_token):
        url = f"http://{host}:1616/api/service/token"
        github_token = {"token": github_token}
        result = requests.put(url,
                              headers={'Content-Type': 'application/json',
                                       'Authorization': '{}'.format(access_token)}, json=github_token)
        if result.status_code == 200:
            return True
        else:
            return False

    @staticmethod
    def install_wires_plat(host, token):
        payload = [{"service": "RUBIX_PLAT", "version": "v1.7.0"}]
        access_token = token
        url = f"http://{host}:1616/api/app/download"
        download_state_url = f"http://{host}:1616/api/app/download_state"
        result = requests.post(url,
                               headers={'Content-Type': 'application/json', 'Authorization': '{}'.format(access_token)},
                               json=payload)
        if result.status_code != 200:
            print("Failed to download", result.json())
            print("Clearing download state...")
            requests.delete(download_state_url,
                            headers={'Content-Type': 'application/json',
                                     'Authorization': '{}'.format(access_token)},
                            json=payload)
            print("Download state is cleared...")
        else:
            print("Download process has been started, and waiting for it's completion...")
            while True:
                sleep(1)
                download_state = requests.get(download_state_url,
                                              headers={'Content-Type': 'application/json',
                                                       'Authorization': '{}'.format(access_token)},
                                              json=payload)
                print('download_state', download_state.json())
                if download_state.json().get('state') == 'DOWNLOADED':
                    break
            print("Download completed...")
            print("Please insert your installation code here...")
            # Without clearing this state it won't able to start next download
            # Currently rubix-service has an issue so it works without clearing but later it won't work
            print("Clearing download state...")
            requests.delete(download_state_url,
                            headers={'Content-Type': 'application/json',
                                     'Authorization': '{}'.format(access_token)},
                            json=payload)
            print("Download state is cleared...")
