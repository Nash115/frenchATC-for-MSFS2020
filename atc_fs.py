# Version : 2022-10-28
import os
try:
    from SimConnect import *
    import json
    from colorama import Fore, Back, Style
except:
    print("Impossible d'importer les modules nécessaires. Exécutez le programme 'libraries_installer.bat'.")
    os.system("pause")
    exit()

with open("assets/airports-locations.json", "r", encoding="utf-8") as json_file:
        zoneData = json.load(json_file)

AttenteLancement = False
while AttenteLancement == False:
    try:
        sm = SimConnect()
    except ConnectionError:
        print(Fore.RED + "ERREUR   : Connection avec MSFS2020 impossible.")
        print("SOLUTION : Lancez MSFS2020 avant d'exécuter le programme." + Style.RESET_ALL)
        os.system("pause")
        exit()
    else:
        AttenteLancement = True
aq = AircraftRequests(sm, _time=2000)

def getImmatOfAircraft():
    immatF = ""
    immat = str(aq.get("ATC_ID"))
    immat = immat[2:]
    for i in immat:
        if i != "'":
            immatF += i
    return immatF

def getFrequencyInAircraft(frec):
    if aq.get("COM_ACTIVE_FREQUENCY:1") != None:
        frequency = str(round(aq.get("COM_ACTIVE_FREQUENCY:1"), 4))
        while len(frequency)<7:
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

def inZone():
    latitude = str(aq.get("PLANE_LATITUDE"))
    longitude = str(aq.get("PLANE_LONGITUDE"))
    for i in latitude :
        decimal = False
        latitudeD = ""
        latitudeN = ""
        if i != ".":
            if decimal == False:
                latitudeN += i
            else:
                latitudeD += i

def updatePositionAndFrequencies():
    validateAirport = "None"
    if (str(aq.get("PLANE_LATITUDE")) != "None" or str(aq.get("PLANE_LONGITUDE")) != "None"):
        captedFrequences = []
        captedFrequencesUpdated = []
        for i in range(len(zoneData)):
            if(str(zoneData[i]["latitude1"]) == "ALL" and str(zoneData[i]["type"]) == "UNICOM"):
                captedFrequencesUpdated.append("122.800")
            elif(str(aq.get("PLANE_LATITUDE")) <= str(zoneData[i]["latitude1"]) and str(aq.get("PLANE_LATITUDE")) >= str(zoneData[i]["latitude2"]) and str(aq.get("PLANE_LONGITUDE")) >= str(zoneData[i]["longitude1"]) and str(aq.get("PLANE_LONGITUDE")) <= str(zoneData[i]["longitude2"])):
                read_json = "assets/airports/" + str(zoneData[i]["OACI"]) + ".json"
                validateAirport = str(zoneData[i]["OACI"])
                captedFrequencesUpdated = updateFrequences(read_json,captedFrequences,i)
        if str(type(validateAirport)) != "<class 'NoneType'>":
            return captedFrequencesUpdated,validateAirport
        else:
            return captedFrequencesUpdated,"None"
