import os
import json

def maker(airport)->dict:
    """
    Permet de créer un dictionnaire à l'aide du fichier json de l'aéroport possédant le code OACI donné en paramètre
    Pré  : str : code OACI de l'aéroport
    Post : dict des informations dans le json de l'aéroport
    """
    read_json = "assets/airports/" + airport + ".json"

    airportDataMaked = {}

    if not os.path.exists(read_json):
        airportDataMaked = {"OACI":"NONE"}
    else:
        with open(read_json, "r", encoding="utf-8") as json_file:
            airportDataMaked = json.load(json_file)

    return airportDataMaked