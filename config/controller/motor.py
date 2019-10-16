# import cartas

class Server:
    all_players, id_player = 0, 0
    limit_players = 4
    # players = {}

    def _init_(self, gamblers):
        self.cards = []
        self.gamblers = gamblers

    def online_player(self):
        self.all_players = self.all_players+1
        self.id_player = 'Player-'+str(self.all_players) #creando id de jugador
        # self.players[self.id_player] = []

    def limit_player(self):
        return True if self.limit_players < 4 else False

class RulesGame():
    def __init__(self):
        return


# server = Server()
# server.online_player()
# print(server.id_player)
# baraja = cartas.Cartas()
# baraja.tipo = ['Picas','Corazones','Diamantes','Tréboles']
# baraja.cartas = ['1','2','3','4','5','6','7','8','9','10','11','12','13']
# baraja.mazo()
# baraja.barajar()
# baraja.repartir(3)

# print(baraja.player)