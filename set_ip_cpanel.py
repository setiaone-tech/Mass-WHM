import requests

WHM_TOKEN = ''
WHM_HOST = ''
WHM_USERNAME = ''
headers = {
    "Authorization": f"whm {WHM_USERNAME}:{WHM_TOKEN}"
}

with open('list_domain.txt') as f:
    data = f.readlines()
f.close()

with open('list_ip.txt') as f:
    data_ip = f.readlines()
f.close()
 
for i in range(len(data)-1):
    domain = data[i]
    user = data[i].split('.')[0]
    user = user[:16]
    url = f"https://{WHM_HOST}:2087/json-api/setsiteip?ip={data_ip[i]}&{domain}&user={user}"
    response = requests.get(url, headers=headers, verify=False)
    print(response.status_code)
