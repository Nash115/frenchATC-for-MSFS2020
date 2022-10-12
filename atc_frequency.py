# Version : 2022-10-12

from SimConnect import *

sm = SimConnect()
aq = AircraftRequests(sm, _time=2000)

def getFrequency(frec):
    if aq.get("COM_ACTIVE_FREQUENCY:1") != None:
        frequency = str(round(aq.get("COM_ACTIVE_FREQUENCY:1"), 4))
        while len(frequency)<6:
            frequency += "0"
        return frequency
    else:
        print("Frquence introuvable, paramétrage de la dernière fréquence")
        return frec