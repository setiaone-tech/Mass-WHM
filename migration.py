from fabric import Connection

def run_commands(account):
    try:
        conn = Connection(
            host=host,
            user=username,
            connect_kwargs={
                "password": password,
            }
        )
        
        full_migrate_command = migrate_command.format(project_path.format(account))
        full_seed_command = seed_command.format(project_path.format(account))
        
        # Menjalankan perintah migrate
        migrate_result = conn.run(full_migrate_command, hide=True)
        print(f"Migration output for {account}:\n{migrate_result.stdout}")
        if migrate_result.stderr:
            print(f"Migration error for {account}:\n{migrate_result.stderr}")
        
        # Menjalankan perintah db:seed
        seed_result = conn.run(full_seed_command, hide=True)
        print(f"Seed output for {account}:\n{seed_result.stdout}")
        if seed_result.stderr:
            print(f"Seed error for {account}:\n{seed_result.stderr}")
        
        conn.close()
    except Exception as e:
        print(f"Failed to run commands for {account}: {str(e)}")

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

    # Host SSH
    host = f"{ip}"

    # Kredensial SSH
    username = f"{user}"
    password = ""

    # Path ke direktori proyek Laravel di setiap akun
    project_path = f"/home/{user}/public_html"

    # Perintah untuk menjalankan migrate dan db:seed
    migrate_command = f"php {project_path}/artisan migrate"
    seed_command = f"php {project_path}/artisan db:seed"

    run_commands(user)
