from gtts import gTTS
import os
import atc_meteo

def reconaissanceATC(pilot,callsign,clr):
    clearance = clr
    texte = callsign + ", je n'ai pas compris votre demande, pouvez vous répéter ?"
    #fonctions

    #Premier contact
    if "bonjour" in pilot:
        texte = callsign + " bonjour, transmettez"
        print("ATC >",texte)

    #Clearance tours de pistes
    if "tours de piste" in pilot:
        texte = callsign + " Transpondeur 7000, Roulez point d'arret alpha unité piste 17"
        clearance = "tourDePiste"
        print("ATC >",texte)

    #Clearance décollage
    if "départ dans l'axe" in pilot:
        texte = callsign + " Transpondeur 7000, Roulez point d'arret alpha unité piste 17"
        clearance = "departDsAxe"
        print("ATC >",texte)

    #Shoot a la tour + aligner et décoller
    if "point d'arrêt" in pilot:
        if "prêts au départ" in pilot:
            #texte = callsign + " alignez vous piste 17, autorisé décollage, vent " + str(wind_hdg)  + " degrés, " + str(wind_spd) + " noeuds, rappelez vent arriere piste 17"
            if clearance == "tourDePiste":
                meteoPrise = atc_meteo.getMeteo()
                texte = callsign + " alignez vous piste 17, autorisé décollage, vent " + str(meteoPrise[0])  + " degrés, " + str(meteoPrise[1]) + " noeuds, rappelez vent arriere piste 17"
                clearance = "air"
            elif clearance == "departDsAxe":
                meteoPrise = atc_meteo.getMeteo()
                texte = callsign + " alignez vous piste 17, autorisé décollage, vent " + str(meteoPrise[0])  + " degrés, " + str(meteoPrise[1]) + " noeuds."
                clearance = "air"
            print("ATC >",texte)
        else:
            texte = callsign + " contactez la tour 118 décimale 625, au revoir"
            print("ATC >",texte)

    #Clearance atérissages touchés & passages bas
    if "finale" in pilot:
        if "touché" in pilot and clearance == "air":
            meteoPrise = atc_meteo.getMeteo()
            texte = callsign + " autorisé touché piste 17, vent " + str(meteoPrise[0])  + " degrés, " + str(meteoPrise[1]) + " noeuds."
            clearance = "atteri"
        elif "passage bas" in pilot and clearance == "air":
            meteoPrise = atc_meteo.getMeteo()
            texte = callsign + " autorisé passage bas piste 17, vent " + str(meteoPrise[0])  + " degrés, " + str(meteoPrise[1]) + " noeuds."
            clearance = "atteri"
        elif clearance == "air":
            meteoPrise = atc_meteo.getMeteo()
            texte = callsign + " autorisé atérissage piste 17, vent " + str(meteoPrise[0])  + " degrés, " + str(meteoPrise[1]) + " noeuds."
            clearance = "atteri"
        print("ATC >",texte)
        
    #Contact sol
    if "piste dégagée" in pilot and clearance == "atteri":
        texte = callsign + " contactez le sol 121 décimale 805, au revoir"
        clearance = "departDsAxe"
        print("ATC >",texte)



    textS = gTTS(text=texte, lang="fr", slow=False)
    textS.save("conv.mp3")
    os.popen("conv.mp3")
    return clearance