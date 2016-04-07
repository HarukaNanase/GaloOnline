from GaloOnlineAPI import *

#Define
Sender = "Server"
THIS = "Client"
Version = "v0.02"
ServerIP = "Acer7745G"
Port = 8000
ServerAddress = (ServerIP, Port)
ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
SuccessMessage = "ACK"
ErrorMessage = "ERR"
#EndDefine


#Message Encodes
SuccessMessage = SuccessMessage.encode()
ErrorMessage = ErrorMessage.encode()
#


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
                else:
                    print("Failed to login. Wrong username or password")






