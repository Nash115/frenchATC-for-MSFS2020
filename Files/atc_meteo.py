DATA_PROVIDER = "https://www.getmetar.com"

import os
try:
    import requests
    from bs4 import BeautifulSoup
except Exception as e:
    print("atc.meteo : Impossible d'importer les modules nécessaires. Exécutez le programme 'libraries_installer.bat'. " + str(e))
    os.system("pause")
    exit()

actuTimeMetar = ""

def getMeteo(airport)->tuple:
    """
    Permet de créer un tuple contenant les informations météos de l'aéroport
    Pré  : str : code OACI de l'aéroport
    Post : tuple contenant : le cap du vent, la vitesse du vent, la pression atmosphérique (qnh) en hPa
    """

    url = DATA_PROVIDER+airport

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, features="html.parser")

        actuMetarFC = soup.find('h4').text # Récupération du METAR
        print(actuMetarFC)

        hdgWind = actuMetarFC[actuMetarFC.index("KT")-5] + actuMetarFC[actuMetarFC.index("KT")-4] + actuMetarFC[actuMetarFC.index("KT")-3]
        if actuMetarFC[actuMetarFC.index("KT")-2] == "0":
            spdWind = actuMetarFC[actuMetarFC.index("KT")-1]
        else:
            spdWind = actuMetarFC[actuMetarFC.index("KT")-2] + actuMetarFC[actuMetarFC.index("KT")-1]
        qnh = actuMetarFC[actuMetarFC.index("Q")+1] + actuMetarFC[actuMetarFC.index("Q")+2] + actuMetarFC[actuMetarFC.index("Q")+3] + actuMetarFC[actuMetarFC.index("Q")+4] + " hPa"

        print(f"Informations météo délivrées par {DATA_PROVIDER}   nous nous excusons en cas d'imprecision ou d'erreurs.")
    else:
        print(f"Erreur lors de la récupération des informations météo. (Code d'erreur : {response.status_code})")
        return ("000","0","1013 hPa")
    return (hdgWind,spdWind,qnh)