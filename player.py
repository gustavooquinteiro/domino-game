from multiprocessing.connection import Client
import constants


class Player():
    def __init__(self, nome):
        self.nome = nome
        self.pecas = []
        self.move = None
    
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
        return False, None
    
    def ganhador(self):
        return len(self.pecas) == 0

if __name__ == "__main__":
    client = Client(constants.TUPLE)
    nome = input("Nome: ")
    player = Player(nome)
    client.send(player)
