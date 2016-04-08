from GaloOnlineAPI import *
from AccountSystem import *
import json
import sys


#Define
Sender = "Client"
THIS = "Server"
ServerIP = socket.gethostname()
Port = 8000
UsersPath = "./users/"
FileExtension = ".txt"
SuccessMessage = "ACK"
ErrorMessage = "ERR"
MessageMaxSize = 256
NumberOfTries = 5
TimeOut = 2
#EndDefine

#Message Encodes

#

def main():
    CheckDir()
    Accounts = {}
    LoadAccounts(Accounts)
    print(Accounts)
    LoggedInUsers = {}
    ServerSocket = CreateSocket(THIS)
    print("Hosting @"+ServerIP)
    while 1:
        Data = ReadFromSocket(ServerSocket)
        UserIP = Data[1]
        OpCode = Data[0]
        print("Mensagem recebida: ", OpCode)
        OpCode = OpCode.split()
        print(OpCode[0])
        if OpCode[0] == "REG":
            Success = CreateAccount(OpCode[1], OpCode[2], Accounts)
            if Success == False:
                print("Account creation failed. Now continuing.")
                WriteToSocket(ServerSocket, ErrorMessage, UserIP)
            else:
                WriteToSocket(ServerSocket, SuccessMessage, UserIP)
                #Accounts = Sucess
                print(Accounts)
        elif OpCode[0] == "LOG":
            Success = Login(OpCode[1], OpCode[2], Accounts, LoggedInUsers, UserIP)
            if Success:
                WriteToSocket(ServerSocket, SuccessMessage, UserIP)
                print("User " + OpCode[1] + " has logged in.")
                print(LoggedInUsers)
            else:
                WriteToSocket(ServerSocket, ErrorMessage, UserIP)
                print("User " + OpCode[1] + " has entered a wrong password./")
        elif OpCode[0] == "LIST":
            StateList = {}
            for user in LoggedInUsers:
                State = LoggedInUsers.get(user)
                State = State[1]
                StateList[user] = State
            print(StateList)
            StateList = json.dumps(StateList)
            print("Tamanho da lista a enviar:", len(StateList))
            print(WriteToSocket(ServerSocket, StateList, UserIP))
        else:
            continue


if __name__ == '__main__':
    main()




