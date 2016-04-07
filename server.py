from GaloOnlineAPI import *
import os


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



def CheckDir():
    if os.path.exists(UsersPath):
        return True
    else:
        os.makedirs(UsersPath)
        return False


def CreateAccount(name, password, Accounts):
    if os.path.isfile(UsersPath + name + FileExtension) or name in Accounts:
        return False
    else:
        try:
            userfile = open(UsersPath + name + FileExtension, 'a+')
            userfile.write(password)
            userfile.close()
            Accounts[name] = password
            print("Account created!")
            #return accounts
        except IOError:
            print("Error opening file.")
            return False


def LoadAccounts(Accounts):
    files = []
    for(dirpath, dirnames, filenames) in os.walk(UsersPath):
        files.extend(filenames)
    for(FileName) in files:
        try:
            OpenFile = open(UsersPath + FileName)
            UserPassword = OpenFile.read()
            OpenFile.close()
            username = os.path.splitext(FileName)
            Accounts[username[0]] = UserPassword
        except IOError:
            print("Error loading account database... Server won't be loaded with any account")
            continue


def Login(name, password, Accounts, LoggedInUsers, UserIP):
    if os.path.isfile(UsersPath + name + FileExtension) or name in Accounts:
        try:
            userfile = open(UsersPath + name + FileExtension, 'r')

            userData = userfile.read()

            userData = userData.split()

            passUser = userData[0]

            userfile.close()
            if password == passUser:
                LoggedInUsers[name] = UserIP
                return True
            else:
                return False
        except IOError:
            print("Error while reading file during login.")
            return False
    else:
        return False


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
        print(OpCode[1])
        print(OpCode[2])
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
        else:
            continue


if __name__ == '__main__':
    main()




