from GaloOnlineAPI import *
from AccountSystem import *



#Define
Sender = "Client"
THIS = "Server"

SuccessMessage = "ACK"
ErrorMessage = "ERR"

#EndDefine



def main():
    CheckDir()
    Accounts = {}
    Jogos = {}
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
            print("Tamanho da lista a enviar:", len(StateList))
            print(SendPackets(ServerSocket, StateList, UserIP))
        elif OpCode[0] == "INV":

            User1 = OpCode[1]
            User1IP = LoggedInUsers.get(User1)[0]
            if (not CheckLogin(LoggedInUsers, OpCode[0])):
                Sent = WriteToSocket(ServerSocket, ErrorMessage, User1IP)
                continue
            User2 = OpCode[2]

            User2IP = LoggedInUsers.get(User2)[0]

            print(User1IP)
            print(User2IP)
            if (LoggedInUsers.get(User2)[1] == "Playing" or LoggedInUsers.get(User2)[1] == "Invited"):
                Sent = WriteToSocket(ServerSocket, ErrorMessage, User1IP)
                continue
            OpCode = OpCode[0] + " " + OpCode[1] + " " + OpCode[2]
            Sent = WriteToSocket(ServerSocket, OpCode, User2IP)
            LoggedInUsers[User2] = User2IP, "Invited"


        elif OpCode[0] == "PLAY":
            GameRoomID = int(OpCode[1])
            PlayPosition = OpCode[2]
            print(Jogos.get(GameRoomID))
            Player1 = Jogos.get(GameRoomID)[0]
            Player2 = Jogos.get(GameRoomID)[1]
            Player1IP = LoggedInUsers.get(Player1)[0]
            Player2IP = LoggedInUsers.get(Player2)[0]
            print(Player2IP)
            MessageForClient = "PLAY " + str(GameRoomID) + " " + PlayPosition
            if(UserIP == Player1IP):
                WriteToSocket(ServerSocket, MessageForClient, Player2IP)
            else:
                WriteToSocket(ServerSocket, MessageForClient, Player1IP)

        elif (OpCode[0] == "WIN" or OpCode[0] == "LOSE") and int(OpCode[1]) in Jogos:
            print(Jogos)
            print(Jogos.get(int(OpCode[1])))
            Player1 = Jogos.get(int(OpCode[1]))[0]
            Player2 = Jogos.get(int(OpCode[1]))[1]
            Player1IP = LoggedInUsers.get(Player1)[0]
            Player2IP = LoggedInUsers.get(Player2)[0]
            Sent = WriteToSocket(ServerSocket, SuccessMessage, Player1IP)
            print(Sent)
            Sent = WriteToSocket(ServerSocket, SuccessMessage, Player2IP)
            print(Sent)
            LoggedInUsers[Player1] = Player1IP, "Online"
            LoggedInUsers[Player2] = Player2IP, "Online"
            #Remover o jogo da sala de jogos?? ou guardar historico?

        elif (OpCode[0] == "ACCEPT"):
                User1 = OpCode[1]
                User2 = OpCode[2]
                User1IP = LoggedInUsers.get(User1)[0]
                User2IP = LoggedInUsers.get(User2)[0]
                Sent = WriteToSocket(ServerSocket, OpCode[0] + " " + OpCode[1] + " " + OpCode[2], User1IP)
                LoggedInUsers[User1] = (LoggedInUsers.get(User1)[0], "Playing")
                LoggedInUsers[User2] = (LoggedInUsers.get(User2)[0], "Playing")
                Jogos[len(Jogos)] = (User1, User2)
                print(Jogos)
                Sent = WriteToSocket(ServerSocket, str(len(Jogos) - 1), User1IP)
                Sent = WriteToSocket(ServerSocket, str(len(Jogos) - 1), User2IP)

        elif (OpCode[0] == "DENY"):
            User1 = OpCode[1]
            User2 = OpCode[2]
            User1IP = LoggedInUsers.get(User1)[0]
            User2IP = LoggedInUsers.get(User2)[0]

            Sent = WriteToSocket()




        elif (OpCode[0] == "INVON"):
            User1 = OpCode[1]
            LoggedInUsers[User1] = LoggedInUsers.get(User1)[0], "Invitable"

        else:
            continue


if __name__ == '__main__':
    main()




