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

NumberOfTries = 5
TimeOut = 2
#EndDefine

#Message Encodes

#

def main():
    CheckDir()
    Accounts = {}
    Jogos = []
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
                # Accounts = Sucess
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

        if CheckLoggedIn(LoggedInUsers, UserIP):
                if OpCode[0] == "LIST" and CheckLoggedIn(LoggedInUsers, UserIP):
                    StateList = {}
                    for user in LoggedInUsers:
                        State = LoggedInUsers.get(user)
                        State = State[1]
                        StateList[user] = State
                        print(StateList)
                        print("Tamanho da lista a enviar:", len(StateList))
                        print(SendPackets(ServerSocket, StateList, UserIP))
                elif OpCode[0] == "INV":

                    User1 = OpCode[1]
                    User2 = OpCode[2]
                    User1IP = LoggedInUsers.get(User1)[0]
                    User2IP = LoggedInUsers.get(User2)[0]
                    if (LoggedInUsers.get(User2)[1] == "Playing"):
                        Sent = WriteToSocket(ServerSocket, ErrorMessage, User1IP)
                        continue
                    OpCode = OpCode[0] + " " + OpCode[1] + " " + OpCode[2]
                    Sent = WriteToSocket(ServerSocket, OpCode, User2IP)
                    Read = ReadFromSocket(ServerSocket)

                    if Read[0] == SuccessMessage:
                        Sent = WriteToSocket(ServerSocket, SuccessMessage, User1IP)
                        LoggedInUsers[User1] = (LoggedInUsers.get(User1)[0], "Playing")
                        LoggedInUsers[User2] = (LoggedInUsers.get(User2)[0], "Playing")
                        Jogos.append((len(Jogos), (User1, User2)))
                        Sent = WriteToSocket(ServerSocket, str(len(Jogos) - 1), User1IP)
                        Sent = WriteToSocket(ServerSocket, str(len(Jogos) - 1), User2IP)
                        continue
                    else:
                        Sent = WriteToSocket(ServerSocket, ErrorMessage, User1IP)
                        continue
        else:

            continue

if __name__ == '__main__':
    main()




