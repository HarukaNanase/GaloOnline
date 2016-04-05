import socket


#Define
ServerIP = socket.gethostname()
Port = 8000
UsersPath = "./users/"
FileExtension = ".txt"
SuccessMessage = "ACK"
ErrorMessage = "ERR"
MessageMaxSize = 256
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
        data = ServerSocket.recvfrom(256)
        UserEndPoint = data[1]
        userMsg = data[0]
        userMsg = userMsg.split()

        if userMsg[0] == SuccessMessage:
            return True
        else:
            print("Error on receiving ACK from client " + data[1][0])
            return False
    except socket.error:
        print("Unable to send message to address %s", address)
        return False


def ReadFromSocket(ServerSocket):
    DataRead = ServerSocket.recvfrom(MessageMaxSize)
    if(DataRead[0] == ""):
        ServerSocket.sendto(ErrorMessage,)

