import requests
from requests.auth import HTTPBasicAuth

def create_sub(url, subdo):
    username = url.split('.')[0]
    if len(username) > 16:
        username = username[:16]
    # Informasi otentikasi
    cpanel_user = username
    cpanel_password = "Winwinwin828!"
    cpanel_host = f"https://{url}:2083"

    # URL API untuk membuat subdomain
    uapi_url = f"{cpanel_host}/execute/SubDomain/addsubdomain"

    # Data yang dikirimkan
    data = {
        "domain": f"{subdo}.{url}",
        "rootdomain": f"{url}",
        "dir": f"/home/{cpanel_user}/public_html/{subdo}.{url}"
    }

    # Mengirim permintaan POST dengan otentikasi dasar
    response = requests.post(uapi_url, auth=HTTPBasicAuth(cpanel_user, cpanel_password), params=data)

    # Mengecek hasil
    if response.status_code == 200:
        result = response.json()
        if result.get("status") == 1:
            print(f"{username} => {subdo}")
        else:
            print(f"Gagal membuat subdomain: {result.get('errors')}")
    else:
        print(f"Error {response.status_code}: {response.text}")

with open('user.txt') as f:
    data = [line.strip() for line in f.readlines()]
f.close()

# create_sub('aptitudecreator.xyz', 'timnas')

for i in data:
    create_sub(i, 'basketball')
    create_sub(i, 'esports')
    create_sub(i, 'f1')
    create_sub(i, 'motogp')
    create_sub(i, 'timnas')
