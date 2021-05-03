from reportlab.pdfgen import canvas
from locataire import sql_database
import os


# pdf function generator
class pdf_generator():

    def __init__(self, pdf, nom, prenom, adresse, ville, sci, loyer, charge, day, month, years, cat):
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
        self.year = years
        self.cat = cat
        self.database = sql_database()

    def generator(self):
        if self.cat == 1:  # habitation case
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
            self.pdf.drawString(350, 600, f"A LIEU le {self.day}/{self.month}/{self.year}")
            # corps
            self.pdf.drawString(150, 550,
                                f"Quittance de loyer pour le mois de {self.month_list[int(self.month)]} {self.year}")
            self.pdf.drawString(150, 500, "Montant hors charges")
            self.pdf.drawString(350, 500, f"{self.loyer} €")
            self.pdf.drawString(150, 485, "Charges")
            self.pdf.drawString(357, 485, f"{self.charge} €")
            self.pdf.drawString(150, 450, "Total")
            self.pdf.drawString(350, 450, f"{int(self.loyer) + int(self.charge)} €")

            self.pdf.showPage()
            self.pdf.save()

        else:  # shop case
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
            self.pdf.drawString(350, 600, f"A LIEU le {self.day}/{self.month}/{self.year}")
            # corps
            self.pdf.drawString(150, 570, f"FACTURE N° {self.month}/{self.year}")
            self.pdf.drawString(150, 550,
                                f"Quittance de loyer pour le mois de {self.month_list[int(self.month)]} {self.year}")

            self.pdf.drawString(150, 500, "Montant hors charges")
            self.pdf.drawString(350, 500, f"{self.loyer} €")

            self.pdf.drawString(150, 485, "TVA 20.00 %")
            self.pdf.drawString(357, 485, f"{float(self.loyer) * 1.20 - float(self.loyer)} €")

            self.pdf.drawString(150, 460, "Charges")
            self.pdf.drawString(357, 460, f"{self.charge} €")

            self.pdf.drawString(150, 445, "Montant TTC")
            self.pdf.drawString(350, 445, f"{int(self.loyer) + int(self.charge)} €")

            self.pdf.drawString(150, 420, "Rest à payer")
            self.pdf.drawString(350, 420, f"{float(self.loyer) * 1.20 + float(self.charge)} €")

            self.pdf.showPage()
            self.pdf.save()


class make_directories():
    def __init__(self, years, month):
        self.years = years
        self.month = month
        self.database = sql_database()

        sci_list = []
        for elt in self.database.elt_table("SCI", "location"):
            if elt[0] not in sci_list:
                sci_list.append(elt[0])
        directory = os.path.dirname(__file__)
        for n in sci_list:
            dir = (os.path.join(directory, n + "\\" + self.years + "\\" + self.month + "\\"))
            if not os.path.exists(dir):
                os.makedirs(dir)


if __name__ == "__main__":
    database = sql_database()
    make_directories("2020", "01")

    day, month, year = "2", "8", "2020"
    # make_directories(year, month)
    directories = os.path.dirname(__file__)

    for elt in database.pdf_table():
        nom, prenom, adresse, ville, sci, loyer, charges = elt
        print(nom, prenom, adresse, ville, sci, loyer, charges)
        name_pdf = directories + "\\" + sci + "\\" + year + "\\" + month + "\\" + nom + ".pdf"
        pdf = canvas.Canvas(name_pdf)
        pdf_gen = pdf_generator(pdf, nom, prenom, adresse, ville, sci, loyer,
                                charges, day, month, year, cat="c")
        pdf_gen.generator()
