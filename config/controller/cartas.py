import random
import re as regex
import json
import engine

server = engine.Server()
rule = engine.RulesGame({'n_player': 4})

class Cartas:
    tipo = []
    cartas, cards, all_data = [], [], {'flop': [], 'total': []}
    
    def mazo(self): #creamos el mazo normal de cartas 
        for card in self.cartas:
            for x in self.tipo:
                self.cards.append([card, x])
        print('Mazo de cartas listo...')

    def barajar(self):
        random.shuffle(self.cards) #barajando de forma aleatoria
        print('Cartas barajadas ...')

    def repartir(self, playerlimit):
        for i in range(playerlimit): #añadimos el id de jugador a la mesa
            server.online_player()
            self.all_data[server.id_player] = [] 
            self.all_data['total'].append([]) 
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
        print('Cartas repartidas ...')
    #agregando nuevo flop, updating #polimorfismo de dos funciones :)
    def new_flop(self, action, cards, shifts): #nueva baraja del flop
        flop = self.all_data['flop']
        player = self.all_data['Player-'+str(1)]
        if action == 'sum':
            i = 1
            river = rule.rule_sum(self.all_data, cards)
            if isinstance(cards[0], list): #si se suma una carta del flop y una tuya
                for card in cards[0]:
                    flop.pop(card-i)
                    i += 1
                flop.insert(cards[0][0]-1, river)
            else: # si sse suma una carta tuya y del flop
                flop.pop(cards[0]-1)
                flop.insert(cards[0]-1, river)

        elif action == 'get_card':
            i = 0
            for card in cards[0]:
                if flop[card-1][0] == player[0][cards[-1]-1]:
                    if i == 0:
                        self.all_data['total'][0].append(flop[cards[0][i]-1])
                    else:
                        flop[cards[0][i]-1].pop(0) #eliminamos el valor del grupo de cartas
                        # river = regex.sub(r'^\[|\]$', '', str(flop[cards[0][i]-1]))
                        self.all_data['total'][0].extend((flop[cards[0][i]-1], player[cards[0][0]-1]))

                else:
                    return False #no puedes llevarte el grupo de cartas
                i += 1   
            
        
# baraja = Cartas()
# baraja.tipo = ['Picas','Corazones','Diamantes','Tréboles']
# baraja.cartas = [1,2,3,4,5,6,7,8,9,10,11,12,13]
# baraja.mazo()
# baraja.barajar()

# baraja.repartir(4)

# rule.shifts() #turnos

# baraja.all_data = {'flop': [[12, 'Diamantes'], [5, 'Corazones'], [2, 'Diamantes'], [12, 'Corazones']], 'Player-1': [[12, 'Corazones'], [5, 'Tréboles'], [4, 'Tréboles'], [8, 'Picas']], 'Player-2': [[9, 'Picas'], [10, 'Tréboles'], [2, 'Corazones'], [3, 'Picas']], 'Player-3': [[11, 'Tréboles'], [13, 'Diamantes'], [10, 'Diamantes'], [7, 'Corazones']], 'Player-4': [[3, 'Tréboles'], [6, 'Picas'], [9, 'Diamantes'], [11, 'Diamantes']], 'total': [[],[],[],[]]}

# baraja.new_flop('sum', [[2, 3], 2], 0)
# baraja.new_flop('get_card', [[1, 2], 1], 0)

# print(baraja.all_data['total'])
