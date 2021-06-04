import sqlite3

class Tenant:
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


class Sci:
    def __init__(self, nom, adresse, cp_ville, tel, mail, siret, solde=0):
        self.nom = nom
        self.adresse = adresse
        self.cp_ville = cp_ville
        self.tel = tel
        self.mail = mail
        self.siret = siret
        self.solde = solde


class Shareholder:
    def __init__(self, nom, prenom, sci, part, mail):
        self.nom = nom
        self.prenom = prenom
        self.sci = sci
        self.part = part
        self.email = mail

class Sql_database_init():
    def __init__(self):
        self.conn = sqlite3.connect("tenant_db.db")
        self.c = self.conn.cursor()
        self.create_table_sql()

    def create_table_sql(self):
        sql_create_tenant_table = """ CREATE TABLE IF NOT EXISTS tenant(
               id INTEGER PRIMARY KEY,
               nom TEXT NOT NULL,
               prenom TEXT NOT NULL,
               adresse TEXT NOT NULL,
               cp_ville TEXT NOT NULL,
               tel TEXT NOT NULL,
               mail TEXT NOT NULL,
               cat INTEGER NOT NULL
               );"""

        sql_create_location_table = """ CREATE TABLE IF NOT EXISTS location(
               id INTEGER PRIMARY KEY,
               sci TEXT NOT NULL,
               nom TEXT NOT NULL,
               type TEXT NOT NULL,
               loyer REAL NOT NULL,
               base_loyer REAL NOT NULL,
               charges INTEGER NOT NULL,
               date_entree DATE NOT NULL,
               indice_base REAL NOT NULL
           );"""

        sql_create_sci_table = """CREATE TABLE IF NOT EXISTS sci(
               id INTEGER PRIMARY KEY,
               nom TEXT NOT NULL,
               adresse TEXT NOT NULL,
               cp_ville TEXT NOT NULL,
               tel TEXT NOT NULL,
               mail TEXT NOT NULL,
               siret TEXT NOT NULL,
               solde REAL,
               frais REAL
               );"""

        sql_create_shareholder_table = """ CREATE TABLE IF NOT EXISTS shareholder(
                id INTEGER PRIMARY KEY,
                nom TEXT NOT NULL,
                prenom TEXT NOT NULL,
                sci TEXT NOT NULL,
                mail TEXT NOT NULL,
                part INTEGER NOT NULL
                );"""

        sql_create_records_tenant = """ CREATE TABLE IF NOT EXISTS records_tenant(
                    id INTEGER PRIMARY KEY,
                    nom TEXT NOT NULL,
                    prenom TEXT NOT NULL,
                    sci TEXT NOT NULL,
                    loyer INTEGER NOT NULL,
                    charges INTEGER NOT NULL,
                    date DATE NOT NULL
                    );"""

        sql_create_records_shareholder = """ CREATE TABLE IF NOT EXISTS records_shareholder(
                    id INTEGER PRIMARY KEY,
                    nom TEXT NOT NULL,
                    prenom TEXT NOT NULL,
                    sci TEXT NOT NULL
                    );"""



        self.c.execute(sql_create_tenant_table)
        self.c.execute(sql_create_location_table)
        self.c.execute(sql_create_sci_table)
        self.c.execute(sql_create_shareholder_table)
        self.c.execute(sql_create_records_tenant)
        self.c.execute(sql_create_records_shareholder)


class Sql_database():
    def __init__(self):
        self.conn = sqlite3.connect("tenant_db.db")
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

    def update_entry(self, id, table, insert: dict):
        sql = ""
        for k, v in insert.items():
            sql += f"{k} = '{v}',"
        sql = sql[:-1]
        sql_update_entry = f"""UPDATE {table}
                            SET {sql} 
                            WHERE
                            id = {id}; """
        print(sql_update_entry)
        self.c.execute(sql_update_entry)
        self.conn.commit()


    def delete_entry(self, table, id):
        sql_delete_entry = f"""DELETE FROM {table} WHERE id = {id}"""
        print(sql_delete_entry)
        self.c.execute(sql_delete_entry)
        self.conn.commit()

    def elt_table(self, elt, table):
        sql_elt_table = f"""SELECT id, {elt} FROM {table} """
        self.c.execute(sql_elt_table)
        elt = self.c.fetchall()
        return elt

    def elt_table_one(self, elt, table, champs):
        sql_elt_table = f"""SELECT * FROM {table} 
                            WHERE {elt}= "{champs}";"""
        self.c.execute(sql_elt_table)
        elt = self.c.fetchall()
        return elt

    def one_elt(self, elt, table, id):
        sql_one_elt = f"""SELECT {elt} FROM {table}
                            WHERE id = {id}"""
        self.c.execute(sql_one_elt)
        elt = self.c.fetchall()
        return elt

    def pdf_table_single(self, index):
        sql_pdf_table_single = f"""SELECT  t.id, l.id,   t.nom, prenom, t.adresse, t.CP_ville, loyer, charges, t.mail, cat, s.nom, 
                                s.adresse, s.cp_ville, s.tel, s.mail, s.siret
                                FROM location as l
                                INNER JOIN tenant as t
                                ON l.id = t.id
                                INNER JOIN sci as s
                                ON l.sci = s.nom
                                WHERE t.id = {index};"""
        #print(sql_pdf_table_single)
        self.c.execute(sql_pdf_table_single)
        pdf_table = self.c.fetchall()
        return pdf_table

    def letter_request(self, index):
        sql_letter_request = f"""SELECT t.id, t.nom, prenom, t.adresse, t.cp_ville, indice_base, l.id, s.nom,
                            loyer, charges, cat, s.nom, s.adresse, s.cp_ville, s.tel, s.mail, s.siret, t.mail,
                            date_entree
                            FROM tenant as t
                            INNER JOIN location as l
                            ON t.id=l.id
                            INNER JOIN sci as s
                            ON l.sci = s.nom
                            WHERE t.id = {index};
                                                    """
        self.c.execute(sql_letter_request)
        pdf_table = self.c.fetchall()
        return pdf_table

    def test_table(self):
        sql_test_table = f"""SELECT t.id, l.id, t.nom, prenom, loyer, charges,sci, date_entree
                                FROM tenant as t
                                INNER JOIN location as l
                                ON t.id = l.id;"""
        self.c.execute(sql_test_table)
        affichage_table = self.c.fetchall()
        return affichage_table

    def info_table(self, id):
        sql_info_table = f"""SELECT t.id, prenom, adresse, cp_ville, tel, mail, sci, cat, date_entree
                                FROM tenant as t
                                INNER JOIN location as l
                                ON t.id = l.id
                                WHERE t.id = {id};"""
        self.c.execute(sql_info_table)
        affichage_table = self.c.fetchall()
        return affichage_table

    def info_sci(self, id):
        sql_info_sci = f"""SELECT *
                            FROM sci
                            WHERE id ={id}"""
        self.c.execute(sql_info_sci)
        affichage_table = self.c.fetchall()
        return affichage_table

    def modification_call(self, id):
        sql_affichage_table = f"""SELECT t.id, t.nom, prenom, t.adresse, t.CP_ville, tel, t.mail, l.sci, date_entree, loyer, charges, indice_base, cat
                                FROM tenant as t
                                INNER JOIN location as l
                                ON t.nom = l.nom
                                WHERE t.id = "{id}";"""

        self.c.execute(sql_affichage_table)
        affichage_table = self.c.fetchone()
        return affichage_table

    def maj_rent_request(self, value, index):
        sql_maj_rent_request = f"""UPDATE location 
                                        SET loyer =  '{value}'
         
                                       WHERE id = {index};"""
        print(sql_maj_rent_request)
        self.c.execute(sql_maj_rent_request)
        self.conn.commit()

    def shareholder_call(self, id):
        sql_sharholder_table = f""" SELECT * FROM shareholder
                                WHERE id = {id};"""
        self.c.execute(sql_sharholder_table)
        return self.c.fetchall()

    def shareholder_aff(self):
        sql_shareholder_aff = """SELECT id, sci, nom, prenom, part
                                FROM shareholder
                                ORDER BY sci;"""
        self.c.execute(sql_shareholder_aff)
        return self.c.fetchall()

    def sum_sci(self):
        sql_sum_sci = """SELECT id, SUM(loyer), sci
                        FROM "records_tenant"
                        GROUP BY sci;"""
        self.c.execute(sql_sum_sci)
        return self.c.fetchall()

if __name__ == "__main__":
    pass