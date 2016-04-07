import socket
#Define
Sender = "Client"
#THIS = "Server"
ServerIP = socket.gethostname()
Port = 8000
#UsersPath = "./users/"
#FileExtension = ".txt"
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


def CreateSocket(THIS):
    if(THIS == "Client"):
        try:
            ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            return ClientSocket
        except socket.error:
            print("Error creating Client Socket.")
    else:
        try:
            ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print("Socket Sucessfully Created!")
            ServerSocket.bind((ServerIP, Port))
            print("Socket binded Sucessfully")
            return ServerSocket
        except socket.error:
            print("Unable to create Socket.")


def WriteToSocket(Socket, msg, address):
    try:
        msg = msg.encode()
        Socket.sendto(msg, address)
        data = 0
        i = 0
        Socket.settimeout(TimeOut)
        while i < NumberOfTries:
            data = Socket.recvfrom(MessageMaxSize)
            if data == 0:
                Socket.sendto(msg, address)
                i += 1
            else:
                Socket.settimeout(None)
                break
        UserEndPoint = data[1]
        userMsg = data[0]
        userMsg = userMsg.decode()
        #  print(userMsg)

        if userMsg == SuccessMessage.decode():
            print("Message Successfully Sent. Received ACK from:", UserEndPoint[0] + ":", UserEndPoint[1])
            return True
        else:
            print("Error on receiving ACK from " + data[1][0])
            return False
    except socket.error:
        print("Unable to send message to address: ", address)
        return False


def ReadFromSocket(Socket):
    Received = 0
    Received = Socket.recvfrom(MessageMaxSize)
    if Received == 0:
        print("Didn't receive anything. Error on socket / Nothing was sent to us.")
        return False
    else:
        ReceivedMsg = Received[0].decode()
        SenderEndPoint = Received[1]
        if ReceivedMsg != "":
            Socket.sendto(SuccessMessage, SenderEndPoint)
            return ReceivedMsg, SenderEndPoint
        else:
            Socket.sendto(ErrorMessage, SenderEndPoint)
            return False

