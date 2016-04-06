from GaloOnlineAPI import *
import os

#Define
Sender = "Client"
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
SuccessMessage = SuccessMessage.encode()
ErrorMessage = ErrorMessage.encode()
#

def CreateServerSocket():
    try:
        ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("Socket Sucessfully Created!")
        ServerSocket.bind((ServerIP, Port))
        print("Socket binded Sucessfully")
        return ServerSocket
    except socket.error:
        print("Unable to create Socket.")


def WriteToSocket(ServerSocket, msg, address):
    try:
        ServerSocket.sendto(msg, address)
        data = 0
        i = 0
        ServerSocket.settimeout(TimeOut)
        while i < NumberOfTries:
            data = ServerSocket.recvfrom(MessageMaxSize)
            if data == 0:
                ServerSocket.sendto(msg, address)
                i += 1
            else:
                ServerSocket.settimeout(None)
                break
        UserEndPoint = data[1]
        userMsg = data[0]
        userMsg = userMsg.decode()
        #  print(userMsg)

        if userMsg == SuccessMessage.decode():
            print("Message Successfully Sent. Received ACK from:", Sender +" " + UserEndPoint[0] + ":" +"%d", UserEndPoint[1])
            return True
        else:
            print("Error on receiving ACK from client " + data[1][0])
            return False
    except socket.error:
        print("Unable to send message to address: ", address)
        return False


def ReadFromSocket(ServerSocket):
    return ServerSocket.recvfrom(MessageMaxSize)

def CheckDir():
    if os.path.exists(UsersPath):
        return True
    else:
        os.makedirs(UsersPath)
        return False


def CreateAccount(name, password, accounts):
    if os.path.isfile(UsersPath + name + FileExtension):
        return False
    else:
        try:
            userfile = open(UsersPath + name + FileExtension, 'a+')
            userfile.write(password)
            userfile.close()
            accounts[name] = password
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


def Login(name, password):
    if os.path.isfile(UsersPath + name + FileExtension):
        try:
            userfile = open(UsersPath + name + FileExtension, 'r')

            userData = userfile.read()

            userData = userData.split()

            passUser = userData[0]

            userfile.close()
            if password == passUser:
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
    ServerSocket = CreateServerSocket()
    print("Hosting @"+ServerIP)
    while 1:
        Data = ReadFromSocket(ServerSocket)
        UserIP = Data[1]
        OpCode = Data[0].decode()
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
        else:
            continue


if __name__ == '__main__':
    main()




