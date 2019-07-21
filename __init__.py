from multiprocessing.connection import Listener
from jogo import Jogo
from jogo import Tabuleiro
from player import Player
from constants import TUPLE


class Server():
    def __init__(self, board, quantidade_players=2, where_to_listen=TUPLE):
        self.server = Listener(where_to_listen)
        self.quantidade_players = quantidade_players
        self.hosted_board = board
        self.host_connected = []
        self.wait_players()
        
    def wait_players(self):
        while len(self.host_connected) != self.quantidade_players:
            with self.server.accept() as connection:
                client = connection.recv()
                self.host_connected.append(client)
                print("{} entered the server" .format(client))
        self.run_game()
    
    def run_game(self):
        self.host_connected = self.hosted_board.distribute(self.host_connected)
        self.hosted_game = Jogo(self.host_connected, self.hosted_board)
        while not self.hosted_game.ganhador:
            self.hosted_game.play()
        print("{} won..." .format(self.hosted_game.ganhador))

if __name__ == "__main__":
    tabuleiro  = Tabuleiro()
    try:
        quantidade_players = int(input("Quantidade de players: "))
    except ValueError:
        quantidade_players = 2
    server = Server(tabuleiro, quantidade_players)
