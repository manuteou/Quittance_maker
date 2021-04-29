from locataire import locataire
from pdf_generator import pdf_generator
from mail_sender import send_mail
from reportlab.pdfgen import canvas
from tinydb import TinyDB, where, Query
import json
import os

# test variables will be implement in code later
years = "2021"
month = "02"
day = "01"
#############################################
# database's initialisation
db = TinyDB('db.json')
locataire_db = db.table('locataire')

# open config
with open('config.json', 'r') as config_json:
    config = json.load(config_json)

# directories' creation
directory = os.path.dirname(__file__)
for n in config["sci"]:
    dir = (os.path.join(directory, n + "\\" + years + "\\" + month + "\\"))
    print(dir)
    if not os.path.exists(dir):
        os.makedirs(dir)

# locataire's initialisation
test_mail = config['email_test']
client1 = locataire('Bubu', 'prenom', 'adresse', 'ville', 'tel', test_mail, 'sci_1', 1200, 100)
client2 = locataire('baba', 'prenom', 'adresse', 'ville', 'tel', test_mail, 'sci_2', 1200, 100, 'c')
client3 = locataire('zaza', 'prenom', 'adresse', 'ville', 'tel', test_mail, 'sci_2', 1200, 100, 'c')
client4 = locataire('lala', 'prenom', 'adresse', 'ville', 'tel', test_mail, 'sci_1', 1200, 100)

client1.save_contact()
client2.save_contact()
client3.save_contact()
client4.save_contact()

# pdf generation
user = Query()
el = locataire_db.all()[0]
for i in range(len(locataire_db)):
    el = locataire_db.all()[i]
    name_pdf = directory + "\\" + el['sci'] + "\\" + years + "\\" + month + "\\" + el['nom'] + ".pdf"
    pdf = canvas.Canvas(name_pdf)
    pdf_generator(pdf, el['nom'], el['prenom'], el['adresse'],el['ville'], el['sci'], el['loyer'],
                  el['charges'], day, month, years, el['cat'])
    pdf.showPage()
    pdf.save()

# mail's sending
for i in range(len(locataire_db)):
    el = locataire_db.all()[i]
    path = os.path.join(directory, el['sci'] + "\\" + years + "\\" + month + "\\") + el["nom"] + ".pdf"
    mail = send_mail("Quittance", config["master_mail"], config["password"],
                     el["mail"], config['smtp'], config['port'], path)
    mail.send()

client1.del_contact()
client2.del_contact()
client3.del_contact()
client4.del_contact()