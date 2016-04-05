import socket
import getpass
import sys

#Define
Version = "v0.02"
ServerAddress = "Acer7745G"
Port = 8000
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
        tos = input('Aceita as condiçoes? Y/N:')
        if tos == "Y" or tos == "y":
            username = input('Introduza o username desejado:')
            password = input('Introduza a password desejada:')
            MsgToSend = "REG "+ username + " " + password
            Sent = ClientSocket.sendto(MsgToSend.encode(), (ServerAddress, Port))
            if Sent == 0:
                print("Nothing was sent. Error?")
            else:
                print("Message was sucessfully sent!")
                print("Now awaiting server answer...")
                #i = 0
                #while i < 5:
                Received = ClientSocket.recvfrom(256)
                ServerAns = Received[0]
                ServerAns = ServerAns.decode()
                ServerAns = ServerAns.split()
                if ServerAns[0] == 0:
                    print("Didn't receive anything from server...")
                elif ServerAns[0] == "ERR":
                    print("Erro no servidor. Conta não foi criada.")
                    ClientSocket.sendto(SuccessMessage,(ServerAddress, Port))
                else:
                    if ServerAns[0] == "ACK":
                        ClientSocket.sendto(SuccessMessage, (ServerAddress, Port))
                        print("Conta Registada com sucesso!")
                #       break
            #TODO: Ligação ao servidor para o registo



