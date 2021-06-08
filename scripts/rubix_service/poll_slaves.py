import requests

host = '178.128.119.166'
port = '1616'
payload = {"username": "admin", "password": "N00BWires"}
get_token = requests.post(f"http://{host}:{port}/api/users/login", json=payload)
res = get_token.json()
access_token = res.get('access_token')
print(access_token)
payload = {"version": "latest"}

url = f"http://{host}:{port}/api/discover/remote_devices"
result = requests.get(url,
                      headers={'Content-Type': 'application/json', 'Authorization': '{}'.format(access_token)},
                      json=payload)

json_result = result.json()
# print(json_result)
for global_uuid in json_result:
    url = f"http://{host}:{port}/slave/{global_uuid}/api/system/ping"
    result = requests.get(url,
                          headers={'Content-Type': 'application/json', 'Authorization': '{}'.format(access_token)},
                          json=payload)
    device_name = json_result[global_uuid].get('device_name')
    site_name = json_result[global_uuid].get('site_name')
    public_ip = result.json().get('public_ip')
    print("---------------------------------------------------------------------------")
    print(f"public_ip: {public_ip}, device_name: {device_name}, site_name: {site_name}")
