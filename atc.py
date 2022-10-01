import argparse
import os
import queue
import sounddevice as sd
import vosk
import sys
import json
from colorama import Fore, Back, Style

import atc_paroles as atc

q = queue.Queue()

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
    with open(read_json, "r") as json_file:
        airportData = json.load(json_file)
    print(Fore.BLUE + "Fichier aéroport :" + read_json + Fore.GREEN + " chargé avec succès !" + Style.RESET_ALL)
#pprint.pprint(airportData)

print(Fore.GREEN +"ATC paramétré avec l'aéroport " + airportData["name"] + Style.RESET_ALL)

callsign = input("Your callsign : " + Fore.BLUE)
print(Style.RESET_ALL)
clearance = "sol"
lastClearance = clearance
ifNeedCollation = False
frequency = "Ground"
lastfrequency = frequency

rep = [clearance,ifNeedCollation,frequency]

os.system("title ATC by Nash115")

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
    print('Service ATC en fonction !'+ Fore.GREEN +' Bon vol !' + Style.RESET_ALL)
    print('#' * 73 + Fore.RED +"NASH115"+Style.RESET_ALL)

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
                data = q.get()
                if rec.AcceptWaveform(data):
                    parler = json.loads(rec.FinalResult())
                    if not(str(parler['text']) == "")  and "fox" in str(parler['text']):
                        os.popen("debut.wav")
                        #print(parler['text'])
                        if ifNeedCollation == False:
                            frequency = rep[2]
                            rep = atc.reconaissanceATC(str(parler['text']),callsign,clearance,frequency,airportData)
                            ifNeedCollation = rep[1]
                            frequency = rep[2]
                        elif "répéter" in parler['text'] or "répétez" in parler['text'] or "répété" in parler['text']:
                            os.popen("conv.mp3")
                        else:
                            #print("En attente de collation '" + ifNeedCollation + "' ... ")
                            if ifNeedCollation in parler['text'] or "copié" in parler['text'] or "copier" in parler['text']:
                                ifNeedCollation = False
                                print(Back.GREEN +"Collationné"+Style.RESET_ALL)
                                os.popen("collation.wav")
                                if frequency != lastfrequency:
                                    print( print(Back.BLUE +"Fréquence modifiée :" + frequency +Style.RESET_ALL))
                                    lastfrequency = frequency
                            else:
                                print(Fore.RED +"Merci de collationner !"+Style.RESET_ALL + "("+ifNeedCollation+")")
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
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
