import socket
import os

#Define
Port = 8000
UsersPath = "./users/"
FileExtension = ".txt"

#EndDefine
def CheckDir():
    if os.path.exists(UsersPath):
        return True
    else:
        os.makedirs(UsersPath)
        return False


def CreateServerSocket():
    try:
        ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("Socket Sucessfully Created!")
        ServerSocket.bind((socket.gethostname(), Port))
        print("Socket binded Sucessfully")
        return ServerSocket
    except socket.error:
        print("Unable to create Socket.")


def WriteToSocket(ServerSocket, msg, address):
    try:
        ServerSocket.sendto(msg, address)
        return True
    except socket.error:
        print("Unable to send message to address %s", address)
        return False


def ReadFromSocket(ServerSocket):
    return ServerSocket.recvfrom(256)


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
            return accounts
        except IOError:
            print("Error opening file.")
            return False

def LoadAccounts():
    #TODO


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
    LoggedInUsers = {}
    ServerSocket = CreateServerSocket()
    print(socket.gethostname())
    while 1:
        Data = ReadFromSocket(ServerSocket)
        UserIP = Data[1]
        OpCode = Data[0].decode()
        print(OpCode)
        OpCode = OpCode.split()
        print(OpCode[0])
        print(OpCode[1])
        print(OpCode[2])
        if OpCode[0] == "REG":
            Sucess = CreateAccount(OpCode[1], OpCode[2], Accounts)
            if Sucess == False:
                print("Account creation failed. Now continuing.")
                continue
            else:
                #Accounts = Sucess
                print(Accounts)
        else:
            continue


if __name__ == '__main__':
    main()




