from cgitb import text
from gtts import gTTS
import os
import atc_meteo

def reconaissanceATC(pilot,callsign,clr,frequency):
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
            texte = callsign + " Transpondeur 7000, Roulez point d'arret alpha unité piste 17"
            needCollation = "alpha unité"
            clearance = "tourDePiste"

        #Clearance point d'arret
        if "départ dans l'axe" in pilot:
            texte = callsign + " Transpondeur 7000, Roulez point d'arret alpha unité piste 17"
            needCollation = "alpha unité"
            clearance = "departDsAxe"

        #Shoot a la tour + aligner et décoller
        if "point d'arrêt" in pilot:
            texte = callsign + " contactez la tour 118 décimale 625, au revoir"
            needCollation = "la tour"
            frequency_f = "Tower"

    elif frequency_f == "Tower":
        #Shoot a la tour + aligner et décoller
        if "point d'arrêt" in pilot:
            if clearance == "tourDePiste":
                meteoPrise = atc_meteo.getMeteo()
                texte = callsign + " alignez vous piste 17, autorisé décollage, vent " + str(meteoPrise[0])  + " degrés, " + str(meteoPrise[1]) + " noeuds, rappelez en étape de base"
                needCollation = "autorisé décollage"
                clearance = "air"
            elif clearance == "departDsAxe":
                meteoPrise = atc_meteo.getMeteo()
                texte = callsign + " alignez vous piste 17, autorisé décollage, vent " + str(meteoPrise[0])  + " degrés, " + str(meteoPrise[1]) + " noeuds."
                needCollation = "autorisé décollage"
                clearance = "air"

        if "remise des gaz" in pilot and clearance == "air":
            texte = callsign + " remise des gaz compiée, rappelez en étape de base"
            clearance = "air"

        if "base" in pilot and clearance == "air":
            texte = callsign + " rappelez en vent arrière"

        if "vent arrière" in pilot and clearance == "air":
            texte = callsign + " rappelez en finale"

        #Clearance atérissages touchés & passages bas
        if "finale" in pilot:
            if "touché" in pilot and clearance == "air":
                meteoPrise = atc_meteo.getMeteo()
                texte = callsign + " autorisé touché piste 17, vent " + str(meteoPrise[0])  + " degrés, " + str(meteoPrise[1]) + " noeuds."
                needCollation = "autorisé"
                clearance = "air"
            elif "passage bas" in pilot and clearance == "air":
                meteoPrise = atc_meteo.getMeteo()
                texte = callsign + " autorisé passage bas piste 17, vent " + str(meteoPrise[0])  + " degrés, " + str(meteoPrise[1]) + " noeuds."
                needCollation = "autorisé"
                clearance = "air"
            elif clearance == "air":
                meteoPrise = atc_meteo.getMeteo()
                texte = callsign + " autorisé atérissage piste 17, vent " + str(meteoPrise[0])  + " degrés, " + str(meteoPrise[1]) + " noeuds."
                needCollation = "autorisé atterrissage"
                clearance = "atteri"
            
        #Contact sol
        if "piste dégagée" in pilot and clearance == "atteri":
            texte = callsign + " contactez le sol 121 décimale 805, au revoir"
            needCollation = "le sol"
            clearance = "sol"
            frequency_f = "Ground"


    else:
        texte = "Fréquence invalide..."


    textS = gTTS(text=texte, lang="fr", slow=False)
    textS.save("conv.mp3")
    os.popen("conv.mp3")
    return clearance,needCollation,frequency_f
