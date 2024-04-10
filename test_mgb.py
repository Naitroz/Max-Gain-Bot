import yfinance as yf
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
print(val_close)

"série arma/arima"
class Action:

    __slots__ = ["nom_action","periode","dates","val_open","val_close"]

    def __init__(self,nom_action,periode):
        self.nom_action = nom_action
        if periode == "1 mois":
            self.periode = "1mo"
        elif periode == "1 an":
            self.periode = "1ye"
        self.dates = []
        self.val_open = []
        self.val_close = []