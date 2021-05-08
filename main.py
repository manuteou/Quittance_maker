from GUI import main_gui
from locataire import sql_database_init
from pathlib import Path
import json

# initialisation
p = Path()
c = p / 'config.json'
d = p / 'tenant_db.db'

if c.exists() == False:
    config = {"master_mail": "", "password": "", "SMTP": "", "port": "", "sci": []}
    with open('config.json','w') as json_files:
        json.dump(config, json_files)
    print("création fichier config")


if d.exists() == False:
    print("création base de données")
    sql_database_init()

# GUI launch
main_gui().mainloop()