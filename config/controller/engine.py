# import cartas

class Server:
    all_players, id_player = 0, 0
    limit_players = 4

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
    inning = 0 #turnos
    new_flop = 0
    turn = []

    def __init__(self, data):
        self.serverData = data

    def shifts(self): #sistema de turnos
        self.inning = 1 if self.inning == self.serverData['n_player'] else self.inning + 1
        return self.inning
    
    def rule_sum(self, data, cards): #working
        player = data['Player-'+str(self.inning)] #obteniendo turno
        flop = data['flop'] #obteniendo barajas en tablero
        if isinstance(cards[0], list):
            for card in cards[0]:
                self.new_flop = self.new_flop + flop[card-1][0] #agregado los cartas sumadas 
                self.turn.append(flop[card-1])
            self.turn.append(player[cards[1]-1]) 
        else:
            self.new_flop = flop[cards[0]-1][0]
            self.turn.extend((flop[cards[0]-1], player[cards[1]-1]))
            
        self.turn.insert(0, self.new_flop+player[cards[1]-1][0])
        return self.turn
        

rule = RulesGame({'n_player': 4})
turno = rule.shifts()

rule.rule_sum({'flop': [[2, 'Corazones'], [8, 'picas'], [10, 'Diamantes'], [1, 'Tréboles']], 'Player-1': [[1, 'joker'], [13, 'Diamantes'], [10, 'Picas'], [5, 'Tréboles']], 'Player-2': [[7, 'Picas'], [12, 'Picas'], [8, 'Diamantes'], [11, 'Picas']], 'Player-3': [[13, 'Corazones'], [3, 'Tréboles'], [1, 'Diamantes'], [5, 'Tréboles']], 'Player-4': [[10, 'Corazones'], [9, 'Picas'], [12, 'Tréboles'], [11, 'Corazones']]}, 
    [2, 4]
)


# print(rule.shifts())

        
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