import os
try:
    from SimConnect import *
    import json
    from colorama import Fore, Back, Style
except Exception as e:
    print("atc.fs : Impossible d'importer les modules nécessaires. Exécutez le programme 'libraries_installer.bat'. " + str(e))
    os.system("pause")
    exit()

with open("assets/airports-locations.json", "r", encoding="utf-8") as json_file:
    try :
        zoneData = json.load(json_file)
    except:
        print("Erreur lors du paramétrage de la position des aéroports.")
        print("Erreur courante : erreur de syntaxe dans le fichier json concernant la position des aéroports. (/assets/airports-locations.json)")
        os.system("pause")
        exit()

AttenteLancement = False
os.system("cls")
print(Fore.RED + "Si ce message ne disparait pas, cela signifie que la connection avec MSFS2020 n'a pas abouti.")
print(Fore.YELLOW + "En attente de la connection avec Flight Simulator..." + Style.RESET_ALL)
while AttenteLancement == False:
    try:
        sm = SimConnect()
    except ConnectionError:
        AttenteLancement = False
    else:
        AttenteLancement = True
        print(Fore.GREEN + "Flight Simulator lancé ! Démarrage..." + Style.RESET_ALL)
os.system("cls")
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
        #print("Frequence introuvable, paramétrage de la dernière fréquence")
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
        try :
            with open(pathFile, "r", encoding="utf-8") as json_file:
                freqInJson = json.load(json_file)["frequency"]
                if str(zoneData[i]["type"]) == "auto": # autoinformation
                    capted.append(freqInJson["twr"])
                elif str(zoneData[i]["type"]) == "all":
                    capted.append(freqInJson["grd"])
                    capted.append(freqInJson["twr"])
                    capted.append(freqInJson["app"])
                elif str(zoneData[i]["type"]) == "app":
                    capted.append(freqInJson["app"])
                elif str(zoneData[i]["type"]) == "twr":
                    capted.append(freqInJson["twr"])
                elif str(zoneData[i]["type"]) == "grd":
                    capted.append(freqInJson["grd"])
                return capted
        except:
            print("Erreur lors du paramétrage des fréquences.")
            print("Erreur courante : erreur de syntaxe dans un des fichiers json concernant un des aéroports. (/assets/airports/????.json)")
            os.system("pause")
            exit()

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
