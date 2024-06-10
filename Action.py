# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 21:20:26 2024

@author: khaloud
"""

class action :
    __slots__ = ['date','prix','nombre_actions']
    def __init__(self, nombre_actions,prix, date ):
        self.date= date
        self.prix=prix
        self.nombre_actions = nombre_actions
        
    