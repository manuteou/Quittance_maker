from locataire import sql_database
from pathlib import Path
import os


# pdf function generator
class PdfGenerator:

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

        if self.cat == 0:  # habitation case
            self.pdf.drawString(150, 550,
                                f"Loyer pour le mois de {self.month_list[int(self.month)]} {self.year}")
            self.pdf.drawString(140, 450, "Loyer")
            self.pdf.drawString(340, 450, f"{float(self.loyer):0.2f} €")
            self.pdf.drawString(140, 420, "Provision pour charges")
            self.pdf.drawString(345, 420, f"{float(self.charge):0.2f} €")
            self.pdf.drawString(140, 400, "Total")
            self.pdf.drawString(340, 400, f"{float(self.loyer) + float(self.charge):0.2f} €")

        else:
            self.pdf.drawString(150, 570, f"FACTURE N° {self.month}/{self.year}")
            self.pdf.drawString(100, 530,
                                f"Loyer pour le mois de {self.month_list[int(self.month)]} {self.year}")

            self.pdf.drawString(100, 450, "Loyer hors taxes")
            loyer_ht = (float(self.loyer / 1.20))
            self.pdf.drawString(350, 450, f"{loyer_ht:0.2f} €")

            self.pdf.drawString(100, 430, "TVA 20 %")
            self.pdf.drawString(355, 430, f"{(float(self.loyer) - loyer_ht):0.2f} €")

            self.pdf.drawString(100, 410, "Provision pour charges")
            self.pdf.drawString(355, 410, f"{float(self.charge):0.2f} €")

            self.pdf.drawString(100, 390, "Montant TTC")
            self.pdf.drawString(350, 390, f"{float(self.loyer) + float(self.charge):0.2f} €")

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
        self.pdf.drawString(350, 600, f"A {self.sci_cp_ville.split(' ', 1)[1]} le {self.day}/{self.month}/{self.year}")
        # corps
        self.pdf.drawCentredString(160, 613, "QUITTANCE DE LOYER")

        # graphic elements
        self.pdf.line(10, 630, 590, 630)
        self.pdf.line(10, 595, 590, 595)
        self.pdf.line(10, 630, 10, 595)
        self.pdf.line(590, 630, 590, 595)
        p = Path()
        s = p / 'sign.PNG'
        if s.exists():
            self.pdf.drawImage("sign.PNG", 350, 80, width=120, height=120)
        # ending
        self.pdf.showPage()
        self.pdf.save()


class IndexLetter:
    def __init__(self, pdf, nom, prenom, adresse, ville, loyer, charge, day, month, year,
                 sci_nom, sci_adresse, sci_cp_ville, sci_tel, sci_mail, sci_siret, indice_base, indice_new, cat, date_entree):
        self.month_list = {1: ["Janvier", "1er trimestre"], 2: ["Fevrier", "1er trimestre"], 3: ["Mars", "1er trimestre"],
                           4: ["Avril", "2eme trimestre"], 5: ["Mai", "2eme trimestre"], 6: ["Juin", "2eme trimestre"],
                           7: ["Juillet", "3eme trimestre"], 8: ["Aout", "3eme trimestre"], 9: ["Septembre", "3eme trimestre"],
                           10: ["Octobre", "3eme trimestre"], 11: ["Novembre", "3eme trimestre"], 12: ["Decembre", "3eme trimestre"]}

        self.pdf = pdf
        self.nom = nom
        self.prenom = prenom
        self.adresse = adresse
        self.ville = ville
        self.loyer = float(loyer) * float(indice_new) / float(indice_base)
        self.charge = charge
        self.day = day
        self.month = month
        self.year = year
        self.sci_nom = sci_nom
        self.sci_adresse = sci_adresse
        self.sci_cp_ville = sci_cp_ville
        self.sci_tel = sci_tel
        self.sci_mail = sci_mail
        self.sci_siret = sci_siret
        self.indice_base = indice_base
        self.new_indice = indice_new
        self.cat = cat
        self.date_entree = date_entree
        self.database = sql_database()
        if self.cat == 1:
            self.type ="loyers commerciaux"
        else:
            self.type ="de références des loyers"

    def generator(self):
        self.pdf.setFont("Helvetica", 15)
        if self.cat == 1:
            self.pdf.drawString(60, 300, "Loyer hors charges")
            self.pdf.drawString(250, 300, f"{float(self.loyer) / 1.20:0.2f} €")
            self.pdf.drawString(60, 280, "TVA")
            self.pdf.drawString(250, 280, f"{float(self.loyer) - float(self.loyer) / 1.20:0.2f} €")
            self.pdf.drawString(60, 260, "Provisions pour charges")
            self.pdf.drawString(255, 260, f"{self.charge:0.2f} €")
            self.pdf.drawString(60, 240, "Total")
            self.pdf.drawString(250, 240, f"{float(self.loyer) + float(self.charge):0.2f} €")

        else:
            self.pdf.drawString(60, 300, "Loyer")
            self.pdf.drawString(250, 300, f"{float(self.loyer):0.2f} €")
            self.pdf.drawString(60, 280, "Provisions pour charges")
            self.pdf.drawString(255, 280, f"{self.charge:0.2f} €")
            self.pdf.drawString(60, 260, "Total")
            self.pdf.drawString(250, 260, f"{float(self.loyer) + float(self.charge):0.2f} €")

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
        self.pdf.drawString(350, 613, f"A {self.sci_cp_ville.split(' ', 1)[1]} le {self.day}/{self.month}/{self.year}")
        # Corps
        self.pdf.drawString(20, 560, "OBJET : REVISION DU LOYER")
        self.pdf.drawString(20, 500, "Madame, Monsieur")
        self.pdf.drawString(20, 460, f"Par la présente, je vous informe qu'à compter du {self.day} {self.month_list[int(self.month)][0]} {self.year} , votre loyer principal")
        self.pdf.drawString(20, 440, f"mensuel s'élèvera à la somme de {self.loyer:0.2f} € TTC.Cette variation a été calculée")
        self.pdf.drawString(20, 420, f"selon l'indice de révision (indice national des {self.type} prévu dans ")
        self.pdf.drawString(20, 400, "votre bail conformément à la législation en vigeur. Le loyer hors charges est augmenté")
        self.pdf.drawString(20, 380, f"de {float(self.new_indice) / float(self.indice_base):0.2f} %. Les deux indices considérés sont :")
        self.pdf.drawString(60, 360, f"-      {self.month_list[int(self.month)][1]} {self.date_entree.split('/')[2]}: {self.indice_base}")
        self.pdf.drawString(60, 340, f"-      {self.month_list[int(self.month)][1]} {self.year} : {self.new_indice}")
        self.pdf.drawString(20, 320, "Les nouvelles données de votre quittance seront dorénavant les suivantes :")

        self.pdf.drawString(20, 220, "Je reste à votre dispositionpour de plus amples renseignements. Dans cette attente")
        self.pdf.drawString(20, 200, "veuillez agréer, Madame, Monsieur, l'expression de mes salutaions distinguées")
        self.pdf.drawString(20, 160, "Le Gérant.")
        p = Path()
        s = p / 'sign.PNG'
        if s.exists():
            self.pdf.drawImage("sign.PNG", 20, 30, width=120, height=120)
        self.pdf.showPage()
        self.pdf.save()


if __name__ == "__main__":
    from reportlab.pdfgen import canvas

    directory = Path(__file__).parent
    directory.mkdir(parents=True, exist_ok=True)
    path = directory.joinpath("test.pdf")
    pdf = canvas.Canvas(str(path))
    pdf_gen = PdfGenerator(pdf, nom="SEBAN", prenom="Emmanuel", adresse="7 rue ducis", ville="78000 VERSAILLES",
                          loyer=1000, charge="200", day="12", month="05", years="2020", cat=1,
                           sci_nom="JOMO",
                           sci_adresse="19 rue laurent Gaudet", sci_cp_ville="78150 LE CHESNAY",
                           sci_tel="01 39 55 16 69", sci_mail="marcelseban@hotmail.fr", sci_siret="155522220")

    #pdf_gen = IndexLetter(pdf, nom="SEBAN", prenom="Emmanuel", adresse="7 rue ducis", ville="78000 VERSAILLES",
                          # loyer="1000", charge="200", day="12", month="5", year="2020", sci_nom="JOMO",
                          #  sci_adresse="19 rue laurent Gaudet", sci_cp_ville="78150 LE CHESNAY", sci_tel="01 39 55 16 69"
                          # , sci_mail="marcelseban@hotmail.fr", sci_siret="155522220", indice_base="110", indice_new="115", cat=0)

    pdf_gen.generator()
