#  Maciej Dąbkowski
#  WCY19IJ3S1

import pygame

from network_client import *

WIDTH = 1000
HEIGHT = 600

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
window.fill((255, 255, 255))
pygame.display.set_caption("Pan Client")
network = None


class Button:
    def __init__(self, txt, x, y, color, width, height):
        self.txt = txt
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y - self.height, self.width, self.height))
        font = pygame.font.SysFont('Arial', 40)
        txt = font.render(self.txt, True, (255, 255, 255))
        window.blit(txt,
                    (self.x + self.width / 2 - txt.get_width() / 2, self.y - self.height / 2 - txt.get_height() / 2))

    def btnClick(self, pos):
        return self.x <= pos[0] <= self.x + self.width and \
               (self.y - self.height) <= pos[1] <= (self.y - self.height) + self.height


class Card:
    def __init__(self, card, nr):
        self.suit = card.getSuit()
        self.type = card.getType()
        self.nr = nr
        self.x = (50 * self.nr) * 1.4 + 30

        # print(f'XXX {card.getSuit()}, {card.getType()}{card.isSelected()}')
        self.selected = card.isSelected()
        self.y = window.get_height() * 0.6
        self.img = pygame.image.load(f'img/{self.suit}{self.type}.png')
        self.img = pygame.transform.scale(self.img, (60, self.img.get_height() * 0.40))
        #self.x = (window.get_width()/2 - (self.nr * self.img.get_width()/2)) + (50 * self.nr) * 1.4 + 30

    def draw(self, window):
        if self.selected:
            pygame.draw.rect(window, (0, 255, 0),
                             (self.x - 2, self.y - 2, self.img.get_width() + 2, self.img.get_height() + 2))
        else:
            pygame.draw.rect(window, (0, 0, 255),
                             (self.x - 2, self.y - 2, self.img.get_width() + 2, self.img.get_height() + 2))

        window.blit(self.img,  (self.x, self.y))

    def isSelected(self):
        return self.selected

    def draw2(self, window):
        img = pygame.transform.scale(self.img, (134, 184))
        if (self.suit == '9') and (self.type == '♥'):
            window.blit(img, (434, 116))
        else:
            pygame.draw.rect(window, (0, 0, 0),
                             (30 * self.nr + 70 - 2, 116 - 2, img.get_width() + 2, img.get_height() + 2))
            window.blit(img, (30 * self.nr + 70, 116))

    def get_img(self):
        return self.img

    def btnClick(self, pos):
        return self.x <= pos[0] <= self.x + self.img.get_width() and \
               self.y <= pos[1] <= self.y + self.img.get_height()

    def get_card(self):
        # (f'{self.x}, {self.y} : {self.suit}, {self.type}')
        return self.suit, self.type


def menu():
    global network
    show = True
    offline = False
    click = True
    font = pygame.font.SysFont('Arial', 40)
    msg = font.render("WAITING FOR CONNECTION", True, (0, 0, 0))
    window.blit(msg, (500 - msg.get_width() / 2, 250 - msg.get_height()))

    while show:

        if offline:
            font = pygame.font.SysFont('Arial', 40)
            msg = font.render("Server Offline", True, (255, 0, 0))
            window.blit(msg, (500 - msg.get_width() / 2, 250 + msg.get_height()))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                show = False
            if event.type == pygame.MOUSEBUTTONUP:
                offline = False
                try:
                    if click:
                        click = False
                        network = Network()
                        show = False
                        main()
                        break
                except socket.error as error:
                    offline = True
                    click = True
                    print("BRAK WOLNEGO SERWERA")


def redraw_window(window, game, player, cards, button, cardDeck, button2, button3):
    window.fill((7, 63, 24))
    font = pygame.font.SysFont("Arial", 40)

    for card in cards:
        card.draw(window)

    if game.get_turn() == 0:
        if game.getStartingPlayer() != player:
            text1 = font.render("Zaczyna gracz z [9 Kier]", True, (0, 0, 0))
        else:
            text1 = font.render("Twoj ruch", True, (0, 0, 0))
    elif game.get_turn() == player:
        text1 = font.render("Twoj ruch", True, (0, 255, 0))
    else:
        text1 = font.render(f"Ruch gracza {game.get_turn()}", True, (255, 0, 0))
    window.blit(text1, (window.get_width() / 2 - text1.get_width() / 2, 20))

    button2.draw(window)
    button3.draw(window)

    if len(cardDeck) == 0:
        button.draw(window)
    else:
       # imt = pygame.image.load(f'img/card.png')
        #img = pygame.transform.scale(imt, (138, 188))
        #window.blit(img, (434, 300-188))
        for card in cardDeck:
            card.draw2(window)
            #print(card.get_card())
    pygame.display.update()


def main():
    global network
    run = True
    button = Button("START", 434, 300, (0, 0, 0), 132, 187)
    button2 = Button("Wez 3 karty", 0, window.get_height() - 100, (0, 0, 0), window.get_width(), 50)
    button3 = Button("Zatwierdz ruch", 0, window.get_height() - 25, (0, 0, 0), window.get_width(), 50)

    clock = pygame.time.Clock()
    player = int(network.get_id())
    print(f"You are player {player}")

    while run:
        clock.tick(15)

        try:
            game = network.send_data("update")
            cardStack = [Card(item, index) for index, item in enumerate(game.get_player(player).cards)]
            cardDeck = [Card(item, index) for index, item in enumerate(game.deck)]
        except:
            run = False
            print("Couldnt update game")
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if (game.get_turn() == 0) and (player == game.getStartingPlayer()):
                    for card in cardStack:
                        if card.btnClick(pos):
                            index = game.players[player - 1].get_card_index(card.get_card()[0], card.get_card()[1])
                            network.send_data("select " + str(index))
                    if button3.btnClick(pos):
                        network.send_data("confirm")
                if game.get_turn() == player:
                    for card in cardStack:
                        if card.btnClick(pos):
                            index = game.players[player - 1].get_card_index(card.get_card()[0], card.get_card()[1])
                            network.send_data("select " + str(index))
                    if button3.btnClick(pos):
                        network.send_data("confirm")
                    if button2.btnClick(pos):
                        network.send_data("get3cards")

        if game is not None:
            redraw_window(window, game, player, cardStack, button, cardDeck, button2, button3)


menu()
