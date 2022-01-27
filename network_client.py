#  Maciej Dąbkowski
#  WCY19IJ3S1

import pickle
import socket


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = "127.0.0.1"
        self.port = 2138
        self.id = self.connect()
        print(self.id)

    def get_id(self):
        return self.id

    def connect(self):
        self.client.connect((self.ip, self.port))
        return self.client.recv(4096)

    def send_data(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(4096))
        except socket.error as error:
            print(error)
