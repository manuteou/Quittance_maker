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

if not d.exists():
    print("création base de données")
    sql_database_init()

if d.exists():
# to do ---> save current database
    pass


if not m.exists():
    text = 'Bonjour ci-joint la quittance de loyer'
    with open('message.txt', 'w') as text_file:
        text_file.write(text)

# GUI launch


SplashScreen().mainloop()
