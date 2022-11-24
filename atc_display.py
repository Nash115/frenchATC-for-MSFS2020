import os

def display(str):
    print(str)

def defTitleOfWindow(str):
    os.system("title " + str)

def clear():
    os.system("cls")