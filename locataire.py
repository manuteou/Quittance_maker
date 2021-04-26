

class locataire:
    def __init__(self, nom, prenom, adresse, ville, tel, mail, sci):
        self.nom = nom
        self.prenom = prenom
        self.tel = tel
        self.mail = mail
        self.sci = sci
        self.adresse = adresse
        self.ville = ville

    def get_sci(self, sci):
        return print(f" {sci}\n 19 rue laurent Gaudet\n 78150 Le Chesnay Rocquencourt")

    def get_locataire(self):
        return print(f" {self.nom} {self.prenom} \n {self.adresse} \n {self.ville}")

    def get_contact(self):
        return print(f" telephone : {self.tel} \n mail : {self.mail}")

    def save_contact(self):
        with open ('locataire.csv','a') as f:
            f.write(f"{self.nom},{self.prenom},{self.adresse},{self.ville},{self.tel},{self.mail},{self.sci}\n")

nom = "bubu"
prenom = "lulu"
adresse = "15 rue des lolo"
ville = "labas"
tel = "0105030632"
mail = "zaeazr@eaze.fr"
sci = "FFRE"

client1 = locataire(nom, prenom, adresse, ville, tel, mail, sci)

client1.get_locataire()
client1.save_contact()