# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 16:39:30 2024

@author: khaloud
"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from ActionManeger import ActionManager
from Entreprise import entreprise
from Action import action
import pickle
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class DonneesActions(tk.Tk):
    __slots__ = ['nom_label', 'nombre_total_label', 'bouton_retour', 'libelle_actions', 'symboles_entreprises', 'labels', 'frame', 'label_text', 'ajouter_frame', 'ident_entry', 'nombre_actions_label', 'benefice_label']

    def __init__(self):
        super().__init__()

        self.title("Mon Portefeuille")
        self.geometry("800x600")
        self.configure(bg="#f0f0f0")  # Couleur de fond de la fenêtre
        file = open('portefeuille', 'rb')
        self.portefeuille = pickle.load(file)
        file.close()
        self.interface_principale()


    def interface_principale(self):
        self.nettoyer_interface()

        self.bouton_ajouter_action = tk.Button(self, text="Ajouter action", command=lambda: self.saisir_action_interface("acheter"), font=("Helvetica", 12), bg="#4CAF50", fg="white")
        self.bouton_ajouter_action.pack(pady=20)

        self.bouton_vendre_action = tk.Button(self, text="Vendre action", command=lambda: self.saisir_action_interface("vendre"), font=("Helvetica", 12), bg="#4CAF50", fg="white")
        self.bouton_vendre_action.pack(pady=20)

        self.bouton_actions_achetees = tk.Button(self, text="Actions achetees", command=lambda: self.afficher_symboles_entreprises("acheter"), font=("Helvetica", 12), bg="#4CAF50", fg="white")
        self.bouton_actions_achetees.pack(pady=20)

        self.bouton_actions_vendues = tk.Button(self, text="Actions vendues", command=lambda: self.afficher_symboles_entreprises("vendre"), font=("Helvetica", 12), bg="#4CAF50", fg="white")
        self.bouton_actions_vendues.pack(pady=20)

    def afficher_symboles_entreprises(self, transaction):
        if transaction == "acheter": 
            x = self.portefeuille.entreprises_achetes.items()
            text = "Mes actions achetees"
        else: 
            x = self.portefeuille.entreprises_vendus.items()
            text = "Mes actions vendues"
        self.nettoyer_interface()
        self.libelle_actions = tk.Label(self, text=text, font=("Helvetica", 16, "bold"), bg="#f0f0f0")
        self.libelle_actions.pack(pady=20)
        self.symb_entreprises_achetes = tk.Frame(self, bg="#f0f0f0") # frame pour organiser l'interface 
        self.symb_entreprises_achetes.pack(pady=10)
        for ident, entreprise in x:
            if entreprise.nb_actions_de_symb_tot != 0:
                nom_entreprise = entreprise.nom
                label_text = f"{nom_entreprise} ({ident})"
                self.label = tk.Label(self.symb_entreprises_achetes, text=label_text, bg="#e0f7fa", font=("Helvetica", 12), padx=5, pady=5)
                self.label.pack(anchor='w', pady=2)
                self.label.bind("<Button-1>", lambda event, ident=ident: self.afficher_details_action(ident, transaction))
         
        if transaction == "acheter" :
            self.nombre_label = tk.Label(self.symb_entreprises_achetes, text=f"Nombre totale d'actions achetees : {self.portefeuille.nb_actions_acheter_totale}", font=("Helvetica", 14), bg="#f0f0f0")
            self.nombre_label.pack(anchor='center', pady=5) 
            self.bouton_pie_chart = tk.Button(self.symb_entreprises_achetes, text="Afficher le graphique en secteurs", command=self.afficher_pie_chart, font=("Helvetica", 12), bg="#2196F3", fg="white")
            self.bouton_pie_chart.pack(pady=20) 
        else : 
            self.nombre_label = tk.Label(self.symb_entreprises_achetes, text=f"Nobmre totale d'actions vendues: {self.portefeuille.nb_actions_vendues_totale}", font=("Helvetica", 14), bg="#f0f0f0")
            self.nombre_label.pack(anchor='center', pady=5)
            self.nombre_label = tk.Label(self.symb_entreprises_achetes, text=f"Benefice totale d'actions vendues : {self.portefeuille.benefices_totale}", font=("Helvetica", 14), bg="#f0f0f0")
            self.nombre_label.pack(anchor='center', pady=5)
        self.retour_bouton = tk.Button(self.symb_entreprises_achetes, text="Retour", command=lambda : self.interface_principale(), font=("Helvetica", 14), bg="#f44336", fg="white")
        self.retour_bouton.pack(pady=10)

    def afficher_details_action(self, ident, transaction):
        if transaction == "acheter": 
            dico = self.portefeuille.entreprises_achetes
            self.prix = "Prix d'achat"
            self.date = "Date d'achat"
            self.nb = "Nombre d'actions achetées"
        else: 
            dico = self.portefeuille.entreprises_vendus
            self.prix = "Prix de vente"
            self.date = "Date de vente"
            self.nb = "Nombre d'actions vendues"
        self.nettoyer_interface()
        self.details_frame = tk.Frame(self, bg="#f0f0f0")
        self.details_frame.pack(pady=20)
        self.nom_entreprise = dico[ident].nom
        self.nom_label = tk.Label(self.details_frame, text=f"Nom de l'entreprise : {self.nom_entreprise}", font=("Helvetica", 14), bg="#f0f0f0")
        self.nom_label.pack(anchor='w', pady=5)
        for action in dico[ident].actions:
            self.action_frame = tk.Frame(self.details_frame, bg="#e0f7fa", bd=2, relief="groove", padx=10, pady=10)
            self.action_frame.pack(fill="x", pady=5)

            self.date_label = tk.Label(self.action_frame, text=f"{self.date} : {action.date}", font=("Helvetica", 12), bg="#e0f7fa")
            self.date_label.grid(row=0, column=0, padx=5, pady=2, sticky='w')
            self.prix_label = tk.Label(self.action_frame, text=f"{self.prix} : {action.prix} $", font=("Helvetica", 12), bg="#e0f7fa")
            self.prix_label.grid(row=0, column=1, padx=5, pady=2, sticky='w')
            self.nombre_label = tk.Label(self.action_frame, text=f"{self.nb} : {action.nombre_actions}", font=("Helvetica", 12), bg="#e0f7fa")
            self.nombre_label.grid(row=0, column=2, padx=5, pady=2, sticky='w')
        
        self.nombre_label = tk.Label(self.details_frame, text=f"Nombre d'total de l'entreprise : {dico[ident].nb_actions_de_symb_tot}", font=("Helvetica", 14), bg="#f0f0f0")
        self.nombre_label.pack(anchor='center', pady=5)
        
        if transaction != "acheter" :
            self.nombre_label = tk.Label(self.details_frame, text=f"Benefices d'actions : {dico[ident].benefices}", font=("Helvetica", 14), bg="#f0f0f0")
            self.nombre_label.pack(anchor='center', pady=5)
            
        
        self.bouton_retour = tk.Button(self.details_frame, text="Retour", command=lambda: self.afficher_symboles_entreprises(transaction), font=("Helvetica", 12), bg="#4CAF50", fg="white")
        self.bouton_retour.pack(pady=20)

    def saisir_action_interface(self, transaction):
        self.nettoyer_interface()
        self.ajouter_frame = tk.Frame(self, bg="#f0f0f0")
        self.ajouter_frame.pack(pady=20)
        self.ident_label = tk.Label(self.ajouter_frame, text="Identite de l'entreprise :", font=("Helvetica", 14), bg="#f0f0f0")
        self.ident_label.pack(anchor='w', pady=5)
        self.ident_entry = tk.Entry(self.ajouter_frame, font=("Helvetica", 14))
        self.ident_entry.pack(anchor='w', pady=5)
    
        self.verifier_bouton = tk.Button(self.ajouter_frame, text="Verifier", command=lambda: self.verifier_identite(transaction), font=("Helvetica", 14), bg="#4CAF50", fg="white")
        self.verifier_bouton.pack(pady=10)
    
        self.retour_bouton = tk.Button(self.ajouter_frame, text="Retour", command= lambda : self.interface_principale(), font=("Helvetica", 14), bg="#f44336", fg="white")
        self.retour_bouton.pack(pady=10)
        

    def verifier_identite(self, transaction):
        ident = self.ident_entry.get()
        if not ident:
            messagebox.showerror("Erreur", "le champ doit être rempli.")
            return
                
        if transaction == "vendre":
            if ident in self.portefeuille.entreprises_vendus.keys():
                self.afficher_champs_ajout(ident, transaction)
            else:
                messagebox.showerror("Erreur", "Vous n'avez pas acheté d'actions pour cette entreprise. Veuillez réessayer.")
        elif transaction == "acheter":
            if ident in self.portefeuille.entreprises_achetes.keys():
                self.afficher_champs_ajout(ident, transaction)
            else:
                messagebox.showerror("Erreur", "Identité de l'entreprise non trouvée. Veuillez réessayer.")
                
                
    def afficher_champs_ajout(self, ident, transaction):
        
        self.nettoyer_interface()
        
        self.current_dateTime = datetime.now()
        
        self.jour = self.current_dateTime.day
        self.mois = self.current_dateTime.month
        self.annee = self.current_dateTime.year
        
        
        if transaction == "acheter": 
            dico = self.portefeuille.entreprises_achetes
            self.prixx = "Prix d'achat"
            self.datee = f"Date d'achat : {self.jour}/{self.mois}/{self.annee}"

        else: 
            dico = self.portefeuille.entreprises_vendus
            self.prixx = "Prix de vente"
            self.datee = f"Date de vente : {self.jour}/{self.mois}/{self.annee}"
      
        date = f"{self.jour}/{self.mois}/{self.annee}"
        self.ajouter_frame = tk.Frame(self, bg="#f0f0f0")
    
        self.ajouter_frame.pack(pady=20)
    
        # Ajoutez un label pour le nom de l'entreprise
        nom_entreprise = dico[ident].nom
        self.nom_label = tk.Label(self.ajouter_frame, text=f"Nom de l'entreprise : {nom_entreprise}", font=("Helvetica", 14), bg="#f0f0f0")
        self.nom_label.pack(anchor='w', pady=5)
        
        self.nombre_label = tk.Label(self.ajouter_frame, text="Nombre d'actions :", font=("Helvetica", 14), bg="#f0f0f0")
        self.nombre_label.pack(anchor='w', pady=5)
        self.nombre_entry = tk.Entry(self.ajouter_frame, font=("Helvetica", 14))
        self.nombre_entry.pack(anchor='w', pady=5)
    
        self.prix_label = tk.Label(self.ajouter_frame, text= self.prixx, font=("Helvetica", 14), bg="#f0f0f0")
        self.prix_label.pack(anchor='w', pady=5)
        self.prix_entry = tk.Entry(self.ajouter_frame, font=("Helvetica", 14))
        self.prix_entry.pack(anchor='w', pady=5)
    
        self.date_label = tk.Label(self.ajouter_frame, text=self.datee, font=("Helvetica", 14), bg="#f0f0f0")
        self.date_label.pack(anchor='w', pady=5)

        self.bouton_sauvegarder = tk.Button(self.ajouter_frame, text="Sauvegarder", command=lambda: self.sauvegarder_nouvelle_action(ident, transaction,date), font=("Helvetica", 12), bg="#4CAF50", fg="white")
        self.bouton_sauvegarder.pack(pady=20)
    
        self.bouton_retour = tk.Button(self.ajouter_frame, text="Retour", command=lambda: self.afficher_symboles_entreprises(transaction), font=("Helvetica", 12), bg="#4CAF50", fg="white")
        self.bouton_retour.pack(pady=20)
    
    def sauvegarder_nouvelle_action(self, ident, transaction,date):
        nombre = self.nombre_entry.get()
        prix = self.prix_entry.get()
        # Vérification des entrées
        if not nombre or not prix:
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

        nombre = int(nombre)
        prix = float(prix) 
        
        # Debug print
        print(f"Debug: nombre={nombre}, type={type(nombre)}, prix={prix}, type={type(prix)}")
        
        if transaction == "acheter":
            self.portefeuille.acheter_actions(ident, nombre, prix, date)
            messagebox.showinfo("Succès", "L'action a été ajoutée avec succès.")
            self.afficher_symboles_entreprises(transaction)
        else :  
            self.portefeuille.entreprises_achetes[ident].update_entreprise()
            if int(nombre) > self.portefeuille.entreprises_achetes[ident].nb_actions_de_symb_tot: 
                messagebox.showerror("Erreur","Vous n'avez pas ce nombre d'actions pour les vendre")
            else : 
                self.portefeuille.vendre_actions(ident, nombre, prix, date)
                messagebox.showinfo("Succès", "L'action a été vendue avec succès.")
                self.afficher_symboles_entreprises(transaction)
    
    def nettoyer_interface(self):
        for widget in self.winfo_children():
            widget.destroy()     


    def afficher_pie_chart(self):
        self.nettoyer_interface()
        
        if self.portefeuille.nb_actions_acheter_totale != 0:
            self.labels = []
            self.sizes = []
            base_colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0','#ffb3e6']
    
            # Mise à jour des entreprises et collecte des données
            for k,e in self.portefeuille.entreprises_achetes.items():
                if e.nb_actions_de_symb_tot !=0 :
                    e.update_entreprise()
                    self.labels.append(k)
                    self.sizes.append(e.nb_actions_de_symb_tot)
    
            # Générer plus de couleurs si nécessaire
            n_colors = len(self.labels)
            if n_colors > len(base_colors):
                self.colors = plt.cm.tab20(np.linspace(0, 1, n_colors))
            else:
                self.colors = base_colors[:n_colors]
    
            # Vérification des valeurs dans self.sizes
            if len(self.labels) > 0:
                plt.ioff()
                fig, ax = plt.subplots()
                
                # Ajout des propriétés pour améliorer la lisibilité
                wedges, texts, autotexts = ax.pie(
                    self.sizes, 
                    labels=self.labels, 
                    colors=self.colors, 
                    autopct='%1.1f%%', 
                    startangle=140, 
                    wedgeprops=dict(width=0.3, edgecolor='w')
                )
                
                # Encadrer les labels pour éviter le chevauchement
                for text in texts:
                    text.set_bbox(dict(facecolor='white', alpha=0.8, edgecolor='none'))
                
                ax.axis('equal')  # Assure que le pie chart est dessiné comme un cercle.
        
                self.canvas = FigureCanvasTkAgg(fig, master=self)
                self.canvas.draw()
                self.canvas.get_tk_widget().pack(pady=20)
            
        else:
            self.label = tk.Label(self, text="Il n'y a pas des actions achetées", font=("Helvetica", 14), bg="#f0f0f0")
            self.label.pack(anchor='center', pady=5)
            
        self.bouton_retour = tk.Button(self, text="Retour", command=lambda: self.afficher_symboles_entreprises("acheter"), font=("Helvetica", 12), bg="#4CAF50", fg="white")
        self.bouton_retour.pack(pady=20)

if __name__ == "__main__":
    app = DonneesActions()
    app.mainloop()
    file = open('portefeuille', 'wb')
    pickle.dump(app.portefeuille, file)
    file.close()
