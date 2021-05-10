import tkinter as tk
from tkinter import ttk
from datetime import date
from locataire import locataire, sql_database, sci
from pdf_generator import pdf_generator, make_directories
from mail_sender import send_mail
from tkinter import messagebox
import sys, json, re
from reportlab.pdfgen import canvas
from pathlib import Path

class main_gui(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.geometry("850x350")
        self.master.minsize(300, 150)
        self.master.title("Quittances Maker V1.42")
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
        self.head_list = tk.Listbox(frame1, selectmode=tk.NONE, font=("Helvetica", 15), width=600, height=1, bg="#333366",
                                      fg='white')
        self.tenant_list = tk.Listbox(frame1, selectmode=tk.SINGLE, font=("Helvetica", 15), width=600, bg="#5472AE",
                                      fg='white')
        self.head_list.insert(0, 5 * " " + "NOM" + 10 * " " + "PRENOM" + 10 * " " + "LOYER" + 5 * " " + "CHARGES" + 5 * " " +"DATE D'ENTREE")
        for i, nom in enumerate(self.database.elt_table("nom", "tenant")):
            aff_nom = self.database.affichage_table(nom[0])[0][0]
            aff_prenom = self.database.affichage_table(nom[0])[0][1]
            aff_loyer = int(self.database.affichage_table(nom[0])[0][2])
            aff_charges = self.database.affichage_table(nom[0])[0][3]
            aff_date = self.database.affichage_table(nom[0])[0][4]
            align_nom_prenom = int(round(150 / (len(aff_nom) + len(aff_prenom))))
            align_prenom_loyer = int(round(130 / (len(aff_prenom) + len(str(aff_loyer)))))
            align_loyer_charges = int(round(30 / len(str(aff_loyer)) + len(str(aff_charges))))
            align_charges_date = int(round(10 / len(str(aff_charges)) + len(aff_date)))
            self.tenant_list.insert(i + 1,  aff_nom + align_nom_prenom * " " + aff_prenom + align_prenom_loyer * " " +
                                    str(aff_loyer) + align_loyer_charges * " " + str(aff_charges) +
                                    align_charges_date * " " + aff_date + " " + self.maj_tenant(nom))
        # widgets under left
        date_s_label = tk.Label(frame2, text="Jour d'édition", borderwidth=2, padx=-1)
        date_s_entry = tk.Entry(frame2, textvariable=self.date_s, borderwidth=2, relief=tk.GROOVE)

        button_all = tk.Button(frame2, text="Créer Quittance et Envoyer pour TOUS", borderwidth=2, relief=tk.GROOVE,
                               command=self.validation_button_all)
        button_selection = tk.Button(frame2, text="Créer Quittance et Envoyer pour selection", borderwidth=2,
                                     relief=tk.GROOVE, command=self.validation_button_s)
        # widgets on right
        button_config = tk.Button(frame3, text='Config', borderwidth=2, relief=tk.GROOVE, command=self.config)
        button_blk0 = tk.Button(frame3, state='disabled', bd=0)
        button_blk1 = tk.Button(frame3, state='disabled', bd=0)
        button_info = tk.Button(frame3, text='Info Locataire', borderwidth=2, relief=tk.GROOVE, command=self.info_entry)
        button_blk2 = tk.Button(frame3, state='disabled', bd=0)
        button_new = tk.Button(frame3, text='Nouvelle Entrée', borderwidth=2, relief=tk.GROOVE, command=self.new_entry)
        button_modify = tk.Button(frame3, text="Modifier un locataire", borderwidth=2, relief=tk.GROOVE,
                                  command=self.modify_entry)
        button_del = tk.Button(frame3, text="Supprimer un locataire", borderwidth=2, relief=tk.GROOVE,
                               command=self.del_entry)
        button_rent_maj = tk.Button(frame3, text='MAJ LOYER', borderwidth=2, relief=tk.GROOVE,
                                    command=self.maj_rent)
        button_sci = tk.Button(frame3, text="Gestion SCI", borderwidth=2, relief=tk.GROOVE,
                               command=self.config_sci)
        # widgets' position
        frame1.grid(column=0, row=0, sticky='NSEW')
        frame2.grid(column=0, row=1, sticky='NSEW')
        frame3.grid(column=1, row=0)
        ##position widgets 1
        self.head_list.grid(column=0, row=0)
        self.tenant_list.grid(column=0, row=1, rowspan=10)
        ##position widget 2
        date_s_label.grid(column=0, row=0, sticky='NW')
        date_s_entry.grid(column=0, row=0, sticky='NE')
        button_all.grid(column=0, row=10, sticky='NSEW')
        button_selection.grid(column=0, row=9, sticky='NSEW')
        ##position widgets3
        button_config.grid(column=0, row=0, sticky='NSEW')
        button_rent_maj.grid(column=0, row=3, sticky='NSEW')
        button_blk0.grid(column=0, row=1, sticky='NSEW')
        button_blk1.grid(column=0, row=4, sticky='NSEW')
        button_info.grid(column=0, row=5, sticky='NSEW')
        button_blk2.grid(column=0, row=6, sticky='NSEW')
        button_new.grid(column=0, row=7, sticky='NSEW')
        button_modify.grid(column=0, row=8, sticky='NSEW')
        button_del.grid(column=0, row=9, sticky='NSEW')
        button_sci.grid(column=0, row=1, sticky='NSEW')

    def validation_button_all(self):
        print("debut de l'envoie pour tous")
        day, month, year = self.date_s.get().split("/")
        make_directories(year, month)
        if getattr(sys, 'frozen', False):
            directory = Path(sys.executable).parent
        else:
            directory = Path(__file__).parent
        print(directory)
        #directory = os.path.dirname(__file__)
        with open("config.json", "r") as json_file:
            config = json.load(json_file)
        for elt in self.database.pdf_table():
            #print(elt)
            nom, prenom, adresse, ville, loyer, charges, mail, cat, sci_nom, sci_adresse, \
            sci_cp_ville, sci_tel, sci_mail, sci_siret = elt
            path_dir = directory.joinpath(sci_nom, year, month)
            print(path_dir)
            path_dir.mkdir(parents=True, exist_ok=True)
            path = path_dir.joinpath(nom + ".pdf")
            print(path)
            pdf = canvas.Canvas(str(path))
            pdf_gen = pdf_generator(pdf, nom, prenom, adresse, ville, loyer, charges, day, month, year, cat,
                                    sci_nom, sci_adresse, sci_cp_ville, sci_tel, sci_mail, sci_siret)
            pdf_gen.generator()
            print(f"Quittance {nom} ----> crée")
            print(f"""SMTP{config["SMTP"]}""")
            mail = send_mail("Quittance", config["master_mail"], config["password"], mail, config["SMTP"],
                             config["port"], path)
            mail.send()
            print("mail : mail ----> envoyé")

        print("fin de l'envoie")
        messagebox.showinfo("Information", "Envoies effectués")


    def validation_button_s(self):
        value = (self.tenant_list.get(tk.ACTIVE))
        print(f"""debut de l"envoie pour {(value.split(" ")[0])}""")
        day, month, year = self.date_s.get().split("/")
        make_directories(year, month)
        if getattr(sys, 'frozen', False):
            directory = Path(sys.executable).parent
        else:
            directory = Path(__file__).parent
        print(directory)
        with open("config.json", "r") as json_file:
            config = json.load(json_file)
        print(self.database.pdf_table_single(f'{value.split(" ")[0]}'))
        nom, prenom, adresse, ville, loyer, charges, mail, cat, sci_nom, sci_adresse, sci_cp_ville, sci_tel, \
        sci_mail, sci_siret = self.database.pdf_table_single(f'{value.split(" ")[0]}')[0]
        path_dir = directory.joinpath(sci_nom, year, month)
        print(path_dir)
        path_dir.mkdir(parents=True, exist_ok=True)
        path = path_dir.joinpath(nom + ".pdf")

        print(path)
        pdf = canvas.Canvas(str(path))
        pdf_gen = pdf_generator(pdf, nom, prenom, adresse, ville, loyer, charges, day, month, year, cat,
                                sci_nom, sci_adresse, sci_cp_ville, sci_tel, sci_mail, sci_siret)
        print(f"Quittance {nom} ----> crée")
        pdf_gen.generator()
        mail = send_mail("Quittance", config["master_mail"], config["password"], mail, config["SMTP"],
                         config["port"], path)
        mail.send()
        print("mail : mail ----> envoyé")
        messagebox.showinfo("Information", "Envoie effectue")

    def new_entry(self):
        with open('config.json', 'r') as json_files:
            config = json.load(json_files)
        if config['sci'] == []:
            messagebox.showinfo("Attention", "Renseigner un SCI, avant de pouvoir acceder à ce menu")
            pass
        else:
            self.destroy()
            creation_gui().mainloop()

    def modify_entry(self):
        self.destroy()
        modification_gui().mainloop()

    def del_entry(self):
        self.destroy()
        delete_gui().mainloop()

    def info_entry(self):
        value = (self.tenant_list.get(tk.ACTIVE).split(" ")[0])
        info_gui(value)

    def config(self):
        self.destroy()
        config_gui().mainloop()

    def maj_rent(self):
        value = (self.tenant_list.get(tk.ACTIVE).split(" ")[0])
        self.destroy()
        maj_rent_gui(value).mainloop()

    def maj_tenant(self, nom):
        self.month = date.today().month
        month_tenant = int(self.database.affichage_table(nom[0])[0][4].split("/")[1])
        if (self.month - month_tenant) == 0:
            return "MAJ Loyer"
        else:
            return ""

    def config_sci(self):
        self.destroy()
        gestion_sci().mainloop()


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
        self.prenomVar = tk.StringVar()
        self.adresseVar = tk.StringVar()
        self.villeVar = tk.StringVar()
        self.telVar = tk.StringVar()
        self.mailVar = tk.StringVar()
        self.sciVar = tk.StringVar()
        self.loyerVar = tk.IntVar()
        self.chargesVar = tk.IntVar()
        self.selectorVar = tk.IntVar()
        self.selectorVar.set(1)
        self.date_entreeVar = tk.StringVar()
        self.indice_base = tk.IntVar()
        # Validation pack
        ok_tel = self.register(self.verification_tel)
        ok_mail = self.register(self.verification_mail)
        ok_date = self.register(self.verification_date)
        ok_loyer = self.register(self.verification_loyer)
        ok_charge = self.register(self.verification_charges)
        ok_indice = self.register(self.verification_indice)
        # widgets' creation
        main_frame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE)
        main_frame.columnconfigure(0, weight=0)
        main_frame.columnconfigure(1, weight=1)
        nom_label = tk.Label(main_frame, text="Nom")
        prenom_label = tk.Label(main_frame, text="Prenom")
        adresse_label = tk.Label(main_frame, text="Adresse")
        ville_label = tk.Label(main_frame, text="CP_ville")
        tel_label = tk.Label(main_frame, text="Telephone")
        mail_label = tk.Label(main_frame, text="Email")
        sci_label = tk.Label(main_frame, text="SCI")
        date_label = tk.Label(main_frame, text="Date d'entrée")
        loyer_label = tk.Label(main_frame, text="Loyer")
        charges_label = tk.Label(main_frame, text="Charges")
        indice_label = tk.Label(main_frame, text="Indice de base")

        nom_entry = tk.Entry(main_frame, textvariable=self.nomVar)
        prenom_entry = tk.Entry(main_frame, textvariable=self.prenomVar)
        adresse_entry = tk.Entry(main_frame, textvariable=self.adresseVar)
        ville_entry = tk.Entry(main_frame, textvariable=self.villeVar)
        tel_entry = tk.Entry(main_frame, textvariable=self.telVar, validatecommand=ok_tel, validate='focusout')
        mail_entry = tk.Entry(main_frame, textvariable=self.mailVar, validatecommand=ok_mail, validate='focusout')

        sci_choise = ttk.Combobox(main_frame, textvariable=self.sciVar, state='readonly')
        with open('config.json', 'r') as json_files:
            config = json.load(json_files)
        sci_choise['values'] = config['sci']
        date_entry = tk.Entry(main_frame, textvariable=self.date_entreeVar, validatecommand=ok_date,
                              validate='focusout')
        loyer_entry = tk.Entry(main_frame, textvariable=self.loyerVar, validatecommand=ok_loyer, validate='focusout')
        charges_entry = tk.Entry(main_frame, textvariable=self.chargesVar, validatecommand=ok_charge,
                                 validate='focusout')

        indice_entry = tk.Entry(main_frame, textvariable=self.indice_base, validatecommand=ok_indice,
                                validate='focusout')
        selector1 = tk.Radiobutton(main_frame, text="Particulier", variable=self.selectorVar, value=1, bd=2,
                                   relief=tk.GROOVE)
        selector2 = tk.Radiobutton(main_frame, text="Professionel", variable=self.selectorVar, value=2, bd=3,
                                   relief=tk.GROOVE)

        button = tk.Button(main_frame, text="Valider la saisie", command=self.validation_tenant)
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
        date_label.grid(column=0, row=9, sticky="EW")
        date_entry.grid(column=1, row=9, sticky="EW")
        loyer_label.grid(column=0, row=10, sticky="EW")
        loyer_entry.grid(column=1, row=10, sticky="EW")
        charges_label.grid(column=0, row=11, sticky="EW")
        charges_entry.grid(column=1, row=11, sticky="EW")
        indice_label.grid(column=0, row=12, sticky="EW")
        indice_entry.grid(column=1, row=12, sticky="EW")
        selector1.grid(column=0, row=0, sticky="EW")
        selector2.grid(column=1, row=0, sticky="W")
        button.grid(column=1, columnspan=1, row=13, sticky='NSEW')
        button2.grid(column=0, columnspan=1, row=13, sticky='NSEW')

    def validation_tenant(self):
        if self.nomVar.get() == "" or self.prenomVar.get() == "" or self.adresseVar.get() == ""\
            or self.villeVar.get() == "" or self.telVar.get() == ""or self.mailVar.get() == ""\
            or self.sciVar.get() == "" or self.loyerVar.get() == ""or self.chargesVar.get() == ""\
                or self.indice_base.get() == "":
            print("champs vide")
            messagebox.showinfo("Attention", "un ou plusieurs champs vides, validation impossible")
            pass

        else:
            client = locataire(self.nomVar.get(), self.prenomVar.get(), self.adresseVar.get(),
                               self.villeVar.get(), self.telVar.get(), self.mailVar.get(),
                               self.sciVar.get(), self.loyerVar.get(), self.chargesVar.get(),
                               self.selectorVar.get(), self.date_entreeVar.get(), self.indice_base.get())

            insert_tenant = {'nom': client.nom, 'prenom': client.prenom, 'adresse': client.adresse,
                             'CP_ville': client.cp_ville, 'tel': client.tel, 'mail': client.mail.lower(),
                             'cat': client.cat}

            insert_location = {'SCI': client.sci.upper(), 'nom': client.nom, 'type': client.cat,
                               'loyer': client.loyer,
                               'charges': client.charges, 'date_entree': client.date_entree,
                               'indice_base': client.base_indice}

            self.database.create_entry("tenant", insert_tenant)
            self.database.create_entry("location", insert_location)
            messagebox.showinfo("Nouvelle Entrée", "Locataire enregistré")
            print(self.nomVar.get(), self.prenomVar.get(), self.adresseVar.get(), self.villeVar.get(), self.telVar.get(),
                  self.mailVar.get(), self.sciVar.get(), self.loyerVar.get(), self.chargesVar.get())

    def quit(self):
        self.destroy()
        main_gui().mainloop()


    def verification_mail(self):

        pattern = re.compile(r"^[a-z\d].+[a-z]@[a-z\d]+.[a-z]+$")
        if re.match(pattern, self.mailVar.get()):
            print("Format du mail  correct")
            return True
        else:
            print("Format de saisie incorrect")
            messagebox.showinfo("Mail", "Saisie incorrect")
            return False

    def verification_tel(self):
        num = re.sub(r"[^\\+|\d]", "", self.telVar.get())
        pattern = re.compile(r"(\+33|^0)\d{9}$")
        print(pattern)
        if re.match(pattern, num):
            print("Format telephone valide")
            return True
        else:
            print("Format de saisie  telephone incorrect")
            messagebox.showinfo("Telephone", "Saisie incorrect")
            return False

    def verification_date(self):
        pattern = re.compile(
            r"^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$")
        if re.match(pattern, self.date_entreeVar.get()):
            print(" format date compatible")
            return True
        else:
            print("Format de saisie incorrect")
            messagebox.showinfo("Date", "Saisie incorrect")
            return False

    def verification_loyer(self):
        if isinstance(self.loyerVar.get(), str):
            print("valeur incorrect")
            messagebox.showinfo("Loyer", "Saisie incorrect")
            return False
        else:
            print("(loyer) format saisie correct")
            return True

    def verification_charges(self):
        if isinstance(self.chargesVar.get(), str):
            print("valeur incorrect")
            messagebox.showinfo("Charges", "Saisie incorrect")
            return False
        else:
            print("(saisie) format saisie correct")
            return True

    def verification_indice(self):
        if isinstance(self.indice_base.get(), str):
            print("valeur incorrect")
            messagebox.showinfo("Indice", "Saisie incorrect")
            return False
        else:
            print("(indice) format saisie correct")
            return True


class modification_gui(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title("modification de locataire")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")
        self.database = sql_database()
        self.createWidgets()


    def createWidgets(self):
        self.tenant_var = tk.StringVar()
        self.champs_var = tk.StringVar()
        self.newval_var = tk.StringVar()
        # check box
        ok_format = self.register(self.check_format)
        # widget creation
        main_frame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE)
        main_frame.columnconfigure(0, weight=0)
        main_frame.columnconfigure(1, weight=1)
        tenant_label = tk.Label(main_frame, text="nom du locataire")
        selec_entry = ttk.Combobox(main_frame, textvariable=self.tenant_var, state='readonly')
        tenant_list = self.database.elt_table("nom", "tenant")
        selec_entry['values'] = tenant_list
        nom_label = tk.Label(main_frame, text="champs à modifier")

        champs_entry = ttk.Combobox(main_frame, textvariable=self.champs_var, state='readonly')
        champs_list = ["nom", "prenom", "adresse", "cp_ville", "tel", "mail", "cat", "sci", "loyer",
                       "charges", "indice de base"]
        champs_entry['values'] = champs_list

        mod_label = tk.Label(main_frame, text="modification")
        mod_entry = tk.Entry(main_frame, textvariable=self.newval_var, validatecommand=ok_format, validate='focusout')

        button_val = tk.Button(main_frame, text="Appliquer la modification", command=self.mod_entry)
        button_back = tk.Button(main_frame, text="Quitter et revenir", command=self.quit)
        # widget position
        main_frame.grid(column=0, row=0, sticky="NSEW")
        tenant_label.grid(column=0, row=0, sticky="EW")
        selec_entry.grid(column=1, row=0, sticky="EW")
        nom_label.grid(column=0, row=1, sticky="EW")
        champs_entry.grid(column=1, row=1, sticky="EW")
        mod_label.grid(column=0, row=3, sticky="EW")
        mod_entry.grid(column=1, row=3, sticky="EW")
        button_val.grid(column=1, row=4, sticky="NSEW")
        button_back.grid(column=0, row=4, sticky="NSEW")

    def quit(self):
        self.destroy()
        main_gui().mainloop()

    def mod_entry(self):
        self.database.modif_table(self.tenant_var.get(), self.champs_var.get(),
                                  self.newval_var.get())
        print(self.tenant_var.get(), self.champs_var.get(), self.newval_var.get())
        print("modification effectuée")

    def check_format(self):
        if self.champs_var.get() == "tel":
            num = re.sub(r"\D", "", self.newval_var.get())
            pattern = re.compile(r"(\+33|^0)\d{9}$")
            print(pattern)
            if re.match(pattern, num):
                print("Format telephone valide")
                return True
            else:
                print("Format de saisie  telephone incorrect")
                messagebox.showinfo("Telephone", "Saisie incorrect")
                return False

        elif self.champs_var.get() == "mail":
            pattern = re.compile(r"^[a-z\d]+@[a-z\d]+.[a-z]+$")
            if re.match(pattern, self.newval_var.get()):
                print("Format du mail  correct")
                return True
            else:
                print("Format de saisie incorrect")
                messagebox.showinfo("mail", "Saisie incorrect")
                return False

        elif self.champs_var.get() == "date":
            pattern = re.compile(
                r"^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$")
            if re.match(pattern, self.newval_var.get()):
                print(" format date compatible")
                return True
            else:
                print("Format de saisie incorrect")
                messagebox.showinfo("date", "Saisie incorrect")
                return False

        else:
            return True

class delete_gui(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title("Supression de locataire")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")
        self.database = sql_database()
        self.createWidgets()


    def createWidgets(self):
        # variable creation
        self.nom_var = tk.StringVar()
        self.nom_var.set("Attention action definitive")
        # widget creation
        main_frame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE)
        main_frame.columnconfigure(0, weight=0)
        main_frame.columnconfigure(1, weight=1)
        nom_label = tk.Label(main_frame, text="Nom du loctaire")
        selec_entry = ttk.Combobox(main_frame, textvariable=self.nom_var, state='readonly')
        list_tenant = self.database.elt_table("nom", "tenant")
        selec_entry['values'] = list_tenant
        button_val = tk.Button(main_frame, text="Supprimer et revenir", command=self.del_entry)
        button_back = tk.Button(main_frame, text="Quitter et revenir", command=self.quit)
        # widget position
        main_frame.grid(column=0, row=0, sticky="NSEW")
        nom_label.grid(column=0, row=0, sticky="EW")
        selec_entry.grid(column=1, row=0, sticky="EW")
        button_val.grid(column=1, row=1, sticky="NSEW")
        button_back.grid(column=0, row=1, sticky="NSEW")

    def del_entry(self):
        if self.nom_var.get() != "Attention action definitive":
            self.database.delete_entry("tenant", self.nom_var.get())
            self.database.delete_entry("location", self.nom_var.get())
            print("suppression effectuée")
            messagebox.showinfo("Attention", "Supression effectuée")
            self.destroy()
            main_gui().mainloop()

    def quit(self):
        self.destroy()
        main_gui().mainloop()


class info_gui(tk.Frame):
    def __init__(self, value):
        tk.Frame.__init__(self)
        self.master.title("Information")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")
        self.nom = value
        self.database = sql_database()
        self.createWidgets()

    def createWidgets(self):
        _, _, _, adresse, ville, tel, mail, _ = self.database.elt_table_one("nom", "tenant", self.nom)[0]
        # widget label
        main_frame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE)
        label_adresse = tk.Label(main_frame, text=adresse)
        label_ville = tk.Label(main_frame, text=ville)
        label_tel = tk.Label(main_frame, text=tel)
        label_mail = tk.Label(main_frame, text=mail)
        button_back = tk.Button(main_frame, text="Quitter et revenir", command=self.quit)
        # widget position
        main_frame.grid(column=0, row=0, sticky="NSEW")
        label_adresse.grid(column=0, row=0, sticky="NSEW")
        label_ville.grid(column=0, row=1, sticky="NSEW")
        label_tel.grid(column=0, row=2, sticky="NSEW")
        label_mail.grid(column=0, row=3, sticky="NSEW")
        button_back.grid(column=0, row=4, sticky="NSEW")

    def quit(self):
        self.destroy()


class maj_rent_gui(tk.Frame):
    def __init__(self, value):
        tk.Frame.__init__(self)
        self.master.title("MAJ Loyer")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")
        self.nom = value
        self.database = sql_database()
        self.createWidgets()

    def createWidgets(self):
        # variables
        _, _, _, _, self.rent, _, _, self.base_indice = self.database.elt_table_one("nom", "location", self.nom)[0]
        self.new_indice = tk.IntVar()
        self.new_indice.set(self.base_indice)
        # widget label
        main_frame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE)
        rent_label = tk.Label(main_frame, text="Loyer")
        rent_aff = tk.Label(main_frame, text=int(self.rent))
        base_indice_lable = tk.Label(main_frame, text='Indice de base')
        base_indice_aff = tk.Label(main_frame, text=self.base_indice)
        new_indice_label = tk.Label(main_frame, text="Nouvel indice")
        new_indice_entry = tk.Entry(main_frame, textvariable=self.new_indice)
        button_blk0 = tk.Button(main_frame, state='disabled', bd=0)
        button_val = tk.Button(main_frame, text="Appliquer", command=self.validation)
        button_back = tk.Button(main_frame, text="Quitter et revenir", command=self.quit)
        # widget position
        main_frame.grid(column=0, row=0, sticky="NSEW")
        rent_label.grid(column=0, row=0, sticky="NSEW")
        base_indice_lable.grid(column=1, row=0, sticky="NSEW")
        new_indice_label.grid(column=2, row=0, sticky="NSEW")

        rent_aff.grid(column=0, row=1, sticky="NSEW")
        base_indice_aff.grid(column=1, row=1, sticky="NSEW")
        new_indice_entry.grid(column=2, row=1, sticky="NSEW")

        button_blk0.grid(column=4, row=1, sticky="NSEW")
        button_val.grid(column=3, row=1, sticky="NSEW")
        button_back.grid(column=5, row=1, sticky="NSEW")

    def quit(self):
        self.destroy()
        main_gui().mainloop()

    def validation(self):
        new_rent = int(self.rent) * (int(self.new_indice.get()) / int(self.base_indice))
        self.database.modif_table(self.nom, "loyer", new_rent)


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
            self.config = json.load(json_files)
        # variables
        self.master_mail_var = tk.StringVar()
        self.master_mail_var.set(self.config["master_mail"])
        self.password_var = tk.StringVar()
        self.password_var.set(self.config["password"])
        self.smtp_var = tk.StringVar()
        self.smtp_var.set(self.config['SMTP'])
        self.port_var = tk.StringVar()
        self.port_var.set(self.config["port"])

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
        button_validation = tk.Button(main_frame, text="Appliquer les modification", command=self.mod_entry)
        button_exit = tk.Button(main_frame, text="Quitter", command=self.quit)


        # position
        main_frame.grid(column=0, row=0, sticky="NSEW")
        master_mail_label.grid(column=0, row=0, sticky="NSEW")
        master_mail_entry.grid(column=0, row=1, sticky="NSEW")
        password_label.grid(column=1, row=0, sticky="NSEW")
        password_entry.grid(column=1, row=1, sticky="NSEW")
        smtp_label.grid(column=2, row=0, sticky="NSEW")
        smtp_entry.grid(column=2, row=1, sticky="NSEW")
        port_label.grid(column=3, row=0, sticky="NSEW")
        port_entry.grid(column=3, row=1, sticky="NSEW")
        button_validation.grid(column=0, row=3, sticky="NSEW")
        button_exit.grid(column=0, row=4, sticky="NSEW")

    def quit(self):
        self.destroy()
        main_gui().mainloop()

    def mod_entry(self):
        self.config["master_mail"] = self.master_mail_var.get()
        self.config["password"] = self.password_var.get()
        self.config['SMTP'] = self.smtp_var.get()
        self.config["port"] = self.port_var.get()
        with open('config.json', 'w') as json_files:
            json.dump(self.config, json_files)
        print("mise à jour du fichier config")
        messagebox.showinfo("Information", "Modification(s) effectuée(s)")

class gestion_sci(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title("Configuration sci")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")
        self.createWidgets()

    def createWidgets(self):
        # Widget
        main_frame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE)
        boutton_add = tk.Button(main_frame, text="Ajouter SCI", command=self.add_sci)
        boutton_mod = tk.Button(main_frame, text="Modifier SCI", command=self.mod_sci)
        boutton_sup = tk.Button(main_frame, text="Supprimer SCI", command=self.del_sci)
        boutton_quitter = tk.Button(main_frame, text="Quitter", command=self.quit)
        # position
        main_frame.grid(column=0, row=0, sticky="NSEW")
        boutton_add.grid(column=0, row=0, sticky="NSEW")
        boutton_mod.grid(column=1, row=0, sticky="NSEW")
        boutton_sup.grid(column=2, row=0, sticky="NSEW")
        boutton_quitter.grid(column=3, row=0, sticky="NSEW")

    def add_sci(self):
        new_sci_gui().mainloop()

    def mod_sci(self):
        mod_sci_gui().mainloop()

    def del_sci(self):
        del_sci_gui().mainloop()

    def quit(self):
        self.destroy()
        main_gui().mainloop()


class new_sci_gui(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title("Nouvelle sci")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")
        self.database = sql_database()
        self.createWidgets()

    def createWidgets(self):
        # Variables
        self.name_var = tk.StringVar()
        self.adresse_var = tk.StringVar()
        self.city_var = tk.StringVar()
        self.tel_var = tk.StringVar()
        self.mail_var = tk.StringVar()
        self.siret_var = tk.StringVar()
        # Widget
        main_frame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE)
        name_label = tk.Label(main_frame, text="SCI")
        adresse_label = tk.Label(main_frame, text="Adresse")
        city_label = tk.Label(main_frame, text="CP/ville")
        tel_label = tk.Label(main_frame, text="Tel")
        mail_label = tk.Label(main_frame, text="Email")
        siret_label = tk.Label(main_frame, text="SIRET")
        name_entry = tk.Entry(main_frame, textvariable=self.name_var)
        adresse_entry = tk.Entry(main_frame, textvariable=self.adresse_var)
        city_entry = tk.Entry(main_frame, textvariable=self.city_var)
        tel_entry = tk.Entry(main_frame, textvariable=self.tel_var)
        mail_entry = tk.Entry(main_frame, textvariable=self.mail_var)
        siret_entry = tk.Entry(main_frame, textvariable=self.siret_var)
        boutton_add = tk.Button(main_frame, text="Ajouter", command=self.add_sci)
        boutton_quitter = tk.Button(main_frame, text="Quitter", command=self.quit)

        # position
        main_frame.grid(column=0, row=0, sticky="NSEW")
        name_label.grid(column=0, row=0, sticky="NSEW")
        adresse_label.grid(column=0, row=1, sticky="NSEW")
        city_label.grid(column=0, row=2, sticky="NSEW")
        tel_label.grid(column=0, row=3, sticky="NSEW")
        mail_label.grid(column=0, row=4, sticky="NSEW")
        siret_label.grid(column=0, row=5, sticky="NSEW")
        name_entry.grid(column=1, row=0, sticky="NSEW")
        adresse_entry.grid(column=1, row=1, sticky="NSEW")
        city_entry.grid(column=1, row=2, sticky="NSEW")
        tel_entry.grid(column=1, row=3, sticky="NSEW")
        mail_entry.grid(column=1, row=4, sticky="NSEW")
        siret_entry.grid(column=1, row=5, sticky="NSEW")
        boutton_add.grid(column=0, row=6, sticky="NSEW")
        boutton_quitter.grid(column=1, row=6, sticky="NSEW")

    def add_sci(self):
        new_sci = sci(self.name_var.get().upper(), self.adresse_var.get(), self.city_var.get(),
                      self.tel_var.get(), self.mail_var.get(), self.siret_var.get())

        insert_sci = {'nom': new_sci.nom, 'adresse': new_sci.adresse, 'cp_ville': new_sci.cp_ville,
                      'tel': new_sci.tel, 'mail': new_sci.mail, 'siret': new_sci.siret}

        print({'nom': new_sci.nom, 'adresse': new_sci.adresse, 'cp_ville': new_sci.cp_ville,
               'tel': new_sci.tel, 'mail': new_sci.mail, 'siret': new_sci.siret})

        self.database.create_entry("sci", insert_sci)
        with open('config.json', 'r') as json_files:
            config = json.load(json_files)
        config["sci"].append(self.name_var.get())
        with open('config.json', 'w') as json_files:
            json.dump(config, json_files)
        print("sci rajouter au json")
        messagebox.showinfo("Attention", "SCI Ajoutée")

    def quit(self):
        self.destroy()
        gestion_sci.mainloop(self)


class mod_sci_gui(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title("Modification sci")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")
        self.database = sql_database()
        self.createWidgets()



    def createWidgets(self):
        self.sci_var = tk.StringVar()
        self.sci_var.set("nom de la sci à modifier")
        self.champs_var = tk.StringVar()
        self.champs_var.set("champs à modifier")
        self.newval_var = tk.StringVar()
        self.newval_var.set("nouvelle valeur")
        # widget creation
        main_frame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE)
        main_frame.columnconfigure(0, weight=0)
        main_frame.columnconfigure(1, weight=1)
        sci_label = tk.Label(main_frame, text="sci")
        selec_entry = ttk.Combobox(main_frame, textvariable=self.sci_var, state='readonly')
        sci_list = self.database.elt_table("nom", "sci")
        selec_entry['values'] = sci_list
        champs_label = tk.Label(main_frame, text="champs à modifier")
        champs_entry = ttk.Combobox(main_frame, textvariable=self.champs_var, state='readonly')
        champs_list = ['nom', 'adresse', 'cp_ville', 'tel', 'mail', 'siret']
        champs_entry['values'] = champs_list
        selec_entry['values'] = sci_list
        mod_label = tk.Label(main_frame, text="modification")
        mod_entry = tk.Entry(main_frame, textvariable=self.newval_var)

        boutton_add = tk.Button(main_frame, text="Ajouter", command=self.mod_sci)
        boutton_quitter = tk.Button(main_frame, text="Quitter", command=self.quit)
        # position
        main_frame.grid(column=0, row=0, sticky="NSEW")
        main_frame.grid(column=0, row=0, sticky="NSEW")
        sci_label.grid(column=0, row=0, sticky="EW")
        selec_entry.grid(column=1, row=0, sticky="EW")
        champs_label.grid(column=0, row=1, sticky="EW")
        champs_entry.grid(column=1, row=1, sticky="EW")
        mod_label.grid(column=0, row=2, sticky="EW")
        mod_entry.grid(column=1, row=2, sticky="EW")
        boutton_add.grid(column=0, row=6, sticky="NSEW")
        boutton_quitter.grid(column=1, row=6, sticky="NSEW")

    def mod_sci(self):
        self.database.modif_table(self.sci_var.get(), self.champs_var.get(), self.newval_var.get())
        print(self.sci_var.get(), self.champs_var.get(), self.newval_var.get())
        with open('config.json', 'r') as json_files:
            config = json.load(json_files)
            config['sci'].remove("self.sci_var.get()")
            config['sci'].append("self.newval_var.get()")
        with open('config.json', 'w') as json_files:
            json.dump(config, json_files)

        print("modifications effectuées")
        messagebox.showinfo("Attention", "SCI Ajoutée")

    def quit(self):
        self.destroy()
        gestion_sci.mainloop(self)


class del_sci_gui(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title("Supression SCI")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")
        self.database = sql_database()
        self.createWidgets()


    def createWidgets(self):
        # variable creation
        self.nom_var = tk.StringVar()
        self.nom_var.set("Attention action definitive")
        # widget creation
        main_frame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE)
        main_frame.columnconfigure(0, weight=0)
        main_frame.columnconfigure(1, weight=1)
        nom_label = tk.Label(main_frame, text="Nom de la sci")
        selec_entry = ttk.Combobox(main_frame, textvariable=self.nom_var, state='readonly')
        sci_list = self.database.elt_table("nom", "sci")
        selec_entry['values'] = sci_list
        boutton_add = tk.Button(main_frame, text="Supprimer", command=self.del_entry)
        boutton_quitter = tk.Button(main_frame, text="Quitter", command=self.quit)
        # widget position
        main_frame.grid(column=0, row=0, sticky="NSEW")
        nom_label.grid(column=0, row=0, sticky="EW")
        selec_entry.grid(column=1, row=0, sticky="EW")
        boutton_add.grid(column=0, row=6, sticky="NSEW")
        boutton_quitter.grid(column=1, row=6, sticky="NSEW")

    def del_entry(self):
        if self.nom_var.get() != "Attention action definitive":
            self.database.delete_entry("sci", self.nom_var.get())
            print("sci", self.nom_var.get())
            print("suppression effectuée")
        with open('config.json', 'r') as json_files:
            config = json.load(json_files)
        config["sci"].remove(self.nom_var.get())
        with open('config.json', 'w') as json_files:
            json.dump(config, json_files)
        print("suppression effectuée")
        messagebox.showinfo("Attention", "SCI suprimée")

    def quit(self):
        self.destroy()
        gestion_sci.mainloop(self)


if __name__ == "__main__":

    def verification_indice(value):
        if isinstance(value, str):
            print("valeur incorrect")
            # messagebox.showinfo("Attention", "Saisie incorrect")
        else:
            print("(indice) format saisie correct")



    verification_indice(15)
