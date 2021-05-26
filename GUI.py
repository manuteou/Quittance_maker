import tkinter as tk
from tkinter import ttk
from datetime import date
import functions
from locataire import locataire, sql_database, sci
from pdfgenerator import PdfGenerator, IndexLetter
from mail_sender import send_mail
from tkinter import messagebox
import json, re
from reportlab.pdfgen import canvas
from pathlib import Path
from functions import Verification
import webbrowser
from tkinter.colorchooser import askcolor

class Gui_aspect:
    def __init__(self):
        with open("config.json", "r") as json_files:
            self.config = json.load(json_files)

    def setting(self):
        bg = self.config["interface"]["bg"]
        button_color = self.config["interface"]["button_color"]
        fg = self.config["interface"]["fg"]
        fg_size = self.config["interface"]["fg_size"]
        tableau = self.config["interface"]['tableau']
        font_gui = self.config["interface"]["font_gui"]
        return bg, button_color, fg, fg_size, tableau, font_gui

class SplashScreen(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        height, width = self.get_display_size()
        print(height, width)
        height = int(height/2) - 175
        width = int(width/2) - 425
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
        self.master.geometry("970x350")
        self.master.overrideredirect(False)
        self.master.minsize(300, 150)
        self.master.title("Quittances Maker V1.00")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")
        self.bg, self.button_color, self.fg, self.fg_size, self.tableau, self.fontGui = Gui_aspect().setting()
        self.database = sql_database()
        # variable's creation
        self.today = date.today()
        self.date_s = tk.StringVar()
        self.date_s.set(f"{self.today.day}/{self.today.month}/{self.today.year}")
        self.info = tk.StringVar()
        # widget's Creation
        main_frame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE, bg=self.button_color
                              )
        main_frame.columnconfigure(0, weight=0)
        main_frame.columnconfigure(1, weight=1)

        frame1 = tk.LabelFrame(self, main_frame, text="LOCATAIRES", font=('Courier', self.fg_size, "bold"), fg=self.fg, borderwidth=4, relief=tk.GROOVE, bg=self.tableau)
        frame2 = tk.Frame(self, main_frame, borderwidth=2, relief=tk.GROOVE, bg=self.button_color
                          )
        frame3 = tk.Frame(self, main_frame, bg=self.button_color
                          )
        frame1.grid(column=0, row=0, sticky='NSEW')
        frame2.grid(column=0, row=1, sticky='NSEW')
        frame3.grid(column=1, row=0, rowspan=2, sticky='NSEW')
        # widgets menu*

        self.selection = []
        # widgets on the left side
        #
        column = ["Select", "nom", "prenom", "loyer", "charges", "info", "statut"]
        i = 0
        for e in column:
            label = tk.Label(frame1, text=e.upper(), font=('Courier', self.fg_size, "bold"), fg=self.fg, bg=self.tableau)
            label.grid(column=i, row=0, sticky='W', padx=10)
            i += 1

        aff_list = self.database.test_table()

        variable_list = []
        for e in aff_list:
            variable_list.append(e[2])

        r = 1
        for i, elt in enumerate(aff_list):
            c = 1
            self.selection.append(tk.BooleanVar(value=0))
            check_box = tk.Checkbutton(frame1, variable=self.selection[i], bg=self.tableau)
            check_box.grid(column=0, row=r)


            if self.info_tenant(elt[7]) == 0:
                info_field = tk.Label(frame1, text="MAJ Loyer", bg=self.tableau, fg='white', font=("Times", self.fg_size))
                info_field.grid(column=5, row=r)
            if self.info_tenant(elt[7]) == 1:
                info_field = tk.Label(frame1, text="Lettre d'indexation", bg=self.tableau, fg='white', font=("Times", self.fg_size))
                info_field.grid(column=5, row=r)
            else:
                info_field = tk.Label(frame1, bg=self.tableau, fg='white', font=("Times", self.fg_size))
                info_field.grid(column=5, row=r)

            if not self.statut_check(elt[2], elt[3], elt[6]):

                statut_field = tk.Label(frame1, text="NOT SEND", bg=self.tableau, fg='white', font=("Times", self.fg_size))
                statut_field.grid(column=6, row=r)
            else:
                statut_field = tk.Label(frame1, text="SEND", bg=self.tableau, fg='green', font=("Times", self.fg_size))
                statut_field.grid(column=6, row=r)

            for e in elt[2:-2]:
                label = tk.Label(frame1, text=e, bg=self.tableau, fg='white', font=("Times", self.fg_size))
                label.grid(column=c, row=r, sticky='NSEW', padx=10)
                c += 1
            r += 1

        # widgets under
        date_s_label = tk.Label(frame2, text="Jour d'édition", borderwidth=2, padx=-1, bg=self.button_color
                                , font=('Courier', 10, "bold"), fg=self.fg)
        date_s_label.grid(column=0, row=0, sticky='NW')

        date_s_entry = tk.Entry(frame2, textvariable=self.date_s, borderwidth=2, relief=tk.GROOVE, bg="#4F7292", bd=0, font=('Courier', 10, "bold"), fg="white")
        date_s_entry.grid(column=1, row=0, sticky='NE')

        # button_all = tk.Button(frame2, text=" ENVOIE TOUS", height=2, borderwidth=2, relief=tk.GROOVE, bg=se, font=('Courier', 9, "bold"), fg='#74D0F1', command=self.validation_all_tenant)
        # button_all.grid(column=0, row=10, sticky='NSEW')

        button_selection = tk.Button(frame2, text="ENVOIE SELECTION", height=2, borderwidth=2, bg=self.bg
, font=('Courier', 9, "bold"), fg=self.fg, relief=tk.GROOVE, command=self.validation_select_tenant)
        button_selection.grid(column=0, row=9, sticky='NSEW')


        # widgets on right
        button_config = tk.Button(frame3, text='CONFIG', borderwidth=2, relief=tk.GROOVE, command=self.config, bg=self.bg, fg=self.fg, font=('Courier', self.fg_size, "bold"))
        button_config.grid(column=0, row=0, sticky='NSEW')

        button_blk0 = tk.Button(frame3, state='disabled', bd=0, bg=self.button_color
                                )
        button_blk0.grid(column=0, row=1, sticky='NSEW')

        self.menu_sci = tk.StringVar()
        menu_sci_list = ["création", "modification", "suppression"]
        self.menu_sci.set("SCI")
        SciMenu = tk.OptionMenu(frame3, self.menu_sci, *menu_sci_list, command=self.sci_menu_selection)
        SciMenu.configure(bg=self.bg, font=('Courier', self.fg_size, "bold"), fg=self.fg, bd=0)
        SciMenu.grid(column=0, row=2, sticky='NSEW')

        button_blk1 = tk.Button(frame3, state='disabled', bd=0, bg=self.button_color
                                )
        button_blk1.grid(column=0, row=3, sticky='NSEW')

        # menu tenant
        self.menu_tenant = tk.StringVar()
        menu_tenant_list = ["info", "création", "modification", "supression"]
        self.menu_tenant.set("LOCATAIRE")
        tenantMenu = tk.OptionMenu(frame3, self.menu_tenant, *menu_tenant_list, command=self.tenant_menu_selection)
        tenantMenu.configure(bg=self.bg, fg=self.fg, font=('Courier', self.fg_size, "bold"), bd=0)
        tenantMenu.grid(column=0, row=4, sticky='NSEW')

        button_blk2 = tk.Button(frame3, state='disabled', bd=0, bg=self.button_color
                                )
        button_blk2.grid(column=0, row=5, sticky='NSEW')

        self.menu_index = tk.StringVar()
        menu_index_list = ["Lettre", "MAJ Loyer"]
        self.menu_index.set("INDEXATION")
        indexMenu = tk.OptionMenu(frame3, self.menu_index, *menu_index_list, command=self.index_menu_selection)
        indexMenu.configure(bg=self.bg, fg=self.fg, font=('Courier', self.fg_size, "bold"), bd=0)
        indexMenu.grid(column=0, row=6, sticky='NSEW')

        button_blk3 = tk.Button(frame3, state='disabled', bd=0, bg=self.button_color
                                )
        button_blk3.grid(column=0, row=7, sticky='NSEW')

        button_blk4 = tk.Button(frame3, state='disabled', bd=0, bg=self.button_color
                                )
        button_blk4.grid(column=0, row=8, sticky='NSEW')

        button_blk5 = tk.Button(frame3, state='disabled', bd=0, bg=self.button_color
                                )

        button_blk5.grid(column=0, row=9, sticky='NSEW')

        button_end = tk.Button(frame3, text="FERMER", borderwidth=2, relief=tk.GROOVE,
                               command=self.closing, bg=self.bg, fg=self.fg, font=('Courier', self.fg_size, "bold"), bd=0)
        button_end.grid(column=0, row=10, sticky='NSEW')

    def closing(self):
        self.master.destroy()

    def validation_all_tenant(self):
        pass

    def validation_select_tenant(self):
        result_selection = []
        list_to_send = []
        for i, e in enumerate(self.selection):
            result_selection.append(self.selection[i].get())

        for i, value in enumerate(result_selection):
            if value:
                list_to_send.append(self.database.pdf_table_single(i+1))

        directory = functions.directory()
        config = functions.config_data()
        day, month, year = self.date_s.get().split("/")

        for elt in list_to_send:
            print(elt[0])
            path_dir = directory.joinpath(elt[0][10], year, month)
            print (path_dir)
            path_dir.mkdir(parents=True, exist_ok=True)
            path = path_dir.joinpath(f"{elt[0][2]}_{elt[0][3]}" + ".pdf")
            pdf = canvas.Canvas(str(path))
            pdf_gen = PdfGenerator(pdf, nom=elt[0][2], prenom=elt[0][3], adresse=elt[0][4], ville=elt[0][5],
                                   loyer=elt[0][6], charge=elt[0][7], day=day, month=month, years=year, cat=elt[0][9],
                                   sci_nom=elt[0][10], sci_adresse=elt[0][11], sci_cp_ville=elt[0][12],
                                   sci_tel=elt[0][13], sci_mail=elt[0][14], sci_siret=elt[0][15])
            pdf_gen.generator()
            mail = send_mail("Quittance", config["master_mail"], config["password"], elt[0][8], config["SMTP"],
                                 config["port"], path)
            mail.send()
            self.destroy()
            MainGui().mainloop()

    def config(self):
        self.destroy()
        ConfigGUI().mainloop()

    def statut_check(self, nom, prenom, sci):
        directory = functions.directory()
        date = self.date_s.get()
        _, month, year = date.split("/")
        path_dir = directory.joinpath(sci, year, month, f"{nom}_{prenom}" + ".pdf")

        if path_dir.exists():
            return True
        else:
            return False

    def info_tenant(self, date_entree):
        month = date.today().month
        month_tenant = int(date_entree.split("/")[1])
        if (month - month_tenant) == 0:
            return 0
        elif (month - month_tenant) == -1:
            return 1

    # Main Menus
    def index_menu_selection(self, v):
        if self.menu_index.get() == 'Lettre':
            self.destroy()
            LetterGui().mainloop()

        elif self.menu_index.get() == 'MAJ Loyer':
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
                CreatModGui(0).mainloop()
        elif self.menu_tenant.get() == 'modification':
            self.destroy()
            CreatModGui(1).mainloop()
        elif self.menu_tenant.get() == 'supression':
            self.destroy()
            DeleteGui().mainloop()

    def sci_menu_selection(self, v):
        if self.menu_sci.get() == "création":
            self.destroy()
            NewModSciGUI(1).mainloop()
        if self.menu_sci.get() == "modification":
            self.destroy()
            NewModSciGUI(0).mainloop()
        if self.menu_sci.get() == "suppression":
            self.destroy()
            DelSciGui().mainloop()



class CreatModGui(tk.Frame):
    def __init__(self, value):
        tk.Frame.__init__(self)
        self.master.geometry("360x350")
        self.combostyle = ttk.Style()
        self.combostyle.theme_use('custom.TCombobox')
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")
        self.database = sql_database()
        self.bg, self.button_color, self.fg, self.fg_size, _, self.fontGui = Gui_aspect().setting()
        # varaibles' creation
        self.tenant_var = tk.StringVar()
        self.prenomVar = tk.StringVar()
        self.adresseVar = tk.StringVar()
        self.villeVar = tk.StringVar()
        self.telVar = tk.StringVar()
        self.mailVar = tk.StringVar()
        self.sciVar = tk.StringVar()
        self.loyerVar = tk.StringVar()
        self.chargesVar = tk.StringVar()
        self.selectorVar = tk.StringVar()
        self.selectorVar.set(1)
        self.date_entreeVar = tk.StringVar()
        self.indice_base = tk.StringVar()

        main_frame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE, bg=self.button_color
                              )
        main_frame.grid(column=0, row=0, sticky="NSEW")

        if value == 1:
            n = 1
            self.type_field = 1
            self.tenant_old = tk.StringVar()
            self.master.title("Modification de Locataire")
            self.tenant_old.trace("w", self.observer)

            selec_entry = ttk.Combobox(main_frame, textvariable=self.tenant_old, state='readonly',
                                       style='custom.TCombobox')
            selec_entry.grid(column=1, row=1, columnspan=2, sticky="EW")

            tenant_list = self.database.elt_table("nom", "tenant")
            selec_entry['values'] = tenant_list


        if value == 0:
            n = 0
            self.type_field = 0
            self.master.title("Création de Locataire")

        selector1 = tk.Radiobutton(main_frame, text="Particulier", variable=self.selectorVar, value=0, bd=0,
                                   relief=tk.FLAT, bg=self.button_color
                                   , fg=self.fg, font=('Courier', self.fontGui))
        selector1.grid(column=1, row=0, sticky="NSEW", padx=1)

        selector2 = tk.Radiobutton(main_frame, text="Professionel", variable=self.selectorVar, value=1, bd=0,
                                   relief=tk.FLAT, bg=self.button_color
                                   , fg=self.fg, font=('Courier', self.fontGui))
        selector2.grid(column=2, row=0, sticky="NSEW", padx=1)
        champs = ["Nom", "Prenom", "Adresse", "CP_ville", "Telephone", "Email", "SCI", "Date d'entrée", "Loyer",
                  "Charges", "Indice"]
        i = 1
        for elt in champs:
            label = tk.Label(main_frame, text=elt, font=('Courier', self.fontGui, "bold"), bg=self.button_color
                             , fg=self.fg)
            label.grid(column=0, row=i + n, sticky="EW")
            i += 1

        entries = [self.tenant_var, self.prenomVar, self.adresseVar, self.villeVar, self.telVar, self.mailVar]
        i = 1
        for elt in entries:
            entry = tk.Entry(main_frame, textvariable=elt, bg="#4F7292", fg='white')
            entry.grid(column=1, row=i + n, columnspan=2, sticky="EW")
            i += 1

        sci_choise = ttk.Combobox(main_frame, textvariable=self.sciVar, state='readonly', style='custom.TCombobox')
        sci_choise.grid(column=1, row=7 + n, columnspan=2, sticky="EW")
        with open('config.json', 'r') as json_files:
            config = json.load(json_files)
        sci_choise['values'] = config['sci']

        entries = [self.date_entreeVar, self.loyerVar, self.chargesVar, self.indice_base]
        i = 8
        for elt in entries:
            entry = tk.Entry(main_frame, textvariable=elt, bg="#4F7292", fg='white')
            entry.grid(column=1, row=i + n, columnspan=2, sticky="EW")
            i += 1


        button = tk.Button(main_frame, text="VALIDER", command=self.validation_tenant, bg=self.bg, fg=self.fg, font=('Courier',
                                                                                                                     self.fontGui, "bold"), bd=0, relief=tk.GROOVE)
        button.grid(column=2, row=13 + n, sticky='NSEW', padx=1)

        button2 = tk.Button(main_frame, text="RETOUR", command=self.quit, bg=self.bg, fg=self.fg, font=('Courier', self.fontGui, "bold"), bd=0, relief=tk.GROOVE)
        button2.grid(column=1, row=13 + n, sticky='NSEW', padx=1)

    def observer(self, *args):
        watch = self.tenant_old.get()
        print(watch)
        modification_table = self.database.modification_call(watch.split(" ")[0])
        print(modification_table)
        self.tenant_id = modification_table[0]
        self.tenant_var.set(modification_table[1])
        self.prenomVar.set(modification_table[2])
        self.adresseVar.set(modification_table[3])
        self.villeVar.set(modification_table[4])
        self.telVar.set(modification_table[5])
        self.mailVar.set(modification_table[6])
        self.sciVar.set(modification_table[7])
        self.date_entreeVar.set(modification_table[8])
        self.loyerVar.set(modification_table[9])
        self.chargesVar.set(modification_table[10])
        self.indice_base.set(modification_table[11])
        self.selectorVar.set(modification_table[12])

    # def cleaning(self, var):
    #     return var.replace("((", "").replace(",),)", "").replace("'", "")

    def check_entry(self):
        print(self.tenant_var.get())
        print(type(self.tenant_var.get()))
        if self.tenant_var.get() == "" or self.prenomVar.get() == "" or self.adresseVar.get() == "" \
                or self.villeVar.get() == "":
            print("champs vide")
            messagebox.showinfo("Attention", "un ou plusieurs champs vides, validation impossible")
            return False

        if not Verification(self.mailVar.get()).verification_mail() or\
            not Verification(self.telVar.get()).verification_tel() or\
            not Verification(self.date_entreeVar.get()).verification_date() or\
            not Verification(float(self.loyerVar.get())).verification_loyer() or\
            not Verification(float(self.chargesVar.get())).verification_charges() or\
            not Verification(float(self.indice_base.get())).verification_indice():
            messagebox.showinfo("Attention", "un ou plusieurs champs mal renseignés, validation impossible")
            return False

        else:
            return True

    def validation_tenant(self):
        if not self.check_entry():
            return "erreur de champs"

        else:
            client = locataire(self.tenant_var.get(), self.prenomVar.get(),
                                self.adresseVar.get(), self.villeVar.get(),
                               self.telVar.get(), self.mailVar.get(),
                               self.sciVar.get(), self.loyerVar.get(),
                               self.chargesVar.get(), self.selectorVar.get()
                               , self.date_entreeVar.get(), self.indice_base.get())
            print(self.selectorVar.get())
            insert_tenant = {'nom': client.nom, 'prenom': client.prenom, 'adresse': client.adresse,
                             'CP_ville': client.cp_ville, 'tel': client.tel, 'mail': client.mail.lower(),
                             'cat': client.cat}

            insert_location = {'SCI': client.sci.upper(), 'nom': client.nom, 'type': client.cat,'loyer': client.loyer,
                                'base_loyer': client.loyer, 'charges': client.charges, 'date_entree': client.date_entree
                                , 'indice_base': client.base_indice}

            if self.type_field == 1:
                print("modification")
                self.database.update_entry(self.tenant_id, "tenant", insert_tenant)
                self.database.update_entry(self.tenant_id, "location", insert_location)
                messagebox.showinfo("Information", "modification(s) enregistré(es)")


            elif self.type_field == 0:
                print("ajout")

                self.database.create_entry("tenant", insert_tenant)
                self.database.create_entry("location", insert_location)
                messagebox.showinfo("Nouvelle Entrée", "Locataire enregistré")
                print("creation")
                print(self.tenant_var.get(), self.prenomVar.get(), self.adresseVar.get(), self.villeVar.get(),
                      self.telVar.get(),
                      self.mailVar.get(), self.sciVar.get(), self.loyerVar.get(), self.chargesVar.get())

    def quit(self):
        self.destroy()
        MainGui().mainloop()


class DeleteGui(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title("Supression de locataire")
        self.master.geometry("160x200")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")
        self.combostyle = ttk.Style()
        self.combostyle.theme_use('custom.TCombobox')
        self.database = sql_database()
        self.bg, self.button_color, self.fg, self.fg_size, _, self.fontGui = Gui_aspect().setting()
        # variable creation
        self.nom_var = tk.StringVar()
        self.nom_var.set("Attention action definitive")
        # widget creation

        main_frame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE, bg=self.button_color
                              )
        main_frame.grid(column=0, row=0, sticky="NSEW")

        nom_label = tk.Label(main_frame, text="Nom du loctaire", font=('Courier', self.fontGui, "bold"), bg=self.button_color
                             , fg=self.fg)
        nom_label.grid(column=0, row=0, sticky="EW")

        selec_entry = ttk.Combobox(main_frame, textvariable=self.nom_var, state='readonly', style='custom.TCombobox')
        list_tenant = self.database.elt_table("nom", "tenant")
        selec_entry['values'] = list_tenant
        selec_entry.grid(column=1, row=0, sticky="EW")

        blank_label = tk.Label(main_frame, bg=self.button_color
                               )
        blank_label.grid(column=1, row=1)

        button_val = tk.Button(main_frame, text="SUPPRIMER", command=self.del_entry, bg=self.bg, fg=self.fg,
                               font=('Courier', self.fontGui, "bold"), bd=0, relief=tk.GROOVE)
        button_val.grid(column=1, row=2, sticky="NSEW")

        blank_label = tk.Label(main_frame, bg=self.button_color
                               )
        blank_label.grid(column=1, row=3)

        button_back = tk.Button(main_frame, text="RETOUR", command=self.quit, bg=self.bg, fg=self.fg,
                                font=('Courier', self.fontGui, "bold"), bd=0, relief=tk.GROOVE)
        button_back.grid(column=1, row=4, sticky="NSEW")


    def del_entry(self):
        if self.nom_var.get() != "Attention action definitive":
            index = self.nom_var.get().split(" ")[0]
            print(index)
            self.database.delete_entry("tenant", index)
            self.database.delete_entry("location", index)
            print("suppression effectuée")
            messagebox.showinfo("Attention", "Supression effectuée")

    def quit(self):
        self.destroy()
        MainGui().mainloop()


class InfoGui(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title("Information")
        self.master.geometry("310x300")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")
        self.combostyle = ttk.Style()
        self.combostyle.theme_use('custom.TCombobox')
        self.database = sql_database()
        self.bg, self.button_color, self.fg, self.fg_size, _, self.fontGui = Gui_aspect().setting()
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

        main_frame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE, bg=self.button_color
                              )
        main_frame.grid(column=0, row=0, sticky="NSEW")
        champs = ["Nom du loctaire", 'Prenom', "Adresse", "CP_Ville", "Tel", "Email", "SCI", "catégorie", "Date_entrée"]
        i = 0

        for elt in champs:
            nom_label = tk.Label(main_frame, text=elt, font=('Courier', self.fontGui, "bold"), bg=self.button_color
                                 ,
                                 fg=self.fg)
            nom_label.grid(column=0, row=i, sticky="EW")
            i +=1
        nom_label = tk.Label(main_frame, text="Nom du loctaire", font=('Courier', self.fontGui, "bold"), bg=self.button_color
                             ,
                             fg=self.fg)
        nom_label.grid(column=0, row=0, sticky="EW")

        selec_entry = ttk.Combobox(main_frame, textvariable=self.nom, state='readonly', style='custom.TCombobox')
        list_tenant = self.database.elt_table("nom", "tenant")
        selec_entry['values'] = list_tenant
        selec_entry.grid(column=1, row=0, sticky="EW")

        entries = [self.prenom, self.adresse, self.ville, self.tel, self.mail, self.sci, self.cat, self.date_entree]
        i = 1
        for elt in entries:
            entry = tk.Label(main_frame, textvariable=elt, font=('Courier', self.fontGui, "bold"), bg=self.button_color
                             , fg=self.fg)
            entry.grid(column=1, row=i, sticky="EW")
            i += 1

        blank_label = tk.Label(main_frame, bg=self.button_color
                               )
        blank_label.grid(column=0, row=self.fontGui, columnspan=2)

        button_back = tk.Button(main_frame, text="RETOUR", command=self.quit, bg=self.bg, fg=self.fg,
                                font=('Courier', self.fontGui, "bold"), bd=0, relief=tk.GROOVE)
        button_back.grid(column=1, row=10, sticky="NSEW")

    def observer(self, *args):
        watch = self.nom.get()
        result = self.database.info_table(watch.split(" ")[0])
        self.prenom.set(result[0][1])
        self.adresse.set(result[0][2])
        self.ville.set(result[0][3])
        self.tel.set(result[0][4])
        self.mail.set(result[0][5])
        self.sci.set(result[0][6])
        self.date_entree.set(result[0][8])
        print(result[0][7])
        if result[0][7] == 0:
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
        self.master.geometry("310x300")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")
        self.database = sql_database()
        self.bg, self.button_color, self.fg, self.fg_size, _, self.fontGui = Gui_aspect().setting()
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

        main_frame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE, bg=self.button_color
                              )
        main_frame.grid(column=0, row=0, sticky="NSEW")

        label_name = tk.Label(main_frame, text="Locataire", bg=self.button_color
                              , font=('Courier', self.fontGui, "bold"), fg=self.fg)
        label_name.grid(column=0, row=0, sticky="W")

        selec_name_entry = ttk.Combobox(main_frame, textvariable=self.tenant_name, state='readonly', style='custom.TCombobox')
        selec_name_entry.grid(column=1, row=0, sticky="NSEW")

        select_name = self.database.elt_table("nom", "tenant")
        selec_name_entry['values'] = select_name

        label_loyer_base = tk.Label(main_frame, text="Base loyer", bg=self.button_color
                                    , font=('Courier', self.fontGui, "bold"), fg=self.fg)
        label_loyer_base.grid(column=0, row=1, sticky="W")

        aff_loyer_base = tk.Label(main_frame, textvariable=self.base_loyer, bg=self.button_color
                                  , font=('Courier', 12, "bold"), fg=self.fg)
        aff_loyer_base.grid(column=1, row=1, sticky="NSEW")

        label_indice = tk.Label(main_frame, text="Nouvel indice", bg=self.button_color
                                , font=('Courier', self.fontGui, "bold"), fg=self.fg)
        label_indice.grid(column=0, row=3, sticky="NSEW")

        Entry_indice = tk.Entry(main_frame, textvariable=self.new_indice, bg="#4F7292", fg='white')
        Entry_indice.grid(column=1, row=3, sticky="NSEW")

        label_new_rent = tk.Label(main_frame, text="Nouveau loyer", bg=self.button_color
                                  , font=('Courier', self.fontGui, "bold"), fg=self.fg)
        label_new_rent.grid(column=0, row=4, sticky="NSEW")

        aff_new_rent = tk.Label(main_frame, textvariable=self.new_rent, bg=self.button_color
                                , font=('Courier', 12, "bold"), fg='red')
        aff_new_rent.grid(column=1, row=4)

        label_blank = tk.Label(main_frame, bg=self.button_color
                               )
        label_blank.grid(column=1, row=6, sticky="NSEW")

        label_validation = tk.Button(main_frame, text="VALIDER", command=self.validation, borderwidth=2,
                                     relief=tk.GROOVE, bg=self.bg
                                     , font=('Courier', self.fontGui, "bold"), fg=self.fg)
        label_validation.grid(column=1, row=7, sticky="NSEW")

        label_blank = tk.Label(main_frame, bg=self.button_color
                               )
        label_blank.grid(column=1, row=8, sticky="NSEW")

        label_retour = tk.Button(main_frame, text="RETOUR", command=self.quitter, borderwidth=2, relief=tk.GROOVE,
                                 bg=self.bg, font=('Courier', self.fontGui, "bold"), fg=self.fg)
        label_retour.grid(column=1, row=self.fontGui, sticky="NSEW")

    def observer(self, *args):
        watch = self.tenant_name.get()
        base_loyer = self.database.one_elt("base_loyer", "location", watch.split(" ")[0])[0][0]
        self.base_loyer.set(f'{float(base_loyer):0.2f} €')

    def observer_2(self, *args):
        if not self.tenant_name.get():
            self.new_rent.set("En attente du locataire")

        else:
            try:
                new_indice = self.new_indice.get()
                pattern = re.compile(r"(^\d+.\d{2})")
                base_rent = pattern.search(self.base_loyer.get())
                base_rent = base_rent.group(0)
                watch = self.tenant_name.get()
                base_indice = self.database.one_elt("indice_base", "location", watch.split(" ")[0])[0][0]
                self.new_rent.set(f"{(float(base_rent) * float(new_indice) / float(base_indice)):0.2f} €")
            except ValueError as e:
                print(e)

    def validation(self):

        pattern = re.compile(r"(^\d+.?|\d{2})")
        if re.match(pattern, self.new_indice.get()):
            num = re.compile(r"(\d+.\d+)")
            new_rent = num.search(self.new_rent.get())
            new_rent = new_rent.group(0)
            watch = self.tenant_name.get()
            print(new_rent, watch.split(" ")[0])
            print(type(new_rent))
            self.database.maj_rent_request(float(new_rent), watch.split(" ")[0])
            messagebox.showinfo("Information", "Loyer enregistré")
            print("done")
        else:
            print(type(self.new_indice.get()))
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
        self.bg, self.button_color, self.fg, self.fg_size, _, self.fontGui = Gui_aspect().setting()
        self.combostyle = ttk.Style()
        self.combostyle.theme_use('custom.TCombobox')
        # variables
        self.tenant_name = tk.StringVar()
        self.new_indice = tk.IntVar()
        self.date = date.today()
        # widget label

        main_frame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE, bg=self.button_color
                              )
        main_frame.grid(column=0, row=0, sticky="NSEW")

        label_indice_particulier = tk.Label(main_frame, text="Indice particulier", borderwidth=2, relief=tk.GROOVE,
                                            bg=self.bg
                                            , font=('Courier', self.fontGui, "bold"), fg=self.fg)
        label_indice_particulier.grid(column=1, row=0, sticky="NSEW")
        label_indice_particulier.bind("<Button-1>", self.callback_particulier)

        label_indice_pro = tk.Label(main_frame, text="Indice professionel", borderwidth=2, relief=tk.GROOVE,
                                    bg=self.bg, font=('Courier', self.fontGui, "bold"), fg=self.fg)
        label_indice_pro.grid(column=1, row=1, sticky="NSEW")
        label_indice_pro.bind("<Button-1>", self.callbackone_professionel)

        label_blank = tk.Label(main_frame, bg=self.button_color
                               )
        label_blank.grid(column=1, row=2, sticky="NSEW")

        label_name = tk.Label(main_frame, text="Locataire", bg=self.button_color
                              , font=('Courier', self.fontGui, "bold"), fg=self.fg)
        label_name.grid(column=0, row=3, sticky="W")

        selec_name_entry = ttk.Combobox(main_frame, textvariable=self.tenant_name, state='readonly', style='custom.TCombobox')
        selec_name_entry.grid(column=1, row=3, sticky="NSEW")

        select_name = self.database.elt_table("nom", "tenant")
        selec_name_entry['values'] = select_name

        label_blank = tk.Label(main_frame, bg=self.button_color
                               )
        label_blank.grid(column=1, row=4, sticky="NSEW")

        label_indice_new = tk.Label(main_frame, text="Nouvelle indice", bg=self.button_color
                                    , font=('Courier', self.fontGui, "bold"), fg=self.fg)
        label_indice_new.grid(column=0, row=5, sticky="NSEW")

        entry_indice = tk.Entry(main_frame, textvariable=self.new_indice, bg="#4F7292", fg='white')
        entry_indice.grid(column=1, row=5, sticky="NSEW")

        label_blank = tk.Label(main_frame, bg=self.button_color
                               )
        label_blank.grid(column=1, row=6, sticky="NSEW")

        label_validation = tk.Button(main_frame, text="ENVOYER", command=self.validation, borderwidth=2,
                                     relief=tk.GROOVE, bg=self.bg
                                     , font=('Courier', self.fontGui, "bold"), fg=self.fg)
        label_validation.grid(column=1, row=7, sticky="NSEW")

        label_blank = tk.Label(main_frame, bg=self.button_color
                               )
        label_blank.grid(column=1, row=8, sticky="NSEW")


        label_retour = tk.Button(main_frame, text="RETOUR", command=self.quitter, borderwidth=2, relief=tk.GROOVE,
                                 bg=self.bg, font=('Courier', self.fontGui, "bold"), fg=self.fg)
        label_retour.grid(column=1, row=self.fontGui, sticky="NSEW")

    @staticmethod
    def callback_particulier(v):
        webbrowser.open_new(r"https://www.insee.fr/fr/statistiques/serie/001515333")

    @staticmethod
    def callbackone_professionel(v):
        webbrowser.open_new(r"https://www.insee.fr/fr/statistiques/serie/001532540")

    def check_entry(self):
        if self.tenant_name.get() == "" or self.new_indice.get() == 0:
            messagebox.showinfo("Attention", "Champs vide")
            return False

        elif not Verification(self.new_indice.get()).verification_indice():
            messagebox.showinfo("Attention", "Valeur incorrecte")
            return False

        else:
            return True

    def validation(self):
        if not self.check_entry():
            return "erreur de champs"

        elif self.check_entry():
            directory = functions.directory()
            config = functions.config_data()
            name = self.tenant_name.get()
            self.letter_pdf(name.split(" ")[0], directory, config)

    def letter_pdf(self, index, directory, config):

        result = self.database.letter_request(index)
        year = str(self.date.year)
        path_dir = directory.joinpath("indexation", year)
        path_dir.mkdir(parents=True, exist_ok=True)
        path = path_dir.joinpath("indexation_" + f"{result[0][1]}_{result[0][2]}" + "_" + year + ".pdf")
        pdf = canvas.Canvas(str(path))
        month = str(self.date.month + 1)
        day = 1
        print(result[0])
        pdf_gen = IndexLetter(pdf, nom=result[0][1], prenom=result[0][2], adresse=result[0][3], ville=result[0][4],
                               loyer=result[0][8], charge=result[0][9], day=day, month=month, year=year,
                               sci_nom=result[0][7], sci_adresse=result[0][12], sci_cp_ville=result[0][13],
                               sci_tel=result[0][14], sci_mail=result[0][15], sci_siret=result[0][16],
                               indice_base=result[0][5], indice_new=self.new_indice.get(), cat=result[0][10],
                              date_entree=result[0][18])

        pdf_gen.generator()
        mail = send_mail("Lettre d'indexation", config["master_mail"], config["password"], result[0][17], config["SMTP"],
                         config["port"], path)
        mail.send()

    def quitter(self):
        self.destroy()
        MainGui().mainloop()


class ConfigGUI(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title("Configuration")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.geometry("310x500")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")
        self.config = self.config_files()
        self.bg, self.button_color, self.fg, self.fg_size, self.tableau, self.fontGui = Gui_aspect().setting()
        # variables
        self.master_mail_var = tk.StringVar()
        self.master_mail_var.set(self.config["master_mail"])
        self.password_var = tk.StringVar()
        self.password_var.set(self.config["password"])
        self.smtp_var = tk.StringVar()
        self.smtp_var.set(self.config['SMTP'])
        self.port_var = tk.StringVar()
        self.port_var.set(self.config["port"])

        self.bg_color = tk.StringVar()
        self.bg_color.set(self.config['interface']['bg'])
        self.btn_color = tk.StringVar()
        self.btn_color.set(self.config['interface']['button_color'])
        self.fg_color = tk.StringVar()
        self.fg_color.set(self.config['interface']['fg'])
        self.tableau_color = tk.StringVar()
        self.tableau_color.set(self.config['interface']['tableau'])

        self.font_size = tk.IntVar()
        self.font_size.set(self.config['interface']['fg_size'])
        self.font_gui = tk.IntVar()
        self.font_gui.set(self.config['interface']['font_gui'])

        # Widget
        main_frame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE, bg=self.button_color)
        main_frame.grid(column=0, row=0, sticky="NSEW")

        main_frame.columnconfigure(0, weight=0)
        main_frame.columnconfigure(1, weight=1)

        master_mail_label = tk.Label(main_frame, text="email du compte", font=('Courier', self.fontGui, "bold"), bg=self.button_color
                                     , fg=self.fg)
        master_mail_label.grid(column=0, row=0, sticky="NSEW")

        master_mail_entry = tk.Entry(main_frame, textvariable=self.master_mail_var, bg="#4F7292", fg='white')
        master_mail_entry.grid(column=1, row=0, sticky="NSEW")

        password_label = tk.Label(main_frame, text="password du compte", font=('Courier', self.fontGui, "bold"), bg=self.button_color
                                  , fg=self.fg)
        password_label.grid(column=0, row=1, sticky="NSEW")

        password_entry = tk.Entry(main_frame, textvariable=self.password_var, bg="#4F7292", fg='white')
        password_entry.grid(column=1, row=1, sticky="NSEW")

        smtp_label = tk.Label(main_frame, text="SMTP", font=('Courier', self.fontGui, "bold"), bg=self.button_color
                              , fg=self.fg)
        smtp_label.grid(column=0, row=2, sticky="NSEW")

        smtp_entry = tk.Entry(main_frame, textvariable=self.smtp_var, bg="#4F7292", fg='white')
        smtp_entry.grid(column=1, row=2, sticky="NSEW")

        port_label = tk.Label(main_frame, text="port", font=('Courier', self.fontGui, "bold"), bg=self.button_color
                              , fg=self.fg)
        port_label.grid(column=0, row=3, sticky="NSEW")

        port_entry = tk.Entry(main_frame, textvariable=self.port_var, bg="#4F7292", fg='white')
        port_entry.grid(column=1, row=3, sticky="NSEW")

        blank_label = tk.Label(main_frame, bg=self.button_color)
        blank_label.grid(column=0, row=4, columnspan=2, sticky="NSEW")

        bg_label = tk.Button(main_frame, text="couleurs bouttons", command=self.change_color, font=('Courier', self.fontGui, "bold"), bg=self.button_color, fg=self.fg)
        bg_label.grid(column=0, row=5, sticky="NSEW")

        self.bg_entry = tk.Entry(main_frame, textvariable=self.bg_color, bg=self.bg_color.get(), fg='white')
        self.bg_entry.grid(column=1, row=5, sticky="NSEW")

        tableau_label = tk.Button(main_frame, text="couleurs du tableau", command=self.change_color_4, font=('Courier',
                                                                                                             self.fontGui, "bold"), bg=self.button_color, fg=self.fg)
        tableau_label.grid(column=0, row=6, sticky="NSEW")

        self.tableau_entry = tk.Entry(main_frame, textvariable=self.tableau_color, bg=self.tableau_color.get(), fg='white')
        self.tableau_entry.grid(column=1, row=6, sticky="NSEW")

        butt_label = tk.Button(main_frame, text="couleurs du fond", command=self.change_color_2, font=('Courier', self.fontGui, "bold"), bg=self.btn_color.get(), fg=self.fg)
        butt_label.grid(column=0, row=7, sticky="NSEW")

        self.button_entry = tk.Entry(main_frame, textvariable=self.btn_color, bg=self.btn_color.get(), fg='white')
        self.button_entry.grid(column=1, row=7, sticky="NSEW")

        font_color = tk.Button(main_frame, text="couleurs des font", command=self.change_color_3, font=('Courier', self.fontGui, "bold"), bg=self.button_color, fg=self.fg)
        font_color.grid(column=0, row=8,sticky="NSEW")

        self.font_entry = tk.Entry(main_frame, textvariable=self.fg_color, bg=self.fg_color.get(), fg='white')
        self.font_entry.grid(column=1, row=8, sticky="NSEW")

        blank_label = tk.Label(main_frame, bg=self.button_color)
        blank_label.grid(column=0, row=9, columnspan=2, sticky="NSEW")

        size = [12, 13, 14, 15, 16]
        font_entry = ttk.Combobox(main_frame, textvariable=self.font_size, state="readonly")
        font_entry['values'] = size
        font_entry.grid(column=1, row=11, sticky="NSEW")

        font_size = tk.Label(main_frame, text="tableau font", font=('Courier', self.fontGui, "bold"), bg=self.button_color,
                             fg=self.fg)
        font_size.grid(column=0, row=11, sticky="NSEW")

        font_gui_size = tk.Label(main_frame, text="font gui", font=('Courier', self.fontGui, "bold"), bg=self.button_color,
                                 fg=self.fg)
        font_gui_size.grid(column=0, row=12, sticky="NSEW")

        size = [8, 9, 10, 11]
        font_entry = ttk.Combobox(main_frame, textvariable=self.font_gui, state="readonly")
        font_entry['values'] = size
        font_entry.grid(column=1, row=12, sticky="NSEW")

        blank_label = tk.Label(main_frame, bg=self.button_color)
        blank_label.grid(column=0, row=13, columnspan=2, sticky="NSEW")

        button_default = tk.Button(main_frame, text="PAR DEFAUT", command=self.default, borderwidth=2, relief=tk.GROOVE, bg=self.bg, font=('Courier',
                                                                                                                                           self.fontGui, "bold"), fg=self.fg)
        button_default.grid(column=0, row=14, sticky="NSEW")


        button_validation = tk.Button(main_frame, text="ENREGISTRER", command=self.mod_entry, borderwidth=2, relief=tk.GROOVE, bg=self.bg, font=('Courier',
                                                                                                                                                 self.fontGui, "bold"), fg=self.fg)
        button_validation.grid(column=1, row=14, sticky="NSEW")

        blank_label = tk.Label(main_frame, bg=self.button_color)
        blank_label.grid(column=0, row=15, columnspan=2, sticky="NSEW")

        button_exit = tk.Button(main_frame, text="RETOUR", command=self.quit, borderwidth=2, relief=tk.GROOVE, bg=self.bg, font=('Courier',
                                                                                                                                 self.fontGui, "bold"), fg=self.fg)
        button_exit.grid(column=1, row=16, sticky="NSEW")

    def quit(self):
        self.destroy()
        MainGui().mainloop()

    def check_color(self):
        check_color = [self.btn_color.get(), self.fg_color.get(), self.tableau_color.get(), self.font_size.get(), self.font_gui.get()]
        for i in check_color():
            if not Verification(i).verification_color():
                return False

    def mod_entry(self):

        self.config["master_mail"] = self.master_mail_var.get()
        self.config["password"] = self.password_var.get()
        self.config['SMTP'] = self.smtp_var.get()
        self.config["port"] = self.port_var.get()
        self.config['interface']['bg'] = self.bg_color.get()
        self.config['interface']['button_color'] = self.btn_color.get()
        self.config['interface']['fg'] = self.fg_color.get()
        self.config['interface']['tableau'] = self.tableau_color.get()
        self.config['interface']['fg_size'] = self.font_size.get()
        self.config['interface']['font_gui'] = self.font_gui.get()

        with open('config.json', 'w') as json_files:
            json.dump(self.config, json_files)
        print("mise à jour du fichier config")
        messagebox.showinfo("Information", "Modification(s) effectuée(s)")

    @staticmethod
    def config_files():
        with open('config.json', 'r') as json_files:
            return json.load(json_files)

    def default(self):
        print(self.config['default']['tableau'])
        self.bg_color.set(self.config['default']['bg'])
        self.bg_entry.config(bg=self.config['default']['bg'])
        self.btn_color.set(self.config['default']['button_color'])
        self.button_entry.config(bg=self.config['default']['button_color'])
        self.fg_color.set(self.config['default']['fg'])
        self.font_entry.config(bg=self.config['default']['fg'])
        self.tableau_entry.config(bg=self.config['default']['tableau'])
        self.tableau_color.set(self.config['default']['tableau'])
        self.font_size.set(self.config['default']['fg_size'])

    def change_color(self):
        colors = askcolor(title="Tkinter Color Chooser")
        self.bg_color.set(colors[1])
        self.bg_entry.config(bg=colors[1])


    def change_color_2(self):
        colors = askcolor(title="Tkinter Color Chooser")
        self.btn_color.set(colors[1])
        self.button_entry.config(bg=colors[1])

    def change_color_3(self):
        colors = askcolor(title="Tkinter Color Chooser")
        self.fg_color.set(colors[1])
        self.font_entry.config(bg=colors[1])

    def change_color_4(self):
        colors = askcolor(title="Tkinter Color Chooser")
        self.tableau_color.set(colors[1])
        self.tableau_entry.config(bg=colors[1])


class NewModSciGUI(tk.Frame):
    def __init__(self, value):
        tk.Frame.__init__(self)

        self.master.geometry("350x350")
        self.combostyle = ttk.Style()
        self.combostyle.theme_use('custom.TCombobox')
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")
        self.database = sql_database()
        self.bg, self.button_color, self.fg, self.fg_size,  _, self.fontGui = Gui_aspect().setting()
        # Variables
        self.name_var = tk.StringVar()
        self.adresse_var = tk.StringVar()
        self.city_var = tk.StringVar()
        self.tel_var = tk.StringVar()
        self.mail_var = tk.StringVar()
        self.siret_var = tk.StringVar()
        # Widget
        self.button_color\
            = "#1A5276"
        main_frame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE, bg=self.button_color
                              )
        main_frame.grid(column=0, row=0, sticky="NSEW")

        if value == 0:
            self.type_field = 0
            n = 1
            self.master.title("Modification sci")
            self.old_var = tk.StringVar()
            self.old_var.trace("w", self.observer)

            selec_entry = ttk.Combobox(main_frame, textvariable=self.old_var, state='readonly', style='custom.TCombobox')
            selec_entry.grid(column=1, row=0, sticky="NSEW", columnspan=2)

            sci_list = self.database.elt_table("nom", "sci")
            selec_entry['values'] = sci_list

        if value == 1:
            self.type_field = 1
            self.master.title("Nouvelle sci")
            n = 0

        champs = ["SCI", "Adresse", "CP/ville", "Tel", "Email", "SIRET"]
        i = 0

        for elt in champs:
            label = tk.Label(main_frame, text=elt, font=('Courier', self.fontGui, "bold"), bg=self.button_color
                             , fg=self.fg)
            label.grid(column=0, row=i + n, sticky="NSEW")
            i += 1

        entries = [self.name_var, self.adresse_var, self.city_var, self.tel_var, self.mail_var, self.siret_var,
                   self.add_sci]
        i = 0
        for elt in entries:
            entry = tk.Entry(main_frame, textvariable=elt, bg="#4F7292", fg='white')
            entry.grid(column=1, row=i + n, sticky="NSEW", columnspan=2)
            i += 1


        boutton_add = tk.Button(main_frame, text="VALIDER", command=self.add_sci, bg=self.bg, fg=self.fg, font=('Courier',
                                                                                                                self.fontGui, "bold"), bd=0, relief=tk.GROOVE)
        boutton_add.grid(column=1, row=6 + n, sticky="NSEW")

        boutton_quitter = tk.Button(main_frame, text="QUITTER", command=self.quit, bg=self.bg, fg=self.fg, font=('Courier',
                                                                                                                 self.fontGui, "bold"), bd=0, relief=tk.GROOVE)
        boutton_quitter.grid(column=2, row=6 + n, sticky="NSEW")

    def observer(self, *args):
        watch = self.old_var.get()
        result = self.database.info_sci(watch.split(" ")[0])


        self.name_var.set(result[0][1])
        self.adresse_var.set(result[0][2])
        self.city_var.set(result[0][3])
        self.tel_var.set(result[0][4])
        self.mail_var.set(result[0][5])
        self.siret_var.set(result[0][6])

    def check_entry(self):
        if self.name_var.get() == "" or self.adresse_var.get() == "" or self.city_var.get() == "":
            print("champs vide")
            messagebox.showinfo("Attention", "un ou plusieurs champs vides, validation impossible")
            return False

        elif not Verification(self.mail_var.get()).verification_mail() or\
            not Verification(self.tel_var.get()).verification_tel():

            messagebox.showinfo("Attention", "un ou plusieurs chamsp mal renseignée, validation impossible")
            return False

        else:
            return True

    def add_sci(self):
        if not self.check_entry():
            return "erreur de champs"

        elif self.check_entry():
            new_sci = sci(self.name_var.get().upper(), self.adresse_var.get(), self.city_var.get(),
                          self.tel_var.get(), self.mail_var.get(), self.siret_var.get())

            insert_sci = {'nom': new_sci.nom, 'adresse': new_sci.adresse, 'cp_ville': new_sci.cp_ville,
                          'tel': new_sci.tel, 'mail': new_sci.mail, 'siret': new_sci.siret}

            print({'nom': new_sci.nom, 'adresse': new_sci.adresse, 'cp_ville': new_sci.cp_ville,
                   'tel': new_sci.tel, 'mail': new_sci.mail, 'siret': new_sci.siret})

            if self.type_field == 0:
                id = self.old_var.get().split(" ")[0]
                self.database.update_entry(id, "sci", insert_sci)

            if self.type_field == 1:
                self.database.create_entry("sci", insert_sci)
                messagebox.showinfo("Information", "SCI enregistrée")

                with open('config.json', 'r') as json_files:
                    config = json.load(json_files)
                    print("Ouverture config")
                try:
                    print("tentative de remove")
                    config['sci'].remove(self.old_var.get().split(" ")[1])
                except AttributeError as e:
                    print("supression non realisée car création")
                finally:
                    print("ecriture de la sci")
                    config["sci"].append(new_sci.nom)
                    with open('config.json', 'w') as json_files:
                        json.dump(config, json_files)
                    print("sci rajouter au json")
                    #messagebox.showinfo("Information", "modification(s) effectué(es)")


    def quit(self):
        self.destroy()
        MainGui().mainloop()

class DelSciGui(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title("Supression SCI")
        self.master.geometry("350x350")
        self.combostyle = ttk.Style()
        self.combostyle.theme_use('custom.TCombobox')
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")
        self.database = sql_database()
        self.bg, self.button_color, self.fg, self.fg_size, _,  self.fontGui = Gui_aspect().setting()
        # variable creation
        self.nom_var = tk.StringVar()
        self.nom_var.set("Attention action definitive")
        # widget creation

        main_frame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE, bg=self.button_color
                              )
        main_frame.grid(column=0, row=0, sticky="NSEW")

        nom_label = tk.Label(main_frame, text="Nom de la sci", font=('Courier', self.fontGui, "bold"), bg=self.button_color
                             , fg=self.fg)
        nom_label.grid(column=0, row=0, sticky="EW")

        selec_entry = ttk.Combobox(main_frame, textvariable=self.nom_var, state='readonly', style='custom.TCombobox')
        selec_entry.grid(column=1, row=0, sticky="EW")
        sci_list = self.database.elt_table("nom", "sci")
        selec_entry['values'] = sci_list


        blank_label = tk.Label(main_frame, bg=self.button_color
                               )
        blank_label.grid(column=1, row=6, columnspan=2, sticky="NSEW")


        boutton_add = tk.Button(main_frame, text="Supprimer", command=self.del_entry, bg=self.bg, fg=self.fg,
                                font=('Courier', self.fontGui, "bold"), bd=0, relief=tk.GROOVE)
        boutton_add.grid(column=1, row=7, sticky="NSEW")

        blank_label = tk.Label(main_frame, bg=self.button_color
                               )
        blank_label.grid(column=1, row=8, columnspan=2, sticky="NSEW")

        boutton_quitter = tk.Button(main_frame, text="Quitter", command=self.quit, bg=self.bg, fg=self.fg,
                                    font=('Courier', self.fontGui, "bold"), bd=0, relief=tk.GROOVE)
        boutton_quitter.grid(column=1, row=self.fontGui, sticky="NSEW")

    def del_entry(self):
        if self.nom_var.get() != "Attention action definitive":
            index = self.nom_var.get().split(" ")[0]
            self.database.delete_entry("sci", index)
        with open('config.json', 'r') as json_files:
            config = json.load(json_files)
        print(self.nom_var.get().split(" ")[1])
        config["sci"].remove(self.nom_var.get().split(" ")[1])
        with open('config.json', 'w') as json_files:
            json.dump(config, json_files)
        messagebox.showinfo("Attention", "SCI supprimée")

    def quit(self):
        self.destroy()
        MainGui().mainloop()


if __name__ == "__main__":
    SplashScreen().mainloop()
