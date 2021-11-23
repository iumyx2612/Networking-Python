import socket
import threading

from message import *

PORT = 5050 # PORT > 1024
#HOST = "192.168.1.84" # cmd -> ipconfig
HOST = socket.gethostbyname(socket.gethostname())
ADDRESS = (HOST, PORT)
DC_MESS = "!DISCONNECT" # client tell the server that they had DC, so no bugs in the future will happens


class Server():
    def __init__(self, socket_families, socket_type, socket_protocol=-1):
        # config socket object. Socket must have: families, type and protocol (optional)
        self.server_socket = socket.socket(socket_families, socket_type, socket_protocol)
        self.buffer = b""
        print("Starting Server...")

    def _listen(self, address):
        # bind socket object to address
        self.server_socket.bind(address)
        # make the socket listen to accept connections from clients
        self.server_socket.listen()
        print(f"Server is listening on {HOST}")

    def handle_client(self, conn, addr):
        # method to handle a single connection
        print(f'{addr} connected.')

        connected = True  # state variable to see if client is being connected
        while connected:
            # socket blocking, will not continue until we receive a message from a client
            # read message from a client and store it in the server's buffer
            # the buffer will then be pass to Message class to debug the message
            self.buffer = conn.recv(4096)  # args: number of bytes we want to receive
            if len(self.buffer) != 0:
                message = Message(self.buffer, addr)
                message.handle_receive()
                print(message.content)
        conn.close()

    def run(self):
        self._listen(ADDRESS)
        while True: # event loop until we don't want to listen to connections anymore
            # conn: new socket object use to send and receive data on the connection
            # addr: address bound to the socket on the other end of connection
            conn, addr = self.server_socket.accept() # this will block the socket, make it wait for new connection

            # make multiple threads so the connected server and client doesn't have to wait for new connection to communicate
            # Handle communication
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            # check number of threads active
            print(
                f'Threads active: {threading.active_count() - 1}')  # subtract 1 because one thread for listening new connections


if __name__ == '__main__':
    server = Server(socket.AF_INET, socket.SOCK_STREAM)
    server.run()
























