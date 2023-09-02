import os

def display(car:str)->bool:
    """
    Affiche la chaine de caractère donnée en paramètre à la manière d'un print
    Pré  : chaine de caractères à afficher
    Post : renvoie un booléen (True) une fois exécuté
    """
    print(car)
    return True

def defTitleOfWindow(car:str)->bool:
    """
    Modifie le titre de la fenêtre de l'invite de commandes
    Pré  : chaine de caractères qui sera le nom de la fenêtre
    Post : renvoie un booléen (True) une fois exécuté
    """
    os.system("title " + car)
    return True

def clear()->bool:
    """
    Efface le texte dans l'invite de commande
    Pré  : /
    Post : renvoie un booléen (True) une fois exécuté
    """
    os.system("cls")
    return True