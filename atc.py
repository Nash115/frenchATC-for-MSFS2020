# Version : 2022-10-28

import argparse
from cgi import test
import os
import queue
from subprocess import call
import sounddevice as sd
import vosk
import sys
import json
from colorama import Fore, Back, Style
import atc_paroles
import atc_fs
import airport_data_maker

q = queue.Queue()

alphabet_min = "abcdefghijklmnopqrstuvwxyz"
alphabet_maj = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphabetAero = ["alpha","bravo","charlie","delta","echo","fox","golf","hotel","india","juliet","kilo","lima","mike","november","oscar","papa","quebec","romeo","sierra","tango","uniform","victor","whisky","x-ray","yankee","zulu"]

airportData = {"OACI":"NONE"}

callsignD = "ASXGS"
os.system("cls")
print(Fore.YELLOW + "En attente du démarrage d'un vol pour commencer..." + Style.RESET_ALL)
while callsignD == "ASXGS":
    callsignD = atc_fs.getImmatOfAircraft()
print(Fore.GREEN + "Immatriculation perso détectée... Démarrage..." + Style.RESET_ALL)

callsign = ""
carractsLettres = [0,4,5]
caract = 0

if not(len(callsignD) == 6 and "-" in callsignD and (callsignD[0] == "F" or callsignD == "f")):
    print(Fore.RED + "Immatriculation invalide : " + callsignD  + " n'est pas de la forme 'F-XXXX' ! " + Style.RESET_ALL)
    while not(len(callsignD) == 6 and "-" in callsignD and (callsignD[0] == "F" or callsignD == "f")):
        callsignD = atc_fs.getImmatOfAircraft()

if len(callsignD) == 6 and "-" in callsignD and (callsignD[0] == "F" or callsignD == "f"):
    for i in callsignD:
        if i in alphabet_min and caract in carractsLettres:
            callsign += alphabetAero[alphabet_min.index(i)]
            callsign += " "
        elif i in alphabet_maj and caract in carractsLettres:
            callsign += alphabetAero[alphabet_maj.index(i)]
            callsign += " "
        caract += 1

print(Fore.BLUE + "Indicatif d'appel :" + callsign + Style.RESET_ALL)

authFrequencies = []
precedAuthFrequencies = []

clearance = "sol"
lastClearance = clearance
ifNeedCollation = False

frequency = "000.000"
lastfrequency = frequency

rep = [clearance,ifNeedCollation,frequency]

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

print(Fore.GREEN +' Démarrage des services en cours... Veuillez patienter...' + Style.RESET_ALL)

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def printHead():
    os.system('cls')
    print('#' * 80)
    if frequency in authFrequencies:
        print("#" + 'Service ATC en fonction !'+ Fore.GREEN +' Bon vol !' + Style.RESET_ALL + ((27-len(frequency))*" ") + Back.CYAN + Fore.BLACK + " " + callsignD + " " + Style.RESET_ALL + " " + Back.BLUE + " " + frequency + " mHz " + Style.RESET_ALL + " #")
    else:
        print("#" + 'Service ATC en fonction !'+ Fore.GREEN +' Bon vol !' + Style.RESET_ALL + ((27-len(frequency))*" ") + Back.CYAN + Fore.BLACK + " " + callsignD + " " + Style.RESET_ALL + " " + Back.RED + " " + frequency + " mHz " + Style.RESET_ALL + " #")
    print('#' * 80)
    print("#" + "Airport : " + airportData["OACI"] + " "*5 + "Freq : " + str(authFrequencies) + " "*(52-len(str(authFrequencies))) + "#")
    print('#' * 80)

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()

print(Fore.GREEN +' Détection des périphériques... Veuillez patienter...' + Style.RESET_ALL)

if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    '-f', '--filename', type=str, metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-m', '--model', type=str, metavar='MODEL_PATH',
    help='Path to the model')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
args = parser.parse_args(remaining)

try:
    if args.model is None:
        args.model = "model"
    if not os.path.exists(args.model):
        print ("Please download a model for your language from https://alphacephei.com/vosk/models")
        print ("and unpack as 'model' in the current folder.")
        parser.exit(0)
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info['default_samplerate'])

    model = vosk.Model(args.model)

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None

    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device, dtype='int16',
                            channels=1, callback=callback):
            printHead()

            rec = vosk.KaldiRecognizer(model, args.samplerate)
            while True:

                testSiTransfertRespNecessaire = atc_paroles.transfertResponsabilitesNecessaire(callsign,frequency,authFrequencies,)
                if testSiTransfertRespNecessaire:
                    ifNeedCollation = "fréquence"

                if atc_fs.updatePositionAndFrequencies()[1] != "None":
                    airportData = airport_data_maker.maker(atc_fs.updatePositionAndFrequencies()[1])
                else:
                    airportData = {"OACI":"NONE"}
                authFrequencies = atc_fs.updatePositionAndFrequencies()[0]
                os.system("title ATC by Nash115 - " + airportData["OACI"] + " ("+callsignD+")")
                frequency = str(atc_fs.getFrequencyInAircraft(frequency))
                if frequency != lastfrequency:
                    print(Back.BLUE +"Fréquence modifiée :" + frequency +Style.RESET_ALL)
                    lastfrequency = frequency
                    printHead()
                if precedAuthFrequencies != authFrequencies:
                    printHead()
                    precedAuthFrequencies = authFrequencies

                data = q.get()
                if rec.AcceptWaveform(data):
                    pilot = json.loads(rec.FinalResult())
                    if not(str(pilot['text']) == "")  and "fox" in str(pilot['text']):
                        os.popen("debut.wav")
                        #print(pilot['text'])
                        if ifNeedCollation == False:
                            if airportData["OACI"] != "None":
                                rep = atc_paroles.reconaissanceATC(str(pilot['text']),callsign,clearance,frequency,airportData)
                            ifNeedCollation = rep[1]
                        elif "répéter" in pilot['text'] or "répétez" in pilot['text'] or "répété" in pilot['text']:
                            os.popen("conv.mp3")
                        else:
                            #print("En attente de collation '" + ifNeedCollation + "' ... ")
                            if ifNeedCollation in pilot['text'] or "copié" in pilot['text'] or "copier" in pilot['text']:
                                ifNeedCollation = False
                                print(Back.GREEN +"Collationné"+Style.RESET_ALL)
                                os.popen("collation.wav")
                            else:
                                print(Fore.RED +"Merci de collationner !"+Style.RESET_ALL + "("+ifNeedCollation+")")
                                print(pilot['text'])
                        if rep[0] != "":
                            clearance = rep[0]
                            if clearance != lastClearance:
                                print(Back.MAGENTA + "Nouvelle Clearance : " + clearance + Style.RESET_ALL)
                                lastClearance = clearance
                    #printHead()
                
                if dump_fn is not None:
                    dump_fn.write(data)


except KeyboardInterrupt:
    print('\nDone')
    parser.exit(0)
