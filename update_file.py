import requests
import base64

def read_local_env_file(local_file_path):
    try:
        with open(local_file_path, 'r') as file:
            content = file.read()
        return content
    except Exception as e:
        print(f"Error membaca file: {e}")
        return None

# Fungsi untuk menulis konten baru ke file .env
def write_env_file(new_content, filename):
    write_url = f"{cpanel_url}/json-api/cpanel"
    params = {
        "cpanel_jsonapi_user": cpanel_username,
        "cpanel_jsonapi_apiversion": "2",
        "cpanel_jsonapi_module": "Fileman",
        "cpanel_jsonapi_func": "savefile",
        "dir": destination_path,
        "filename": filename,
        "content": new_content
    }
    
    response = requests.post(write_url, headers=headers, data=params, verify=False)
    
    if response.status_code == 200:
        result = response.json()
        print(result)
        if result['cpanelresult']['event']['result'] == 1:
            print("File .env berhasil diperbarui.")
        else:
            print("Gagal memperbarui file .env:", result['cpanelresult']['data'][0]['reason'])
    else:
        print(f"Gagal terhubung ke API cPanel. Status Code: {response.status_code}")


print("Proses...")
with open('list_domain_fix.txt') as f:
    data = f.readlines()
f.close()

with open('list_ip_fix.txt') as f:
    data_ip = f.readlines()
f.close()

print(f"{len(data)} Akun...")
for i in range(len(data)-1):
    user = data[i].split('.')[0]
    user = user[:16]
    ip = data_ip[i].replace('\n', '')
    # Konfigurasi
    cpanel_url = f"https://{ip}:2083"  # Ganti dengan domain atau IP cPanel Anda
    cpanel_username = f"{user}"  # Ganti dengan username cPanel Anda
    cpanel_password = ""  # Ganti dengan password cPanel Anda

    # Encode username dan password ke Base64
    credentials = f"{cpanel_username}:{cpanel_password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    # Header untuk otentikasi Basic
    headers = {
        "Authorization": f"Basic {encoded_credentials}"
    }

    destination_path = "/public_html/app/Http/Controllers/Backend/"  # Path tujuan di server cPanel
    local_env_path = "C:/xampp/htdocs/laravel2/app/Http/Controllers/Backend/NewsPostController.php"
    env_content = read_local_env_file(local_env_path)

    # Menulis konten baru ke file .env
    write_env_file(env_content, 'NewsPostController.php')
