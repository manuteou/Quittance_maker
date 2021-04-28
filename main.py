#from locataire import locataire
from pdf_generator import pdf_generator
from reportlab.pdfgen import canvas
import json
import os

# we create a repertory to classify the quittance
directory = os.path.dirname(__file__)
for n in sci_list:
    dir = (os.path.join(directory, n + "\\" + years + "\\" + month + "\\"))
    print(dir)
    if not os.path.exists(dir):
        os.makedirs(dir)

# core
# creating pdf
with open('locataire.txt', 'r') as csvfile:
    info_locataire = csv.reader(csvfile)
    for row in info_locataire:
        nom, prenom, adresse, ville, tel, mail, sci, loyer, charge = [w for w in row]
        name_pdf = directory + "\\" + sci + "\\" + years + "\\" + month + "\\" + str(nom) + ".pdf"
        pdf = canvas.Canvas(name_pdf) # we generate pdf
        pdf_generator(pdf, nom, prenom, adresse, ville, sci, loyer, charge, day, month, years)
        pdf.showPage()
        pdf.save()  # we save them in the directories

# sending mail
with open("config.json") as json_file:
    config = json.load(json_file)

with open("locataire.txt") as json_file:
    locataire = json.load(json_file)
    path = os.path.join(directory, locataire['sci'] + "\\" + years + "\\" + month + "\\") + locataire["nom"] + ".pdf"
    mail = send_mail("Quittance", config["master_mail"], config["password"], locataire["mail"], path)
    mail.send()



