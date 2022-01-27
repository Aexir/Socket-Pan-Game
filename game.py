#  Maciej Dąbkowski
#  WCY19IJ3S1

from collections import deque
from itertools import product

card_suits = ["♠", "♥", "♦", "♣"]
card_types = ["9", "10", "J", "Q", "K", "A"]


# random.shuffle(cards)

class Card:
    def __init__(self, type, suit):
        self.suit = type
        self.type = suit
        self.selected = False

    def get_card(self):
        print(f'CREATE CARD {self.suit}, {self.type}{self.selected}')
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
            print(f"SELECTED {self.selected} {self.type} {self.suit}")
        else:
            self.selected = True
            print(f"SELECTED {self.selected} {self.type} {self.suit}")


class Game:
    def __init__(self):
        cards = [Card(x[0], x[1]) for x in [x for x in product(card_types, card_suits)]]
        self.ready = False
        self.deck = deque()
        #self.deck = cards[:24]
        self.turn = 0
        self.players = [Player(cards[:10], 1), Player(cards[6:12], 2),
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
            card = self.deck
            print(card[0].getSuit())
            if card[0].getSuit() == 'A' and newCard.getSuit() == ("9" or "10" or "J" or "Q" or "K"):
                return False
            elif card[0].getSuit() == 'K' and newCard.getSuit() == ("9" or "10" or "J" or "Q"):
                return False
            elif card[0].getSuit() == 'Q' and newCard.getSuit() == ("9" or "10" or "J"):
                return False
            elif card[0].getSuit() == 'J' and newCard.getSuit() == ("9" or "10"):
                return False
            elif card[0].getSuit() == '10' and newCard.getSuit() == "9":
                return False
            else:
                return True

    def get3Cards(self, player):
        for x in range(3):
            if (self.deck.__getitem__(0).getSuit() == '9') and (self.deck.__getitem__(0).getType() == '♥'):
                return
            else:
                self.players[player - 1].cards.append(self.deck.popleft())

        self.setNextPlayer(player)

    def setNextPlayer(self, player):
        if self.deck.__getitem__(0).getType() == '♠':
            if player == 1:
                self.turn = 4
            else:
                self.turn -= 1
        else:
            if player == 4:
                self.turn = 1
            else:
                self.turn += 1

    def move(self, player, newCard):
        if self.isLegal(newCard):
            if self.turn == 0:
                self.turn = self.getStartingPlayer()
            self.deck.appendleft(newCard)
            index = self.players[player-1].get_card_index(newCard.getSuit(), newCard.getType())
            del self.players[player-1].cards[index]
            if newCard.getType() == '♠':
                if self.turn == 1:
                    self.turn = 4
                else:
                    self.turn -= 1
            else:
                if self.turn == 4:
                    self.turn = 1
                else:
                    self.turn += 1

    def reset_players(self):
        for player in self.players:
            player.finished = False


class Player:
    def __init__(self, cards, id):
        self.cards = cards
        self.id = id
        self.finished = False

    def get_id(self):
        return self.id

    def has_finished(self):
        return self.finished

    def get_card_index(self, suit, type):
        for index, card in enumerate(self.cards):
            if card.getSuit() == suit:
                if card.getType() == type:
                    return index

    def get_selected_cards(self):
        selected = [x for x in self.cards if x.selected]
        return selected
