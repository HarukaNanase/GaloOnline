import socket
#Define
ServerIP = socket.gethostname()
Port = 8000
#UsersPath = "./users/"
#FileExtension = ".txt"
SuccessMessage = "ACK"
ErrorMessage = "ERR"
MessageMaxSize = 256
#EndDefine

#Message Encodes
SuccessMessage = SuccessMessage.encode()
ErrorMessage = ErrorMessage.encode()
#

