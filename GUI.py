import tkinter as tk
from tkinter import ttk
from datetime import date
from locataire import locataire, sql_database, sci
from pdfgenerator import PdfGenerator
from mail_sender import send_mail
from tkinter import messagebox
import sys, json, re, threading, time
from reportlab.pdfgen import canvas
from pathlib import Path

class SplashScreen(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        height, width = self.get_display_size()
        height = int(height/2.5)
        width = int(width/2.5)
        self.master.geometry(f"850x350+{width}+{height}")
        self.master.overrideredirect(True)
        self.master.configure(bg='#1A5276')
        self.splash_screen()
        self.combostyle = ttk.Style()
        self.combostyle.theme_create('custom.TCombobox', parent='clam',
                                     settings={'custom.TCombobox':
                                                   {'configure':
                                                        {'selectbackground': '#4F7292',
                                                         'fieldbackground': '#4F7292',
                                                         'background': '#4F7292',
                                                         'fontground': 'white'

                                                         }}}
                                     )
        self.pack(expand=True)

    def splash_screen(self):
        splash_frame = tk.Frame(self)
        splash_label = tk.Label(splash_frame, text="  QUITTANCE MAKER  ", font=('Courier', 40, "bold"), bg="#1A5276", fg="#74D0F1")
        splash_label2 = tk.Label(splash_frame, text="\nfaciliter la gestion de vos locataires", font=(
            'Courier', 20, "bold"), bg="#1A5276", fg="#74D0F1")
        splash_frame.pack()
        splash_label.pack(expand=True)
        splash_label2.pack()

        self.after(2500, self.quit)

    def get_display_size(self):
        root = tk.Tk()
        root.update_idletasks()
        root.attributes('-fullscreen', True)
        root.state('iconic')
        height = root.winfo_screenheight()
        width = root.winfo_screenwidth()
        root.destroy()
        return height, width

    def quit(self):
        self.destroy()
        MainGui().mainloop()


class MainGui(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.geometry("1050x350")
        self.master.overrideredirect(False)
        self.master.minsize(300, 150)
        self.master.title("Quittances Maker V1.5")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")
        self.database = sql_database()
        # variable's creation
        self.today = date.today()
        self.date_s = tk.StringVar()
        self.date_s.set(f"{self.today.day}/{self.today.month}/{self.today.year}")

        # widget's Creation
        main_frame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE, bg="#1A5276")
        main_frame.columnconfigure(0, weight=0)
        main_frame.columnconfigure(1, weight=1)

        frame1 = tk.LabelFrame(self, main_frame, text="LOCATAIRES", font=('Courier', 14, "bold"), fg='#74D0F1', borderwidth=4, relief=tk.GROOVE,  bg="#1A5276")
        frame2 = tk.Frame(self, main_frame, borderwidth=2, relief=tk.GROOVE, bg="#1A5276")
        frame3 = tk.Frame(self, main_frame, bg="#1A5276")
        frame1.grid(column=0, row=0, sticky='NSEW')
        frame2.grid(column=0, row=1, sticky='NSEW')
        frame3.grid(column=1, row=0, rowspan=2, sticky='NSEW')
        # widgets menu

        # widgets on the left side
        #
        head_nom = tk.Label(frame1, text="NOM", font=('Courier', 14, "bold"), fg='#74D0F1',  bg="#1A5276")
        head_nom.grid(column=0, row=0, sticky='W', padx=10)
        head_prenom = tk.Label(frame1, text="PRENOM", font=('Courier', 14, "bold"), fg='#74D0F1',  bg="#1A5276")
        head_prenom.grid(column=1, row=0, sticky='W', padx=10)
        head_loyer = tk.Label(frame1, text="LOYER", font=('Courier', 14, "bold"), fg='#74D0F1',  bg="#1A5276")
        head_loyer.grid(column=2, row=0, sticky='W', padx=10)
        head_charges = tk.Label(frame1, text="CHARGES", font=('Courier', 14, "bold"), fg='#74D0F1',  bg="#1A5276")
        head_charges.grid(column=3, row=0, sticky='W', padx=10)
        head_info = tk.Label(frame1, text="INFO", font=('Courier', 14, "bold"), fg='#74D0F1',  bg="#1A5276")
        head_info.grid(column=4, row=0, sticky='W', padx=10)
        head_info = tk.Label(frame1, text="STATUT", font=('Courier', 14, "bold"), fg='#74D0F1', bg="#1A5276")
        head_info.grid(column=5, row=0, sticky='W', padx=2)

        self.nom_list = tk.Listbox(frame1, selectmode=tk.MULTIPLE, font=("Times", 12), bg="#1A5276", fg='white', borderwidth=0, relief=tk.FLAT, width=15, highlightthickness=0)
        for i, e in enumerate(self.database.elt_table("nom", "tenant")):
            self.nom_list.insert(tk.END, e[0])
        self.nom_list.grid(column=0, row=1, padx=12)

        self.prenom_list = tk.Listbox(frame1, selectmode=tk.NONE, font=("Times", 12), bg="#1A5276", fg='white', borderwidth=0, width=15, selectbackground="#5472AE",highlightthickness=0, relief=tk.FLAT)
        for i, e in enumerate(self.database.elt_table("prenom", "tenant")):
            self.prenom_list.insert(tk.END, e[0])
        self.prenom_list.grid(column=1, row=1, padx=15)

        self.loyer_list = tk.Listbox(frame1, selectmode=tk.NONE, font=("Times", 12), bg="#1A5276", fg='white',borderwidth=0, width=15, selectbackground="#5472AE", highlightthickness=0, relief=tk.FLAT)
        for i, e in enumerate(self.database.elt_table("loyer", "location")):
            self.loyer_list.insert(tk.END, e[0])
        self.loyer_list.grid(column=2, row=1, padx=20)

        self.charges_list = tk.Listbox(frame1, selectmode=tk.NONE, font=("Times", 12), bg="#1A5276", fg='white',borderwidth=0, width=15, selectbackground="#5472AE",highlightthickness=0, relief=tk.FLAT)
        for i, e in enumerate(self.database.elt_table("charges", "location")):
            self.charges_list.insert(tk.END, e[0])
        self.charges_list.grid(column=3, row=1, padx=30)

        self.info_list = tk.Listbox(frame1, selectmode=tk.NONE, font=("Times", 12), bg="#1A5276", fg='red', borderwidth=0, width=15, selectbackground="#5472AE", highlightthickness=0, relief=tk.FLAT)
        for i, e in enumerate(self.database.elt_table("nom", "tenant")):

            self.info_list.insert(tk.END, self.info_tenant(e))
        self.info_list.grid(column=4, row=1,  padx=12)

        self.info_list = tk.Listbox(frame1, selectmode=tk.NONE, font=("Times", 12), bg="#1A5276", fg='white',
                                    borderwidth=0, width=15, selectbackground="#5472AE", highlightthickness=0,
                                    relief=tk.FLAT)
        for i, e in enumerate(self.database.elt_table("nom", "tenant")):
            self.info_list.insert(tk.END, "X")
        self.info_list.grid(column=5, row=1, padx=20)

        # widgets under
        date_s_label = tk.Label(frame2, text="Jour d'édition", borderwidth=2, padx=-1, bg="#1A5276",  font=('Courier', 10, "bold"), fg='#74D0F1')
        date_s_label.grid(column=0, row=0, sticky='NW')

        date_s_entry = tk.Entry(frame2, textvariable=self.date_s, borderwidth=2, relief=tk.GROOVE, bg="#4F7292", bd=0, font=('Courier', 10, "bold"), fg="white")
        date_s_entry.grid(column=1, row=0, sticky='NE')

        button_all = tk.Button(frame2, text=" ENVOIE TOUS", borderwidth=2, relief=tk.GROOVE, bg="#3D4A56", font=('Courier', 9, "bold"), fg='#74D0F1', command=self.validation_all_tenant)
        button_all.grid(column=0, row=10, sticky='NSEW')

        button_selection = tk.Button(frame2, text="ENVOIE SELECTION", borderwidth=2, bg="#3D4A56",font=('Courier', 9, "bold"), fg='#74D0F1', relief=tk.GROOVE, command=self.validation_select_tenant)
        button_selection.grid(column=0, row=9, sticky='NSEW')

        # Progress bar
        self.bar_send = ttk.Progressbar(frame2, mode="determinate")
        self.bar_send.grid(column=1, row=10)


        # widgets on right
        button_config = tk.Button(frame3, text='CONFIG', borderwidth=2, relief=tk.GROOVE, command=self.config, bg="#3D4A56", fg='#74D0F1', font=('Courier', 14, "bold"))
        button_config.grid(column=0, row=0, sticky='NSEW')

        button_blk0 = tk.Button(frame3, state='disabled', bd=0, bg="#1A5276")
        button_blk0.grid(column=0, row=1, sticky='NSEW')

        self.menu_sci = tk.StringVar()
        menu_sci_list = ["création", "modification", "suppression"]
        self.menu_sci.set("SCI")
        SciMenu = tk.OptionMenu(frame3, self.menu_sci, *menu_sci_list, command=self.sci_menu_selection)
        SciMenu.configure(bg="#3D4A56",  font=('Courier', 14, "bold"), fg='#74D0F1', bd=0)
        SciMenu.grid(column=0, row=2, sticky='NSEW')

        button_blk1 = tk.Button(frame3, state='disabled', bd=0, bg="#1A5276")
        button_blk1.grid(column=0, row=3, sticky='NSEW')

        # menu tenant
        self.menu_tenant = tk.StringVar()
        menu_tenant_list = ["info", "création", "modification", "supression"]
        self.menu_tenant.set("LOCATAIRE")
        tenantMenu = tk.OptionMenu(frame3, self.menu_tenant, *menu_tenant_list, command=self.tenant_menu_selection)
        tenantMenu.configure(bg="#3D4A56", fg='#74D0F1', font=('Courier', 14, "bold"), bd=0)
        tenantMenu.grid(column=0, row=4, sticky='NSEW')

        button_blk2 = tk.Button(frame3, state='disabled', bd=0, bg="#1A5276")
        button_blk2.grid(column=0, row=5, sticky='NSEW')

        self.menu_index = tk.StringVar()
        menu_index_list = ["Lettre", "MAJ Loyer"]
        self.menu_index.set("INDEXATION")
        indexMenu = tk.OptionMenu(frame3, self.menu_index, *menu_index_list, command=self.index_menu_selection)
        indexMenu.configure(bg="#3D4A56", fg='#74D0F1', font=('Courier', 14, "bold"), bd=0)
        indexMenu.grid(column=0, row=6, sticky='NSEW')

        button_blk3 = tk.Button(frame3, state='disabled', bd=0, bg="#1A5276")
        button_blk3.grid(column=0, row=7, sticky='NSEW')

        button_blk4 = tk.Button(frame3, state='disabled', bd=0, bg="#1A5276")
        button_blk4.grid(column=0, row=8, sticky='NSEW')

        button_blk5 = tk.Button(frame3, state='disabled', bd=0, bg="#1A5276")
        button_blk5.grid(column=0, row=9, sticky='NSEW')

        button_end = tk.Button(frame3, text="FERMER", borderwidth=2, relief=tk.GROOVE,
                               command=self.closing, bg="#3D4A56", fg='#74D0F1', font=('Courier', 14, "bold"), bd=0)
        button_end.grid(column=0, row=10, sticky='NSEW')


    def closing(self):
        self.master.destroy()

    def progress_bar(self):
        self.bar_send.start(5)
        time.sleep(1)
        self.bar_send.stop()

    @staticmethod
    def config_data():
        with open("config.json", "r") as json_file:
            return json.load(json_file)

    @staticmethod
    def directory():
        if getattr(sys, 'frozen', False):
            directory = Path(sys.executable).parent
        else:
            directory = Path(__file__).parent
        return directory

    def validation_all_tenant(self):
        directory = self.directory()
        config = self.config_data()
        for elt in self.database.affichage_table_all():
            thread = threading.Thread(target=self.progress_bar)
            thread.start()
            result = ""
            for i in elt:
                result += str(f"{i}   ")
            self.creation_pdf(result, directory, config)
        messagebox.showinfo("Information", "Envoies effectués")

    def validation_select_tenant(self):
        elt = (self.nom_list.curselection())
        list_selected = []
        for i in elt:
            for n, e in enumerate(self.database.elt_table("nom", "tenant")):
                if n == i:
                    list_selected.append(e[0])
        directory = self.directory()
        config = self.config_data()
        for elt in list_selected:
            thread = threading.Thread(target=self.progress_bar)
            thread.start()
            self.creation_pdf(elt, directory, config)
        messagebox.showinfo("Information", "Envoie effectué")

    def creation_pdf(self, tenant, directory, config):
        day, month, year = self.date_s.get().split("/")
        nom, prenom, adresse, ville, loyer, charges, mail, cat, sci_nom, sci_adresse, sci_cp_ville, sci_tel, \
            sci_mail, sci_siret = self.database.pdf_table_single(f'{tenant.split("  ")[0]}')[0]
        path_dir = directory.joinpath(sci_nom, year, month)
        path_dir.mkdir(parents=True, exist_ok=True)
        path = path_dir.joinpath(nom + ".pdf")
        pdf = canvas.Canvas(str(path))
        pdf_gen = PdfGenerator(pdf, nom, prenom, adresse, ville, loyer, charges, day, month, year, cat, sci_nom,
                               sci_adresse, sci_cp_ville, sci_tel, sci_mail, sci_siret)
        pdf_gen.generator()
        print(config["master_mail"], config["password"], mail, config["SMTP"],
              config["port"], path)
        mail = send_mail("Quittance", config["master_mail"], config["password"], mail, config["SMTP"],
                         config["port"], path)
        mail.send()

    def config(self):
        self.destroy()
        ConfigGUI().mainloop()

    def info_tenant(self, nom):
        month = date.today().month
        month_tenant = int(self.database.affichage_table(nom[0])[0][4].split("/")[1])
        if (month - month_tenant) == 0:
            return "Loyer indexation"
        elif (month - month_tenant) == -1:

            return "lettre d'indexation"
        else:
            return ""
    def statut(self):
        pass

    # Main Menus
    def index_menu_selection(self, v):
        if self.menu_index.get() == 'Lettre':
            self.destroy()
            LetterGui().mainloop()

        elif self.menu_index.get()== 'MAJ Loyer':
            self.destroy()
            MajRentGui().mainloop()

    def tenant_menu_selection(self, v):
        if self.menu_tenant.get() == 'info':
            self.destroy()
            InfoGui().mainloop()
        elif self.menu_tenant.get() == 'création':
            with open('config.json', 'r') as json_files:
                config = json.load(json_files)
            if not config['sci']:
                messagebox.showinfo("Attention", "Renseigner un SCI, avant de pouvoir acceder à ce menu")
                pass
            else:
                self.destroy()
                CreationGui().mainloop()
        elif self.menu_tenant.get() == 'modification':
            self.destroy()
            ModificationGui().mainloop()
        elif self.menu_tenant.get() == 'supression':
            self.destroy()
            DeleteGui().mainloop()

    def sci_menu_selection(self, v):
        if self.menu_sci.get() == "création":
            self.destroy()
            NewSciGUI().mainloop()
        if self.menu_sci.get() == "modification":
            self.destroy()
            ModSciGui().mainloop()
        if self.menu_sci.get() == "suppression":
            self.destroy()
            DelSciGui().mainloop()



class CreationGui(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title("Création de Locataire")
        self.master.geometry("350x350")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")
        self.combostyle = ttk.Style()
        self.combostyle.theme_use('custom.TCombobox')
        self.database = sql_database()
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
        main_frame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE, bg="#1A5276")
        main_frame.columnconfigure(0, weight=0)
        main_frame.columnconfigure(1, weight=1)
        nom_label = tk.Label(main_frame, text="Nom", font=('Courier', 9, "bold"), bg="#1A5276", fg="#74D0F1")
        prenom_label = tk.Label(main_frame, text="Prenom", font=('Courier', 9, "bold"), bg="#1A5276", fg="#74D0F1")
        adresse_label = tk.Label(main_frame, text="Adresse", font=('Courier', 9, "bold"), bg="#1A5276", fg="#74D0F1")
        ville_label = tk.Label(main_frame, text="CP_ville", font=('Courier', 9, "bold"), bg="#1A5276", fg="#74D0F1")
        tel_label = tk.Label(main_frame, text="Telephone", font=('Courier', 9, "bold"), bg="#1A5276", fg="#74D0F1")
        mail_label = tk.Label(main_frame, text="Email", font=('Courier', 9, "bold"), bg="#1A5276", fg="#74D0F1")
        sci_label = tk.Label(main_frame, text="SCI", font=('Courier', 9, "bold"), bg="#1A5276", fg="#74D0F1")
        date_label = tk.Label(main_frame, text="Date d'entrée", font=('Courier', 9, "bold"), bg="#1A5276", fg="#74D0F1")
        loyer_label = tk.Label(main_frame, text="Loyer", font=('Courier', 9, "bold"), bg="#1A5276", fg="#74D0F1")
        charges_label = tk.Label(main_frame, text="Charges", font=('Courier', 9, "bold"), bg="#1A5276", fg="#74D0F1")
        indice_label = tk.Label(main_frame, text="Indice", font=('Courier', 9, "bold"), bg="#1A5276", fg="#74D0F1")

        nom_entry = tk.Entry(main_frame, textvariable=self.nomVar, bg="#4F7292", fg='white')
        prenom_entry = tk.Entry(main_frame, textvariable=self.prenomVar, bg="#4F7292", fg='white')
        adresse_entry = tk.Entry(main_frame, textvariable=self.adresseVar, bg="#4F7292", fg='white')
        ville_entry = tk.Entry(main_frame, textvariable=self.villeVar, bg="#4F7292", fg='white')
        tel_entry = tk.Entry(main_frame, textvariable=self.telVar, validatecommand=ok_tel, validate='focusout', bg="#4F7292", fg='white')
        mail_entry = tk.Entry(main_frame, textvariable=self.mailVar, validatecommand=ok_mail, validate='focusout', bg="#4F7292", fg='white')

        sci_choise = ttk.Combobox(main_frame, textvariable=self.sciVar, state='readonly', style='custom.TCombobox')
        with open('config.json', 'r') as json_files:
            config = json.load(json_files)
        sci_choise['values'] = config['sci']
        date_entry = tk.Entry(main_frame, textvariable=self.date_entreeVar, validatecommand=ok_date,
                              validate='focusout', bg="#4F7292")
        loyer_entry = tk.Entry(main_frame, textvariable=self.loyerVar, validatecommand=ok_loyer, validate='focusout', bg="#4F7292", fg='white')
        charges_entry = tk.Entry(main_frame, textvariable=self.chargesVar, validatecommand=ok_charge,
                                 validate='focusout', bg="#4F7292", fg='white')

        indice_entry = tk.Entry(main_frame, textvariable=self.indice_base, validatecommand=ok_indice,
                                validate='focusout', bg="#4F7292", fg='white')
        selector1 = tk.Radiobutton(main_frame, text="Particulier", variable=self.selectorVar, value=1, bd=0,
                                   relief=tk.FLAT,  bg="#1A5276", fg='#74D0F1', font=('Courier', 9))
        selector2 = tk.Radiobutton(main_frame, text="Professionel", variable=self.selectorVar, value=2, bd=0,
                                   relief=tk.FLAT,  bg="#1A5276", fg='#74D0F1', font=('Courier', 9))

        button = tk.Button(main_frame, text="VALIDER", command=self.validation_tenant, bg="#3D4A56", fg='#74D0F1', font=('Courier', 9, "bold"), bd=0, relief=tk.GROOVE)
        button2 = tk.Button(main_frame, text="RETOUR", command=self.quit, bg="#3D4A56", fg='#74D0F1', font=('Courier', 9, "bold"), bd=0, relief=tk.GROOVE)

        # widgets' position
        main_frame.grid(column=0, row=0, sticky="NSEW")
        nom_label.grid(column=0, row=1, sticky="EW")
        nom_entry.grid(column=1, row=1, columnspan=2, sticky="EW")
        prenom_label.grid(column=0, row=2, sticky="EW")
        prenom_entry.grid(column=1, row=2, columnspan=2, sticky="EW")
        adresse_label.grid(column=0, row=3, sticky="EW")
        adresse_entry.grid(column=1, row=3, columnspan=2, sticky="EW")
        ville_label.grid(column=0, row=4, sticky="EW")
        ville_entry.grid(column=1, row=4, columnspan=2, sticky="EW")
        tel_label.grid(column=0, row=5, sticky="EW")
        tel_entry.grid(column=1, row=5, columnspan=2, sticky="EW")
        mail_label.grid(column=0, row=6, sticky="EW")
        mail_entry.grid(column=1, row=6, columnspan=2, sticky="EW")
        mail_label.grid(column=0, row=7, sticky="EW")
        mail_entry.grid(column=1, row=7, columnspan=2, sticky="EW")

        sci_label.grid(column=0, row=8, sticky="EW")
        sci_choise.grid(column=1, row=8, columnspan=2, sticky="EW")
        date_label.grid(column=0, row=9, sticky="EW")
        date_entry.grid(column=1, row=9, columnspan=2, sticky="EW")
        loyer_label.grid(column=0, row=10, sticky="EW")
        loyer_entry.grid(column=1, row=10, columnspan=2, sticky="EW")
        charges_label.grid(column=0, row=11, sticky="EW")
        charges_entry.grid(column=1, row=11, columnspan=2, sticky="EW")
        indice_label.grid(column=0, row=12, sticky="EW")
        indice_entry.grid(column=1, row=12, columnspan=2, sticky="EW")
        selector1.grid(column=1, row=0, sticky="NSEW", padx=1)
        selector2.grid(column=2, row=0, sticky="NSEW", padx=1)
        button.grid(column=2, row=13, sticky='NSEW', padx=1)
        button2.grid(column=1, row=13, sticky='NSEW', padx=1)

    def validation_tenant(self):
        if self.nomVar.get() == "" or self.prenomVar.get() == "" or self.adresseVar.get() == "" \
                or self.villeVar.get() == "" or self.telVar.get() == "" or self.mailVar.get() == "" \
                or self.sciVar.get() == "" or self.loyerVar.get() == "" or self.chargesVar.get() == "" \
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

            insert_location = {'SCI': client.sci.upper(), 'nom': client.nom, 'type': client.cat,'loyer': client.loyer,
                                'base_loyer': client.loyer, 'charges': client.charges, 'date_entree': client.date_entree
                                , 'indice_base': client.base_indice}

            self.database.create_entry("tenant", insert_tenant)
            self.database.create_entry("location", insert_location)
            messagebox.showinfo("Nouvelle Entrée", "Locataire enregistré")
            print(self.nomVar.get(), self.prenomVar.get(), self.adresseVar.get(), self.villeVar.get(),
                  self.telVar.get(),
                  self.mailVar.get(), self.sciVar.get(), self.loyerVar.get(), self.chargesVar.get())

    def quit(self):
        self.destroy()
        MainGui().mainloop()

    def verification_mail(self):
        Verification(self.mailVar.get()).verification_mail()

    def verification_tel(self):
        Verification(self.telVar.get()).verification_tel()

    def verification_date(self):
        Verification(self.date_entreeVar.get()).verification_date()

    def verification_loyer(self):
        Verification(self.loyerVar.get()).verification_loyer()

    def verification_charges(self):
        Verification(self.chargesVar.get()).verification_charges()

    def verification_indice(self):
        Verification(self.indice_base.get()).verification_indice()


class ModificationGui(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title("modification de locataire")
        self.master.geometry("350x350")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")
        self.combostyle = ttk.Style()
        self.combostyle.theme_use('custom.TCombobox')
        self.database = sql_database()
        # variables
        self.tenant_var = tk.StringVar()
        self.champs_var = tk.StringVar()
        self.newval_var = tk.StringVar()
        self.old_var = tk.StringVar()
        self.old_var.set("En Attente de la selection")
        # tracing
        self.champs_var.trace("w", self.observer)
        # check box
        ok_format = self.register(self.check_format)
        # widget creation
        main_frame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE, bg="#1A5276")
        main_frame.grid(column=0, row=0, sticky="NSEW")

        tenant_label = tk.Label(main_frame, text="nom du locataire", font=('Courier', 9, "bold"), bg="#1A5276", fg="#74D0F1")
        tenant_label.grid(column=0, row=0, sticky="EW")

        selec_entry = ttk.Combobox(main_frame, textvariable=self.tenant_var, state='readonly', style='custom.TCombobox')
        selec_entry.grid(column=1, row=0, sticky="EW")

        tenant_list = self.database.elt_table("nom", "tenant")
        selec_entry['values'] = tenant_list
        nom_label = tk.Label(main_frame, text="champs à modifier", font=('Courier', 9, "bold"), bg="#1A5276", fg="#74D0F1")
        nom_label.grid(column=0, row=1, sticky="EW")

        champs_entry = ttk.Combobox(main_frame, textvariable=self.champs_var, state='readonly', style='custom.TCombobox')
        champs_list = ["nom", "prenom", "adresse", "cp_ville", "tel", "mail", "cat", "sci", "loyer",
                       "charges", "indice de base"]
        champs_entry['values'] = champs_list
        champs_entry.grid(column=1, row=1, sticky="EW")

        old_label = tk.Label(main_frame, text="Valeur actuelle", font=('Courier', 9, "bold"), bg="#1A5276", fg="#74D0F1")
        old_label.grid(column=0, row=4, sticky="EW")

        old_data = tk.Label(main_frame, textvariable=self.old_var, font=('Courier', 9, "bold"), bg="#1A5276", fg="#74D0F1")
        old_data.grid(column=1, row=4, sticky="EW")

        mod_label = tk.Label(main_frame, text="modification", font=('Courier', 9, "bold"), bg="#1A5276", fg="#74D0F1")
        mod_label.grid(column=0, row=3, sticky="EW")

        mod_entry = tk.Entry(main_frame, textvariable=self.newval_var, validatecommand=ok_format, validate='focusout',
                             bg="#4F7292", fg='red')
        mod_entry.grid(column=1, row=3, sticky="EW")

        blank_label = tk.Label(main_frame, bg="#1A5276")
        blank_label.grid(column=1, row=5)

        button_val = tk.Button(main_frame, text="Appliquer la modification", command=self.mod_entry, bg="#3D4A56",
                               fg='#74D0F1', font=('Courier', 9, "bold"), bd=0, relief=tk.GROOVE)
        button_val.grid(column=1, row=6, sticky="NSEW")

        blank_label = tk.Label(main_frame, bg="#1A5276")
        blank_label.grid(column=1, row=7)

        button_back = tk.Button(main_frame, text="Quitter et revenir", command=self.quit, bg="#3D4A56", fg='#74D0F1',
                                font=('Courier', 9, "bold"), bd=0, relief=tk.GROOVE)
        button_back.grid(column=1, row=8, sticky="NSEW")


    def observer(self, *args):
        watch = self.champs_var.get()
        nom, prenom, adresse, cp_ville, loyer, charges, mail, cat, sci, _, _, _, _, _ = \
            self.database.pdf_table_single(self.tenant_var.get())[0]
        tel = self.database.one_elt("tel", "tenant", self.tenant_var.get())
        mail = self.database.one_elt("mail", "tenant", self.tenant_var.get())
        value = {"nom": nom, "prenom": prenom, "adresse": adresse, "cp_ville": cp_ville, "tel": tel, "mail": mail,
                 "cat": cat, "sci": sci, "loyer": loyer, "charges": charges, "indice de base": "test"}
        self.old_var.set(value[watch])

    def quit(self):
        self.destroy()
        MainGui().mainloop()

    def mod_entry(self):
        print(self.tenant_var.get(), self.champs_var.get(), self.newval_var.get())
        self.database.modif_table(self.tenant_var.get(), self.champs_var.get(),
                                  self.newval_var.get())
        print(self.tenant_var.get(), self.champs_var.get(), self.newval_var.get())
        print("modification effectuée")

    def check_format(self):
        if self.champs_var.get() == "tel":
            Verification(self.newval_var.get()).verification_tel()

        elif self.champs_var.get() == "mail":
            Verification(self.newval_var.get()).verification_mail()

        elif self.champs_var.get() == "date":
            Verification(self.newval_var.get()).verification_date()


class DeleteGui(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title("Supression de locataire")
        self.master.geometry("150x200")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")
        self.combostyle = ttk.Style()
        self.combostyle.theme_use('custom.TCombobox')
        self.database = sql_database()
        # variable creation
        self.nom_var = tk.StringVar()
        self.nom_var.set("Attention action definitive")
        # widget creation
        main_frame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE, bg="#1A5276")
        main_frame.grid(column=0, row=0, sticky="NSEW")

        nom_label = tk.Label(main_frame, text="Nom du loctaire", font=('Courier', 9, "bold"), bg="#1A5276", fg="#74D0F1")
        nom_label.grid(column=0, row=0, sticky="EW")

        selec_entry = ttk.Combobox(main_frame, textvariable=self.nom_var, state='readonly', style='custom.TCombobox')
        list_tenant = self.database.elt_table("nom", "tenant")
        selec_entry['values'] = list_tenant
        selec_entry.grid(column=1, row=0, sticky="EW")

        blank_label = tk.Label(main_frame, bg="#1A5276")
        blank_label.grid(column=1, row=1)

        button_val = tk.Button(main_frame, text="SUPPRIMER", command=self.del_entry, bg="#3D4A56", fg='#74D0F1',
                                font=('Courier', 9, "bold"), bd=0, relief=tk.GROOVE)
        button_val.grid(column=1, row=2, sticky="NSEW")

        blank_label = tk.Label(main_frame, bg="#1A5276")
        blank_label.grid(column=1, row=3)

        button_back = tk.Button(main_frame, text="RETOUR", command=self.quit, bg="#3D4A56", fg='#74D0F1',
                                font=('Courier', 9, "bold"), bd=0, relief=tk.GROOVE)
        button_back.grid(column=1, row=4, sticky="NSEW")


    def del_entry(self):
        if self.nom_var.get() != "Attention action definitive":
            print(self.nom_var.get())
            self.database.delete_entry("tenant", self.nom_var.get())
            self.database.delete_entry("location", self.nom_var.get())
            print("suppression effectuée")
            messagebox.showinfo("Attention", "Supression effectuée")

    def quit(self):
        self.destroy()
        MainGui().mainloop()


class InfoGui(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title("Information")
        self.master.geometry("300x300")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")
        self.combostyle = ttk.Style()
        self.combostyle.theme_use('custom.TCombobox')
        self.database = sql_database()
        #variables
        self.nom = tk.StringVar()
        self.nom.set("En Attente de la selection")
        self.nom.trace("w", self.observer)
        self.prenom = tk.StringVar()
        self.adresse = tk.StringVar()
        self.ville = tk.StringVar()
        self.tel = tk.StringVar()
        self.mail = tk.StringVar()
        self.sci = tk.StringVar()
        self.date_entree = tk.StringVar()
        self.cat = tk.StringVar()

        main_frame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE, bg="#1A5276")
        main_frame.grid(column=0, row=0, sticky="NSEW")

        nom_label = tk.Label(main_frame, text="Nom du loctaire", font=('Courier', 9, "bold"), bg="#1A5276",
                             fg="#74D0F1")
        nom_label.grid(column=0, row=0, sticky="EW")

        selec_entry = ttk.Combobox(main_frame, textvariable=self.nom, state='readonly', style='custom.TCombobox')
        list_tenant = self.database.elt_table("nom", "tenant")
        selec_entry['values'] = list_tenant
        selec_entry.grid(column=1, row=0, sticky="EW")

        label_prenom = tk.Label(main_frame, text='Prenom', font=('Courier', 9, "bold"), bg="#1A5276", fg="#74D0F1")
        label_prenom.grid(column=0, row=1, sticky="NSEW")

        aff_prenom = tk.Label(main_frame, textvariable=self.prenom, font=('Courier', 9, "bold"), bg="#1A5276", fg="#74D0F1")
        aff_prenom.grid(column=1, row=1, sticky="EW")

        label_adresse = tk.Label(main_frame, text="Adresse", font=('Courier', 9, "bold"), bg="#1A5276", fg="#74D0F1")
        label_adresse.grid(column=0, row=2, sticky="NSEW")

        aff_adresse = tk.Label(main_frame, textvariable=self.adresse, font=('Courier', 9, "bold"), bg="#1A5276",
                              fg="#74D0F1")
        aff_adresse.grid(column=1, row=2, sticky="EW")

        label_ville = tk.Label(main_frame, text="CP_Ville", font=('Courier', 9, "bold"), bg="#1A5276", fg="#74D0F1")
        label_ville.grid(column=0, row=3, sticky="NSEW")

        aff_ville = tk.Label(main_frame, textvariable=self.ville, font=('Courier', 9, "bold"), bg="#1A5276",
                              fg="#74D0F1")
        aff_ville.grid(column=1, row=3, sticky="EW")

        label_tel = tk.Label(main_frame, text="Tel", font=('Courier', 9, "bold"), bg="#1A5276", fg="#74D0F1")
        label_tel.grid(column=0, row=4, sticky="NSEW")

        aff_tel = tk.Label(main_frame, textvariable=self.tel, font=('Courier', 9, "bold"), bg="#1A5276",
                              fg="#74D0F1")
        aff_tel.grid(column=1, row=4, sticky="EW")

        label_mail = tk.Label(main_frame, text="Email", font=('Courier', 9, "bold"), bg="#1A5276", fg="#74D0F1")
        label_mail.grid(column=0, row=5, sticky="NSEW")

        aff_mail = tk.Label(main_frame, textvariable=self.mail, font=('Courier', 9, "bold"), bg="#1A5276",
                              fg="#74D0F1")
        aff_mail.grid(column=1, row=5, sticky="EW")

        label_sci = tk.Label(main_frame, text="SCI", font=('Courier', 9, "bold"), bg="#1A5276", fg="#74D0F1")
        label_sci.grid(column=0, row=6, sticky="NSEW")

        aff_sci = tk.Label(main_frame, textvariable=self.sci, font=('Courier', 9, "bold"), bg="#1A5276",
                            fg="#74D0F1")
        aff_sci.grid(column=1, row=6, sticky="EW")

        label_cat = tk.Label(main_frame, text="catégorie", font=('Courier', 9, "bold"), bg="#1A5276", fg="#74D0F1")
        label_cat.grid(column=0, row=7, sticky="NSEW")

        aff_cat = tk.Label(main_frame, textvariable=self.cat, font=('Courier', 9, "bold"), bg="#1A5276",
                            fg="#74D0F1")
        aff_cat.grid(column=1, row=7, sticky="EW")

        label_date = tk.Label(main_frame, text="Date_entrée", font=('Courier', 9, "bold"), bg="#1A5276", fg="#74D0F1")
        label_date.grid(column=0, row=8, sticky="NSEW")

        aff_date = tk.Label(main_frame, textvariable=self.date_entree, font=('Courier', 9, "bold"), bg="#1A5276",
                            fg="#74D0F1")
        aff_date.grid(column=1, row=8, sticky="EW")

        blank_label = tk.Label(main_frame, bg="#1A5276")
        blank_label.grid(column=0, row=9, columnspan=2)

        button_back = tk.Button(main_frame, text="RETOUR", command=self.quit,  bg="#3D4A56", fg='#74D0F1',
                                font=('Courier', 9, "bold"), bd=0, relief=tk.GROOVE)
        button_back.grid(column=1, row=10, sticky="NSEW")

    def observer(self, *args):
        watch = self.nom.get()
        _, _, prenom, adresse, ville, tel, mail, cat = self.database.elt_table_one("nom", "tenant", watch)[0]
        _, sci, _, _, _, _, _, dates_entree, _ = self.database.elt_table_one("nom", "location", watch)[0]
        print(prenom, adresse, ville, tel, mail, cat, sci, dates_entree)
        self.prenom.set(prenom)
        self.adresse.set(adresse)
        self.ville.set(ville)
        self.tel.set(tel)
        self.mail.set(mail)
        self.sci.set(sci)
        self.date_entree.set(dates_entree)
        if cat == "0":
            self.cat.set("Particulier")
        else:
            self.cat.set("Professionnel")

    def quit(self):
        self.destroy()
        MainGui().mainloop()

class MajRentGui(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title("MAJ Loyer")
        self.master.geometry("300x300")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")
        self.database = sql_database()
        self.combostyle = ttk.Style()
        self.combostyle.theme_use('custom.TCombobox')
        # variables
        self.tenant_name = tk.StringVar()
        self.tenant_name.trace("w", self.observer)
        self.base_loyer = tk.StringVar()
        self.base_loyer.set("----------")
        self.new_indice = tk.StringVar()
        self.new_indice.trace("w", self.observer_2)
        self.new_rent = tk.StringVar()
        self.new_rent.set("")
        # widget label
        main_frame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE, bg="#1A5276")
        main_frame.grid(column=0, row=0, sticky="NSEW")


        label_name = tk.Label(main_frame, text="Locataire", bg="#1A5276", font=('Courier', 9, "bold"), fg='#74D0F1')
        label_name.grid(column=0, row=0, sticky="W")

        selec_name_entry = ttk.Combobox(main_frame, textvariable=self.tenant_name, state='readonly', style='custom.TCombobox')
        selec_name_entry.grid(column=1, row=0, sticky="NSEW")

        select_name = self.database.elt_table("nom", "tenant")
        selec_name_entry['values'] = select_name

        label_loyer_base = tk.Label(main_frame, text="Base loyer", bg="#1A5276", font=('Courier', 9, "bold"), fg='#74D0F1')
        label_loyer_base.grid(column=0, row=1, sticky="W")

        aff_loyer_base = tk.Label(main_frame, textvariable=self.base_loyer, bg="#1A5276", font=('Courier', 12, "bold"), fg='#74D0F1')
        aff_loyer_base.grid(column=1, row=1, sticky="NSEW")

        label_indice = tk.Label(main_frame, text="Nouvel indice", bg="#1A5276", font=('Courier', 9, "bold"), fg='#74D0F1')
        label_indice.grid(column=0, row=3, sticky="NSEW")

        Entry_indice = tk.Entry(main_frame, textvariable=self.new_indice, bg="#4F7292", fg='white')
        Entry_indice.grid(column=1, row=3, sticky="NSEW")

        label_new_rent = tk.Label(main_frame, text="Nouveau loyer", bg="#1A5276", font=('Courier', 9, "bold"), fg='#74D0F1')
        label_new_rent.grid(column=0, row=4, sticky="NSEW")

        aff_new_rent = tk.Label(main_frame, textvariable=self.new_rent, bg="#1A5276", font=('Courier', 12, "bold"), fg='red')
        aff_new_rent.grid(column=1, row=4)

        label_blank = tk.Label(main_frame, bg="#1A5276")
        label_blank.grid(column=1, row=6, sticky="NSEW")

        label_validation = tk.Button(main_frame, text="VALIDER", command=self.validation, borderwidth=2,
                                     relief=tk.GROOVE, bg="#3D4A56", font=('Courier', 9, "bold"), fg='#74D0F1')
        label_validation.grid(column=1, row=7, sticky="NSEW")

        label_blank = tk.Label(main_frame, bg="#1A5276")
        label_blank.grid(column=1, row=8, sticky="NSEW")

        label_retour = tk.Button(main_frame, text="RETOUR", command=self.quitter, borderwidth=2, relief=tk.GROOVE,
                                 bg="#3D4A56", font=('Courier', 9, "bold"), fg='#74D0F1')
        label_retour.grid(column=1, row=9, sticky="NSEW")

    def observer(self, *args):
        watch = self.tenant_name.get()
        self.base_loyer.set(f'{self.database.one_elt("base_loyer", "location", watch)[0][0]} €')

    def observer_2(self, *args):
        if not self.tenant_name.get():
            self.new_rent.set("En attente du locataire")
        else:
            try:
                watch = self.new_indice.get()
                new_indice = float(watch)
                num = re.compile(r"(\d+.\d+)")
                base_rent = num.search(self.base_loyer.get())
                base_rent = int(base_rent.group(0))
                base_indice = self.database.one_elt("indice_base", "location", self.tenant_name.get())[0][0]
                self.new_rent.set(f"{round(base_rent * new_indice / base_indice, 2)} €")
            except ValueError as e:
                print (e)

    def validation(self):
        pattern = re.compile(r"(^\d+.\d{2}$)")
        if re.match(pattern, self.new_indice.get()):
            num = re.compile(r"(\d+.\d+)")
            new_rent = num.search(self.new_rent.get())
            new_rent = new_rent.group(0)
            self.database.modif_table(self.tenant_name.get(), "loyer", new_rent)

        else:
            messagebox.showinfo("Attention", "Saisie de l'indice incorrect")

    def quitter(self):
        self.destroy()
        MainGui().mainloop()

class LetterGui(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title("Lettre")
        self.master.geometry("300x300")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")
        self.database = sql_database()
        self.combostyle = ttk.Style()
        self.combostyle.theme_use('custom.TCombobox')
        # variables
        self.tenant_name = tk.StringVar()
        # widget label
        main_frame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE, bg="#1A5276")
        main_frame.grid(column=0, row=0, sticky="NSEW")

        label_name = tk.Label(main_frame, text="Locataire", bg="#1A5276", font=('Courier', 9, "bold"), fg='#74D0F1')
        label_name.grid(column=0, row=0, sticky="W")

        selec_name_entry = ttk.Combobox(main_frame, textvariable=self.tenant_name, state='readonly', style='custom.TCombobox')
        selec_name_entry.grid(column=1, row=0, sticky="NSEW")

        select_name = self.database.elt_table("nom", "tenant")
        selec_name_entry['values'] = select_name

        label_blank = tk.Label(main_frame, bg="#1A5276")
        label_blank.grid(column=1, row=6, sticky="NSEW")

        label_validation = tk.Button(main_frame, text="ENVOYER", command=self.validation, borderwidth=2,
                                     relief=tk.GROOVE, bg="#3D4A56", font=('Courier', 9, "bold"), fg='#74D0F1')
        label_validation.grid(column=1, row=7, sticky="NSEW")

        label_blank = tk.Label(main_frame, bg="#1A5276")
        label_blank.grid(column=1, row=8, sticky="NSEW")

        label_retour = tk.Button(main_frame, text="RETOUR", command=self.quitter, borderwidth=2, relief=tk.GROOVE,
                                 bg="#3D4A56", font=('Courier', 9, "bold"), fg='#74D0F1')
        label_retour.grid(column=1, row=9, sticky="NSEW")

    def validation(self):
        pass

    def quitter(self):
        self.destroy()
        MainGui().mainloop()


class ConfigGUI(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title("Configuration")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.geometry("300x200")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")
        self.config = self.config_files()
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
        main_frame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE, bg="#1A5276")
        main_frame.grid(column=0, row=0, sticky="NSEW")

        main_frame.columnconfigure(0, weight=0)
        main_frame.columnconfigure(1, weight=1)

        master_mail_label = tk.Label(main_frame, text="email du compte",font=('Courier', 9, "bold"), bg="#1A5276", fg="#74D0F1")
        master_mail_label.grid(column=0, row=0, sticky="NSEW")

        master_mail_entry = tk.Entry(main_frame, textvariable=self.master_mail_var, bg="#4F7292", fg='white')
        master_mail_entry.grid(column=1, row=0, sticky="NSEW")

        password_label = tk.Label(main_frame, text="password du compte", font=('Courier', 9, "bold"), bg="#1A5276", fg="#74D0F1")
        password_label.grid(column=0, row=1, sticky="NSEW")

        password_entry = tk.Entry(main_frame, textvariable=self.password_var, bg="#4F7292", fg='white')
        password_entry.grid(column=1, row=1, sticky="NSEW")

        smtp_label = tk.Label(main_frame, text="SMTP", font=('Courier', 9, "bold"), bg="#1A5276", fg="#74D0F1")
        smtp_label.grid(column=0, row=2, sticky="NSEW")

        smtp_entry = tk.Entry(main_frame, textvariable=self.smtp_var, bg="#4F7292", fg='white')
        smtp_entry.grid(column=1, row=2, sticky="NSEW")

        port_label = tk.Label(main_frame, text="port", font=('Courier', 9, "bold"), bg="#1A5276", fg="#74D0F1")
        port_label.grid(column=0, row=3, sticky="NSEW")

        port_entry = tk.Entry(main_frame, textvariable=self.port_var, bg="#4F7292", fg='white')
        port_entry.grid(column=1, row=3, sticky="NSEW")

        blank_label = tk.Label(main_frame, bg="#1A5276")
        blank_label.grid(column=0, row=4, columnspan=2, sticky="NSEW")

        button_validation = tk.Button(main_frame, text="ENREGISTRER", command=self.mod_entry, borderwidth=2, relief=tk.GROOVE,
                                 bg="#3D4A56", font=('Courier', 9, "bold"), fg='#74D0F1')
        button_validation.grid(column=1, row=5, sticky="NSEW")

        blank_label = tk.Label(main_frame, bg="#1A5276")
        blank_label.grid(column=0, row=6, columnspan=2, sticky="NSEW")

        button_exit = tk.Button(main_frame, text="RETOUR", command=self.quit, borderwidth=2, relief=tk.GROOVE,
                                 bg="#3D4A56", font=('Courier', 9, "bold"), fg='#74D0F1')
        button_exit.grid(column=1, row=7, sticky="NSEW")

    def quit(self):
        self.destroy()
        MainGui().mainloop()

    def mod_entry(self):
        self.config["master_mail"] = self.master_mail_var.get()
        self.config["password"] = self.password_var.get()
        self.config['SMTP'] = self.smtp_var.get()
        self.config["port"] = self.port_var.get()
        with open('config.json', 'w') as json_files:
            json.dump(self.config, json_files)
        print("mise à jour du fichier config")
        messagebox.showinfo("Information", "Modification(s) effectuée(s)")

    @staticmethod
    def config_files():
        with open('config.json', 'r') as json_files:
            return json.load(json_files)


class NewSciGUI(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title("Nouvelle sci")
        self.master.geometry("350x350")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")
        self.database = sql_database()
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
        MainGui().mainloop(self)


class ModSciGui(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title("Modification sci")
        self.master.geometry("350x350")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")
        self.database = sql_database()
        # widgets variables
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
        MainGui().mainloop(self)


class DelSciGui(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title("Supression SCI")
        self.master.geometry("350x350")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")
        self.database = sql_database()
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
        MainGui().mainloop(self)


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
            messagebox.showinfo("Mail", "Saisie incorrect")
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
            messagebox.showinfo("Telephone", "Saisie incorrect")
            return False

    def verification_date(self):
        pattern = re.compile(
            r"^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$")
        if re.match(pattern, self.value):
            print(" format date compatible")
            return True
        else:
            print("Format de saisie incorrect")
            messagebox.showinfo("Date", "Saisie incorrect")
            return False

    def verification_loyer(self):
        if isinstance(self.value, str):
            print("valeur incorrect")
            messagebox.showinfo("Loyer", "Saisie incorrect")
            return False
        else:
            print("(loyer) format saisie correct")
            return True

    def verification_charges(self):
        if isinstance(self.value, str):
            print("valeur incorrect")
            messagebox.showinfo("Charges", "Saisie incorrect")
            return False
        else:
            print("(saisie) format saisie correct")
            return True

    def verification_indice(self):
        if isinstance(self.value, str):
            print("valeur incorrect")
            messagebox.showinfo("Indice", "Saisie incorrect")
            return False
        else:
            print("(indice) format saisie correct")
            return True


if __name__ == "__main__":
    SplashScreen().mainloop()
