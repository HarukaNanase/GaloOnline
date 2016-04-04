import socket


class socketUDP:
    """Create a UDP Socket to use with GaloOnline"""
    def __init__(self,sock=None):
        if sock is None:
                self.Sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            self.sock = sock


    def connect(self, host, port):
        self.sock.connect((host, port))

    def mysend(self, msg):
        bytesSent = 0
        while bytesSent < len(msg):
              sent = self.sock.send(msg[bytesSent:])
              if sent == 0:
                  raise RuntimeError("A ligaçao foi quebrada")
              bytesSent = bytesSent + sent


