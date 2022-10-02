## Version V0.5.0-2022-10-02

from cgitb import text
from gtts import gTTS
import os
import atc_meteo
from random import randint

def reconaissanceATC(pilot,callsign,clr,frequency,airportData):
    frequency_f = frequency
    needCollation = False
    clearance = clr
    texte = callsign + ", je n'ai pas compris votre demande, pouvez vous répéter ?"
    #fonctions




    if frequency_f == airportData["frequency"]["grd"][1]: ### FREQUENCE SOL ###
        #Premier contact
        if "bonjour" in pilot:
            texte = callsign + " bonjour, transmettez"

        #Clearance tours de pistes
        elif "tours de piste" in pilot:
            meteoPrise = atc_meteo.getMeteo(airportData["OACI"])
            texte = callsign + " Transpondeur 7000, QNH" + meteoPrise[2] + ", Roulez jusqu'au point d'arret " + str(airportData["runways"][airportData["rwyTakeoff"]][randint(0,len(airportData["runways"][airportData["rwyTakeoff"]])-1)]) + " de la piste " + str([airportData["rwyTakeoff"]])
            needCollation = "point d'arrêt"
            clearance = "tourDePiste"

        #Clearance point d'arret
        elif "départ dans l'axe" in pilot:
            meteoPrise = atc_meteo.getMeteo(airportData["OACI"])
            texte = callsign + " Transpondeur 7000, QNH" + meteoPrise[2] + ", Roulez jusqu'au point d'arret " + str(airportData["runways"][airportData["rwyTakeoff"]][randint(0,len(airportData["runways"][airportData["rwyTakeoff"]])-1)]) + " de la piste " + str([airportData["rwyTakeoff"]])
            needCollation = "point d'arrêt"
            clearance = "departDsAxe"

        #Shoot a la tour
        elif "point d'arrêt" in pilot:
            texte = callsign + " contactez la tour "+ str(airportData["frequency"]["twr"][0]) +", au revoir"
            needCollation = "tour"
            frequency_f = airportData["frequency"]["twr"][1]

        #Roulage parking
        elif "parking" in pilot and clearance == "sol":
            texte = callsign + " roulez jusqu'au parking de l'aviation générale en empruntant les taxiways."
            needCollation = "parking"
        
        #Quitter la fréquence
        elif "quitter la fréquence" in pilot:
            texte = callsign + " vous pouvez quitter la fréquence, au revoir"




    elif frequency_f == airportData["frequency"]["twr"][1]: ###FREQUENCE TOUR ###
        #aligner et décoller
        if "point d'arrêt" in pilot:
            if clearance == "tourDePiste":
                meteoPrise = atc_meteo.getMeteo(airportData["OACI"])
                texte = callsign + " alignez vous piste "+ str([airportData["rwyTakeoff"]]) +", autorisé décollage, vent " + str(meteoPrise[0])  + " degrés, " + str(meteoPrise[1]) + " noeuds, rappelez en vent arrière"
                needCollation = "autorisé décollage"
                clearance = "air"
            elif clearance == "departDsAxe":
                meteoPrise = atc_meteo.getMeteo(airportData["OACI"])
                texte = callsign + " alignez vous piste "+ str([airportData["rwyTakeoff"]]) +", autorisé décollage, vent " + str(meteoPrise[0])  + " degrés, " + str(meteoPrise[1]) + " noeuds."
                needCollation = "autorisé décollage"
                clearance = "air"

        elif "remise des gaz" in pilot:
            texte = callsign + " remise des gaz copiée, rappelez en vent arrière"
            clearance = "air"

        elif "vent arrière" in pilot and clearance == "air":
            texte = callsign + " rappelez en étape de base"

        elif "base" in pilot and clearance == "air":
            texte = callsign + " rappelez en finale"

        #Clearance atérissages touchés & passages bas
        elif "finale" in pilot:
            if "touché" in pilot and clearance == "air":
                meteoPrise = atc_meteo.getMeteo(airportData["OACI"])
                texte = callsign + " autorisé touché piste "+ str([airportData["rwyLanding"]]) +", vent " + str(meteoPrise[0])  + " degrés, " + str(meteoPrise[1]) + " noeuds."
                needCollation = "autorisé"
                clearance = "air"
            elif "passage bas" in pilot and clearance == "air":
                meteoPrise = atc_meteo.getMeteo(airportData["OACI"])
                texte = callsign + " autorisé passage bas piste "+ str([airportData["rwyLanding"]]) +", vent " + str(meteoPrise[0])  + " degrés, " + str(meteoPrise[1]) + " noeuds."
                needCollation = "autorisé"
                clearance = "air"
            elif clearance == "air":
                meteoPrise = atc_meteo.getMeteo(airportData["OACI"])
                texte = callsign + " autorisé atérissage piste "+ str([airportData["rwyLanding"]]) +", vent " + str(meteoPrise[0])  + " degrés, " + str(meteoPrise[1]) + " noeuds."
                needCollation = "autorisé atterrissage"
                clearance = "atteri"

        #Annuler les intensions
        elif "annul" in pilot:
            if clearance == "air":
                    texte = callsign + " décollage annulé, sortez par la première voie de circulation et rappelez piste dégagée."
                    needCollation = "rappel"
                    clearance = "sol"
            elif clearance == "atteri":
                texte = callsign + " atterissage annulé."
                needCollation = "atterissage"
                clearance = "air"
            
        #Contact sol
        elif "piste" in pilot and "dégag" in pilot and clearance == "atteri":
            texte = callsign + " contactez le sol "+ str(airportData["frequency"]["grd"][0]) +", au revoir"
            needCollation = "sol"
            clearance = "sol"
            frequency_f = airportData["frequency"]["grd"][1]
        


    else:
        texte = "Fréquence invalide..."


    if "je n'ai pas compris votre demande, pouvez vous répéter ?" in texte:
        print(pilot)
    textS = gTTS(text=texte, lang="fr", slow=False)
    textS.save("conv.mp3")
    os.popen("conv.mp3")
    return clearance,needCollation,frequency_f
