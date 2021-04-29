from tinydb import TinyDB, where, Query

class locataire:
    def __init__(self, nom, prenom, adresse, ville, tel, mail, sci, loyer, charges, cat='a'):
        self.nom = nom
        self.prenom = prenom
        self.tel = tel
        self.mail = mail
        self.sci = sci
        self.adresse = adresse
        self.ville = ville
        self.loyer = loyer
        self.charge = charges
        self.cat = cat

    def get_sci(self, sci):
        return print(f" {sci}\n xx rue lllala tralala\n 98150 les moutons bleus\n telephone\n mail")

    def get_locataire(self):
        return print(f" {self.nom} {self.prenom} \n {self.adresse} \n {self.ville}")

    def get_contact(self):
        return print(f" telephone : {self.tel} \n mail : {self.mail}")

    def save_contact(self):
        db = TinyDB('db.json')
        locataire_db = db.table('locataire')
        user = Query()
        check = locataire_db.search(user.nom == self.nom)
        if check == []:
            locataire_db.insert({"nom": self.nom, "prenom": self.prenom, "adresse": self.adresse,
                "ville": self.ville, "tel": self.tel, "mail": self.mail,
                "sci": self.sci, "loyer": self.loyer, "charges": self.charge, "cat": self.cat})
        else:
            print(f'Utilisateur {self.nom} déjà dans la base')

    def del_contact(self):
        db = TinyDB('db.json')
        locataire_db = db.table('locataire')
        user = Query()
        locataire_db.remove(user.nom == self.nom)


if __name__ == "__main__":
    mail = 'frogenmanu@hotmail.com'
    client1 = locataire('Bubu', 'prenom', 'adresse', 'ville', 'tel', mail, 'sci', 1200, 100)
    client2 = locataire('baba', 'prenom', 'adresse', 'ville', 'tel', mail, 'sci', 1200, 100, 'c')
    client3 = locataire('zaza', 'prenom', 'adresse', 'ville', 'tel', mail, 'sci', 1200, 100, 'c')
    client4 = locataire('lala', 'prenom', 'adresse', 'ville', 'tel', mail, 'sci', 1200, 100)

    client1.save_contact()
    client2.save_contact()
    client3.save_contact()
    client4.save_contact()
    #client1.del_contact()


