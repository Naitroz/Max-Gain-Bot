# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 21:17:19 2024

@author: khaloud
"""
from Action import action 

class entreprise: 
    __slots__ = ['nom','nb_actions_de_symb_tot' , 'prix_achatOUvent_tot','actions','benefices']
    def __init__(self, nom):
        self.nom = nom
        self.nb_actions_de_symb_tot = 0 
        self.prix_achatOUvent_tot = 0 
        self.actions = [] # on va stocker les instances de la classe actions [action 1 , action 2 , action 3 ]
        self.benefices = 0 
       
        
        
    def calcul_actions_tot(self): # calculer le nomb d'action total achete par un entreprise 
        nb_actions= 0 
        for e in self.actions:  # e est element de la liste self.actions et un instance de la calsse actions
           # print(f"Debug: nombre={e.nombre_actions}")
            nb_actions += int(e.nombre_actions )
        self.nb_actions_de_symb_tot = nb_actions 
        
    def calcul_prix_tot(self): 
        prix = 0 
        for e in self.actions: 
            prix += float(float(e.prix)*int(e.nombre_actions))
        self.prix_achatOUvent_tot = prix 
        
           
    
    def update_entreprise(self): 
        self.calcul_actions_tot()
        self.calcul_prix_tot()
        
        


