from pecas import Peca
from player import Player
import random
import collections


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
            if any(player.ganhador() for player in players):
                break
        
    def distribute(self):
        pecas_per_player = len(self.pecas) // len(self.players)
        for player in self.players:
            for _ in range(pecas_per_player):
                pedra = random.choice(self.pecas)
                player.set_pecas(pedra)
                self.pecas.remove(pedra)
            print(player)
            
    def next_player(self):
        while self.players[0].nome != self.turn.nome:
            self.players = self.players[1:] + [self.players[0]]
        self.players = self.players[1:] + [self.players[0]]
        self.turn = self.players[0]
        
    def whos_turn(self):
        if self.first_play:
            for player in self.players:
                if player.startable():
                    self.turn = player
                    print(self.turn.nome)
                    break
        else:
            self.next_player()
        print ("vez de {} ".format(self.turn.nome))

    def play(self):
        print("Tabuleiro")
        print(*self.tabuleiro.board, sep='\n')
        self.whos_turn()
        if self.first_play:
            self.tabuleiro.west_edge = self.turn.move
            self.tabuleiro.east_edge = self.turn.move
            self.tabuleiro.board.append(self.turn.move)
            self.first_play = False
        played, edge = self.turn.jogar_pedra(self.tabuleiro)
        print("played {} edge {}" .format(played, edge))
        if played:
            print("{} jogou {}" .format(self.turn.nome, self.turn.move))
            if edge:
                self.tabuleiro.board.append(self.turn.move)
            else:
                self.tabuleiro.board.appendleft(self.turn.move)
            
        
t = Tabuleiro()
a = Player('A')
b = Player('B')
players = []
players.append(a)
players.append(b)
n =Jogo(players, t)
