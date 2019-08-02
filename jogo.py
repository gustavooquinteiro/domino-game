import pygame
import collections
from pecas import Domino
import random
from constants import *

class Tabuleiro: 
    def __init__(self, players):
        pygame.init()
        size = [SCREEN_WIDTH, SCREEN_HEIGHT]
        self.screen = pygame.display.set_mode(size)
        numeros = [0, 1, 2, 3, 4, 5, 6]
        self.pieces = []
        self.font_name = pygame.font.match_font(FONT)
        self.clock = pygame.time.Clock()
        self.players = players
        for numerador in numeros:
            for denominador in numeros:
                nova_peca = Domino(numerador, denominador,
                                 SCREEN_WIDTH * numerador + 1,
                                 denominador * (
                                     SCREEN_HEIGHT - SCREEN_HEIGHT / 4
                                     )
                                 )
                if nova_peca not in self.pieces:
                    self.pieces.append(nova_peca)
        self.board = collections.deque()
        self.changed = False
        self.game = Jogo()
        self.show_start_screen()

    def show_start_screen(self):
        self.screen.fill(WHITE)

        self.draw_text(TITLE,
                       48,
                       BLACK,
                       SCREEN_WIDTH /2,
                       SCREEN_HEIGHT / 4)

        self.draw_text(START,
                       32,
                       BLACK,
                       SCREEN_WIDTH / 2,
                       SCREEN_HEIGHT / 2)

        pygame.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_q:
                       pygame.quit()
                    if event.key == pygame.K_RETURN:
                        waiting = False

    def next_player(self):
        while self.players[0].nome != self.game.turn.nome:
            self.players = self.players[1:] + [self.players[0]]
        self.players = self.players[1:] + [self.players[0]]
        self.game.turn = self.players[0]
        
    def whos_turn(self, fucou=False):
        if self.game.first_play:
            player = list(filter(
                lambda player: player.startable(), self.players))
            self.game.turn = player[0]
        elif not fucou:
            self.next_player()

    def distribute(self):
        pecas_per_player = len(self.pieces) // len(self.players)
        if len(self.players) == 3:
            bucha_zero = list(filter(lambda p: p.is_removable(),
                                     self.pieces))[0]
            self.pieces.remove(bucha_zero)
        X = (SCREEN_HEIGHT - 300) / 2 + 25
        Y = (SCREEN_WIDTH - (SCREEN_WIDTH/8)) - 34
        offset = 50
        for player in self.players:
            for _ in range(pecas_per_player):
                pedra = random.choice(self.pieces)
                self.pieces.remove(pedra)
                pedra.x = X + offset
                pedra.y = Y
                X += offset
                player.set_pecas(pedra)
            Y = SCREEN_WIDTH / 8 - 34
            X = (SCREEN_HEIGHT - 565) / 2 + 25
    
    def left_edge(self):
        return self.board[0].first
    
    def right_edge(self):
        return self.board[-1].second
    
    def change_edges(self):
        print("abrir o jogo")
        print(self.board, sep='\n')
        if self.left_edge() == self.right_edge():
            c = random.choice([True, False])
            if c:
                pedra = self.board.pop()
                self.board.appendleft(pedra)
            else:
                pedra = self.board.popleft()
                self.board.append(pedra)
            print(self.board, sep='\n')
            self.changed = True

    def verify(self, peca):
        pass 
    
    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw(self):
        self.screen.fill(BLACK)
        for jogador in self.players:
            for peca in jogador.pecas:
                peca.draw(self.screen)
        pygame.display.flip()
        pygame.display.update()

class Jogo:
    def __init__(self):
        self.turn = None
        self.has_winner = False
        self.ganhador = None
        self.first_play = True

    def count_points(self):
        points = []
        for player in self.players:
            points.append(
                sum(pedra.first + pedra.second for pedra in player.pecas))
        self.has_winner = True
        return self.players[points.index(min(points))], min(points)
        
    def play(self):
        pass
        #if not self.ganhador:
            #self.ganhador = list(filter(lambda player: player.ganhador(), 
                                        #self.players))
        #if self.ganhador:
            #return
        #if self.first_play:
            #self.tabuleiro.board.append(self.turn.move)
            #self.first_play = False
        #played, edge = self.turn.jogar_pedra(self.tabuleiro)
        #if played:
            #print("{} jogou {}" .format(self.turn.nome, self.turn.move))
            #if edge:
                #self.tabuleiro.board.append(self.turn.move)
            #else:
                #self.tabuleiro.board.appendleft(self.turn.move)

        #if all(jogador.passed for jogador in self.players):
            #if not self.tabuleiro.changed:
                #self.tabuleiro.change_edges()
            #else:
                #print("Vitoria por pontos")
                #self.ganhador, points = self.count_points()
                #print("{} ganhou com {}" .format(self.ganhador, points))

