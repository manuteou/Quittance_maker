

class locataire:
    def __init__(self, nom, prenom, adresse, ville, tel, mail, sci, loyer, charges):
        self.nom = nom
        self.prenom = prenom
        self.tel = tel
        self.mail = mail
        self.sci = sci
        self.adresse = adresse
        self.ville = ville
        self.loyer = loyer
        self.charge = charges

    def get_sci(self, sci):
        return print(f" {sci}\n xx rue lllala tralala\n 98150 les moutons bleus\n telephone\n mail")

    def get_locataire(self):
        return print(f" {self.nom} {self.prenom} \n {self.adresse} \n {self.ville}")

    def get_contact(self):
        return print(f" telephone : {self.tel} \n mail : {self.mail}")

    def save_contact(self):
        with open ('locataire.csv','a') as f:
            f.write(f"{self.nom},{self.prenom},{self.adresse}, {self.ville},{self.tel},{self.mail},{self.sci},{loyer},{charges}\n")

    def del_contact(self):
        pass

