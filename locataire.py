import sqlite3

class locataire:
    def __init__(self, nom, prenom, adresse, ville, tel, mail, sci, loyer, charges, cat):
        self.nom = nom
        self.prenom = prenom
        self.tel = tel
        self.mail = mail
        self.sci = sci
        self.adresse = adresse
        self.cp_ville = ville
        self.loyer = loyer
        self.charges = charges
        self.cat = cat

class sql_database():
    def __init__(self):
        self.conn = sqlite3.connect("tenatdb.db")
        self.c = self.conn.cursor()
        self.create_table_sql()

    def create_table_sql(self):
        sql_create_tenant_table = """ CREATE TABLE IF NOT EXISTS tenant(
            id integer PRIMARY KEY,
            nom text NOT NULL,
            prenom text NOT NULL,
            adresse text NOT NULL,
            CP_ville text NOT NULL,
            tel text NOT NULL,
            mail text NOT NULL,
            cat integer NOT NULL
            );"""

        sql_create_location_table = """ CREATE TABLE IF NOT EXISTS location(
            id integer PRIMARY KEY,
            SCI text NOT NULL,
            nom text NOT NULL,
            type text NOT NULL,
            loyer integer NOT NULL,
            charges integer NOT NULL
        );"""

        self.c.execute(sql_create_tenant_table)
        self.c.execute(sql_create_location_table)


    def create_entry(self, table, insert: dict):
        field_name = ""
        field_value = []
        field = ""
        table_choice = table
        for k, v in insert.items():
            field_name += str(k) + ", "
            field_value.append(v)
            field += "?, "

        field_name = field_name[:-2]
        field = field[:-2]

        sql_insert_entry = f""" INSERT INTO {table_choice}({field_name}) 
            VALUES({field})"""

        self.c.execute(sql_insert_entry, field_value)
        self.conn.commit()

    def delete_entry(self, table, entry):
        sql_delete_entry = f"""DELETE FROM {table} WHERE nom= '{entry}'"""
        self.c.execute(sql_delete_entry)
        self.conn.commit()

    def update_entry(self):
        pass

    def list_table(self, table):
        sql_list_table = f"""SELECT * FROM {table}"""
        self.c.execute(sql_list_table)
        rows = self.c.fetchall()
        return rows

    def elt_table(self, elt, table):
        sql_elt_table = f"""SELECT {elt} FROM {table} """
        self.c.execute(sql_elt_table)
        elt = self.c.fetchall()
        return elt

    def pdf_table(self):
        sql_pdf_table = """SELECT t.nom, prenom, adresse, CP_ville, SCI, loyer, charges  
                            FROM tenant as t
                            INNER JOIN location as l
                            ON t.nom = l.nom;"""
        self.c.execute(sql_pdf_table)
        pdf_table = self.c.fetchall()
        return pdf_table

if __name__ == "__main__":
    client = locataire('Bubu', 'prenom', 'adresse treze', 'ville', 'tel', 'mail', 'sci_1', 1200, 100, 1)
    db = sql_database()
    insert_tenant = {'nom': client.nom, 'prenom': client.prenom, 'adresse': client.adresse, 'CP_ville': client.cp_ville,
                  'tel': client.tel, 'mail': client.mail, 'cat': client.cat}
    insert_location = ({'SCI': client.sci, 'nom': client.nom, 'type': client.cat, 'loyer': client.loyer,
                    'charges': client.charges})

    db.create_entry("tenant", insert_tenant)
    db.create_entry("location", insert_location)
    for row in db.pdf_table():
        print (row)
