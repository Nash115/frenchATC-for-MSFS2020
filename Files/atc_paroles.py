import os
try:
    from gtts import gTTS
    import Files.atc_meteo as atc_meteo
    from random import randint
except Exception as e:
    print("atc.paroles : Impossible d'importer les modules nécessaires. Exécutez le programme 'libraries_installer.bat'. " + str(e))
    os.system("pause")
    exit()

capteeBefore = False

def transfertResponsabilitesNecessaire(callsign:str,frequency:str,captee:list)->bool:
    """
    Permet de renvoyer True si 
    Pré  : callsign de l'avion, fréquence entrée dans l'avion, tableau de fréquences disponibles
    Post : booléen correspondant si un transfert de responsabilités est nécessaire
    """
    global capteeBefore

    if frequency in captee:
        capteeBefore = True
    else:
        if capteeBefore:
            capteeBefore = False
            textS = gTTS(text= callsign + " vous sortez de ma zone de contrôle, vous pouvez changer de fréquence.", lang="fr", slow=False)
            textS.save("conv.mp3")
            os.popen("conv.mp3")
            return True
    return False

def frequenceToPrononciation(freq):
    """
    Permet de retourner la prononciation d'une fréquence
    Pré  : str : fréquence à rendre prononçable
    Post : une chaine de caractères contenant la fréquence "prononçable"
    """
    result=""
    for i in freq:
        if i == ".":
            result += " décimale "
        else:
            result += i
    return result

def recoFreqType(freq,airportData):
    returner = []
    try: 
        if freq == airportData["frequency"]["grd"]:
            returner.append("grd")
        if freq == airportData["frequency"]["twr"]:
            returner.append("twr")
        if freq == airportData["frequency"]["app"]:
            returner.append("app")
        try:
            if airportData["frequency"]["param"] == "autoinformation":
                returner.append("auto")
        except KeyError:
            pass
    except KeyError:
        return 'pasReconnu'
    if returner == []:
        return 'pasReconnu'
    return returner

def reconaissanceATC(pilot,callsign,clr,frequency,airportData):
    needCollation = False
    clearance = clr
    texte = callsign + ", je n'ai pas compris votre demande, pouvez vous répéter ?"
    #fonctions

    if frequency == "122.800" or "auto" in recoFreqType(frequency,airportData): # UNICOM
        os.popen("Sounds/collation.wav")
        needCollation = False
        return clearance,needCollation

    if "grd" in recoFreqType(frequency,airportData): ### FREQUENCE SOL ###
        #Premier contact
        if "bonjour" in pilot:
            texte = callsign + " bonjour, transmettez"

        #Clearance tours de pistes
        elif "tours de piste" in pilot:
            meteoPrise = atc_meteo.getMeteo(airportData["OACI"])
            if airportData["runways"][airportData["rwyTakeoff"]] != []:
                texte = callsign + " Transpondeur 7000, QNH" + meteoPrise[2] + ", Roulez jusqu'au point d'arret " + str(airportData["runways"][airportData["rwyTakeoff"]][randint(0,len(airportData["runways"][airportData["rwyTakeoff"]])-1)]) + " de la piste " + str([airportData["rwyTakeoff"]])
            else:
                texte = callsign + " Transpondeur 7000, QNH" + meteoPrise[2] + ", Roulez jusqu'à la piste " + str([airportData["rwyTakeoff"]])
            needCollation = "point d'arrêt"
            clearance = "tourDePiste"

        #Clearance départ dans l'axe
        elif "départ dans l'axe" in pilot:
            meteoPrise = atc_meteo.getMeteo(airportData["OACI"])
            if airportData["runways"][airportData["rwyTakeoff"]] != []:
                texte = callsign + " Transpondeur 7000, QNH" + meteoPrise[2] + ", Roulez jusqu'au point d'arret " + str(airportData["runways"][airportData["rwyTakeoff"]][randint(0,len(airportData["runways"][airportData["rwyTakeoff"]])-1)]) + " de la piste " + str([airportData["rwyTakeoff"]])
            else:
                texte = callsign + " Transpondeur 7000, QNH" + meteoPrise[2] + ", Roulez jusqu'à la piste " + str([airportData["rwyTakeoff"]])
            needCollation = "point d'arrêt"
            clearance = "departDsAxe"

        #Shoot a la tour
        elif "point d'arrêt" in pilot:
            texte = callsign + " contactez la tour "+ frequenceToPrononciation(airportData["frequency"]["twr"]) +", au revoir"
            needCollation = "tour"

        #Roulage parking
        elif "parking" in pilot and clearance == "sol":
            texte = callsign + " roulez jusqu'au parking de l'aviation générale en empruntant les taxiways."
            needCollation = "parking"
        
        #Quitter la fréquence
        elif "quitter la fréquence" in pilot:
            texte = callsign + " vous pouvez quitter la fréquence, au revoir"
            
        #Annuler les intensions
        elif "annul" in pilot:
            if clearance == "air":
                    texte = callsign + " décollage annulé, sortez par la première voie de circulation et rappelez piste dégagée."
                    needCollation = "rappel"
                    clearance = "sol"
            elif clearance == "atteri":
                texte = callsign + " atterrissage annulé."
                needCollation = "atterrissage"
                clearance = "air"




    if "twr" in recoFreqType(frequency,airportData) or "app" in recoFreqType(frequency,airportData): ###FREQUENCE TOUR ###
        #aligner et décoller
        if "point d'arrêt" in pilot:
            if clearance == "tourDePiste":
                meteoPrise = atc_meteo.getMeteo(airportData["OACI"])
                texte = callsign + " alignez vous piste "+ str([airportData["rwyTakeoff"]]) +", autorisé décollage, vent " + str(meteoPrise[0])  + " degrés, " + str(meteoPrise[1]) + " noeuds, rappelez en vent arrière"
                needCollation = "autorisé décollage"
                clearance = "air"
            else:
                meteoPrise = atc_meteo.getMeteo(airportData["OACI"])
                texte = callsign + " alignez vous piste "+ str([airportData["rwyTakeoff"]]) +", autorisé décollage, vent " + str(meteoPrise[0])  + " degrés, " + str(meteoPrise[1]) + " noeuds."
                needCollation = "autorisé décollage"
                clearance = "air"

        elif "remise des gaz" in pilot:
            texte = callsign + " remise des gaz copiée, rappelez en vent arrière"
            clearance = "air"

        elif "vent arrière" in pilot and clearance == "air":
            texte = callsign + " rappelez en étape de base"
            needCollation = "base"

        elif "base" in pilot and clearance == "air":
            texte = callsign + " rappelez en finale"
            needCollation = "finale"

        #Clearance atérissages touchés & passages bas
        elif "finale" in pilot:
            if "touch" in pilot and clearance == "air":
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
                texte = callsign + " atterrissage annulé."
                needCollation = "atterrissage"
                clearance = "air"
            
        #Contact sol
        elif "piste" in pilot and "dégag" in pilot and clearance == "atteri":
            texte = callsign + " contactez le sol "+ frequenceToPrononciation(airportData["frequency"]["grd"]) +", au revoir"
            needCollation = "sol"
            clearance = "sol"

        #Quitter la fréquence
        elif "quitter la fréquence" in pilot:
            texte = callsign + " vous pouvez quitter la fréquence, au revoir"

    # else:
    #     texte = "Fréquence invalide..."

    if "je n'ai pas compris votre demande, pouvez vous répéter ?" in texte:
            print(frequency+" <- "+pilot)

    if not(str(recoFreqType(frequency,airportData)) == 'pasReconnu'):
        textS = gTTS(text=texte, lang="fr", slow=False)
        textS.save("conv.mp3")
        os.popen("conv.mp3")
    return clearance,needCollation