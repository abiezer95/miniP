import random as r
import engine

server = engine.Server()
rule = engine.RulesGame({'n_player': 4})

class Cartas:
    tipo = []
    cartas, cards, all_data = [], [], {'flop': []}
    
    def mazo(self): #creamos el mazo normal de cartas 
        for card in self.cartas:
            for x in self.tipo:
                self.cards.append([card, x])

    def barajar(self):
        r.shuffle(self.cards) #barajando de forma aleatoria

    def repartir(self, playerlimit):
        for i in range(playerlimit): #añadimos el id de jugador a la mesa
            server.online_player()
            self.all_data[server.id_player] = [] 
            ############
        i = 0
        e = 1
        flop = playerlimit*4
        for card in self.cards:
            if i >= flop:
                self.all_data['flop'].append(card)
                if i >= flop+3:
                    break
            else:
                self.all_data['Player-'+str(e)].append(card)
            e = 1 if e == playerlimit else e + 1 #comienza a repartir desde el primer jugador
            i += 1                
    
    #agregando nuevo flop, updating #polimorfismo de dos funciones :)
    def new_flop(self, action, cards, eleminate): #nueva baraja del flop
        if action == 'sum':
            i = 1
            river = rule.rule_sum(self.all_data, cards)
            if isinstance(cards[0], list):
                for card in cards[0]:
                    self.all_data['flop'].pop(card-i)
                    i += 1
                self.all_data['flop'].insert(cards[0][0]-1, river)
            else:
                self.all_data['flop'].pop(cards[0]-1)
                self.all_data['flop'].insert(cards[0]-1, river)
        else:
            return
        

baraja = Cartas()
baraja.tipo = ['Picas','Corazones','Diamantes','Tréboles']
baraja.cartas = [1,2,3,4,5,6,7,8,9,10,11,12,13]
baraja.mazo()
baraja.barajar()

baraja.repartir(4)

rule.shifts() #turnos

baraja.new_flop('sum', [[2, 3], 2], 0)

print(baraja.all_data)
