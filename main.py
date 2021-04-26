#from locataire import locataire
from pdf_generator import pdf_generator
from reportlab.pdfgen import canvas
import csv
import os


################################################################################
# this variables are just for execution before graphic interface
years = "2021"
month = "02"
day = "01"
sci_list = ["SCI", "SCI2", "SCI3"]
# nom = "bubu"
# prenom = "lulu"
# adresse = "15 rue des lolo"
# ville = "labas"
# tel = "0105030632"
# mail = "zaeazr@eaze.fr"
# sci = "SCI"
# loyer = 1500
# charges = 200
##################################################################################
# this part will be use later in graphic interface
#client1 = locataire(nom, prenom, adresse, ville, tel, mail, sci, loyer, charges)
#client1.get_locataire()
#client1.save_contact()
##################################################################################

# we create a repertory to classify the quittance
directory = os.path.dirname(__file__)
for n in sci_list:
    dir = (os.path.join(directory, n + "\\" + years + "\\" + month + "\\"))
    print(dir)
    if not os.path.exists(dir):
        os.makedirs(dir)

# core
with open('locataire.csv','r') as csvfile: # we open the client's files
    info_locataire = csv.reader(csvfile)
    for row in info_locataire:
        nom, prenom, adresse, ville, tel, mail, sci, loyer, charge = [w for w in row]
        name_pdf = directory + "\\" + sci + "\\" + years + "\\" + month + "\\" + str(nom) + ".pdf"
        pdf = canvas.Canvas(name_pdf) # we generate pdf
        pdf_generator(pdf, nom, prenom, adresse, ville, sci, loyer, charge, day, month, years)
        pdf.showPage()
        pdf.save()  # we save them in the directories
        #send_mail(name_pdf, mail) # We send mail


