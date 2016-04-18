from GaloOnlineAPI import *
from JogoGaloNetwork import *

#Define
Sender = "Server"
THIS = "Client"
Version = "v0.02"

ServerAddress = (ServerIP, Port)
ClientSocket = CreateSocket(THIS)
SuccessMessage = "ACK"
ErrorMessage = "ERR"
comandos = ["/login","/registo","/invite","/inviteon","/lista"]
#EndDefine

Username = ""
GameRoom = -1
LoggedIn = False
print("Bem vindo ao cliente do GaloOnline\nVersão:"+Version+"\nHave Fun!\n")

print("Escreva /registo para se registar!\nSe já se encontrar registado, utilize /login para efectuar o seu login")

while(True):
        if LoggedIn == False:
            print("")
            print("Lista de comandos:")
            print("/login - Efectue o login")
            print("/registo - Efectue o registo")

        if LoggedIn == True:
            print("")
            print("/invite - Convide um jogador para jogar consigo! (Só funciona após o login")
            print("/lista - Peça a lista de jogadores e os seus estados")
            print("/inviteon - Entre em modo de ser convidado")

        command = input("Introduza o seu comando:")
        if command == "/registo" and not LoggedIn:
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
        if command == "/login" and not LoggedIn:
            username = input('Introduza o seu username:')
            password= input('Introduza a sua password:')
            if(username == "" or password == ""):
                print("Introduziu um username ou password invalidos!")
                continue
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
                        LoggedIn = True
                    else:
                        print("Failed to login. Wrong username or password")
        elif command == "/lista" and LoggedIn:
                Sent = WriteToSocket(ClientSocket, "LIST", ServerAddress)
                Received = ReadPackets(ClientSocket)
                print(Received)

        elif command == "/invite" and LoggedIn:
            PlayerNr2 = input("Introduza o nome do jogador que deseja convidar:")
            if PlayerNr2 == "":
                print("Introduziu um nome invalido! Tente novamente.")
                continue
            while PlayerNr2 == Username:
                    PlayerNr2 = input("Não pode convidar-se a si proprio. Introduza outro nome:")
            InviteMessage = "INV " + Username + " " + PlayerNr2
            Sent = WriteToSocket(ClientSocket, InviteMessage, ServerAddress)
            Read = ReadFromSocket(ClientSocket)
            Read = Read[0].split()
            if Read[0] == "ACCEPT":
                print("Irá ser colocado num jogo com o jogador: " + PlayerNr2)
                #TODO
                Read = ReadFromSocket(ClientSocket)
                GameRoom = Read[0]
                print("Sala do jogo: ", GameRoom)
                player = "1"
                Symbol = "X"
                turno = 1
                Board = NewBoard()
                while CheckWinner(Board) == "False" and turno < 9:
                    if turno%2 != 0:
                        print("It's your turn to play!")
                        CurrentBoard(Board)
                        Jogada = ReadPlay(Board)
                        Play(Board, Jogada, Symbol)
                        Msg = "PLAY " + GameRoom + " " + Jogada
                        WriteToSocket(ClientSocket,Msg,ServerAddress)
                        turno += 1
                    else:
                        CurrentBoard(Board)
                        Read = ReadFromSocket(ClientSocket)
                        Read = Read[0].split()
                        if Read[0] == "PLAY" and Read[1] == GameRoom:
                            Play(Board, Read[2], "O")
                            CurrentBoard(Board)
                            print("O jogador adversário jogou na posiçao: ", Read[2])
                            turno += 1
                CurrentBoard(Board)
                Winner = CheckWinner(Board)
                if(Winner == Symbol):
                    Sent = WriteToSocket(ClientSocket,"LOSE" + " " + GameRoom, ServerAddress)
                    print("Awaiting result...")
                    Read = ReadFromSocket(ClientSocket)
                    print("Parabens! Ganhou o jogo.")
                else:
                    Sent = WriteToSocket(ClientSocket,"WIN" + " " + GameRoom ,ServerAddress)
                    print("Awaiting result...")
                    Read = ReadFromSocket(ClientSocket)
                    print("Para a proxima corre melhor!")
            else:
                print("O convite foi recusado.")
                continue

        elif command == "/inviteon" and LoggedIn:
            Sent = WriteToSocket(ClientSocket, "INVON" + " " + Username, ServerAddress)
            print("Now awaiting an invite from a player...")
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
                        Sent = WriteToSocket(ClientSocket, "ACCEPT" + " " + Invite[1] + " " + Invite[2], EndPointIP)
                        Read = ReadFromSocket(ClientSocket)
                        GameRoom = Read[0]
                        print("Sala de jogo: ", GameRoom)
                        player = "2"
                        turno = 1
                        Symbol = "O"
                        Board = NewBoard()
                        while(CheckWinner(Board) == "False"):
                            if turno % 2 != 0:
                                CurrentBoard(Board)
                                print("Awaiting the other player's turn")
                                Read = ReadFromSocket(ClientSocket)
                                Read = Read[0].split()
                                if Read[0] == "PLAY" and Read[1] == GameRoom:
                                    Play(Board, Read[2], "X")
                                    CurrentBoard(Board)
                                    print("O jogador adversário jogou na posiçao: ", Read[2])
                                    turno += 1
                            else:
                                print("It's your turn to play")
                                CurrentBoard(Board)
                                Jogada = ReadPlay(Board)
                                Play(Board, Jogada, Symbol)
                                Msg = "PLAY " + GameRoom + " " + Jogada
                                WriteToSocket(ClientSocket, Msg, ServerAddress)
                                turno += 1
                        CurrentBoard(Board)
                    #  Sent = WriteToSocket(ClientSocket, "WIN" + " " + GameRoom, ServerAddress)
                        print("Awaiting result...")
                        Read = ReadFromSocket(ClientSocket)
                        Read = Read[0].split()
                        if(CheckWinner(Board) == Symbol):
                            print("You won the game!")
                        else:
                            print("You lost the game!")

                    else:
                        Sent = WriteToSocket(ClientSocket, ErrorMessage, EndPointIP)
                        continue



        else:
            if command not in comandos:
                print("Esse comando não existe.")
                continue
            elif not LoggedIn:
                print("Tem de efectuar o login para utilizar esse comando.")
            elif LoggedIn:
                print("Para efectuar esse commando não pode estar loggado.")