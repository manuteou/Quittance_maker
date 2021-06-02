from GUI import SplashScreen
from tablesdb import sql_database_init
from pathlib import Path
import json
from functions import directory
from datetime import datetime, date
import sqlite3
import glob
import os

# initialisation
p = Path()
c = p / 'config.json'
database = p / 'tenant_db.db'
m = p / 'message.txt'
today = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
#today = date.today()

if not c.exists():
    config = {"master_mail": "",
              "password": "",
              "SMTP": "",
              "port": "",
              "sci": [],
              "interface": {
                  "bg": "#3D4A56",
                  "button_color": "#1A5276",
                  "fg": '#74D0F1',
                  "tableau": "#3D4A90",
                  "fg_size": 14,
                  "font_gui": 8
                        },
              "default": {
                  "bg": "#3D4A56",
                  "button_color": "#1A5276",
                  "tableau": "#3D4A90",
                  "fg": '#74D0F1',
                  "fg_size": 14,
                  "font_gui": 8
              }
              }

    with open('config.json', 'w') as json_files:
        json.dump(config, json_files)
    print("création fichier config")

if not database.exists():
    print("création base de données")
    sql_database_init()

if database.exists():
    sql_database_init()
    directory = directory()
    path_dir = directory.joinpath("save_db")
    path_dir.mkdir(parents=True, exist_ok=True)
    path = path_dir.joinpath(f"{today}_{database}")
    con = sqlite3.connect("tenant_db.db")
    back = sqlite3.connect(path)
    con.backup(back)
    back.close()
    print(path_dir)
    all_path = path_dir.joinpath("*")
    list_path = []
    for path in glob.glob(str(all_path)):
        list_path.append(path)
    if len(list_path) > 5:
        for i in list_path[4:]:
            os.remove(i)
        print(f"remove {i}")

if not m.exists():
    text = 'Bonjour ci-joint la quittance de loyer'
    with open('message.txt', 'w') as text_file:
        text_file.write(text)


# GUI launch


SplashScreen().mainloop()
