from GUI import main_gui
from locataire import sql_database_init
from pathlib import Path
import json

# initialisation
p = Path()
c = p / 'config.json'
d = p / 'tenatdb.db'

if c.exists() == False:
    config = {"master_mail": "", "password": "", "SMTP": "", "port": "", "sci": []}
    with open('config.json','w') as json_files:
        json.dump(config, json_files)
    print("création")


if d.exists() == False:
    print("création")
    sql_database_init()

# GUI launch
main_gui().mainloop()