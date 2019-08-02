import api

def start_server():
    try:
        quantidade_players = int(input("Quantidade de players: "))
        return quantidade_players
    except ValueError:
        start_server()
    
if __name__ == "__main__":
    server = api.Server(start_server())
