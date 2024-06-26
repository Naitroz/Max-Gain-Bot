# -*- coding: utf-8 -*-
"""
Created on Tue May  7 16:13:46 2024

@author: gabin cauchi
"""

import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import csv
from math import inf
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time
from test_mgb import Action
import fonctions as fct
import moyenne_qui_marche as mb





class FenetrePrincipale(tk.Tk):
    
    __slots__ = ["liste_actions","Combo","valeurs","temps","fiabilite","conseil","temporalite","timer_thread","bouton1",
                 "bouton2","bouton3","bouton4","bouton5","saisie1","saisie2","label1","label2","label3","label4",
                 "label5","label6","label7","choix","radio1","radio2","radio3","radio4","figure","ax"]
    
    def __init__(self):        
        super().__init__()
        self.title("Trading Bot")
        self.geometry("500x600")
        self.liste_actions = ["AAPL","AMZN","GOOGL","FB","MSFT","TSLA","V"]
        self.date = []
        self.valeurs = []
        self.volume = []
        self.ordonnees_ind = []
        self.abscisses_ind = []
        self.conseil = "Investir !"
        self.date1 = []
        self.fiabilite = 0
        self.periode = 0
        self.temporalite = "jour"
        self.action_choisie = ""
        self.creer_widget()
        self.afficher_courbe()
        self.timer_thread1 = threading.Thread(target=self.actualisation_periodique)
        self.timer_thread1.daemon = True
        self.timer_thread1.start()
        self.timer_thread2 = threading.Thread(target=self.message_indicateur)
        self.timer_thread2.daemon = True
        self.timer_thread2.start()


    def creer_widget(self) :       
        """
        Permet de créer les différents widgets qui figurent dans l'interface utilisateur (IHM)
        args : 
        return : 
        """

        #création du widget de sélection de l'action
        self.Combo = ttk.Combobox(self, values = self.liste_actions)
        self.Combo.set("Pick an Action")
        self.Combo.grid(row = 0, column = 0)
        self.Combo.bind("<<ComboboxSelected>>", self.choix_action)
        
        

        #création des widgets boutons
        self.bouton1 = tk.Button(self, text = "Mon porte-feuille")
        self.bouton1.grid(row = 0,column = 2)

        self.bouton2 = tk.Button(self, text = "Acheter")
        self.bouton2.grid(row = 6,columnspan = 2)

        self.bouton3 = tk.Button(self, text = "Vendre")
        self.bouton3.grid(row = 7,column = 0, columnspan = 2)

        self.bouton4 = tk.Button(self, text = "Choisir")
        self.bouton4.grid(row = 3,column = 2)
        self.bouton4.bind('<Button-1>', self.choix_indicateur)

        self.bouton5 = tk.Button(self, text = "Actualiser")
        self.bouton5.bind('<Button-1>',self.actualiser)
        self.bouton5.grid(row = 0,column = 1)

        #création des widgets de saisie
        self.saisie1 = tk.Entry(self)
        self.saisie1.grid(row= 5, column = 1)

        self.saisie2 = tk.Entry(self)
        self.saisie2.grid(row= 2, column = 2)
        self.saisie2.insert(0,"Paramètre indicateur")

        #création des widgets de label
        self.label1 = tk.Label(self, text = "Quantité : ")
        self.label1.grid(row = 5,column = 0)

        self.label2 = tk.Label(self, text = "Conseil : ")
        self.label2.grid(row = 5,column = 2)


        self.label3 = tk.Label(self, text = "Fiabilité : ")
        self.label3.grid(row = 7,column = 2)

        self.label4 = tk.Label(self, text = self.conseil, font = "Helvetica 10 bold")
        self.label4.grid(row = 6,column = 2)

        self.label5 = tk.Label(self, text = f"{self.fiabilite} %", font = "Helvetica 10 bold")
        self.label5.grid(row = 8,column = 2)

        self.label6 = tk.Label(self, text = "")
        self.label6.grid(row = 4,column = 2)

        self.label7 = tk.Label(self, text = "")
        self.label7.grid(row = 4,column = 0)

        self.choix = tk.StringVar()   # Variable commune aux 3 RadioButtons
        self.choix.set("Message")

        #création des radiobuttons
        self.radio1 = tk.Radiobutton(self, text= "Moyenne mobile", variable=self.choix, value="Moyenne mobile")
        self.radio1.grid(row= 2, column = 0)
        self.radio2 = tk.Radiobutton(self, text="Moyenne mobile exp", variable=self.choix, value="Moyenne mobile exp")
        self.radio2.grid(row = 2, column = 1)       
        self.radio3 = tk.Radiobutton(self, text="RSI", variable=self.choix, value="RSI")
        self.radio3.grid(row = 3, column = 0)
        self.radio4 = tk.Radiobutton(self, text="Volume", variable=self.choix, value="Volume")
        self.radio4.grid(row = 3, column = 1)
        
    def choix_action (self, event) :
        
        self.date = []
        self.valeurs = []
        self.action_choisie = self.Combo.get()
        print(self.action_choisie)
        donnees_action = Action(self.action_choisie, "1mo")
        for i in range(len(donnees_action.dates)) :
            self.date.append(donnees_action.dates[i]) 
            self.date.append(donnees_action.dates[i])
            self.valeurs.append(donnees_action.val_open[i]) 
            self.valeurs.append(donnees_action.val_close[i])
        #self.date = donnees_action.dates
        #self.valeurs = donnees_action.val_close
        print(len(self.date))
        print(len(self.valeurs))
        self.date1 = donnees_action.dates
        self.volume = donnees_action.val_volume
        self.actualiser("")
        
    def choix_indicateur (self,event) :        
                
        if self.choix.get() == "Moyenne mobile" :
            self.periode = int(self.saisie2.get())
            self.ordonnees_ind, self.abscisses_ind = mb.moyenne_mobile(self.date, self.valeurs, self.periode)
            
        elif self.choix.get() == "Moyenne mobile exp" :
            self.ordonnees_ind = fct.moyenne_mobile_exponentielle(self.valeurs, float(self.saisie2.get()))
            self.abscisses_ind = self.date
            
            if len(self.ordonnees_ind) != len(self.date) :
                self.date.pop(len(self.date)-1)
        
        elif self.choix.get() == "RSI" :
            self.periode = int(self.saisie2.get())
            self.abscisses_ind, self.ordonnees_ind = fct.RSI (self.date, self.valeurs, self.periode)
         
        elif self.choix.get() == "Volume" :
            fct.volume_trace(self.date1, self.volume)
            
        self.actualiser(event)
            
        #else :
            #self.bouton4.config(text = "Rechoisir")
            #self.saisie2.insert(0, "Choisir un paramètre valide")
            
            
        


    def afficher_courbe(self) :
        """
        Permet d'afficher une courbe matplotlib sur la base d'une liste de valeurs et de temps propre à l'action choisie
        args : 
        return : 
        """
        #création de la courbe matplotlib
        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.plot(self.date, self.valeurs)
        self.ax2 = self.ax.twinx()
        self.ax2.plot(self.abscisses_ind,self.ordonnees_ind, 'r--')
        self.ax.set_xlabel(f'Date ({self.temporalite})')
        self.ax.set_ylabel('Valeurs ($)')
        #insertion de la figure matplotlib dans un canvas
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=3)

    def actualiser(self,event) :
        """
        Permet d'actualiser la courbe de données en mettant à jour les listes de valeurs 
        et de temps de l'action puis d'afficher la courbe en conséquence
        args :
        return : 
        """

        self.afficher_courbe()

    def actualisation_periodique(self) :
        """
        Permet l'actualisation toutes les minutes de la courbe de données
        args :
        return :
        """
        
        
        while True :
            self.actualiser("")
            time.sleep(60) #attend une minute

    def message_indicateur(self) :
        message_prec = ""
        while True :
            message = self.choix.get()
            if message == "Moyenne mobile" and message != message_prec :
                self.saisie2.delete(0,tk.END)
                self.saisie2.insert(0,"Renseignez la période.")
                
            elif message == "Moyenne mobile exp" and message != message_prec:
                self.saisie2.delete(0,tk.END)
                self.saisie2.insert(0,"Renseignez le coefficient.")
                
            elif message == "RSI" and message != message_prec :
                self.saisie2.delete(0,tk.END)
                self.saisie2.insert(0,"Renseignez la période.(9 ou 14")
             
            elif message == "Volume" and message != message_prec:
                self.saisie2.delete(0,tk.END)
                self.saisie2.insert(0,"Appuyez sur Choisir.")
            message_prec = message
                
            time.sleep(0.01)
            
    
            
        




app = FenetrePrincipale()
app.mainloop()

