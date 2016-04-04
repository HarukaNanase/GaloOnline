import socket
import getpass

print("Bem vindo ao cliente do GaloOnline\nVersão 0.01\nHave Fun!\n\n")

print("Escreva /registo para se registar!\nSe já se encontrar registado, utilize /login para efectuar o seu login")

while(True):
    command = input("Introduza o seu comando:")
    if command == "/registo":
        print("Irá proceder ao registo de uma conta no GaloOnline.\nAo se registar está a aceitar os termos"
              "e condições propostas.")
        tos = input('Aceita as condiçoes? Y/N:')
        if tos == "Y" or tos == "y":
            username = input('Introduza o username desejado:')
            password = getpass.getpass("Introduza a password desejada:")
            #TODO: Ligação ao servidor para o registo


