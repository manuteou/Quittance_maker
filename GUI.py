import tkinter as tk
from tkinter import ttk
from datetime import date
from locataire import locataire, sql_database
from pdf_generator import pdf_generator, make_directories
from mail_sender import send_mail
import os
from reportlab.pdfgen import canvas
import json

class main_gui(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.geometry("800x300")
        self.master.minsize(300, 150)
        self.master.title("Quittances")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")
        self.database = sql_database()
        self.createWidgets()

    def loadconfig(self):
        with open("config.json", "r") as json_file:
            config = json.load(json_file)
        return config

    def createWidgets(self):
        # variable's creation
        self.today = date.today()
        self.date_s = tk.StringVar()
        self.date_s.set(f"{self.today.day}/{self.today.month}/{self.today.year}")

        # widget's Creation
        main_frame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE)
        main_frame.columnconfigure(0, weight=0)
        main_frame.columnconfigure(1, weight=1)

        frame1 = tk.LabelFrame(self, main_frame, text="LOCATAIRES", borderwidth=2, relief=tk.GROOVE)
        frame2 = tk.Frame(self, main_frame, borderwidth=2, relief=tk.GROOVE)
        frame3 = tk.Frame(self, main_frame)
        # widgets on the left side
        self.tenant_list = tk.Listbox(frame1, selectmode=tk.SINGLE, font=("Helvetica", 15), width=600)
        for i, row in enumerate(self.database.list_table("tenant")):
            self.tenant_list.insert(i, row)
        # widgets under left
        date_s_label = tk.Label(frame2, text="Jour d'édition", borderwidth=2, padx=-1)
        date_s_entry = tk.Entry(frame2, textvariable=self.date_s, borderwidth=2, relief=tk.GROOVE)

        button_all = tk.Button(frame2, text="Créer Quittance et Envoyer pour TOUS", borderwidth=2, relief=tk.GROOVE,
                               command=self.validation_button_all)
        button_selection = tk.Button(frame2, text="Créer Quittance et Envoyer pour selection", borderwidth=2, relief=tk.GROOVE
                                     , command=self.validation_button_s)
        # widgets on right
        button_info = tk.Button(frame3, text='Info Locataire', borderwidth=2, relief=tk.GROOVE, command=self.info_entry)
        button_blk = tk.Button(frame3, state='disabled', bd=0)
        button_new = tk.Button(frame3, text='Nouvelle Entrée', borderwidth=2, relief=tk.GROOVE, command=self.new_entry)
        button_modify = tk.Button(frame3, text="Modifier un locataire", borderwidth=2, relief=tk.GROOVE, command=self.modify_entry)
        button_del = tk.Button(frame3, text="Supprimer un locataire", borderwidth=2, relief=tk.GROOVE, command=self.del_entry)

        #widgets' position
        frame1.grid(column=0, row=0, sticky='NSEW')
        frame2.grid(column=0, row=1, sticky='NSEW')
        frame3.grid(column=1, row=0)
        ##position widgets 1
        self.tenant_list.grid(column=0, row=0, rowspan=10)
        ##position widget 2
        date_s_label.grid(column=0, row=0, sticky='NW')
        date_s_entry.grid(column=0, row=0, sticky='NE')
        button_all.grid(column=0, row=10, sticky='NSEW')
        button_selection.grid(column=0, row=9, sticky='NSEW')
        ##position widgets3
        button_info.grid(column=0, row=0, sticky='NSEW')
        button_blk.grid(column=0, row=1, sticky='NSEW')
        button_new.grid(column=0, row=2, sticky='NSEW')
        button_modify.grid(column=0, row=3, sticky='NSEW')
        button_del.grid(column=0, row=4, sticky='NSEW')

    def validation_button_all(self):
        day, month, year = self.date_s.get().split("/")
        make_directories(year, month)
        directory = os.path.dirname(__file__)
        with open("config.json", "r") as json_file:
            config = json.load(json_file)

        for elt in self.database.pdf_table():
            nom, prenom, adresse, ville, sci, loyer, charges, mail, cat = elt
            path = directory + "\\" + sci + "\\" + year + "\\" + month + "\\" + nom + ".pdf"
            pdf = canvas.Canvas(path)
            pdf_gen = pdf_generator(pdf, nom, prenom, adresse, ville, sci, loyer, charges, day, month, year, cat)# Cat valeur temporaire car pas encore interger GUI
            pdf_gen.generator()
            mail = send_mail("Quittance", config["master_mail"], config["password"], mail, config["SMTP"], config["port"], path)
            mail.send()


    def validation_button_s(self):
        value = (self.tenant_list.get(tk.ACTIVE))
        day, month, year = self.date_s.get().split("/")
        make_directories(year, month)
        directory = os.path.dirname(__file__)
        with open("config.json", "r") as json_file:
            config = json.load(json_file)
        nom, prenom, adresse, ville, sci, loyer, charges, mail, cat = self.database.pdf_table_single(f'"{value[1]}"')[0]
        path = directory + "\\" + sci + "\\" + year + "\\" + month + "\\" + nom + ".pdf"
        pdf = canvas.Canvas(path)
        pdf_gen = pdf_generator(pdf, nom, prenom, adresse, ville, sci, loyer, charges, day, month, year,
                                cat)  # Cat valeur temporaire car pas encore interger GUI
        pdf_gen.generator()
        mail = send_mail("Quittance", config["master_mail"], config["password"], mail, config["SMTP"], config["port"],
                         path)
        mail.send()


    def new_entry(self):
        self.destroy()
        creation_gui().mainloop()

    def modify_entry(self):
        self.destroy()
        modification_gui().mainloop()

    def del_entry(self):
        self.destroy()
        delete_gui().mainloop()

    def info_entry(self):
        value = (self.tenant_list.get(tk.ACTIVE))[1]
        print(value)
        #info_gui()
class creation_gui(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title("Création de Locataire")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")
        self.createWidgets()
        self.database = sql_database()

    def createWidgets(self):
        # varaibles' creation
        self.nomVar = tk.StringVar()
        self.nomVar.set("Mini")
        self.prenomVar = tk.StringVar()
        self.prenomVar.set("Cooper")
        self.adresseVar = tk.StringVar()
        self.adresseVar.set("15 rue des anges")
        self.villeVar = tk.StringVar()
        self.villeVar.set("75000 Paris")
        self.telVar = tk.StringVar()
        self.telVar.set("090807060")
        self.mailVar = tk.StringVar()
        self.mailVar.set("frogenmanu@hotmail.com")
        self.sciVar = tk.StringVar()
        self.loyerVar = tk.StringVar()
        self.loyerVar.set("1500")
        self.chargesVar = tk.StringVar()
        self.chargesVar.set("200")
        self.selectorVar = tk.IntVar()
        self.selectorVar.set(1)

        # widgets' creation
        main_frame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE)
        main_frame.columnconfigure(0, weight=0)
        main_frame.columnconfigure(1, weight=1)
        nom_label = tk.Label(main_frame, text="Nom")
        prenom_label = tk.Label(main_frame, text="Prenom")
        adresse_label = tk.Label(main_frame, text="Adresse")
        ville_label = tk.Label(main_frame, text="CP_ville")
        tel_label = tk.Label(main_frame, text="Telephone")
        mail_label = tk.Label(main_frame, text="mail")

        sci_label = tk.Label(main_frame, text="SCI")

        loyer_label = tk.Label(main_frame, text="loyer")
        charges_label = tk.Label(main_frame, text="charges")



        nom_entry = tk.Entry(main_frame, textvariable=self.nomVar)
        prenom_entry = tk.Entry(main_frame, textvariable=self.prenomVar)
        adresse_entry = tk.Entry(main_frame, textvariable=self.adresseVar)
        ville_entry = tk.Entry(main_frame, textvariable=self.villeVar)
        tel_entry = tk.Entry(main_frame, textvariable=self.telVar)
        mail_entry = tk.Entry(main_frame, textvariable=self.mailVar)

        sci_choise = ttk.Combobox(main_frame, textvariable=self.sciVar)
        with open('config.json', 'r') as json_files:
            config = json.load(json_files)
        sci_choise['values'] = config['sci']
        loyer_entry = tk.Entry(main_frame, textvariable=self.loyerVar)
        charges_entry = tk.Entry(main_frame, textvariable=self.chargesVar)
        selector1 = tk.Radiobutton(main_frame, text="Particulier", variable=self.selectorVar, value=1, bd=2, relief=tk.GROOVE)
        selector2 = tk.Radiobutton(main_frame, text="Professionel", variable=self.selectorVar, value=2, bd=3, relief=tk.GROOVE)

        button = tk.Button(main_frame, text="Valider la saisie", command=self.validation_tenant) # faire un bouton system etes vous sur de vouloir ajoueter le client
        button2 = tk.Button(main_frame, text="Quitter et revenir", command=self.quit)

        # widgets' position
        main_frame.grid(column=0, row=0, sticky="NSEW")
        nom_label.grid(column=0, row=1, sticky="EW")
        nom_entry.grid(column=1, row=1, sticky="EW")
        prenom_label.grid(column=0, row=2, sticky="EW")
        prenom_entry.grid(column=1, row=2, sticky="EW")
        adresse_label.grid(column=0, row=3, sticky="EW")
        adresse_entry.grid(column=1, row=3, sticky="EW")
        ville_label.grid(column=0, row=4, sticky="EW")
        ville_entry.grid(column=1, row=4, sticky="EW")
        tel_label.grid(column=0, row=5, sticky="EW")
        tel_entry.grid(column=1, row=5, sticky="EW")
        mail_label.grid(column=0, row=6, sticky="EW")
        mail_entry.grid(column=1, row=6, sticky="EW")
        mail_label.grid(column=0, row=7, sticky="EW")
        mail_entry.grid(column=1, row=7, sticky="EW")

        sci_label.grid(column=0, row=8, sticky="EW")
        sci_choise.grid(column=1, row=8, sticky="EW")

        loyer_label.grid(column=0, row=9, sticky="EW")
        loyer_entry.grid(column=1, row=9, sticky="EW")
        charges_label.grid(column=0, row=10, sticky="EW")
        charges_entry.grid(column=1, row=10, sticky="EW")
        selector1.grid(column=0, row=0, sticky="EW")
        selector2.grid(column=1, row=0, sticky="EN")
        button.grid(column=1, columnspan=1, row=11, sticky='NSEW')
        button2.grid(column=0, columnspan=1, row=11, sticky='NSEW')

    def validation_tenant(self):
        client = locataire(self.nomVar.get(), self.prenomVar.get(), self.adresseVar.get(),
                             self.villeVar.get(), self.telVar.get(), self.mailVar.get(),
                             self.sciVar.get(), self.loyerVar.get(), self.chargesVar.get(), self.selectorVar.get())

        insert_tenant = {'nom': client.nom,  'prenom': client.prenom, 'adresse': client.adresse, 'CP_ville': client.cp_ville,
                  'tel': client.tel, 'mail': client.mail, 'cat': client.cat}

        insert_location = {'SCI': client.sci, 'nom': client.nom, 'type': client.cat, 'loyer': client.loyer,
                           'charges': client.charges}

        self.database.create_entry("tenant", insert_tenant)
        self.database.create_entry("location", insert_location)

        print(self.nomVar.get(), self.prenomVar.get(), self.adresseVar.get(), self.villeVar.get(), self.telVar.get(),
              self.mailVar.get(), self.sciVar.get(), self.loyerVar.get(), self.chargesVar.get())

    def quit(self):
        self.destroy()
        main_gui().mainloop()


class modification_gui(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title("modification de locataire")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")
        self.createWidgets()
        self.database = sql_database()

    def createWidgets(self):
        self.tenant_var = tk.StringVar()
        self.tenant_var.set("nom du locataire")
        self.champs_var = tk.StringVar()
        self.champs_var.set("champs à modifier")
        self.newval_var = tk.StringVar()
        self.newval_var.set("nouvelle valeur")
        # widget creation
        main_frame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE)
        main_frame.columnconfigure(0, weight=0)
        main_frame.columnconfigure(1, weight=1)
        tenant_label = tk.Label(main_frame, text="nom du locataire")
        tenant_entry = tk.Entry(main_frame, textvariable=self.tenant_var)
        nom_label = tk.Label(main_frame, text="champs à modifier")
        nom_entry = tk.Entry(main_frame, textvariable=self.champs_var)
        mod_label = tk.Label(main_frame, text="champs à modifier")
        mod_entry = tk.Entry(main_frame, textvariable=self.newval_var)

        button_val = tk.Button(main_frame, text="Appliquer la modification", command=self.mod_entry)
        button_back = tk.Button(main_frame, text="Quitter et revenir", command=self.quit)
        # widget position
        main_frame.grid(column=0, row=0, sticky="NSEW")
        tenant_label.grid(column=0, row=0, sticky="EW")
        tenant_entry.grid(column=1, row=0, sticky="EW")
        nom_label.grid(column=0, row=1, sticky="EW")
        nom_entry.grid(column=1, row=1, sticky="EW")
        mod_label.grid(column=0, row=2, sticky="EW")
        mod_entry.grid(column=1, row=2, sticky="EW")
        button_val.grid(column=1, row=3, sticky="NSEW")
        button_back.grid(column=0, row=3, sticky="NSEW")

    def quit(self):
        self.destroy()
        main_gui().mainloop()

    def mod_entry(self):
        self.database.modif_table(self.tenant_var.get(), self.champs_var.get(), self.newval_var.get())

class delete_gui(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title("Supression de locataire")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")
        self.createWidgets()
        self.database = sql_database()

    def createWidgets(self):
        # variable creation
        self.nom_var = tk.StringVar()
        self.nom_var.set("Attention action definitive")
        # widget creation
        main_frame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE)
        main_frame.columnconfigure(0, weight=0)
        main_frame.columnconfigure(1, weight=1)
        nom_label = tk.Label(main_frame, text="Nom du loctaire")
        nom_entry = tk.Entry(main_frame, textvariable=self.nom_var)
        button_val = tk.Button(main_frame, text="Supprimer et revenir", command=self.del_entry)
        button_back = tk.Button(main_frame, text="Quitter et revenir", command=self.quit)
        # widget position
        main_frame.grid(column=0, row=0, sticky="NSEW")
        nom_label.grid(column=0, row=0, sticky="EW")
        nom_entry.grid(column=1, row=0, sticky="EW")
        button_val.grid(column=1, row=1, sticky="NSEW")
        button_back.grid(column=0, row=1, sticky="NSEW")

    def del_entry(self):
        if self.nom_var.get() != "Attention action definitive":
            self.database.delete_entry("tenant", self.nom_var.get())
            self.database.delete_entry("location", self.nom_var.get())
            print("Action effectuée")
            self.destroy()
            main_gui().mainloop()
        else:
            print("action impossible")

    def quit(self):
        self.destroy()
        main_gui().mainloop()

class config_gui(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title("Configuration")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")
        self.createWidgets()


    def createWidgets(self):
        with open('config.json', 'r') as json_files:
            config = json.load(json_files)
        # variables
        self.master_mail_var = tk.StringVar()
        self.master_mail_var.set(config["master_mail"])
        self.password_var = tk.StringVar()
        self.password_var.set(config["password"])
        self.smtp_var = tk.StringVar()
        self.smtp_var.set(config['SMTP'])
        self.port_var = tk.StringVar()
        self.port_var.set(config["port"])

        # Widget
        main_frame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE)
        main_frame.columnconfigure(0, weight=0)
        main_frame.columnconfigure(1, weight=1)
        master_mail_label = tk.Label(main_frame, text="email du compte")
        master_mail_entry = tk.Entry(main_frame, textvariable=self.master_mail_var)
        password_label = tk.Label(main_frame, text="password du compte")
        password_entry = tk.Entry(main_frame, textvariable=self.password_var)
        smtp_label = tk.Label(main_frame, text="SMTP")
        smtp_entry = tk.Entry(main_frame, textvariable=self.smtp_var)
        port_label = tk.Label(main_frame, text="port")
        port_entry = tk.Entry(main_frame, textvariable=self.port_var)
        #boutton valider/quitter
        #button  Quitter sans valider

        #position
        main_frame.grid(column=0, row=0, sticky="NSEW")
        master_mail_label.grid(column=0, row=0, sticky="NSEW")
        master_mail_entry.grid(column=0, row=1, sticky="NSEW")
        password_label.grid(column=1, row=0, sticky="NSEW")
        password_entry.grid(column=1, row=1, sticky="NSEW")
        smtp_label.grid(column=2, row=0, sticky="NSEW")
        smtp_entry.grid(column=2, row=1, sticky="NSEW")
        port_label.grid(column=3, row=0, sticky="NSEW")
        port_entry.grid(column=3, row=1, sticky="NSEW")

    def quit(self):
        self.destroy()
        main_gui().mainloop()


if __name__ == "__main__":
    #creation_gui().mainloop()
    #modification_gui().mainloop()
    #main_gui().mainloop()
    config_gui().mainloop()