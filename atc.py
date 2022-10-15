# Version : 2022-10-15

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
import atc_paroles as atc
import atc_fs


q = queue.Queue()

alphabet_min = "abcdefghijklmnopqrstuvwxyz"
alphabet_maj = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphabetAero = ["alpha","bravo","charlie","delta","echo","fox","golf","hotel","india","juliet","kilo","lima","mike","november","oscar","papa","quebec","romeo","sierra","tango","uniform","victor","whisky","x-ray","yankee","zulu"]

airport = input("OACI code of your airport :")
read_json = "assets/airports/" + airport + ".json"

airportData = {}

if not os.path.exists(read_json):
    print(Fore.BLUE + "Fichier aéroport :" + read_json + Fore.RED + " inexistant..." + Style.RESET_ALL)
    print(Fore.YELLOW +"Le code OACI de l'aéroport saisi est inconnu. Vérifier l'ortographe.")
    print("Si l'ortographe est correct, l'aéroport n'a pas été paramétré pour ce programme, vous pouvez le créer et lui donner le nom OACI correct." + Style.RESET_ALL)
    os.system("pause")
    exit()
else:
    with open(read_json, "r", encoding="utf-8") as json_file:
        airportData = json.load(json_file)
    print(Fore.BLUE + "Fichier aéroport :" + read_json + Fore.GREEN + " chargé avec succès !" + Style.RESET_ALL)
#pprint.pprint(airportData)

print(Fore.GREEN +"ATC paramétré avec l'aéroport " + airportData["name"] + Style.RESET_ALL)

callsignD = input("Votre immatriculation (F-ABCD) : " + Fore.BLUE)
callsign = ""
carractsLettres = [0,4,5]
caract = 0

if len(callsignD) == 6 and "-" in callsignD and (callsignD[0] == "F" or callsignD == "f"):
    for i in callsignD:
        if i in alphabet_min and caract in carractsLettres:
            callsign += alphabetAero[alphabet_min.index(i)]
            callsign += " "
        elif i in alphabet_maj and caract in carractsLettres:
            callsign += alphabetAero[alphabet_maj.index(i)]
            callsign += " "
        caract += 1
else:
    print(Fore.RED + "Immatriculation invalide" + Style.RESET_ALL)
    os.system("pause")
    exit()

print(Fore.BLUE + "Indicatif d'appel :" + callsign + Style.RESET_ALL)

os.system("title ATC by Nash115 - " + airportData["OACI"] + " ("+callsignD+")")

print(Fore.CYAN + "Frequencies :")
print("🛩️ Ground : " + airportData["frequency"]["grd"][1])
print("🛫 Tower  : " + airportData["frequency"]["twr"][1])
print("✈️ Appr   : " + airportData["frequency"]["app"][1] + Style.RESET_ALL)

authFrequencies = [airportData["frequency"]["grd"][1],airportData["frequency"]["twr"][1],airportData["frequency"]["app"][1]]

clearance = "sol"
lastClearance = clearance
ifNeedCollation = False

# tryFrequency = True
# while tryFrequency:
#     frequency = input("Frequency : " + Fore.BLUE)
#     if airportData["frequency"]["grd"][1] == frequency:
#         tryFrequency = False
#     elif airportData["frequency"]["twr"][1] == frequency:
#         tryFrequency = False
#     elif airportData["frequency"]["app"][1] == frequency:
#         tryFrequency = False
#     else:
#         print(Fore.RED + "FREQUENCE INVALIDE - COMMUNICATION IMPOSSIBLE" + Style.RESET_ALL)

frequency = str(atc_fs.getFrequency(airportData["frequency"]["grd"][1]))
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
        print("#" + 'Service ATC en fonction !'+ Fore.GREEN +' Bon vol !' + Style.RESET_ALL + ((27-len(airportData["frequency"]["grd"][1])-4)*" ") + Back.CYAN + Fore.BLACK + " " + callsignD + " " + Style.RESET_ALL + " " + Back.RED + " GRD:" + airportData["frequency"]["grd"][1] + " mHz " + Style.RESET_ALL + " #")
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
                frequency = str(atc_fs.getFrequency(frequency))
                if frequency != lastfrequency:
                    print(Back.BLUE +"Fréquence modifiée :" + frequency +Style.RESET_ALL)
                    lastfrequency = frequency
                    printHead()

                data = q.get()
                if rec.AcceptWaveform(data):
                    pilot = json.loads(rec.FinalResult())
                    if not(str(pilot['text']) == "")  and "fox" in str(pilot['text']):
                        os.popen("debut.wav")
                        #print(pilot['text'])
                        if ifNeedCollation == False:
                            rep = atc.reconaissanceATC(str(pilot['text']),callsign,clearance,frequency,airportData)
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
