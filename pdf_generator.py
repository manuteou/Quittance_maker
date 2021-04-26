from reportlab.pdfgen import canvas
import csv
import os

# pdf function generator
class pdf_generator:


    def __init__(self, pdf, nom, prenom, adresse, ville, sci, loyer, charge, day, month, years):

        self.month_list = {1: "Janvier", 2: "Fevrier", 3: "Mars",
                           4: "Avril", 5: "Mai", 6: "Juin",
                           7: "Juillet", 8: "Aout", 9: "Septembre",
                           10: "Octobre", 11: "Novembre", 12: "Decembre"}

        self.pdf = pdf
        self.nom = nom
        self.prenom = prenom
        self.adresse = adresse
        self.ville = ville
        self.sci = sci
        self.loyer = loyer
        self.charge = charge
        self.day = day
        self.month = month
        self.years = years

        # Coordonnées de la SCI
        self.pdf.drawString(20, 800, f"{self.sci}")  # colon, row ( 0 down / 800 up) ( 0 left / 600 right)
        self.pdf.drawString(20, 785, "xx rue lllala tralala")
        self.pdf.drawString(20, 770, "98150 les moutons bleus")
        self.pdf.drawString(20, 755, "telephone")
        self.pdf.drawString(20, 740, "mail")
    # Coordonnées du locataire
        self.pdf.drawString(350, 700, f"{self.nom} {self.prenom}")
        self.pdf.drawString(350, 685, f"{self.adresse}")
        self.pdf.drawString(350, 670, f"{self.ville}")
    # Date
        self.pdf.drawString(350, 600, f"A LIEU le {day}/{month}/{years}")
    # corps
        self.pdf.drawString(150, 550, f"Quittance de loyer pour le mois de {self.month_list[int(self.month)]} {self.years}")
        self.pdf.drawString(150, 500, "Montant hors charges")
        self.pdf.drawString(350, 500, f"{self.loyer} €")
        self.pdf.drawString(150, 485, "Charges")
        self.pdf.drawString(357, 485, f"{self.charge} €")
        self.pdf.drawString(150, 450, "Total")
        self.pdf.drawString(350, 450, f"{int(self.loyer) + int(self.charge)} €")



