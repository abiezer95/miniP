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
    inning = 1 #turnos
    new_flop = 0
    turn = []

    def __init__(self, data):
        self.serverData = data

    def shifts(self): #sistema de turnos
        self.inning = 1 if self.inning == self.serverData['n_player'] else self.inning + 1
        return self.inning
    
    def rule_sum(self, data, cards): #working
        self.turn = []
        player = data['Player-'+str(self.inning)] #obteniendo turno
        flop = data['flop'] #obteniendo barajas en tablero

        if isinstance(cards[0], list): #si se suma mas de un flop y tus cartas
            for card in cards[0]:
                self.new_flop = self.new_flop + flop[int(card)-1][0] #agregado los cartas sumadas
                
                self.turn.append(flop[int(card)-1])
            self.turn.append(player[int(cards[1])-1])
        else: 
            getted = flop[int(cards[0])-1]
            self.new_flop = getted[0] #carta del flop
            self.turn.extend((getted, player[int(cards[1])-1]))

            if isinstance(getted[1], list): #quitando primer digito
                self.turn = []
                for card in getted:
                    if isinstance(card, list):
                        self.turn.append(int(card))
                self.turn.append(player[int(cards[1])-1])

        self.turn.insert(0, self.new_flop+player[int(cards[1])-1][0])
        
        return self.turn
    
    def rule_get(self, data, cards, player):
        river = []
        flop = data['flop']
        if isinstance(cards[0], list):
            None
                # for card in flop:
                #     print(card)
        else:
            card1 = int(cards[0])
            card2 = int(cards[1])
            if flop[card1-1][0] ==  player[card2-1][0]:
                if isinstance(flop[card1-1][1], list): #si ya habian sumadas
                    flop[card1-1].pop(0) #eliminamos primer digito inservible
                    [river.append(i) for i in flop[card1-1]]
                    river.append(player[card2-1])
                else:
                    river.extend((flop[card1-1], player[card2-1])) #agregamos
                    
                flop.pop(card1-1), player.pop(card2-1) #eliminamos cartas
                [data['total'][self.inning-1].append(i) for i in river]
            else:
                return False

        return river


        
             
            
        

