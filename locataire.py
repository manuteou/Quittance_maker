import sqlite3

class locataire:
    def __init__(self, nom, prenom, adresse, ville, tel, mail, sci, loyer, charges, cat, date, indice):
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
        self.date_entree = date
        self.base_indice = indice

class sql_database_init():
    def __init__(self):
        self.conn = sqlite3.connect("tenatdb.db")
        self.c = self.conn.cursor()
        self.create_table_sql()

    def create_table_sql(self):
        sql_create_tenant_table = """ CREATE TABLE IF NOT EXISTS tenant(
               id INTEGER PRIMARY KEY,
               nom TEXT NOT NULL,
               prenom TEXT NOT NULL,
               adresse TEXT NOT NULL,
               CP_ville TEXT NOT NULL,
               tel TEXT NOT NULL,
               mail TEXT NOT NULL,
               cat INTEGER NOT NULL
               );"""

        sql_create_location_table = """ CREATE TABLE IF NOT EXISTS location(
               id INTEGER PRIMARY KEY,
               SCI TEXT NOT NULL,
               nom TEXT NOT NULL,
               type TEXT NOT NULL,
               loyer INTEGER NOT NULL,
               charges INTEGER NOT NULL,
               date_entree DATE NOT NULL,
               indice_base INTEGER NOT NULL
           );"""

        sql_create_sci_table = """CREATE TABLE IF NOT EXISTS sci(
               id INTEGER PRIMARY KEY,
               nom TEXT NOT NULL,
               adresse TEXT NOT NULL,
               CP_ville TEXT NOT NULL,
               tel TEXT NOT NULL,
               mail TEXT NOT NULL,
               SIRET TEXT NOT NULL);"""

        self.c.execute(sql_create_tenant_table)
        self.c.execute(sql_create_location_table)
        self.c.execute(sql_create_sci_table)

class sql_database():
    def __init__(self):
        self.conn = sqlite3.connect("tenatdb.db")
        self.c = self.conn.cursor()

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

    def elt_table_one(self, elt, table, champs):
        sql_elt_table = f"""SELECT * FROM {table} 
                            WHERE {elt}= "{champs}";"""
        self.c.execute(sql_elt_table)
        elt = self.c.fetchall()
        return elt

    def pdf_table(self):
        sql_pdf_table = """SELECT t.nom, prenom, adresse, CP_ville, SCI, loyer, charges, mail , cat
                            FROM tenant as t
                            INNER JOIN location as l
                            ON t.nom = l.nom;"""
        self.c.execute(sql_pdf_table)
        pdf_table = self.c.fetchall()
        return pdf_table

    def pdf_table_single(self, nom):
        sql_pdf_table_single = f"""SELECT t.nom, prenom, adresse, CP_ville, SCI, loyer, charges, mail , cat
                            FROM tenant as t
                            INNER JOIN location as l
                            ON t.nom = l.nom
                            WHERE t.nom = {nom};"""
        self.c.execute(sql_pdf_table_single)
        pdf_table = self.c.fetchall()
        return pdf_table

    def affichage_table(self, nom):
        sql_affichage_table = f"""SELECT t.nom, prenom, loyer, charges, date_entree 
                                FROM tenant as t
                                INNER JOIN location as l
                                ON t.nom = l.nom
                                WHERE t.nom = "{nom}";"""
        self.c.execute(sql_affichage_table)
        affichage_table = self.c.fetchall()
        return affichage_table

    def modif_table(self, nom, champs, valeur):
        if (champs == 'loyer') or (champs == 'charges'):
            table = "location"
            sql_table_modif = f"""UPDATE {table}
                                SET {champs} = {valeur}
                                WHERE nom = '{nom}';"""
            print(sql_table_modif)

        else:
            for table in ["tenant", "location"]:
                sql_table_modif = f"""UPDATE {table}
                                    SET {champs} = '{valeur}'
                                     WHERE nom = '{nom}';"""
                try:
                    self.c.execute(sql_table_modif)
                except:
                    pass
        self.c.execute(sql_table_modif)
        self.conn.commit()

if __name__ == "__main__":

    db = sql_database()
    print(db.elt_table_one("nom","tenant", "Mini")[0])

