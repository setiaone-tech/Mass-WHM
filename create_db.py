import requests
import base64

print("Proses...")
with open('list_domain_n.txt') as f:
    data = f.readlines()
f.close()

with open('list_ip_n.txt') as f:
    data_ip = f.readlines()
f.close()

def create_db(user, ip):
    # Informasi API
    cpanel_url = f"https://{ip}:2083/execute/Mysql/create_database"
    cpanel_user = user
    cpanel_password = ""

    # Nama database yang ingin dibuat
    db_name = f"{cpanel_user}_DBNAME",

    # Parameter untuk request
    payload = {
        "name": db_name
    }

    # Encode username dan password ke Base64
    credentials = f"{cpanel_user}:{cpanel_password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

        # Header untuk otentikasi Basic
    headers = {
        "Authorization": f"Basic {encoded_credentials}"
    }

    # Mengirimkan request
    response = requests.get(cpanel_url, headers=headers, data=payload, verify=False)

    # Menampilkan hasil
    if response.status_code == 200:
        print("Database berhasil dibuat:", response.json())
    else:
        print("Gagal membuat database:", response.json())

def create_user (user, ip):
    # Informasi API
    cpanel_url = f"https://{ip}:2083/execute/Mysql/create_user"
    cpanel_user = user
    cpanel_password = ""

    # Nama database yang ingin dibuat
    db_name = f"{cpanel_user}_DBNAME",

    # Parameter untuk request
    payload = {
        "name": db_name,
        "password": ""
    }

    # Encode username dan password ke Base64
    credentials = f"{cpanel_user}:{cpanel_password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

        # Header untuk otentikasi Basic
    headers = {
        "Authorization": f"Basic {encoded_credentials}"
    }

    # Mengirimkan request
    response = requests.get(cpanel_url, headers=headers, data=payload, verify=False)

    # Menampilkan hasil
    if response.status_code == 200:
        print("User berhasil dibuat:", response.json())
    else:
        print("Gagal membuat User:", response.json())

def update_privileges(user, ip):
    # Informasi API
    cpanel_url = f"https://{ip}:2083/execute/Mysql/set_privileges_on_database"
    cpanel_user = user
    cpanel_password = ""

    # Nama database yang ingin dibuat
    db_name = f"{cpanel_user}_DBNAME",

    # Parameter untuk request
    payload = {
        "database": db_name,
        "user": "",
        "privileges": "ALL PRIVILEGES"
    }

    # Encode username dan password ke Base64
    credentials = f"{cpanel_user}:{cpanel_password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

        # Header untuk otentikasi Basic
    headers = {
        "Authorization": f"Basic {encoded_credentials}"
    }

    # Mengirimkan request
    response = requests.get(cpanel_url, headers=headers, data=payload, verify=False)

    # Menampilkan hasil
    if response.status_code == 200:
        print("Berhasil memperbarui user:", response.json())
    else:
        print("Gagal memperbarui User:", response.json())

print(f"{len(data)} Akun...")
for i in range(len(data)-1):
    user = data[i].replace('\n','')[:16]
    ip = data_ip[i].replace('\n', '')
    if create_db(user, ip) and create_user(user, ip):
        update_privileges(user, ip)
