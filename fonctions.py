import matplotlib.pyplot as plt


def liste_prix(prix_entre,prix_sorti) : 
    """
    Permet d'avoir une liste unique de prix des actions a partir des listes des cours d'entrée et de sortie

    Parameters
    ----------
    prix_entré : TYPE
        DESCRIPTION.
    prix_sorti : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    res = []
    
    for i in range(len(prix_entre)) : 
        res.append(prix_entre[i])
        res.append(prix_sorti[i])
        
    return res

def liste_date(date) : 
    """
    Permet d'avoir une liste unique des dates étudiés dans l'ordre des points des cours, car on a deux points pour une même date. 

    Parameters
    ----------
    prix_entré : TYPE
        DESCRIPTION.
    prix_sorti : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    res = []
    
    for i in range(len(date)) : 
        res.insert(date[i])
        res.insert(date[i])
    return res 
          

# Calcul de la moyenne exponentielle :  

def moyenne_mobile_exponentielle(prix, coef) :
    """
    A partir des données date et prix actions, calcul une moyenne exponentielle sur un nombre de période 
    (jour) compris entre 2 et 15 
    Va de la moyenne la plus ancienne a la plus récente

    Parameters
    ----------
     : TYPE
        DESCRIPTION.

    Returns
    si le nombre de periode est compris entre 2 et 15, la moyenne mobile sous forme de listes de listes date,valeur
    
    Sinon message d'erreur 
    -------
    None.

    """
    
    
    moyenne_exp = []
    if len(prix) > 0 : 
        alpha = coef  # Initialisation de la constante alpha
        moyenne_exp.append(prix[0])  # Initialisation de la première valeur de la MME
    
        for i in range(1, len(prix)) : 
                
            moyenne_exp.append(moyenne_exp[i-1] + alpha * (prix[i] - moyenne_exp[i - 1]))

    return moyenne_exp 
    
        
    
# Calcul de RSI :  
      
def RSI (date,prix,periode):
    """
    A partir des données dates et prix, calcul le RSI pour une période de 9 ou 14 jours selon la valeur de periode. 

    Parameters
    ----------
     liste date et prix 
     entier : la periode (9 ou 14) 

    Returns
    Valeur du RSI de chaque période, c'est à dire une valeur comprise entre 0 et 100
    
    -------
    None.

    """
    
    if  periode == 14 or periode == 9: 
         # lsite de la forme : elem 0 : date milieu période, valeur 1 : moyenne mobile de la période 
        if len(date) % periode != 0 : 
            
            for i in range (0,len(date) - 2*periode , 2*periode) : 
                
                moyenne_haut = 0 
                moyenne_bas = 0 
                coef_haut =  0
                coef_bas = 0 
                somme_haut = 0 
                somme_bas = 0 
                
                elem_milieu = periode // 2 
                date_considere = []
                
                date.append(date[i + elem_milieu])
                
                for j in range (2*periode-1) : 
                        
                    if prix[-2*periode+i+j] > prix[-2*periode+i+1+j] :
                            
                        coef_haut +=  1 
                        somme_haut += prix[-2*periode+i+j] 
                            
                    elif prix[-2*periode+i+j] < prix[-2*periode+i+1+j] :
                            
                        coef_bas += 1
                        somme_bas += prix[-2*periode+i+j] 
                    
                moyenne_haut =  somme_haut/coef_haut
                moyenne_bas = somme_bas/coef_bas 
                    
                RSI = 100 - 100/(1 + abs(moyenne_haut)/abs(moyenne_bas))
            
            # elements restants ne formants pas une périodes complète 
            
            if len(prix) % periode != 0 :
                
                dernier_elem = len(prix) % 2*periode
                moyenne_haut = 1
                moyenne_bas = 1
                coef_haut =  1
                coef_bas = 1
                somme_haut = 1
                somme_bas = 1
                
                date_considere.append(date[len(date) - 1])
                
                for i in range (dernier_elem) : 
                        
                    if prix[-2*periode+i] > prix[-2*periode+i+1] :
                            
                        coef_haut +=  1 
                        somme_haut += prix[-2*periode+i] 
                            
                    elif prix[-2*periode+i] < prix[-2*periode+i+1] :
                            
                        coef_bas += 1
                        somme_bas += prix[-2*periode+i] 
                    
                moyenne_haut =  somme_haut/coef_haut
                moyenne_bas = somme_bas/coef_bas 
                    
                RSI = 100 - 100/(1 + abs(moyenne_haut)/abs(moyenne_bas))
                
            return RSI, date_considere 
    
def volume_trace(date,volume) : 
    """
    Permet de representer les volumes d'échanges par joue
    """ 
    
    plt.bar(date, volume)
    plt.title('Evolution des volumes')
    plt.xlabel('date')
    plt.ylabel('volumes échangés ')
    plt.show()

# Exemple : 
     


# Autre idée rendement, PER, BPA


            
            
            
    
            