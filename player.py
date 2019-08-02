from api import Client
from constants import *
import pygame


class Player:
    def __init__(self, nome):
        self.nome = nome
        self.pecas = []
        self.board = None
        self.move = None
        self.passed = False
    
    def set_pecas(self, peca):
        self.pecas.append(peca)
        
    def __repr__(self):
        return "{} com {}" .format(self.nome, self.pecas)
    
    def startable(self):
        peca = list(filter(lambda pedra: pedra.is_startable(), self.pecas))
        if peca:
            self.move = peca[0]
            self.pecas.remove(self.move)
            return True
        return False
    
    def ganhador(self):
        return len(self.pecas) == 0
    
    def verify_piece(self, tabuleiro):
        return any(tabuleiro.right_edge() in peca or 
                   tabuleiro.left_edge() in peca for peca in self.pecas)

    def start_screen(self):
        self.board.screen.fill(WHITE)
        


class Computer(Player):
    def __init__(self):
        super().__init__("COMPUTER")
    
    def play(self, tabuleiro):
        self.passed = False
        self.move = None
        for pedra in self.pecas:
            if tabuleiro.right_edge() in pedra:
                if pedra.second == tabuleiro.right_edge():
                    pedra.invert()
                self.move = pedra
                self.pecas.remove(self.move)
                return True, True
            if tabuleiro.left_edge() in pedra:
                if pedra.first == tabuleiro.left_edge():
                    pedra.invert()
                self.move = pedra
                self.pecas.remove(self.move)
                return True, False
        self.passed = True
        return False, None
    
if __name__ == "__main__":
    nome = input("Nome: ")
    player = Player(nome)
    client = Client(player)
