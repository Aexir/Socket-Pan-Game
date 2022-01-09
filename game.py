import random
from itertools import product
from collections import deque

card_suits = ["♠", "♥", "♦", "♣"]
card_types = ["9", "10", "J", "Q", "K", "A"]
cards = [x for x in product(card_types, card_suits)]
random.shuffle(cards)


class Game:

    def __init__(self):
        self.ready = False
        self.deck = deque()

        self.p1_deck = cards[:6]
        self.p2_deck = cards[6:12]
        self.p3_deck = cards[12:18]
        self.p4_deck = cards[18:24]

        self.turn = 0
        self.players = [Player(self.p1_deck, 1), Player(self.p2_deck, 2),
                        Player(self.p3_deck, 3), Player(self.p4_deck, 4)]

    def is_ready(self):
        return self.ready

    def get_turn(self):
        return self.turn

    def get_player(self, id):
        return self.players[id - 1]

    def move(self):
        pass

    def select(self):
        changed = False

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

    def get_cards(self):
        return self.cards

    def has_finished(self):
        return self.finished