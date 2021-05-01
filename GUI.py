import tkinter as tk
from locataire import locataire

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

    def createWidgets(self):
        # création variable
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

        # création widgets
        mainFrame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE)
        mainFrame.columnconfigure(0, weight=0)
        mainFrame.columnconfigure(1, weight=1)
        nomLabel = tk.Label(mainFrame, text="Nom")
        prenomLabel = tk.Label(mainFrame, text="Prenom")
        adresseLabel = tk.Label(mainFrame, text="Adresse")
        villeLabel = tk.Label(mainFrame, text="ville")
        telLabel = tk.Label(mainFrame, text="Telephone")
        mailLabel = tk.Label(mainFrame, text="mail")
        sciLabel = tk.Label(mainFrame, text="SCI")
        loyerLabel = tk.Label(mainFrame, text="loyer")
        chargesLabel = tk.Label(mainFrame, text="charges")
        # Catégorieselecteur à faire

        nomEntry = tk.Entry(mainFrame, textvariable=self.nomVar)
        prenomEntry = tk.Entry(mainFrame, textvariable=self.prenomVar)
        adresseEntry = tk.Entry(mainFrame, textvariable=self.adresseVar)
        villeEntry = tk.Entry(mainFrame, textvariable=self.villeVar)
        telEntry = tk.Entry(mainFrame, textvariable=self.telVar)
        mailEntry = tk.Entry(mainFrame, textvariable=self.mailVar)
        sciEntry = tk.Entry(mainFrame, textvariable=self.sciVar)
        loyerEntry = tk.Entry(mainFrame, textvariable=self.loyerVar)
        chargesEntry = tk.Entry(mainFrame, textvariable=self.chargesVar)

        button = tk.Button(mainFrame, text="Valider la saisie", command=self.validation_tenant) # faire un bouton system etes vous sur de vouloir ajoueter le client
        button2 = tk.Button(mainFrame, text="Quitter et revenir")

        # position widgets
        mainFrame.grid(column=0, row=0, sticky="NSEW")
        nomLabel.grid(column=0, row=0, sticky="EW")
        nomEntry.grid(column=1, row=0, sticky="EW")
        prenomLabel.grid(column=0, row=1, sticky="EW")
        prenomEntry.grid(column=1, row=1, sticky="EW")
        adresseLabel.grid(column=0, row=2, sticky="EW")
        adresseEntry.grid(column=1, row=2, sticky="EW")
        villeLabel.grid(column=0, row=3, sticky="EW")
        villeEntry.grid(column=1, row=3, sticky="EW")
        telLabel.grid(column=0, row=4, sticky="EW")
        telEntry.grid(column=1, row=4, sticky="EW")
        mailLabel.grid(column=0, row=5, sticky="EW")
        mailEntry.grid(column=1, row=5, sticky="EW")
        mailLabel.grid(column=0, row=6, sticky="EW")
        mailEntry.grid(column=1, row=6, sticky="EW")
        sciLabel.grid(column=0, row=7, sticky="EW")
        sciEntry.grid(column=1, row=7, sticky="EW")
        loyerLabel.grid(column=0, row=8, sticky="EW")
        loyerEntry.grid(column=1, row=8, sticky="EW")
        chargesLabel.grid(column=0, row=9, sticky="EW")
        chargesEntry.grid(column=1, row=9, sticky="EW")

        button.grid(column=1, columnspan=1, row=10, sticky='NSEW')
        button2.grid(column=0, columnspan=1, row=10, sticky='NSEW')

    def validation_tenant(self):
        client1 = locataire(self.nomVar.get(), self.prenomVar.get(), self.adresseVar.get(),
                             self.villeVar.get(), self.telVar.get(), self.mailVar.get(),
                             self.sciVar.get(), self.loyerVar.get(),self.chargesVar.get())

        client1.save_contact()

        print(self.nomVar.get(), self.prenomVar.get(), self.adresseVar.get(), self.villeVar.get(), self.telVar.get(),
              self.mailVar.get(), self.sciVar.get(), self.loyerVar.get(), self.chargesVar.get())


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
    creation_gui().mainloop()
