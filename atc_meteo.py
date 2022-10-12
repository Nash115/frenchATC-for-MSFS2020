# Version : 2022-10-12

import requests
from bs4 import BeautifulSoup

actuTimeMetar = ""

def getMeteo(airport):
    url = 'https://metar-taf.com/'+airport

    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="html.parser")

    actuTimeMetar = (soup.find('code')).text

    actuMetarFC = (soup.find('code')).text

    hdgWind = actuMetarFC[actuMetarFC.index("KT")-5] + actuMetarFC[actuMetarFC.index("KT")-4] + actuMetarFC[actuMetarFC.index("KT")-3]
    if actuMetarFC[actuMetarFC.index("KT")-2] == "0":
        spdWind = actuMetarFC[actuMetarFC.index("KT")-1]
    else:
        spdWind = actuMetarFC[actuMetarFC.index("KT")-2] + actuMetarFC[actuMetarFC.index("KT")-1]
    qnh = actuMetarFC[actuMetarFC.index("Q")+1] + actuMetarFC[actuMetarFC.index("Q")+2] + actuMetarFC[actuMetarFC.index("Q")+3] + actuMetarFC[actuMetarFC.index("Q")+4] + " hPa"

    return [hdgWind,spdWind,qnh]
