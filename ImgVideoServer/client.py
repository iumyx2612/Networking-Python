import socket
import threading
from message import *

import os
import io

from PIL import Image
import numpy as np
import base64

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

    def _send(self, image_path):
        try:
            with open(image_path, 'rb') as f:
                image_bytes = f.read() # read image as bytes
                image_name = os.path.basename(image_path)
                message = Message(image_bytes).create_image_byte_data(image_name)
                self.client_socket.send(message)
        except FileNotFoundError:
            print("Invalid path")
            pass

    def run(self):
        self._connect(ADDRESS)
        while True:
            image_path = input()
            self._send(image_path)
            if image_path == DC_MESS:
                break
        self.client_socket.close()


if __name__ == '__main__':
    client = Client(socket.AF_INET, socket.SOCK_STREAM)
    client.run()
