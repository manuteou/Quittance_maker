from reportlab.pdfgen import canvas
import csv
import os

# pdf function generator
def pdf_generator(pdf):
    # Coordonnées de la SCI
    pdf.drawString(20, 800, f"{sci}")  # colon, row ( 0 down / 800 up) ( 0 left / 600 right)
    pdf.drawString(20, 785, "xx rue lllala tralala")
    pdf.drawString(20, 770, "98150 les moutons bleus")
    pdf.drawString(20, 755, "telephone")
    pdf.drawString(20, 740, "mail")
    # Coordonnées du locataire
    pdf.drawString(350, 700, f"{nom} {prenom}")
    pdf.drawString(350, 685, f"{adresse}")
    pdf.drawString(350, 670, f"{ville}")
    # Date
    pdf.drawString(350, 600, f"A LIEU le {day}/{month}/{years}")
    # corps
    pdf.drawString(150, 550, f"Quittance de loyer pour le mois de {month_list[int(month)]} {years}")
    pdf.drawString(150, 500, "Montant hors charges")
    pdf.drawString(350, 500, f"{loyer} €")
    pdf.drawString(150, 485, "Charges")
    pdf.drawString(357, 485, f"{charge} €")
    pdf.drawString(150, 450, "Total")
    pdf.drawString(350, 450, f"{int(loyer) + int(charge)} €")

month_list = {1:"Janvier", 2:"Fevrier", 3:"Mars", 4:"Avril", 5:"Mai", 6:"Juin", 7:"Juillet", 8:"Aout", 9:"Septembre", 10:"Octobre", 11:"Novembre", 12:"Decembre"}
# this variables are just for execution
years = "2021"
month = "02"
day = "01"
# we create a repertory to classify the quittance
sci_list = ["SCI", "SCI2", "SCI3"]
directory = os.path.dirname(__file__)
for n in sci_list:
    dir = (os.path.join(directory, n + "\\" + years + "\\" + month + "\\"))
    print(dir)
    if not os.path.exists(dir):
        os.makedirs(dir)

# we open the client's files and generate pdf
with open('locataire.csv','r') as csvfile:
    info_locataire = csv.reader(csvfile)
    for row in info_locataire:
        nom, prenom, adresse, ville, tel, mail, sci, loyer, charge = [w for w in row]
        name_pdf = directory + "\\" + sci + "\\" + years + "\\" + month + "\\" + str(nom) + ".pdf"
        print(name_pdf)
        pdf = canvas.Canvas(name_pdf)
        pdf_generator(pdf)
        pdf.showPage()
        pdf.save()