from cgitb import text
from gtts import gTTS
import os
import atc_meteo
from random import randint

dernierT = "Impossible"

def reconaissanceATC(pilot,callsign,clr,frequency,airportData):
    frequency_f = frequency
    needCollation = False
    clearance = clr
    texte = callsign + ", je n'ai pas compris votre demande, pouvez vous répéter ?"
    #fonctions

    if frequency_f == "Ground":
        #Premier contact
        if "bonjour" in pilot:
            texte = callsign + " bonjour, transmettez"

        #Clearance tours de pistes
        if "tours de piste" in pilot:
            texte = callsign + " Transpondeur 7000, Roulez jusqu'au point d'arret" + str(airportData["runways"][0][randint(0,len(airportData["runways"][0]))])
            needCollation = "alpha unité"
            clearance = "tourDePiste"

        #Clearance point d'arret
        if "départ dans l'axe" in pilot:
            texte = callsign + " Transpondeur 7000, Roulez jusqu'au point d'arret" + str(airportData["runways"][0][randint(0,len(airportData["runways"][0]))])
            needCollation = "alpha unité"
            clearance = "departDsAxe"

        #Shoot a la tour
        if "point d'arrêt" in pilot:
            texte = callsign + " contactez la tour "+ airportData["frequency"]["twr"] +", au revoir"
            needCollation = "tour"
            frequency_f = "Tower"

        #Roulage parking
        if "parking" in pilot and clearance == "sol":
            texte = callsign + " roulez jusqu'au parking de l'aviation générale en empruntant les taxiways."
            needCollation = "parking"
        
        #Quitter la fréquence
        if "quitter la fréquence" in pilot:
            texte = callsign + " vous pouvez quitter la fréquence, au revoir"

    elif frequency_f == "Tower":
        #aligner et décoller
        if "point d'arrêt" in pilot:
            if clearance == "tourDePiste":
                meteoPrise = atc_meteo.getMeteo(airportData["OACI"])
                texte = callsign + " alignez vous piste "+ str(airportData["runways"][0]) +", autorisé décollage, vent " + str(meteoPrise[0])  + " degrés, " + str(meteoPrise[1]) + " noeuds, rappelez en vent arrière"
                needCollation = "autorisé décollage"
                clearance = "air"
            elif clearance == "departDsAxe":
                meteoPrise = atc_meteo.getMeteo(airportData["OACI"])
                texte = callsign + " alignez vous piste "+ str(airportData["runways"][0]) +", autorisé décollage, vent " + str(meteoPrise[0])  + " degrés, " + str(meteoPrise[1]) + " noeuds."
                needCollation = "autorisé décollage"
                clearance = "air"

        if "remise des gaz" in pilot and clearance == "air":
            texte = callsign + " remise des gaz compiée, rappelez en vent arrière"
            clearance = "air"

        if "vent arrière" in pilot and clearance == "air":
            texte = callsign + " rappelez en étape de base"

        if "base" in pilot and clearance == "air":
            texte = callsign + " rappelez en finale"

        #Clearance atérissages touchés & passages bas
        if "finale" in pilot:
            if "touché" in pilot and clearance == "air":
                meteoPrise = atc_meteo.getMeteo(airportData["OACI"])
                texte = callsign + " autorisé touché piste "+ str(airportData["runways"][0]) +", vent " + str(meteoPrise[0])  + " degrés, " + str(meteoPrise[1]) + " noeuds."
                needCollation = "autorisé"
                clearance = "air"
            elif "passage bas" in pilot and clearance == "air":
                meteoPrise = atc_meteo.getMeteo(airportData["OACI"])
                texte = callsign + " autorisé passage bas piste "+ str(airportData["runways"][0]) +", vent " + str(meteoPrise[0])  + " degrés, " + str(meteoPrise[1]) + " noeuds."
                needCollation = "autorisé"
                clearance = "air"
            elif clearance == "air":
                meteoPrise = atc_meteo.getMeteo(airportData["OACI"])
                texte = callsign + " autorisé atérissage piste "+ str(airportData["runways"][0]) +", vent " + str(meteoPrise[0])  + " degrés, " + str(meteoPrise[1]) + " noeuds."
                needCollation = "autorisé atterrissage"
                clearance = "atteri"

        #Contact sol
        if "annul" in pilot:
            if clearance == "air":
                    texte = callsign + " décollage annulé, sortez par la première voie de circulation et rappelez piste dégagée."
                    needCollation = "rappel"
                    clearance = "sol"
            elif clearance == "atteri":
                texte = callsign + " atterissage annulé."
                needCollation = "atterissage"
                clearance = "air"
            
        #Contact sol
        if "piste" in pilot and "dégag" in pilot and clearance == "atteri":
            texte = callsign + " contactez le sol "+ airportData["frequency"]["grd"] +", au revoir"
            needCollation = "sol"
            clearance = "sol"
            frequency_f = "Ground"
        

    else:
        texte = "Fréquence invalide..."

    if "répéter" in pilot or "répétez" in pilot or "répété" in pilot:
        texte = dernierT
    dernierT = texte


    textS = gTTS(text=texte, lang="fr", slow=False)
    textS.save("conv.mp3")
    os.popen("conv.mp3")
    return clearance,needCollation,frequency_f
