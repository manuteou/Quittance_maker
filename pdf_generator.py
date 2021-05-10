from locataire import sql_database
from pathlib import Path
import os


# pdf function generator
class pdf_generator():

    def __init__(self, pdf, nom, prenom, adresse, ville, loyer, charge, day, month, years, cat,
                 sci_nom, sci_adresse, sci_cp_ville, sci_tel, sci_mail, sci_siret):
        self.month_list = {1: "Janvier", 2: "Fevrier", 3: "Mars",
                           4: "Avril", 5: "Mai", 6: "Juin",
                           7: "Juillet", 8: "Aout", 9: "Septembre",
                           10: "Octobre", 11: "Novembre", 12: "Decembre"}

        self.pdf = pdf
        self.nom = nom
        self.prenom = prenom
        self.adresse = adresse
        self.ville = ville
        self.loyer = loyer
        self.charge = charge
        self.day = day
        self.month = month
        self.year = years
        self.cat = cat
        self.sci_nom = sci_nom
        self.sci_adresse = sci_adresse
        self.sci_cp_ville = sci_cp_ville
        self.sci_tel = sci_tel
        self.sci_mail = sci_mail
        self.sci_siret = sci_siret
        self.database = sql_database()

    def generator(self):
        self.pdf.setFont("Helvetica", 15)

        if self.cat == 1:  # habitation case
            # Coordonnées de la SCI
            self.pdf.drawString(20, 800, f"{self.sci_nom}")  # colon, row ( 0 down / 800 up) ( 0 left / 600 right)
            self.pdf.drawString(20, 785, f"{self.sci_adresse}")
            self.pdf.drawString(20, 770, f"{self.sci_cp_ville}")
            self.pdf.drawString(20, 755, f"{self.sci_tel}")
            self.pdf.drawString(20, 740, f"{self.sci_siret}")
            # Coordonnées du locataire
            self.pdf.drawString(350, 700, f"{self.nom} {self.prenom}")
            self.pdf.drawString(350, 685, f"{self.adresse}")
            self.pdf.drawString(350, 670, f"{self.ville}")
            # Date
            self.pdf.drawString(350, 600, f"A {self.ville.split()[1]} le {self.day}/{self.month}/{self.year}")
            # corps
            self.pdf.drawCentredString(160, 613, "QUITTANCE DE LOYER")
            self.pdf.drawString(150, 550,
                                f"Loyer pour le mois de {self.month_list[int(self.month)]} {self.year}")
            self.pdf.drawString(140, 450, "Loyer")
            self.pdf.drawString(340, 450, f"{self.loyer} €")
            self.pdf.drawString(140, 420, "Provision pour charges")
            self.pdf.drawString(340, 420, f"{self.charge} €")
            self.pdf.drawString(140, 400, "Total")
            self.pdf.drawString(340, 400, f"{int(self.loyer) + int(self.charge)} €")
            # graphic elements
            self.pdf.line(10, 630, 590, 630)
            self.pdf.line(10, 595, 590, 595)
            self.pdf.line(10, 630, 10, 595)
            self.pdf.line(590, 630, 590, 595)
            p = Path()
            s = p / 'sign.PNG'
            if s.exists() == True:
                self.pdf.drawImage("sign.PNG", 350, 80, width=120, height=120)
            # ending
            self.pdf.showPage()
            self.pdf.save()

        else:  # shop case
            # Coordonnées de la SCI
            self.pdf.drawString(20, 800, f"{self.sci_nom}")  # colon, row ( 0 down / 800 up) ( 0 left / 600 right)
            self.pdf.drawString(20, 785, f"{self.sci_adresse}")
            self.pdf.drawString(20, 770, f"{self.sci_cp_ville}")
            self.pdf.drawString(20, 755, f"{self.sci_tel}")
            self.pdf.drawString(20, 740, f"{self.sci_siret}")
            # Coordonnées du locataire
            self.pdf.drawString(350, 700, f"{self.nom} {self.prenom}")
            self.pdf.drawString(350, 685, f"{self.adresse}")
            self.pdf.drawString(350, 670, f"{self.ville}")
            # Date
            self.pdf.drawString(350, 600, f"A {self.ville.split()[1]} le {self.day}/{self.month}/{self.year}")
            # corps
            self.pdf.drawCentredString(160, 613, "QUITTANCE DE LOYER")
            self.pdf.drawString(150, 570, f"FACTURE N° {self.month}/{self.year}")
            self.pdf.drawString(150, 550,
                                f"Loyer pour le mois de {self.month_list[int(self.month)]} {self.year}")

            self.pdf.drawString(150, 500, "Loyer hors taxes")
            loyer_ht = int(self.loyer / 1.20)
            self.pdf.drawString(350, 500, f"{loyer_ht} €")

            self.pdf.drawString(150, 485, "TVA 20 %")
            self.pdf.drawString(357, 485, f"{int(self.loyer) - loyer_ht} €")

            self.pdf.drawString(150, 460, "Provision pour charges")
            self.pdf.drawString(357, 460, f"{self.charge} €")

            self.pdf.drawString(150, 445, "Montant TTC")
            self.pdf.drawString(350, 445, f"{int(self.loyer) + int(self.charge)} €")

            # graphic elements
            self.pdf.line(10, 630, 590, 630)
            self.pdf.line(10, 595, 590, 595)
            self.pdf.line(10, 630, 10, 595)
            self.pdf.line(590, 630, 590, 595)
            p = Path()
            s = p / 'sign.PNG'
            if s.exists() == True:
                self.pdf.drawImage("sign.PNG", 350, 80, width=120, height=120)

            # ending
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
    pass

