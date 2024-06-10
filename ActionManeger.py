# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 21:16:30 2024

@author: khaloud
"""

import pickle
from Action import action
from Entreprise import entreprise 
import csv

class ActionManager:
    __slots__ = ['nb_actions_acheter_totale','entreprises_achetes' , 'nb_actions_vendues_totale','entreprises_vendus','benefices_totale']
    def __init__(self):
        self.nb_actions_acheter_totale = 0
        self.entreprises_achetes = {}
        self.nb_actions_vendues_totale = 0
        self.entreprises_vendus = {}  
        self.benefices_totale = 0
   
        
    def update_actions_acheter(self): # calcul le nombre total des actions achetes pour tous les entreprises
        nb_actions_tot = 0
        for e in self.entreprises_achetes.values(): # entreprise est un valeur de la dictionnaire entreprises achetes ( leur cle est son ident )et un instance de la classe entreprise 
            nb_actions_tot += e.nb_actions_de_symb_tot
        self.nb_actions_acheter_totale = nb_actions_tot
        
        

    def acheter_actions(self, ident, nb_actions, prix_achat, date_achat): # 
        self.entreprises_achetes[ident].actions.append(action(nb_actions, prix_achat, date_achat))
        nom= self.entreprises_achetes[ident].nom 
        self.remplire_vendue(ident,nom)
        
        # objet de l'entreprise . liste d'actions . append ( creer objet de l'action avec les 3 informations necessaires ) 
        self.entreprises_achetes[ident].update_entreprise()
        self.update_actions_acheter()
        
    def remplire_acheter(self, fichier):
         with open(fichier, newline="") as csvfile:
             reader = csv.reader(csvfile, delimiter=",")
             next(reader)  # Sauter la première ligne 
             for ligne in reader:
                 ident, nom = ligne
                 self.entreprises_achetes[ident] = entreprise(nom) # dictionaire le cle est un ident de l'entreprise et la valeur est instance de la classe entreprise
        
    def update_actions_vendre(self):
        nb_actions_tot = 0
        B=0 
        for e in self.entreprises_vendus.values():
            nb_actions_tot += e.nb_actions_de_symb_tot
            B+= e.benefices
        self.nb_actions_vendues_totale = nb_actions_tot
        self.benefices_totale = B
    
        
    def vendre_actions(self, ident, nb_actions, prix_vente, date_vente):
        self.entreprises_vendus[ident].actions.append(action(nb_actions, prix_vente, date_vente))
        # objet des entreprise deja achetes
        entreprise = self.entreprises_achetes[ident]
        prix_acheter = 0 
        enlever = False
        i=0
        while not enlever and i < len(entreprise.actions):
            if entreprise.actions[i].nombre_actions == nb_actions : # si le nombre actions deja achetes = nb_actions que je veux vendre
                prix_acheter = entreprise.actions[i].prix * nb_actions # prix acheter total
                entreprise.actions.pop(i) # enleve l'objet action  de la liste 
                enlever = True # fermer boucle
                self.entreprises_vendus[ident].benefices += (prix_vente*nb_actions) - prix_acheter
                    
            i += 1
                
                     
        if not enlever : 
            prix_acheter = 0
            vendue = 0 
            i =0
            while vendue != nb_actions and i < len(entreprise.actions):
                if nb_actions - vendue >= entreprise.actions[i].nombre_actions: # law nb_actions demande a vendre >= nombre action deja achete 
                    vendue += entreprise.actions[i].nombre_actions # vendue = nombre actions deja achete 
                    print (vendue)
                    prix_acheter += entreprise.actions[i].nombre_actions * entreprise.actions[i].prix # prix deja achetee
                    print (prix_acheter)
                    entreprise.actions.pop(i) # enleve l'objet action de la liste
                        
                elif nb_actions < entreprise.actions[i].nombre_actions: 
                    entreprise.actions[i].nombre_actions-= (nb_actions)
                    print(entreprise.actions[i].nombre_actions)
                    prix_acheter = entreprise.actions[i].prix 
                    print(prix_acheter)
                    vendue = nb_actions 
                    self.entreprises_vendus[ident].benefices += (prix_vente - prix_acheter)*nb_actions
                        
                else : 
                    prix_acheter += (entreprise.actions[i].nombre_actions - (nb_actions-vendue))*entreprise.actions[i].prix
                    print(prix_acheter)
                    entreprise.actions[i].nombre_actions -= (nb_actions - vendue)
                    print(entreprise.actions[i].nombre_actions)
                    vendue = nb_actions 
                    print(vendue)
                    self.entreprises_vendus[ident].benefices += (prix_vente*nb_actions) - prix_acheter
                i += 1
                    
        self.update_actions_vendre()
        entreprise.calcul_actions_tot()
        self.entreprises_vendus[ident].calcul_actions_tot()
        self.update_actions_acheter() 
        self.update_actions_vendre()
        
        
        
 
        
    def remplire_vendue(self,ident,nom):
        
        self.entreprises_vendus[ident] = entreprise(nom) 
         
                    
"""
if __name__ == "__main__":
    portefeuille = ActionManager()  # Utilisation de la syntaxe correcte pour instancier la classe
    portefeuille.remplire_acheter('ident_nom.csv')
    # Ouvrir un fichier pour stocker les données
    fichier = open('portefeuille', 'wb')
    # Enregistrer les informations dans ce fichier
    pickle.dump(portefeuille, fichier)
    # Fermer le fichier
    fichier.close()
    print("Fait")
"""
