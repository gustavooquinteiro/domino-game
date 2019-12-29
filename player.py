from multiprocessing.connection import Client
from constants import TUPLE
from random import randint
import time


class Player():
    def __init__(self, nome):
        self.nome = nome
        self.pecas = []
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
        
    def jogar_pedra(self, tabuleiro):
        self.passed = False
        self.move = None
        possibilidades = list(filter(
            lambda pedra: pedra.is_playable(tabuleiro),
            self.pecas))
        if possibilidades:
            tamanho = len(possibilidades) - 1
            jogada = possibilidades[randint(0, tamanho)]
            self.move = jogada
            self.pecas.remove(self.move)
            return True, jogada.lugar
        else:
            self.passed = True
        return False, self.move
    
    def ganhador(self):
        return len(self.pecas) == 0

if __name__ == "__main__":
    client = Client(TUPLE)
    nome = input("Nome: ")
    player = Player(nome)
    client.send(player)
