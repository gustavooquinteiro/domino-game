import socket
from jogo import Jogo
from jogo import Tabuleiro

HOST = ''
PORT = 5000
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(1)
players = []

while len(players) < 2:
    con, cliente = tcp.accept()
    while True:
        msf = con.recv(1024)
        if not msf:
            break
        print(cliente, msf.decode())
    print("Finalizando conexao do cliene {}".format(cliente))
    players.append(cliente)
    con.close()
    
tabuleiro  = Tabuleiro()
jogo = Jogo(players, tabuleiro)
