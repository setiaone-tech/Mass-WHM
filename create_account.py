import requests
import json

# Konfigurasi WHM
whm_host = "https://your-whm-server:2087"
whm_user = "root"
whm_token = "YOUR_API_TOKEN"

# Detail akun cPanel baru
new_account = {
    "username": "newcpaneluser",
    "domain": "newdomain.com",
    "password": "yourpassword"
}

def create_cpanel_account():
    url = f"{whm_host}/json-api/createacct"
    headers = {
        "Authorization": f"whm {whm_user}:{whm_token}"
    }
    payload = {
        "username": new_account["username"],
        "domain": new_account["domain"],
        "password": new_account["password"]
    }

    response = requests.post(url, headers=headers, data=payload, verify=False)
    
    if response.status_code == 200:
        response_data = response.json()
        if response_data["status"] == 1:
            print(f"Account for {new_account['username']} created successfully.")
        else:
            print(f"Failed to create account: {response_data['statusmsg']}")
    else:
        print(f"HTTP Error: {response.status_code}")

if __name__ == "__main__":
    create_cpanel_account()
