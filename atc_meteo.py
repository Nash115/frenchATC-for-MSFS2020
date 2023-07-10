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

    url = 'https://metar-taf.com/'+airport

    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="html.parser")
    print(soup.text)

    # actuTimeMetar = (soup.find('code')).text

    actuMetarFC = soup.find('code')
    print(actuMetarFC)
    actuMetarFC = "METAR LFMD 301730Z AUTO VRB02KT CAVOK 27/12 Q1013 NOSIG"

    hdgWind = actuMetarFC[actuMetarFC.index("KT")-5] + actuMetarFC[actuMetarFC.index("KT")-4] + actuMetarFC[actuMetarFC.index("KT")-3]
    if actuMetarFC[actuMetarFC.index("KT")-2] == "0":
        spdWind = actuMetarFC[actuMetarFC.index("KT")-1]
    else:
        spdWind = actuMetarFC[actuMetarFC.index("KT")-2] + actuMetarFC[actuMetarFC.index("KT")-1]
    qnh = actuMetarFC[actuMetarFC.index("Q")+1] + actuMetarFC[actuMetarFC.index("Q")+2] + actuMetarFC[actuMetarFC.index("Q")+3] + actuMetarFC[actuMetarFC.index("Q")+4] + " hPa"

    print("Informations météo délivrées par metar-taf.com   nous nous excusons en cas d'imprecision ou d'erreurs.")
    return (hdgWind,spdWind,qnh)