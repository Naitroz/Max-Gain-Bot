# -*- coding: utf-8 -*-
"""
Created on Tue May  7 15:07:06 2024

@author: khaloud
"""

import tkinter as tk
import csv

class DonneesActions:
    def __init__(self):
        self.dico = {}
        self.fichier = 'actiondata.csv'
        self.lecture_data()
    
    def lecture_data(self):
        """
        Méthode pour lire les données à partir du fichier CSV et les stocker dans le dictionnaire.
        """
        with open(self.fichier, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            next(reader)  # Sauter la première ligne (en-têtes de colonnes)
            for ligne in reader:
                ident, nom, nombre, prix, date = ligne
                if ident not in self.dico:
                    self.dico[ident] = {'nom': nom, 'nombre': int(nombre), 'prix': int(prix), 'date': date}

    def afficher_details_action(self, row):
        """
        Méthode pour afficher les détails de l'action sélectionnée.
        """
        self.nettoyer_interface()
        self.nom_label = tk.Label(fenetre, text=f"Nom de l'entreprise : {row['nom']}")
        self.nom_label.grid(row=1, column=0, padx=5, pady=5)
        self.nombre_label = tk.Label(fenetre, text=f"Nombre d'actions : {row['nombre']}")
        self.nombre_label.grid(row=2, column=0, padx=5, pady=5)
        self.prix_label = tk.Label(fenetre, text=f"Prix d'achat : {row['prix']} $")
        self.prix_label.grid(row=3, column=0, padx=5, pady=5)
        self.date_label = tk.Label(fenetre, text=f"Date d'achat : {row['date']}")
        self.date_label.grid(row=4, column=0, padx=5, pady=5)
        self.bouton_retour = tk.Button(fenetre, text="Retour", command=self.afficher_symboles_entreprises)
        self.bouton_retour.grid(row=5, column=0, padx=5, pady=5)
        for widget in self.symboles_entreprises:
            widget.grid_forget()

    def afficher_symboles_entreprises(self):
        """
        Méthode pour afficher les symboles des entreprises dans l'interface.
        """
        self.nettoyer_interface()
        self.libelle_actions = tk.Label(fenetre, text="Mes actions :")
        self.libelle_actions.grid(row=0, column=0, padx=5, pady=5)
        self.symboles_entreprises = []
        for i, (ident, row) in enumerate(self.dico.items(), start=1):
            nom_entreprise = row['nom']
            label_text = f"{nom_entreprise} ({ident})"
            label = tk.Label(fenetre, text=label_text, bg="lightblue")
            label.grid(row=i, column=0, padx=5, pady=5)
            label.bind("<Button-1>", lambda event, row=row: self.afficher_details_action(row))
            self.symboles_entreprises.append(label)

    def nettoyer_interface(self):
        """
        Méthode pour nettoyer l'interface en détruisant tous les widgets.
        """
        for widget in fenetre.winfo_children():
            widget.destroy()

# Crée une fenêtre Tkinter
fenetre = tk.Tk()
fenetre.title("Mon Portefeuille")
fenetre.geometry("400x300")
# Crée une instance de la classe DonneesActions
donnees_actions = DonneesActions()

# Afficher les symboles des entreprises au démarrage
donnees_actions.afficher_symboles_entreprises()

# Lance la boucle principale Tkinter
fenetre.mainloop()
