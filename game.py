#  Maciej Dąbkowski
#  WCY19IJ3S1
import random
from collections import deque
from itertools import product

card_suits = ["♠", "♥", "♦", "♣"]
card_types = ["9", "10", "J", "Q", "K", "A"]


class Card:
    def __init__(self, type, suit):
        self.suit = type
        self.type = suit
        self.selected = False

    def get_card(self):
        # print(f'CREATE CARD {self.suit}, {self.type}{self.selected}')
        return self.__class__

    def getSuit(self):
        return self.suit

    def getType(self):
        return self.type

    def isSelected(self):
        return self.selected

    def setSelected(self):
        if self.selected:
            self.selected = False
            # print(f"SELECTED {self.selected} {self.type} {self.suit}")
        else:
            self.selected = True
            # print(f"SELECTED {self.selected} {self.type} {self.suit}")


class Game:
    def __init__(self):
        cards = [Card(x[0], x[1]) for x in [x for x in product(card_types, card_suits)]]
        random.shuffle(cards)

        self.ready = False
        self.deck = deque()
        self.turn = 0
        self.players = [Player(cards[:6], 1), Player(cards[6:12], 2),
                        Player(cards[12:18], 3), Player(cards[18:24], 4)]

    def getStartingPlayer(self):
        for player in self.players:
            for card in player.cards:
                if (card.getSuit() == '9') and (card.getType() == '♥'):
                    return player.get_id()

    def is_ready(self):
        return self.ready

    def get_turn(self):
        return self.turn

    def get_player(self, id):
        return self.players[id - 1]

    def isLegal(self, newCard):
        if len(self.deck) == 0:
            suit = newCard.getSuit()
            value = newCard.getType()
            if (suit, value) == ('9', '♥'):
                return True
            else:
                return False
        else:
            print("ISLEGAL2")
            card = self.deck
            # print(f'{card[0].getSuit()}{newCard.getSuit()}')
            if (card[0].getSuit() == 'A') and newCard.getSuit() in ("9", "10", "J", "Q", "K"):
                print("A ZLE")
                return False
            if (card[0].getSuit() == 'K') and newCard.getSuit() in ("9", "10", "J", "Q"):
                print("K ZLE")
                return False
            if (card[0].getSuit() == 'Q') and newCard.getSuit() in ("9", "10", "J"):
                return False
            if (card[0].getSuit() == 'J') and newCard.getSuit() in ("9", "10"):
                print(f"J ZLE {newCard.getSuit()}")
                return False
            if (card[0].getSuit() == '10') and (newCard.getSuit() == "9"):
                return False
            else:
                return True

    def get3Cards(self, player):
        for x in range(3):
            if (self.deck.__getitem__(0).getSuit() == '9') and (self.deck.__getitem__(0).getType() == '♥'):
                break
            else:
                self.players[player - 1].cards.append(self.deck.popleft())

        self.setNextPlayer(player)

    def legal(self, player):
        cards = self.players[player - 1].get_selected_cards()
        count = 0
        if len(cards) > 1:
            typ = cards[0].getSuit()
            for card in cards:
                if card.getSuit() == typ:
                    count += 1
        else:
            return True, 1
        return count == len(cards), count

    def setNextPlayer(self, player):
        inGameIndex = [x.get_id() for x in self.players if not x.has_finished()]
        index = inGameIndex.index(player)
        if self.deck.__getitem__(0).getType() == '♠':
            if player == inGameIndex[0]:
                self.turn = inGameIndex[len(inGameIndex) - 1]
            else:
                self.turn = inGameIndex[index - 1]
        else:
            if player != inGameIndex[len(inGameIndex) - 1]:
                self.turn = inGameIndex[index + 1]
            else:
                self.turn = inGameIndex[0]

    def update(self, player):
        val = self.legal(player)[1]
        if (val == 1) or (val == 4):
            for card in range(val):
                print(card)
                self.move(player, self.players[player - 1].selected_cards[card])

            self.setNextPlayer(player)
            self.players[player - 1].selected_cards.clear()
            for card in self.deck:
                card.selected = False
            if len(self.get_player(player).cards) == 0:
                self.get_player(player).finished = True

    def move(self, player, newCard):
        # if self.isLegal(newCard):
        if self.turn == 0:
            self.turn = self.getStartingPlayer()
        print("X")
        self.deck.appendleft(newCard)
        print("Y")
        index = self.players[player - 1].get_card_index(newCard.getSuit(), newCard.getType())
        print("Z")
        del self.players[player - 1].cards[index]
        print("V")

    def reset_players(self):
        for player in self.players:
            player.finished = False


class Player:
    def __init__(self, cards, id):
        self.cards = cards
        self.id = id
        self.finished = False
        self.selected_cards = deque()

    def get_id(self):
        return self.id

    def has_finished(self):
        return self.finished

    def get_card_index(self, suit, type):
        for index, card in enumerate(self.cards):
            if card.getSuit() == suit:
                if card.getType() == type:
                    return index

    def get_selected_card_index(self, suit, type):
        for index, card in enumerate(self.selected_cards):
            if card.getSuit() == suit:
                if card.getType() == type:
                    return index

    def get_selected_cards(self):
        return self.selected_cards
