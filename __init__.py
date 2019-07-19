from multiprocessing.connection import Listener
from jogo import Jogo
from jogo import Tabuleiro
from player import Player
import constants


server = Listener(constants.TUPLE)

players = []
try:
    quantidade_players = int(input("Quantidade de players: "))
except ValueError:
    quantidade_players = 2
    
while True:
    con = server.accept()    
    cliente = con.recv()
    players.append(cliente)
    print("{} entrou no server" .format(cliente))
    if quantidade_players == len(players):
        break
    
tabuleiro  = Tabuleiro()
jogo = Jogo(players, tabuleiro)
