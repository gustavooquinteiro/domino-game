from constants import TUPLE, MESSAGES
from jogo import Jogo
from jogo import Tabuleiro
import socket
import selectors
import types

selector = selectors.DefaultSelector()

class Server:
    def __init__(self, quantidade_players=2, address=TUPLE):
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(TUPLE)
        self.server.listen()
        self.server.setblocking(False)
        selector.register(self.server, selectors.EVENT_READ, data=None)
        self.quantidade_players = quantidade_players
        self.hosted_players = []
        self.hosted_game = Jogo()
        self.wait_players()

    def wait_players(self):        
        while True:
            events = selector.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    self.accept_wrapper(key.fileobj)
                else:
                    self.service_connection(key, mask)


    def accept_wrapper(self, socket):
        conn, addr = socket.accept()
        print('accepted connection from', addr)
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        selector.register(conn, events, data=data)
    
    def service_connection(self, key, mask):
        client_socket = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = client_socket.recv(1024)  # Should be ready to read
            if recv_data:
                data.outb += recv_data
            else:
                print('closing connection to', data.addr)
                selector.unregister(client_socket)
                client_socket.close()
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                print('echoing', repr(data.outb), 'to', data.addr)
                sent = client_socket.send(data.outb)  # Should be ready to write
                data.outb = data.outb[sent:]


class Client:
    def __init__(self, player, address=TUPLE):
        self.ip = address[0]
        self.port = address[1]
        self.player = player
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(False)
        connid = 28
        self.socket.connect_ex(TUPLE)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(connid=connid,
                                     msg_total=sum(len(m) for m in MESSAGES),
                                     recv_total=0,
                                     messages=list(MESSAGES),
                                     outb=b'')
        selector.register(self.socket, events, data=data)
        self.socket.send(MESSAGES[0])
        
    def service_connection(self, key, mask):
        socket = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = socket.recv(1024)  # Should be ready to read
            if recv_data:
                print('received', repr(recv_data), 'from connection', data.connid)
                data.recv_total += len(recv_data)
            if not recv_data or data.recv_total == data.msg_total:
                print('closing connection', data.connid)
                sel.unregister(socket)
                socket.close()
        if mask & selectors.EVENT_WRITE:
            if not data.outb and data.messages:
                data.outb = data.messages.pop(0)
            if data.outb:
                print('sending', repr(data.outb), 'to connection', data.connid)
                sent = socket.send(data.outb)  # Should be ready to write
                data.outb = data.outb[sent:]

        
    def receive(self):
        while True:
            print(self)
            self.player = self.server_connection.recv()
        
    def __repr__(self):
        return "Host at {} from {} port" .format(self.ip, self.port)
    
    def __contains__(self, ip):
        return ip == self.ip 
        
