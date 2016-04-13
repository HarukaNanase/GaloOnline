from GaloOnlineAPI import *
import json
import sys
import select
import threading


#Define
Sender = "Server"
THIS = "Client"
Version = "v0.02"
ServerIP = "Balbadd"
Port = 8000
ServerAddress = (ServerIP, Port)
ClientSocket = CreateSocket(THIS)
SuccessMessage = "ACK"
ErrorMessage = "ERR"

#EndDefine


Console = False
Socket = False


Username = ""
GameRoom = -1

print("Bem vindo ao cliente do GaloOnline\nVersão:"+Version+"\nHave Fun!\n")

print("Escreva /registo para se registar!\nSe já se encontrar registado, utilize /login para efectuar o seu login")

while(True):
        command = input("Introduza o seu comando:")
        if command == "/registo":
            print("Irá proceder ao registo de uma conta no GaloOnline.\nAo se registar está a aceitar os termos"
                  " e condições propostas.")
            tos = ""
            while tos != "Y" or tos != "y" or tos != "N" or tos != "n":
                tos = input('Aceita as condiçoes? Y/N:')
                if tos == "N" or tos == "n" or tos == "Y" or tos == "y":
                    break
            if tos == "N" or tos == "n":
                continue
            else:
                username = input('Introduza o username desejado:')
                password = input('Introduza a password desejada:')
                MsgToSend = "REG "+ username + " " + password
                Sent = WriteToSocket(ClientSocket, MsgToSend, ServerAddress)
                if Sent == 0:
                    print("Nothing was sent. Error?")
                else:
                    print("Message was sucessfully sent!")
                    print("Now awaiting server answer...")
                    Answer = ReadFromSocket(ClientSocket)
                    if Answer == 0:
                        print("Error receiving answer from server.")
                    else:
                        if(Answer[0] == "ACK"):
                            print("Account Sucessfully Created! Welcome to GaloOnline.")
                        else:
                            print("Account not created. User already exists.")
        if command == "/login":
            username = input('Introduza o seu username:')
            password= input('Introduza a sua password:')
            MsgToSend = "LOG " + username + " " + password
            Sent = WriteToSocket(ClientSocket, MsgToSend, ServerAddress)
            if Sent == 0:
                print("Nothing was sent. Error?")
            else:
                Answer = ReadFromSocket(ClientSocket)
                print("Logging in...")
                if Answer == 0:
                    print("Error logging in. Failed to receive an answer from the server.")
                else:
                    if(Answer[0] == "ACK"):
                        print("Welcome to GaloOnline. Here's the menu for the game options")
                        Username = username
                    else:
                        print("Failed to login. Wrong username or password")
        elif command == "/lista":
                Sent = WriteToSocket(ClientSocket, "LIST", ServerAddress)
                Received = ReadPackets(ClientSocket)
                print(Received)

        elif command == "/invite":
            PlayerNr2 = input("Introduza o nome do jogador que deseja convidar:")
            InviteMessage = "INV " + Username + " " + PlayerNr2
            Sent = WriteToSocket(ClientSocket, InviteMessage, ServerAddress)
            Read = ReadFromSocket(ClientSocket)

            if Read[0] == SuccessMessage:
                print("Irá ser colocado num jogo com o jogador: " + PlayerNr2)
                #TODO
                Read = ReadFromSocket(ClientSocket)
                GameRoom = Read[0]
                print("Sala do jogo: ", GameRoom)
                continue
            else:
                print("O convite foi recusado.")
                continue

        elif command == "/inviteon":
            Invite = ReadFromSocket(ClientSocket)
            print(Invite)
            EndPointIP = Invite[1]
            Invite = Invite[0].split()
            if Invite[0] == "INV":
                if Invite[2] == Username:
                    print("Foi convidado para jogar pelo jogador: " + Invite[1])
                    accept = ""
                    while accept != "Y" or accept != "y" or accept != "N" or accept != "n":
                        accept = input("Deseja Aceitar? Y/N:")
                        if accept == "N" or accept == "n" or accept == "Y" or accept == "y":
                            break

                    if accept == "y" or accept == "Y":
                        Sent = WriteToSocket(ClientSocket, SuccessMessage, EndPointIP)
                        Read = ReadFromSocket(ClientSocket)
                        GameRoom = Read[0]
                        print("Sala de jogo: ", GameRoom)
                    else:
                        Sent = WriteToSocket(ClientSocket, ErrorMessage, EndPointIP)


