# import cartas

class Server:
    all_players, id_player = 0, 0
    limit_players = 0

    def _init_(self, gamblers):
        self.cards = []
        self.gamblers = gamblers

    def online_player(self):
        self.all_players =  self.all_players + 1
        self.id_player = 'Player-'+str(self.all_players) #creando id de jugador
        # self.players[self.id_player] = []
    
    def limit_player(self):
        return self.limit_players
        # return False if self.limit_players <= 1 or self.limit_player > 4 else True

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
        # print(self.turn)
        return self.turn