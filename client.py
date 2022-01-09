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
    def __init__(self, txt, x, y, color):
        self.txt = txt
        self.x = x
        self.y = y
        self.color = color
        self.width = 132
        self.height = 187

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y - self.height, self.width, self.height))
        font = pygame.font.SysFont('Arial', 40)
        txt = font.render(self.txt, True, (255, 255, 255))
        window.blit(txt, (self.x + round(self.width / 2) - round(txt.get_width() / 2),
                          (self.y - self.height) + round((self.y - self.height) / 2) - round(txt.get_height() / 2)))

    def drawStart(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont('Arial', 40)
        txt = font.render(self.txt, True, (255, 255, 255))
        window.blit(txt, (self.x + round(self.width / 2) - round(txt.get_width() / 2),
                          self.y + round(self.height / 2) - round(txt.get_height() / 2)))

    def btnClick(self, pos):
        return self.x <= pos[0] <= self.x + self.width and \
               (self.y - self.height) <= pos[1] <= (self.y - self.height) + self.height


class Card:
    def __init__(self, card, nr):
        self.suit = card[0]
        self.type = card[1]
        self.nr = nr
        self.x = (50 * self.nr) * 1.4 + 30
        self.y = window.get_height() * 0.6
        self.img = pygame.image.load(f'img\{self.suit}{self.type}.png')
        self.img = pygame.transform.scale(self.img, (60, self.img.get_height() * 0.40))

    def draw(self, window):
        pygame.draw.rect(window, (0, 0, 255), (self.x, self.y, self.img.get_width() + 2, self.img.get_height() + 2))
        window.blit(self.img, (self.x, self.y))

    def get_img(self):
        return self.img

    def btnClick(self, pos):
        return self.x <= pos[0] <= self.x + self.img.get_width() and \
               self.y <= pos[1] <= self.y + self.img.get_height(), print(self.suit, self.type)

    def get_card(self):
        print(f'{self.x}, {self.y} : {self.suit}, {self.type}')


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


def redraw_window(window, game, player, cards, button):
    window.fill((255, 255, 255))
    font = pygame.font.SysFont("comicsans", 40)

    for card in cards:
        card.draw(window)
        # print(card.get_card())

    if game.get_turn() == 0:
        text1 = font.render("Zaczyna gracz z [9 Kier]", True, (0, 0, 0))

    elif game.get_turn() == 1 and player == 1:
        text1 = font.render("Twoj ruch", True, (0, 255, 0))
    else:
        text1 = font.render(f"Ruch gracza {game.get_turn()}", True, (255, 0, 0))
    window.blit(text1, (window.get_width() / 2 - text1.get_width() / 2, 20))

    button.draw(window)
    pygame.display.update()


def main():
    global network
    run = True
    # p = Player(50, 50, 10, 10, (0, 255, 0), 0)
    button = Button("START", 434, 300, (0, 0, 0))
    clock = pygame.time.Clock()
    player = int(network.get_id())
    print(f"You are player {player}")

    while run:
        clock.tick(15)

        try:
            game = network.send_data("update")
            cardStack = [Card(item, index) for index, item in enumerate(game.get_player(player).get_cards())]

            for card in cardStack:
                print(card.get_card())

            print("")
        except:
            run = False
            print("Couldnt update game")
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(f'START {button.btnClick(pygame.mouse.get_pos())}')


                for card in cardStack:
                    if card.btnClick(pygame.mouse.get_pos()):
                        print("ELO")
                    else:
                        print("NIE")
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

        # p.move()
        if game is not None:
            redraw_window(window, game, player, cardStack, button)


menu()