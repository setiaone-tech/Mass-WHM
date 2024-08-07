import os
import requests
import base64

# Unggah file zip ke server
def upload_zip_file(zip_file_path, destination_path):
    with open(zip_file_path, 'rb') as file:
        file_name = os.path.basename(zip_file_path)
        # Parameter untuk permintaan API
        files = {
            'file-1': (file_name, file),
        }
        params = {
            "dir": destination_path,
            "file-1": file_name
        }
        
        # URL endpoint untuk mengunggah file
        upload_url = f"{cpanel_url}/execute/Fileman/upload_files"
        
        # Mengirim permintaan POST untuk mengunggah file
        response = requests.post(upload_url, headers=headers, params=params, files=files, verify=False)

        # Memeriksa respons
        if response.status_code == 200:
            result = response.json()
            if result.get('status') == 1:
                print(f"File '{file_name}' berhasil diunggah ke '{destination_path}'.")
                return True
            else:
                print(f"Gagal mengunggah file '{file_name}':", result.get('errors'))
                return False
        else:
            print(f"Gagal terhubung ke API cPanel. Status Code: {response.status_code}")
            return False
        
# Ekstrak file zip di server
def extract_zip_file(zip_file_name):
    params = {
        "op": "extract",  # Operasi ekstraksi
        "sourcefiles": f"/public_html/{zip_file_name}",
        "destfiles": destination_path,
        "doubledecode": "0"  # Set ini ke 1 jika Anda menghadapi masalah pengkodean
    }
    
    # URL endpoint untuk mengekstrak file
    extract_url = f"{cpanel_url}/json-api/cpanel?cpanel_jsonapi_user={cpanel_username}&cpanel_jsonapi_apiversion=2&cpanel_jsonapi_module=Fileman&cpanel_jsonapi_func=fileop"
    
    # Mengirim permintaan POST untuk mengekstrak file
    response = requests.post(extract_url, headers=headers, data=params, verify=False)

    # Memeriksa respons
    if response.status_code == 200:
        result = response.json()
        if result.get('cpanelresult', {}).get('event', {}).get('result') == 1:
            print(f"File '{zip_file_name}' berhasil diekstrak di '{destination_path}'.")
        else:
            errors = result.get('cpanelresult', {}).get('error', 'Gagal mengekstrak file.')
            print(f"Gagal mengekstrak file '{zip_file_name}':", errors)
    else:
        print(f"Gagal terhubung ke API cPanel. Status Code: {response.status_code}")


print("Proses...")
with open('list_domain.txt') as f:
    data = f.readlines()
f.close()

with open('list_ip.txt') as f:
    data_ip = f.readlines()
f.close()

print(f"{len(data)} Akun...")
for i in range(len(data)-1):
    user = data[i].split('.')[0]
    user = user[:16]
    ip = data_ip[i].replace('\n', '')

    # Konfigurasi
    cpanel_url = f"https://{ip}:2083"  # Ganti dengan domain atau IP cPanel Anda
    cpanel_username = user  # Ganti dengan username cPanel Anda
    cpanel_password = ""  # Ganti dengan password cPanel Anda
    zip_file_path = "{path}/laravel_template.zip"  # Path di mana zip file akan disimpan
    destination_path = "/public_html"  # Ganti dengan path tujuan di server cPanel

    # Encode username dan password ke Base64
    credentials = f"{cpanel_username}:{cpanel_password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    # Header untuk otentikasi Basic
    headers = {
        "Authorization": f"Basic {encoded_credentials}"
    }

    # Mengunggah dan mengekstrak file
    if upload_zip_file(zip_file_path, destination_path):
        zip_file_name = os.path.basename(zip_file_path)
        extract_zip_file(zip_file_name)
