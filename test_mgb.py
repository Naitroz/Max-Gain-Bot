import yfinance as yf
import pandas as pd
"""
msft = yf.Ticker("MSFT")
dates = []
dates_str = []
val_open = []
val_close = []
print(msft.history(period="1mo"))
print(type(msft.history(period="1mo"))) 
dico_msft = msft.history(period="1mo").to_dict()
print(dico_msft)
print(dico_msft.keys())
print(dico_msft["Open"].keys())
for cle,val in dico_msft["Open"].items():
    print(cle.date())
    dates.append(cle.date())
    dates_str.append(f"{cle.day}-{cle.month}-{cle.year}")
    val_open.append(dico_msft["Open"][cle])
    val_close.append(dico_msft["Close"][cle])
print(dates)
print(dates_str)
print(dates[0] == dates[1])
print(dates[0] < dates[1])
print(dates[0] > dates[1])
print(val_open)
print("------------")
print(val_close)"""

"série arma/arima"

class Action:

    __slots__ = ["nom_action","periode","dates","val_open","val_close","val_volume","liste_maxi_locaux","liste_min_locaux"]

    def __init__(self,nom_action,periode):
        self.nom_action = nom_action
        self.periode = periode # periodes possibles : 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max.
        self.dates = [] 
        self.val_open = []
        self.val_close = []
        self.val_volume = []
        self.extraire_donnees()
    
    def __str__(self):
        message = f"Action : {self.nom_action}\nSur une période de {self.periode}\nListe des dates : {self.dates}\nListe des valeurs à l'ouverture : {self.val_open}\nListe des valeurs à la fermeture : {self.val_close}\nListe des volumes : {self.val_volume}"
        return message

    def extraire_donnees(self):
        data_action = yf.Ticker(self.nom_action)
        dico_data_action = data_action.history(period=self.periode).to_dict()
        for cle,val in dico_data_action["Open"].items():
            self.dates.append(cle.date())
            self.val_open.append(dico_data_action["Open"][cle])
            self.val_close.append(dico_data_action["Close"][cle])
            self.val_volume.append(dico_data_action["Volume"][cle])

    def trouve_max_min(self):
        self.liste_maxi_locaux = [] # est-ce qu'il faut la déclarer avant/ la mettre dans le slot
        self.liste_min_locaux = []
        liste_val_jours = [(self.val_open[0] + self.val_close[0]) / 2]
        if len(self.val_open) > 2:
            val_jour1 = (self.val_open[1] + self.val_close[1]) / 2
            if val_jour1 > liste_val_jours[0]:
                ascendant = True
                self.liste_min_locaux.append(liste_val_jours[0])
            else:
                ascendant = False
                self.liste_maxi_locaux.append(liste_val_jours[0])
            liste_val_jours.append(val_jour1)
            for i in range(2, len(self.val_open)):
                val_jour = (self.val_open[i] + self.val_close[i]) / 2
                liste_val_jours.append(val_jour)
                if val_jour > liste_val_jours[i-1] and ascendant == False:
                    self.liste_min_locaux.append(liste_val_jours[i-1])
                    ascendant = True
                elif val_jour < liste_val_jours[i-1] and ascendant == True:
                    self.liste_maxi_locaux.append(liste_val_jours[i-1])
                    ascendant = False
            if liste_val_jours[-1] > liste_val_jours[-2]:
                self.liste_maxi_locaux.append(liste_val_jours[-1])
            elif liste_val_jours[-1] < liste_val_jours[-2]:
                self.liste_min_locaux.append(liste_val_jours[-1])

if __name__ == "__main__":
    test_action = Action("MSFT","1mo")
    print(test_action)
    test_action.trouve_max_min()
