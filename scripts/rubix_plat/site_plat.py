import argparse
import csv
import os

import sys

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

CWD = os.getcwd()
FILE_NAME = "site.csv"
file = f"{CWD}/{FILE_NAME}"
print(file)

build_id = 0
sim_number = 1
vpn = 3

device_id = 8
device_name = 9
client_id = 10
client_name = 11
site_id = 12
site_name = 13
site_address = 14
site_city = 15
site_zip = 16
site_state = 17
site_country = 18
# site_lat = 0
# site_lon = 0
time_zone = 19

droplet_1 = 20
droplet_2 = 21
droplet_3 = 22
droplet_4 = 23
zone_1 = 24
zone_2 = 25
zone_3 = 26
zone_4 = 27

with open(file, 'r') as file:
    my_reader = csv.reader(file, delimiter=',')
    for row in my_reader:
        # site details
        build_id = row[build_id]
        sim_number = row[sim_number]
        vpn = row[vpn]
        # plat
        device_id = row[device_id]
        device_name = row[device_name]
        client_id = row[client_id]
        client_name = row[client_name]
        site_id = row[site_id]
        site_name = row[site_name]
        site_address = row[site_address]
        site_city = row[site_city]
        site_zip = row[site_zip]
        site_state = row[site_state]
        site_country = row[site_country]
        time_zone = row[time_zone]
        # droplets
        droplet_1 = row[droplet_1]
        droplet_2 = row[droplet_2]
        droplet_3 = row[droplet_3]
        droplet_4 = row[droplet_4]
        zone_1 = row[zone_1]
        zone_2 = row[zone_2]
        zone_3 = row[zone_3]
        zone_4 = row[zone_4]

body = {
    "device_id": device_id,
    "device_name": device_name,
    "client_id": client_id,
    "client_name": client_name,
    "site_id": site_id,
    "site_name": site_name,
    "site_address": site_address,
    "site_city": site_city,
    "site_state": site_state,
    "site_zip": site_zip,
    "site_country": site_country,
    "site_lat": "-",
    "site_lon": "-",
    "time_zone": time_zone
}

print("SITE:", " ", build_id)
update = True
if update:
    host = IP
    payload = {"username": "admin", "password": "N00BWires"}
    access_token = RubixApi.get_rubix_service_token(host)
    print(access_token)
    if access_token != False:
        app = RubixApi.rubix_update_plat(host, access_token, body)
        print(" rubix_update_plat", app)
    else:
        sys.exit("FAILED to get token")

droplets_ids = (droplet_1, droplet_2, droplet_3, droplet_4)
droplets_zones = (zone_1, zone_2, zone_3, zone_4)

count = 0

host = IP
payload = {"username": "admin", "password": "N00BWires"}
access_token = RubixApi.get_rubix_service_token(host)
print(access_token)
add_droplets = True
if add_droplets:
    for d in droplets_ids:
        print(droplets_zones[count])
        count += 1
        devices_obj = {
            "name": f'dr{count}',
            "id": f'{d}',
            "device_type": "DROPLET",
            "device_model": "DROPLET_THL"
        }
        droplets = True
        if droplets:
            if access_token != False:
                app = RubixApi.rubix_add_droplets(host, access_token, devices_obj)
                # print(" rubix_add_droplets", app)
            else:
                sys.exit("FAILED to get token")
