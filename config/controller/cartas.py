import random as r
import engine

server = engine.Server()
rule = engine.RulesGame({'n_player': 4})

class Cartas:
    tipo = []
    cartas, cards, player = [], [], {'flop': []}
    
    def mazo(self):
        for card in self.cartas:
            for x in self.tipo:
                self.cards.append([card, x])

    def barajar(self):
        r.shuffle(self.cards)

    def repartir(self, playerlimit):
        for i in range(playerlimit):
            server.online_player()
            self.player[server.id_player] = [] #añadimos el id de jugador a la mesa
            ############
        i = 0
        e = 1
        flop = playerlimit*4
        for card in self.cards:
            if i >= flop:
                self.player['flop'].append(card)
                if i >= flop+3:
                    break
            else:
                self.player['Player-'+str(e)].append(card)
            e = 1 if e == playerlimit else e + 1 #comienza a repartir desde el primer jugador
            i += 1                
    
    #agregando nuevo flop, updating #polimorfismo de dos funciones :)
    def new_river(self, add, eleminate): 
        river = rule.rule_sum(self.player, [])


baraja = Cartas()
baraja.tipo = ['Picas','Corazones','Diamantes','Tréboles']
baraja.cartas = [1,2,3,4,5,6,7,8,9,10,11,12,13]
baraja.mazo()
baraja.barajar()
# baraja.repartir(4)
baraja.new_flop(({'flop': [[5, 'Corazones'], [1, 'Corazones'], [10, 'Diamantes'], [4, 'Tréboles']], 'Player-1': [[1, 'Tréboles'], [13, 'Diamantes'], [10, 'Picas'], [7, 'Tréboles']], 'Player-2': [[7, 'Picas'], [12, 'Picas'], [8, 'Diamantes'], [11, 'Picas']], 'Player-3': [[13, 'Corazones'], [3, 'Tréboles'], [1, 'Diamantes'], [5, 'Tréboles']], 'Player-4': [[10, 'Corazones'], [9, 'Picas'], [12, 'Tréboles'], [11, 'Corazones']]}, 
    [[1, 2], 1],
    0
))

print(baraja.player)
