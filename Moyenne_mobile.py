"""

données sous la forme : [] 

3 liste : 
    
date 
prix entré 
prix sorti

"""
date = ["01/02","02/02","03/02","04/02","05/02"]
prix_entré = [12,16,12,16,10]
prix_sorti = [16,20,16,20,18]

def moyenne_mobile(date,prix_entré,prix_sorti,periode):
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
            
        if len(date) % periode != 0 : 
            
            for i in range (0,len(date) - periode , periode) : 
                elem_milieu = periode // 2 
                somme = 0 
                for elem_periode in range(periode) : 
                    somme +=  prix_entré[elem_periode + i] + prix_sorti[elem_periode + i]
                    
                moyenne = somme/(2*periode) 
                res.append([date[elem_milieu + i],moyenne])
            
            dernier_elem = len(date) % periode
            for i in range(dernier_elem) : 
                elem_milieu = periode // 2 
                somme = 0 
                
                for elem_periode in range(len(date)-1,len(date)-dernier_elem -1,-1) : 
                    somme += prix_entré[elem_periode] + prix_sorti[elem_periode]
                    
                moyenne = somme/(2*dernier_elem) 
                
                res.append([date[len(date)-elem_milieu],moyenne])
                
            return(res)
        
        else : 
            for i in range (0,len(date), periode) : 
                elem_milieu = periode // 2 
                somme = 0 
                for elem_periode in range(periode) : 
                    somme +=  prix_entré[elem_periode + i] + prix_sorti[elem_periode + i]
                    
                moyenne = somme/(2*periode) 
                res.append([date[elem_milieu + i],moyenne])  
                
                return(res)
                            
    else :  
        return ("La période doit être entre 2 et 15")

print(moyenne_mobile(date,prix_entré,prix_sorti,4))   