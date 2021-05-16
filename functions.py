import re

class Verification:
    def __init__(self, value_to_check):
        self.value = value_to_check

    def verification_mail(self):
        pattern = re.compile(r"^[a-z\d].+[a-z]@[a-z\d]+.[a-z]+$")
        if re.match(pattern, self.value):
            print("Format du mail  correct")
            return True
        else:
            print("Format de saisie incorrect")
            #messagebox.showinfo("Mail", "Saisie incorrect")
            return False

    def verification_tel(self):
        num = re.sub(r"[^\\+|\d]", "", self.value)
        pattern = re.compile(r"(\+33|^0)\d{9}$")
        print(pattern)
        if re.match(pattern, num):
            print("Format telephone valide")
            return True
        else:
            print("Format de saisie  telephone incorrect")
            #messagebox.showinfo("Telephone", "Saisie incorrect")
            return False

    def verification_date(self):
        pattern = re.compile(
            r"^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$")
        if re.match(pattern, self.value):
            print(" format date compatible")
            return True
        else:
            print("Format de saisie incorrect")
            #messagebox.showinfo("Date", "Saisie incorrect")
            return False

    def verification_loyer(self):
        if isinstance(self.value, str):
            print("valeur incorrect")
            #messagebox.showinfo("Loyer", "Saisie incorrect")
            return False
        else:
            print("(loyer) format saisie correct")
            return True

    def verification_charges(self):
        if isinstance(self.value, str):
            print("valeur incorrect")
            #messagebox.showinfo("Charges", "Saisie incorrect")
            return False
        else:
            print("(saisie) format saisie correct")
            return True

    def verification_indice(self):
        if isinstance(self.value, str):
            print("valeur incorrect")
            #messagebox.showinfo("Indice", "Saisie incorrect")
            return False
        else:
            print("(indice) format saisie correct")
            return True
