import os

def display(str):
    print(str)

def defTitleOfWindow(str):
    os.system("title " + str)

def clear():
    os.system("cls")

def printHead():
    clear()
    display('#' * 80)
    if frequency in authFrequencies:
        display("#" + 'Service ATC en fonction !'+ Fore.GREEN +' Bon vol !' + Style.RESET_ALL + ((27-len(frequency))*" ") + Back.CYAN + Fore.BLACK + " " + callsignD + " " + Style.RESET_ALL + " " + Back.BLUE + " " + frequency + " mHz " + Style.RESET_ALL + " #")
    else:
        display("#" + 'Service ATC en fonction !'+ Fore.GREEN +' Bon vol !' + Style.RESET_ALL + ((27-len(frequency))*" ") + Back.CYAN + Fore.BLACK + " " + callsignD + " " + Style.RESET_ALL + " " + Back.RED + " " + frequency + " mHz " + Style.RESET_ALL + " #")
    display('#' * 80)
    display("#" + "Airport : " + airportData["OACI"] + " "*5 + "Freq : " + str(authFrequencies) + " "*(52-len(str(authFrequencies))) + "#")
    display('#' * 80)