import sqlite3

class locataire:
    def __init__(self, nom, prenom, adresse, ville, tel, mail, sci, loyer, charges, cat='a'):
        self.nom = nom
        self.prenom = prenom
        self.tel = tel
        self.mail = mail
        self.sci = sci
        self.adresse = adresse
        self.cp_ville = ville
        self.loyer = loyer
        self.charge = charges
        self.cat = cat

class sql_database():
    def __init__(self):
        self.database()
        conn = sqlite3.connect("tenatdb.db")
        self.c = conn.cursor()
        self.create_table_sql(self.c)

    def create_table_sql(self):
        sql_create_tenant_table = """ CREATE TABLE IF NOT EXISTS tenant(
            id integer PRIMARY KEY,
            name text NOT NULL,
            prenom text NOT NULL,
            adresse text NOT NULL,
            CP_ville text NOT NULL,
            tel text NOT NULL,
            mail text NOT NULL,
            SCI text NOT NULL
            ); """

        sql_create_location_table = """ CREATE TABLE IF NOT EXISTS location(
            id integer PRIMARY KEY,
            name text NOT NULL,
            type text NOT NULL,
            loyer integer NOT NULL,
            charges integer NOT NULL
        );"""

        self.c.execute(sql_create_tenant_table)
        self.c.execute(sql_create_location_table)

    def create_tenant(self, tenant_insert: dict):
        field_name = ""
        field_value = ""
        for k, v in tenant_insert:
            field_name += k + ", "
            field_value += v + ", "
        field_name = field_name[:-2]
        field_value = field_value[:-2]

        sql_insert_tenant = f""" INSERT INTO tenant({field_name}) 
            VALUES({field_value})"""
        # self.c.execute(sql_insert_tenant)
        print(sql_insert_tenant)

if __name__ == "__main__":
    client1 = locataire('Bubu', 'prenom', 'adresse', 'ville', 'tel', 'mail', 'sci_1', 1200, 100)


