#  Maciej Dąbkowski
#  WCY19IJ3S1

import pickle
import socket
from _thread import *

from game import Game


class Server:
    def __init__(self, ip, port, max_connections):
        self.IP = ip
        self.PORT = port
        self.MAX_CONNECTIONS = max_connections
        # self.clients = set()
        self.game = None
        self.idCount = 0

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((self.IP, self.PORT))
            server.listen()

            print(f"Server started at {self.IP}:{self.PORT}")
            print("Creating a new game...")
            self.game = Game()

            while True:
                if self.idCount < 4:
                    conn, addr = server.accept()

                    print(f'Connection from: {addr}')
                    self.idCount += 1

                    # zmienic na 4
                    if self.idCount == 1:
                        print("Starting a new game...")
                        self.game.ready = True

                    start_new_thread(self.client_thread, (conn, self.idCount))

    def client_thread(self, connection, player):
        connection.send(str.encode(str(player)))
        while True:
            try:
                data = connection.recv(4096).decode()
                if data:
                    if data.count("select") > 0:
                        all = data.split(" ")
                        index = int(all[1])

                        tmpCard = self.game.players[player-1].cards[index]
                        if self.game.isLegal(tmpCard):
                            self.game.players[player - 1].cards[index].setSelected()
                            self.game.players[player - 1].selected_cards.append(
                                self.game.players[player - 1].cards[index])
                            if not self.game.legal(player)[0]:
                                self.game.players[player-1].cards[index].setSelected()
                                index2 = self.game.players[player - 1].get_selected_card_index(
                                    self.game.players[player-1].cards[index].getSuit(),
                                    self.game.players[player-1].cards[index].getType())
                                del self.game.players[player - 1].selected_cards[index2]
                        else:
                            print(f"{player} NIEDOZWOLONY RUCH")
                    if data == "confirm":
                        print("ODEBRANO CONFIRM")
                        if self.game.turn == 0:
                            if len(self.game.players[player-1].get_selected_cards()) != 0:
                                self.game.update(player)
                        else:
                            if len(self.game.players[player - 1].get_selected_cards()) != 0:
                                self.game.update(player)
                            else:
                                print("BRAK ZAZNACZONYCH KART")
                    if data == "get3cards":
                        self.game.get3Cards(player)
                        self.game.setNextPlayer(player)

                    connection.sendall(pickle.dumps(self.game))
                else:
                    print('Disconnected')
                    break

            except socket.error as error:
                print(f'Error: {error}')

        try:
            # del self.game
            print("Deleting game")
        except:
            pass
        self.idCount -= 1
        connection.close()
