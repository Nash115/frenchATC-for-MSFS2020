import os
import json

def maker(airport):
    read_json = "assets/airports/" + airport + ".json"

    airportDataMaked = {}

    if not os.path.exists(read_json):
        airportDataMaked = {"OACI":"NONE"}
    else:
        with open(read_json, "r", encoding="utf-8") as json_file:
            airportDataMaked = json.load(json_file)

    return airportDataMaked

def recoTypeOfFrequency(airport):
    return