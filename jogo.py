import collections
from pecas import Peca
import random


numeros = [0, 1, 2, 3, 4, 5, 6]
pieces = []
for numerador in numeros:
    for denominador in numeros:
        nova_peca = Peca(numerador, denominador)
        if nova_peca not in pieces:
            pieces.append(nova_peca)


class Tabuleiro(): 
    def __init__(self):
        self.board = collections.deque()
        
    def left_edge(self):
        return self.board[0].first
    
    def right_edge(self):
        return self.board[-1].second


class Jogo():
    def __init__(self, players, tabuleiro):
        self.tabuleiro = tabuleiro
        self.pecas = pieces
        self.players = players
        self.turn = None
        self.first_play = True
        self.distribute()
        while True:
            self.play()            
            winner = list(filter(lambda player: player.ganhador(), 
                                      self.players))
            if winner:
                print("{} ganhou!".format(winner[0]))
                break
        
    def distribute(self):
        pecas_per_player = len(self.pecas) // len(self.players)
        if len(self.players) == 3:
            bucha_zero = list(filter(lambda p: p.is_removable(),
                                     self.pecas))[0]
            self.pecas.remove(bucha_zero)
             
        for player in self.players:
            for _ in range(pecas_per_player):
                pedra = random.choice(self.pecas)
                player.set_pecas(pedra)
                self.pecas.remove(pedra)
            
    def next_player(self):
        while self.players[0].nome != self.turn.nome:
            self.players = self.players[1:] + [self.players[0]]
        self.players = self.players[1:] + [self.players[0]]
        self.turn = self.players[0]
        
    def whos_turn(self, fucou=False):
        if self.first_play:
            self.turn = list(filter(lambda player: player.startable(),
                                    self.players))[0]
        elif not fucou:
            self.next_player()

    def play(self, fucou=False):
        self.whos_turn(fucou)
        if self.first_play:
            self.tabuleiro.board.append(self.turn.move)
            self.first_play = False
        played, edge = self.turn.jogar_pedra(self.tabuleiro)
        if played:
            print("{} jogou {}" .format(self.turn.nome, self.turn.move))
            if edge:
                self.tabuleiro.board.append(self.turn.move)
            else:
                self.tabuleiro.board.appendleft(self.turn.move)
        else:
            if self.pecas:
                peca = random.choice(self.pecas)
                self.turn.set_pecas(peca)
                self.pecas.remove(peca)
                play(True)
