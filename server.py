import pickle
import random
import socket
from _thread import *

from game import Game


class Server:
    def __init__(self, ip, port, max_connections):
        self.IP = ip
        self.PORT = port
        self.MAX_CONNECTIONS = max_connections
        self.clients = set()
        self.game = None
        self.idCount = 0

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((self.IP, self.PORT))
            server.listen()

            print(f"Server started at {self.IP}:{self.PORT}")

            while True:
                if self.idCount < 4:
                    conn, addr = server.accept()

                    print(f'Connection from: {addr}')
                    self.idCount += 1

                    print("Creating a new game...")
                    self.game = Game()
                    print("Starting a new game...")

                    #zmienic na 4
                    if self.idCount == 1:

                        self.game.ready = True

                    start_new_thread(self.client_thread, (conn, self.idCount))

    def client_thread(self, connection, player):
        connection.send(str.encode(str(player)))
        while True:
            try:
                data = connection.recv(4096).decode()
                if data:
                    connection.sendall(pickle.dumps(self.game))
                else:
                    print('Disconnected')
                    break

            except socket.error as error:
                print(f'Error: {error}')

        '''
        try:
            del self.game
            print("Deleting game")
        except :
            pass
        self.idCount -= 1
        connection.close()
        '''
