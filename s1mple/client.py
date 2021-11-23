import socket
import threading

PORT = 5050 # PORT > 1024
#HOST = "192.168.1.84" # cmd -> ipconfig
HOST = socket.gethostbyname(socket.gethostname())
ADDRESS = (HOST, PORT)
DC_MESS = "!DISCONNECT" # client tell the server that they had DC, so no bugs in the future will happens


class Client():
    def __init__(self, socket_families, socket_type, socket_protocol=-1):
        self.client_socket = socket.socket(socket_families, socket_type, socket_protocol)

    def _connect(self, addr):
        self.client_socket.connect(addr)
        print(f'Connected to server {addr}')

    def _send(self, msg):
        msg = msg.encode('utf-8')
        self.client_socket.send(msg)

    def run(self):
        self._connect(ADDRESS)
        while True:
            message = input()
            self._send(message)
            if message == DC_MESS:
                break
        self.client_socket.close()


if __name__ == '__main__':
    '''client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect(ADDRESS)

    msg = "Hello! aaecaefascaewefdawlenflawejnfoiawjecawejpfkjap"
    msg = msg.encode('utf-8')
    client_socket.send(msg)
    msg = "!DISCONNECT"
    msg = msg.encode('utf-8')
    client_socket.send(msg)'''
    client = Client(socket.AF_INET, socket.SOCK_STREAM)
    client.run()
