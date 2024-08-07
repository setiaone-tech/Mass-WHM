import requests

# Konfigurasi WHM
whm_host = "https://your-whm-server:2087"
whm_user = "root"
whm_token = "YOUR_API_TOKEN"

# Detail database dan pengguna database baru
db_details = {
    "db_name": "newdatabase",
    "db_user": "dbuser",
    "db_password": "dbpassword"
}

def create_database(cpanel_user):
    url = f"{whm_host}/json-api/cpanel"
    headers = {
        "Authorization": f"whm {whm_user}:{whm_token}"
    }
    payload = {
        "cpanel_jsonapi_user": cpanel_user,
        "cpanel_jsonapi_apiversion": "3",
        "cpanel_jsonapi_module": "Mysql",
        "cpanel_jsonapi_func": "createdb",
        "name": db_details["db_name"]
    }

    response = requests.post(url, headers=headers, data=payload, verify=False)
    response_data = response.json()
    
    if response.status_code == 200 and response_data['cpanelresult']['data'][0]['result']:
        print(f"Database {db_details['db_name']} created successfully.")
        return True
    else:
        print(f"Failed to create database: {response_data}")
        return False

def create_db_user(cpanel_user):
    url = f"{whm_host}/json-api/cpanel"
    headers = {
        "Authorization": f"whm {whm_user}:{whm_token}"
    }
    payload = {
        "cpanel_jsonapi_user": cpanel_user,
        "cpanel_jsonapi_apiversion": "3",
        "cpanel_jsonapi_module": "Mysql",
        "cpanel_jsonapi_func": "createuser",
        "name": db_details["db_user"],
        "password": db_details["db_password"]
    }

    response = requests.post(url, headers=headers, data=payload, verify=False)
    response_data = response.json()

    if response.status_code == 200 and response_data['cpanelresult']['data'][0]['result']:
        print(f"Database user {db_details['db_user']} created successfully.")
        return True
    else:
        print(f"Failed to create database user: {response_data}")
        return False

def set_db_privileges(cpanel_user):
    url = f"{whm_host}/json-api/cpanel"
    headers = {
        "Authorization": f"whm {whm_user}:{whm_token}"
    }
    payload = {
        "cpanel_jsonapi_user": cpanel_user,
        "cpanel_jsonapi_apiversion": "3",
        "cpanel_jsonapi_module": "Mysql",
        "cpanel_jsonapi_func": "setprivileges",
        "database": db_details["db_name"],
        "user": db_details["db_user"],
        "privileges": "ALL PRIVILEGES"
    }

    response = requests.post(url, headers=headers, data=payload, verify=False)
    response_data = response.json()

    if response.status_code == 200 and response_data['cpanelresult']['data'][0]['result']:
        print(f"Privileges set for user {db_details['db_user']} on database {db_details['db_name']}.")
        return True
    else:
        print(f"Failed to set privileges: {response_data}")
        return False

if __name__ == "__main__":
    cpanel_user = ''
    if create_database(cpanel_user) and create_db_user(cpanel_user):
        set_db_privileges(cpanel_user)
