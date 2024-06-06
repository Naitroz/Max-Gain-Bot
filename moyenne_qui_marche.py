def moyenne_mobile(date,prix,periode):
    """
    A partir des données date et prix actions, calcul une moyenne sur un nombre de période 
    (jour) compris entre 2 et 15 

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
    if  2 <= periode <= 15 : 
        res = [] # lsite de la forme : elem 0 : date milieu période, valeur 1 : moyenne mobile de la période 
        res_date = []  
        if len(date) % periode != 0 : 
            
            for i in range (0,len(date) - 2*periode , 2*periode) : 
                elem_milieu = (periode // 2)  + i 
                somme = 0 
                for elem_periode in range(periode) : 
                    somme += prix[2*elem_periode + i] + prix[2*elem_periode + 1 + i]
                    
                moyenne = somme/(2*periode) 
                res.append(moyenne)
                res_date.append(date[elem_milieu])
            
            dernier_elem = len(date) % periode
            somme = 0 
            elem_milieu = periode // 2 
            a = 0
            for i in range(len(prix)-2*dernier_elem) : 

                somme += prix[-i]
                a += 1 
                    
            moyenne = somme/(a) 
            res.append(moyenne)
            res_date.append(date[- dernier_elem//2])
                
            return res, res_date 
                            
    else :  
        return ("La période doit être entre 2 et 15")

prix = [10,11,12,13,14,15,16,17,18,19,20,21,22]
date = ["1","2","3","4","5","6","7","8","9","10","11","12","13"]

print(moyenne_mobile(date,prix,4))



   