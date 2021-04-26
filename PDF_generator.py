from reportlab.pdfgen import canvas
import csv
import os

# pdf function generator
def pdf_generator(pdf):
    pdf.drawString(20, 800, f"{nom} {prenom}")
    pdf.drawString(20, 780, f"{adresse}")
    pdf.drawString(20, 760, f"{ville}")
    pdf.drawString(350, 600, f"{sci}")

# we create a repertory to classify the quittance
years = "2021"
month = "01"
directory = os.path.dirname(__file__)
dir = (os.path.join(directory, years + "\\" + month + "\\"))
print(dir)
if not os.path.exists(dir):
    os.makedirs(dir)

# we open the client's files and generate pdf
with open('locataire.csv','r') as csvfile:
    info_locataire = csv.reader(csvfile)
    for row in info_locataire:
        nom, prenom, adresse, ville, tel, mail, sci = [row for row in row]
        name_pdf = dir + str(nom) + "_" + str(prenom) + ".pdf"
        print(name_pdf)
        pdf = canvas.Canvas(name_pdf)
        pdf_generator(pdf)
        pdf.showPage()
        pdf.save()