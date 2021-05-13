from GUI import SplashScreen
from locataire import sql_database_init
from pathlib import Path
import json

# initialisation
p = Path()
c = p / 'config.json'
d = p / 'tenant_db.db'
m = p / 'message.txt'

if not c.exists():
    config = {"master_mail": "", "password": "", "SMTP": "", "port": "", "sci": []}
    with open('config.json', 'w') as json_files:
        json.dump(config, json_files)
    print("création fichier config")

if not d.exists():
    print("création base de données")
    sql_database_init()

if not m.exists():
    text = 'Bonjour ci-joint la quittance de loyer'
    with open('message.txt', 'w') as text_file:
        text_file.write(text)

# GUI launch
SplashScreen().mainloop()