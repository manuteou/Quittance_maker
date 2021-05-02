import tkinter as tk
from datetime import date
from locataire import locataire, sql_database

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
        self.mailVar.set("azerty@ytreza.fr")
        self.sciVar = tk.StringVar()
        self.sciVar.set("LOL")
        self.loyerVar = tk.StringVar()
        self.loyerVar.set("1500")
        self.chargesVar = tk.StringVar()
        self.chargesVar.set("200")

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
        # Catégorieselecteur à faire

        nom_entry = tk.Entry(main_frame, textvariable=self.nomVar)
        prenom_entry = tk.Entry(main_frame, textvariable=self.prenomVar)
        adresse_entry = tk.Entry(main_frame, textvariable=self.adresseVar)
        ville_entry = tk.Entry(main_frame, textvariable=self.villeVar)
        tel_entry = tk.Entry(main_frame, textvariable=self.telVar)
        mail_entry = tk.Entry(main_frame, textvariable=self.mailVar)
        sci_entry = tk.Entry(main_frame, textvariable=self.sciVar)
        loyer_entry = tk.Entry(main_frame, textvariable=self.loyerVar)
        charges_entry = tk.Entry(main_frame, textvariable=self.chargesVar)

        button = tk.Button(main_frame, text="Valider la saisie", command=self.validation_tenant) # faire un bouton system etes vous sur de vouloir ajoueter le client
        button2 = tk.Button(main_frame, text="Quitter et revenir", command=self.quit)

        # widgets' position
        main_frame.grid(column=0, row=0, sticky="NSEW")
        nom_label.grid(column=0, row=0, sticky="EW")
        nom_entry.grid(column=1, row=0, sticky="EW")
        prenom_label.grid(column=0, row=1, sticky="EW")
        prenom_entry.grid(column=1, row=1, sticky="EW")
        adresse_label.grid(column=0, row=2, sticky="EW")
        adresse_entry.grid(column=1, row=2, sticky="EW")
        ville_label.grid(column=0, row=3, sticky="EW")
        ville_entry.grid(column=1, row=3, sticky="EW")
        tel_label.grid(column=0, row=4, sticky="EW")
        tel_entry.grid(column=1, row=4, sticky="EW")
        mail_label.grid(column=0, row=5, sticky="EW")
        mail_entry.grid(column=1, row=5, sticky="EW")
        mail_label.grid(column=0, row=6, sticky="EW")
        mail_entry.grid(column=1, row=6, sticky="EW")
        sci_label.grid(column=0, row=7, sticky="EW")
        sci_entry.grid(column=1, row=7, sticky="EW")
        loyer_label.grid(column=0, row=8, sticky="EW")
        loyer_entry.grid(column=1, row=8, sticky="EW")
        charges_label.grid(column=0, row=9, sticky="EW")
        charges_entry.grid(column=1, row=9, sticky="EW")

        button.grid(column=1, columnspan=1, row=10, sticky='NSEW')
        button2.grid(column=0, columnspan=1, row=10, sticky='NSEW')

    def validation_tenant(self):
        client = locataire(self.nomVar.get(), self.prenomVar.get(), self.adresseVar.get(),
                             self.villeVar.get(), self.telVar.get(), self.mailVar.get(),
                             self.sciVar.get(), self.loyerVar.get(), self.chargesVar.get())

        insert_tenant = {'nom': client.nom,  'prenom': client.prenom, 'adresse': client.adresse, 'CP_ville': client.cp_ville,
                  'tel': client.tel, 'mail': client.mail}

        insert_location = {'SCI': client.sci, 'nom': client.nom, 'type': client.cat, 'loyer': client.loyer,
                           'charges': client.charges}

        self.database.create_entry("tenant", insert_tenant)
        self.database.create_entry("location", insert_location)

        print(self.nomVar.get(), self.prenomVar.get(), self.adresseVar.get(), self.villeVar.get(), self.telVar.get(),
              self.mailVar.get(), self.sciVar.get(), self.loyerVar.get(), self.chargesVar.get())


    def quit(self):
        self.destroy()
        main_gui().mainloop()

class main_gui(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title("Quittances")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")
        self.createWidgets()


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
        tenant_list = tk.Listbox(frame1, selectmode=tk.MULTIPLE) # recuperer la list des locataires
        tenant_list.insert(1, "test")
        tenant_list.insert(2, "test2")
        tenant_list.insert(2, "test3")
        # widgets under left
        date_s_label = tk.Label(frame2, text="Jour d'édition", borderwidth=2, padx=-1, relief=tk.GROOVE)
        date_s_entry = tk.Entry(frame2, textvariable=self.date_s, borderwidth=2, relief=tk.GROOVE)

        button_all = tk.Button(frame2, text="Créer  PDF et envoyer pour tous", borderwidth=2, relief=tk.GROOVE,
                               command=self.validation_button)
        button_selection = tk.Button(frame2, text="Créer PDF et envoyer pour selection", borderwidth=2, relief=tk.GROOVE
                                     , command=self.validation_button)
        # widgets on right
        button_new = tk.Button(frame3, text='Nouvelle Entrée', borderwidth=2, relief=tk.GROOVE, command=self.new_entry)
        button_modify = tk.Button(frame3, text="Modifier un locataire", borderwidth=2, relief=tk.GROOVE, command=self.modify_entry)
        button_del = tk.Button(frame3, text="Suprimer un locataire", borderwidth=2, relief=tk.GROOVE, command=self.del_entry)

        #widgets' position
        frame1.grid(column=0, row=0, sticky='NSEW')
        frame2.grid(column=0, row=1, sticky='NSEW')
        frame3.grid(column=1, row=0)
        ##position widgets 1
        tenant_list.grid(column=0, row=0, rowspan=10)
        ##position widget 2
        date_s_label.grid(column=0, row=0, sticky='NW')
        date_s_entry.grid(column=0, row=0, sticky='NE')
        button_all.grid(column=0, row=10, sticky='NW')
        button_selection.grid(column=0, row=9, sticky='NW')
        ##position widgets3
        button_new.grid(column=0, row=0, sticky='NW')
        button_modify.grid(column=0, row=1, sticky='NW')
        button_del.grid(column=0, row=2, sticky='NW')

    def tenant_list(self):
        pass


    def validation_button(self):
        pass


    def new_entry(self):
        self.destroy()
        creation_gui().mainloop()


    def modify_entry(self):
        pass

    @classmethod
    def del_entry(cls):
        pass

class modification_gui(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title("Quittances")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")
        self.createWidgets()

    def createWidgets(self):
        pass

class config_gui(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title("Quittances")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")
        self.createWidgets()

    def createWidgets(self):
        pass

if __name__ == "__main__":
    #creation_gui().mainloop()
    main_gui().mainloop()