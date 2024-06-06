# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 16:38:50 2024

@author: gabsu
"""

import tkinter as tk
from tkinter import messagebox
import csv
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

class DonneesActions(tk.Tk):
    __slots__ = ['dico', 'dico2', 'fichier1', 'fichier2', 'nom_label', 'nombre_total_label', 'bouton_retour',
                 'libelle_actions', 'symboles_entreprises', 'labels', 'frame', 'label_text', 'ajouter_frame', 'ident_entry']

    def __init__(self):
        super().__init__()

        self.title("Mon Portefeuille")
        self.geometry("800x600")
        self.configure(bg="#f0f0f0")  # Couleur de fond de la fenêtre
        self.dico = {}
        self.dico2 = {}
        self.fichier1 = 'actiondata.csv'
        self.fichier2 = 'ident_nom.csv'
        self.lecture_data1()
        self.lecture_data2()
        self.afficher_symboles_entreprises()

    def lecture_data1(self):
        with open(self.fichier1, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            next(reader)  # Sauter la première ligne (en-têtes de colonnes)
            for ligne in reader:
                ident, nom, nombre, prix, date = ligne
                if ident not in self.dico:
                    self.dico[ident] = {'nom': nom, 'actions': []}
                self.dico[ident]['actions'].append({'nombre': int(nombre), 'prix': float(prix), 'date': date})

    def lecture_data2(self):
        with open(self.fichier2, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            next(reader)  # Sauter la première ligne (en-têtes de colonnes)
            for ligne in reader:
                ident, nom = ligne
                if ident not in self.dico2:
                    self.dico2[ident] = {'nom': nom}

    def afficher_details_action(self, ident):
        self.nettoyer_interface()

        self.details_frame = tk.Frame(self, bg="#f0f0f0")
        self.details_frame.pack(pady=20)

        self.nom_entreprise = self.dico[ident]['nom']
        self.nom_label = tk.Label(self.details_frame, text=f"Nom de l'entreprise : {self.nom_entreprise}", font=("Helvetica", 14), bg="#f0f0f0")
        self.nom_label.pack(anchor='w', pady=5)
        total_nombre = 0
        for action in self.dico[ident]['actions']:
            total_nombre += action['nombre']
            self.action_frame = tk.Frame(self.details_frame, bg="#e0f7fa", bd=2, relief="groove", padx=10, pady=10)
            self.action_frame.pack(fill="x", pady=5)

            self.date_label = tk.Label(self.action_frame, text=f"Date d'achat : {action['date']}", font=("Helvetica", 12), bg="#e0f7fa")
            self.date_label.grid(row=0, column=0, padx=5, pady=2, sticky='w')
            self.prix_label = tk.Label(self.action_frame, text=f"Prix d'achat : {action['prix']} $", font=("Helvetica", 12), bg="#e0f7fa")
            self.prix_label.grid(row=0, column=1, padx=5, pady=2, sticky='w')
            self.nombre_label = tk.Label(self.action_frame, text=f"Nombre d'actions achetées : {action['nombre']}", font=("Helvetica", 12), bg="#e0f7fa")
            self.nombre_label.grid(row=0, column=2, padx=5, pady=2, sticky='w')
        self.nombre_label = tk.Label(self.details_frame, text=f"Nombre total d'actions : {total_nombre}", font=("Helvetica", 14), bg="#f0f0f0")
        self.nombre_label.pack(anchor='center', pady=5)

        self.bouton_retour = tk.Button(self.details_frame, text="Retour", command=self.afficher_symboles_entreprises, font=("Helvetica", 12), bg="#4CAF50", fg="white")
        self.bouton_retour.pack(pady=20)

    def afficher_symboles_entreprises(self):
        self.nettoyer_interface()

        self.libelle_actions = tk.Label(self, text="Mes actions :", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
        self.libelle_actions.pack(pady=20)

        self.symboles_entreprises = tk.Frame(self, bg="#f0f0f0")
        self.symboles_entreprises.pack(pady=10)

        for ident, ligne in self.dico.items():
            nom_entreprise = ligne['nom']
            label_text = f"{nom_entreprise} ({ident})"
            self.label = tk.Label(self.symboles_entreprises, text=label_text, bg="#e0f7fa", font=("Helvetica", 12), padx=5, pady=5)
            self.label.pack(anchor='w', pady=2)
            self.label.bind("<Button-1>", lambda event, ident=ident: self.afficher_details_action(ident))

        self.bouton_pie_chart = tk.Button(self, text="Afficher le graphique en secteurs", command=self.afficher_pie_chart, font=("Helvetica", 12), bg="#2196F3", fg="white")
        self.bouton_pie_chart.pack(pady=20)

        self.bouton_ajouter_action = tk.Button(self, text="Ajouter une action", command=self.ajouter_action_interface, font=("Helvetica", 12), bg="#4CAF50", fg="white")
        self.bouton_ajouter_action.pack(pady=20)

    def ajouter_action_interface(self):
        self.nettoyer_interface()

        self.ajouter_frame = tk.Frame(self, bg="#f0f0f0")
        self.ajouter_frame.pack(pady=20)

        self.ident_label = tk.Label(self.ajouter_frame, text="Identité de l'entreprise :", font=("Helvetica", 14), bg="#f0f0f0")
        self.ident_label.pack(anchor='w', pady=5)
        self.ident_entry = tk.Entry(self.ajouter_frame, font=("Helvetica", 14))
        self.ident_entry.pack(anchor='w', pady=5)

        self.verifier_bouton = tk.Button(self.ajouter_frame, text="Vérifier", command=self.verifier_identite, font=("Helvetica", 14), bg="#4CAF50", fg="white")
        self.verifier_bouton.pack(pady=10)

        self.retour_bouton = tk.Button(self.ajouter_frame, text="Retour", command=self.afficher_symboles_entreprises, font=("Helvetica", 14), bg="#f44336", fg="white")
        self.retour_bouton.pack(pady=10)

    def verifier_identite(self):
        ident = self.ident_entry.get()

        if ident in self.dico2:
            self.afficher_champs_ajout(ident)
        else:
            messagebox.showerror("Erreur", "Identité de l'entreprise non trouvée. Veuillez réessayer.")

    def afficher_champs_ajout(self, ident):
        self.nettoyer_interface()

        self.ajouter_frame = tk.Frame(self, bg="#f0f0f0")
        self.ajouter_frame.pack(pady=20)

        # Ajoutez un label pour le nom de l'entreprise
        nom_entreprise = self.dico2[ident]['nom']
        self.nom_label = tk.Label(self.ajouter_frame, text=f"Nom de l'entreprise : {nom_entreprise}", font=("Helvetica", 14), bg="#f0f0f0")
        self.nom_label.pack(anchor='w', pady=5)
        
        self.nombre_label = tk.Label(self.ajouter_frame, text="Nombre d'actions :", font=("Helvetica", 14), bg="#f0f0f0")
        self.nombre_label.pack(anchor='w', pady=5)
        self.nombre_entry = tk.Entry(self.ajouter_frame, font=("Helvetica", 14))
        self.nombre_entry.pack(anchor='w', pady=5)

        self.prix_label = tk.Label(self.ajouter_frame, text="Prix d'achat :", font=("Helvetica", 14), bg="#f0f0f0")
        self.prix_label.pack(anchor='w', pady=5)
        self.prix_entry = tk.Entry(self.ajouter_frame, font=("Helvetica", 14))
        self.prix_entry.pack(anchor='w', pady=5)

        self.date_label = tk.Label(self.ajouter_frame, text="Date d'achat :", font=("Helvetica", 14), bg="#f0f0f0")
        self.date_label.pack(anchor='w', pady=5)
        self.date_entry = tk.Entry(self.ajouter_frame, font=("Helvetica", 14))
        self.date_entry.pack(anchor='w', pady=5)

        self.bouton_sauvegarder = tk.Button(self.ajouter_frame, text="Sauvegarder", command=lambda: self.sauvegarder_nouvelle_action(ident), font=("Helvetica", 12), bg="#4CAF50", fg="white")
        self.bouton_sauvegarder.pack(pady=20)

        self.bouton_retour = tk.Button(self.ajouter_frame, text="Retour", command=self.afficher_symboles_entreprises, font=("Helvetica", 12), bg="#4CAF50", fg="white")
        self.bouton_retour.pack(pady=20)

    def sauvegarder_nouvelle_action(self,ident):

        nom = self.dico2[ident]['nom']
        nombre = self.nombre_entry.get()
        prix = self.prix_entry.get()
        date = self.date_entry.get()

        # Vérification des entrées
        if not nombre or not prix or not date:
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
            return

        # Vérification du nombre d'actions (doit être un entier positif)
        if not nombre.isdigit() or int(nombre) <= 0:
            messagebox.showerror("Erreur", "Le nombre d'actions doit être un entier positif.")
            return

        # Vérification du prix d'achat (doit être un nombre flottant positif)
        prix_est_float = prix.replace('.', '', 1).isdigit() and prix.count('.') <= 1 and float(prix) > 0
        if not prix_est_float:
            messagebox.showerror("Erreur", "Le prix d'achat doit être un nombre flottant positif.")
            return

        # Vérification de la date (doit être au format jj/mm/aaaa)
        date_parts = date.split('/')
        if len(date_parts) != 3:
            messagebox.showerror("Erreur", "La date doit être au format jj/mm/aaaa.")
            return

        jour, mois, annee = date_parts
        if len(jour) != 2 or len(mois) != 2 or len(annee) != 4 or not jour.isdigit() or not mois.isdigit() or not annee.isdigit():
            messagebox.showerror("Erreur", "La date doit être au format jj/mm/aaaa.")
            return

        # Vérification supplémentaire pour valider la date (jj/mm/aaaa)
        jour = int(jour)
        mois = int(mois)
        annee = int(annee)
        self.current_dateTime = datetime.now()
        # Vérification supplémentaire pour valider la date (jj/mm/aaaa)
        jour = int(jour)
        mois = int(mois)
        annee = int(annee)
        if jour != self.current_dateTime.day or mois != self.current_dateTime.month or annee != self.current_dateTime.year:
            messagebox.showerror("Erreur", "La date doit être une date valide au format jj/mm/aaaa.")
            return

        nombre = int(nombre)
        prix = float(prix)
        nouvelle_action = {'nombre': nombre, 'prix': prix, 'date': date}

        if ident in self.dico:
            self.dico[ident]['actions'].append(nouvelle_action)
        else:
            self.dico[ident] = {'nom': self.dico2[ident]['nom'], 'actions': [nouvelle_action]}

        # Sauvegarder dans le fichier CSV
        with open(self.fichier1, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['ident', 'nom', 'nombre', 'prix', 'date'])
            for ident, data in self.dico.items():
                for action in data['actions']:
                    writer.writerow([ident, data['nom'], action['nombre'], action['prix'], action['date']])

        messagebox.showinfo("Succès", "L'action a été ajoutée avec succès.")
        self.afficher_symboles_entreprises()
        

    def afficher_pie_chart(self):
        self.nettoyer_interface()

        chart_frame = tk.Frame(self, bg="#f0f0f0")
        chart_frame.pack(pady=20)

        fig, ax = plt.subplots()
        labels = []
        sizes = []
        for ident, row in self.dico.items():
            total = sum(action['nombre'] for action in row['actions'])
            labels.append(row['nom'])
            sizes.append(total)

            plt.ioff()  
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        ax.axis('equal')

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)

        bouton_retour = tk.Button(chart_frame, text="Retour", command=self.afficher_symboles_entreprises, font=("Helvetica", 12), bg="#4CAF50", fg="white")
        bouton_retour.pack(pady=20)

    def nettoyer_interface(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = DonneesActions()
    app.mainloop()