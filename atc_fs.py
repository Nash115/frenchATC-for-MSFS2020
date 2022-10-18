# Version : 2022-10-17

from SimConnect import *
import os
import json
from colorama import Fore, Back, Style

with open("assets/airports-locations.json", "r", encoding="utf-8") as json_file:
        zoneData = json.load(json_file)

sm = SimConnect()
aq = AircraftRequests(sm, _time=2000)

def getFrequency(frec):
    if aq.get("COM_ACTIVE_FREQUENCY:1") != None:
        frequency = str(round(aq.get("COM_ACTIVE_FREQUENCY:1"), 4))
        while len(frequency)<6:
            frequency += "0"
        return frequency
    else:
        print("Frquence introuvable, paramétrage de la dernière fréquence")
        return frec


## POSITION

def updateFrequences(pathFile,capted,i):
    if not os.path.exists(pathFile):
        print(Fore.BLUE + "Fichier aéroport :" + pathFile + Fore.RED + " inexistant..." + Style.RESET_ALL)
        print(Fore.YELLOW +"Le code OACI de l'aéroport saisi est inconnu. Vérifier l'ortographe.")
        print("Si l'ortographe est correct, l'aéroport n'a pas été paramétré pour ce programme, vous pouvez le créer et lui donner le nom OACI correct." + Style.RESET_ALL)
        os.system("pause")
        exit()
    else:
        with open(pathFile, "r", encoding="utf-8") as json_file:
            if str(zoneData[i]["type"]) == "all":
                capted.append(json.load(json_file)["frequency"]["app"])
                capted.append(json.load(json_file)["frequency"]["twr"])
                capted.append(json.load(json_file)["frequency"]["grd"])
            elif str(zoneData[i]["type"]) == "app":
                capted.append(json.load(json_file)["frequency"]["app"])
            elif str(zoneData[i]["type"]) == "twr":
                capted.append(json.load(json_file)["frequency"]["twr"])
            elif str(zoneData[i]["type"]) == "grd":
                capted.append(json.load(json_file)["frequency"]["grd"])
            return capted

def updatePositionAndFrequencies():
    validateAirport = "None"
    if (str(aq.get("PLANE_LATITUDE")) != "None" or str(aq.get("PLANE_LONGITUDE")) != "None"):
        captedFrequences = []
        captedFrequencesUpdated = []
        for i in range(len(zoneData)):
            if(str(aq.get("PLANE_LATITUDE")) <= str(zoneData[i]["latitude1"]) and str(aq.get("PLANE_LATITUDE")) >= str(zoneData[i]["latitude2"]) and str(aq.get("PLANE_LONGITUDE")) >= str(zoneData[i]["longitude1"]) and str(aq.get("PLANE_LONGITUDE")) <= str(zoneData[i]["longitude2"])):
                if(str(aq.get("PLANE_ALTITUDE")) >= str(zoneData[i]["altitudeMin"]) and str(aq.get("PLANE_ALTITUDE")) <= str(zoneData[i]["altitudeMax"])):
                    read_json = "assets/airports/" + str(zoneData[i]["OACI"]) + ".json"
                    validateAirport = str(zoneData[i]["OACI"])
                    captedFrequencesUpdated = updateFrequences(read_json,captedFrequences,i)
        return captedFrequencesUpdated,validateAirport