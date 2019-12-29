import collections
from pecas import Peca
import random


class Tabuleiro(): 
    def __init__(self):
        numeros = [0, 1, 2, 3, 4, 5, 6]
        self.pieces = []
        for numerador in numeros:
            for denominador in numeros:
                nova_peca = Peca(numerador, denominador)
                if nova_peca not in self.pieces:
                    self.pieces.append(nova_peca)
        self.board = collections.deque()
        self.changed = False
    
    def distribute(self, players):
        pecas_per_player = len(self.pieces) // len(players)
        if len(players) == 3:
            bucha_zero = list(filter(lambda p: p.is_removable(),
                                     self.pieces))[0]
            self.pieces.remove(bucha_zero)
             
        for player in players:
            for _ in range(pecas_per_player):
                pedra = random.choice(self.pieces)
                player.set_pecas(pedra)
                self.pieces.remove(pedra)
        return players
    
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


class Jogo():
    def __init__(self, players, tabuleiro):
        self.tabuleiro = tabuleiro
        self.players = players
        self.turn = None
        self.ganhador = None
        self.first_play = True
        
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

    def count_points(self):
        points = []
        for player in self.players:
            points.append(
                sum(pedra.first + pedra.second for pedra in player.pecas))
        return self.players[points.index(min(points))], min(points)
        
    def play(self, fucou=False):
        if not self.ganhador:
            self.ganhador = list(filter(lambda player: player.ganhador(), 
                                        self.players))
        if self.ganhador:
            return
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

        if all(jogador.passed for jogador in self.players):
            if not self.tabuleiro.changed:
                self.tabuleiro.change_edges()
            else:
                print("Vitoria por pontos")
                self.ganhador, points = self.count_points()
                print("{} ganhou com {}" .format(self.ganhador, points))
            for jogador in self.players:
                print("{}", jogador)
