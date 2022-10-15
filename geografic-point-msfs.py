# Version : 2022-10-12

from SimConnect import *
import os
import json
from colorama import Fore, Back, Style

sm = SimConnect()
aq = AircraftRequests(sm, _time=2000)

lastLat = 0
lastLong = 0

with open("assets/airports-locations.json", "r", encoding="utf-8") as json_file:
        zoneData = json.load(json_file)

def updateFrequences(pathFile):
    if not os.path.exists(pathFile):
        print(Fore.BLUE + "Fichier aéroport :" + pathFile + Fore.RED + " inexistant..." + Style.RESET_ALL)
        print(Fore.YELLOW +"Le code OACI de l'aéroport saisi est inconnu. Vérifier l'ortographe.")
        print("Si l'ortographe est correct, l'aéroport n'a pas été paramétré pour ce programme, vous pouvez le créer et lui donner le nom OACI correct." + Style.RESET_ALL)
        os.system("pause")
        exit()
    else:
        with open(pathFile, "r", encoding="utf-8") as json_file:
            if str(zoneData[i]["type"]) == "all":
                captedFrequences.append(json.load(json_file)["frequency"]["app"][1])
                captedFrequences.append(json.load(json_file)["frequency"]["twr"][1])
                captedFrequences.append(json.load(json_file)["frequency"]["grd"][1])
            elif str(zoneData[i]["type"]) == "app":
                captedFrequences.append(json.load(json_file)["frequency"]["app"][1])
            elif str(zoneData[i]["type"]) == "twr":
                captedFrequences.append(json.load(json_file)["frequency"]["twr"][1])
            elif str(zoneData[i]["type"]) == "grd":
                captedFrequences.append(json.load(json_file)["frequency"]["grd"][1])
            return "Done"

while True:
    if (aq.get("PLANE_LATITUDE") != lastLat or aq.get("PLANE_LONGITUDE") != lastLong) and (str(aq.get("PLANE_LATITUDE")) != "None" or str(aq.get("PLANE_LONGITUDE")) != "None"):
        captedFrequences = []
        os.system('cls')
        #print("Latitude :",str(aq.get("PLANE_LATITUDE")))
        #print("Longitude :",str(aq.get("PLANE_LONGITUDE")))
        lastLat = aq.get("PLANE_LATITUDE")
        lastLong = aq.get("PLANE_LONGITUDE")

        for i in range(len(zoneData)):
            if(str(aq.get("PLANE_LATITUDE")) <= str(zoneData[i]["latitude1"]) and str(aq.get("PLANE_LATITUDE")) >= str(zoneData[i]["latitude2"]) and str(aq.get("PLANE_LONGITUDE")) >= str(zoneData[i]["longitude1"]) and str(aq.get("PLANE_LONGITUDE")) <= str(zoneData[i]["longitude2"])):
                if(str(aq.get("PLANE_ALTITUDE")) >= str(zoneData[i]["altitudeMin"]) and str(aq.get("PLANE_ALTITUDE")) <= str(zoneData[i]["altitudeMax"])):
                    #print(str(zoneData[i]["OACI"]))
                    read_json = "assets/airports/" + str(zoneData[i]["OACI"]) + ".json"
                    updateFrequences(read_json)
        print("Fréquences disponibles : ",captedFrequences)