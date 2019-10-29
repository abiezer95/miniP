import random
import re as regex
import json
import engine

server = engine.Server()
rule = engine.RulesGame({'n_player': 4})

class Cartas:
    tipo = []
    cartas, cards, all_data = [], [], {'flop': [], 'total': []}
    icon = ''
    checks = []

    def mazo(self): #creamos el mazo normal de cartas
        i = 0
        for card in self.cartas:
            for x in self.tipo:
                self.cards.append([card, x, self.icon[i]])
                i += 1
                if i == 4:
                    i = 0
                
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
        player = self.all_data['Player-'+str(shifts)]
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
                # n = 0
                # print(river)
                # for i in flop[cards[0]-1]:
                #     if n == 1 and not isinstance(i, list):
                #         flop[cards[0]-1].pop(n)
                #     n += 1
                

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
                
    def check(self, total, card, player_get):
        text = ''
        player = self.all_data['Player-'+str(1)]
        for cards in player:
            if total == cards[0]:
                text = 'Suma: /'+str(player_get)+'/ + /'+text+str(card[0])+card[2]+'/ = '+str(cards[0])+cards[2]
                # text = text+str(player[0])
        return text
        # return text

    def check_cards(self, i):
        player = self.all_data['Player-'+str(1)][i][0]
        for card in self.all_data['flop']:
            total = card[0] + player
            result = self.check(total, card, player)
            if card[0] == self.all_data['Player-'+str(1)][i][0]: 
                print('LLevate el: '+str(self.all_data['Player-'+str(1)][i][0]))
                #este if podia hacerse en la funcion check pero para ejemplo de recursividad lo hice aqui
            if len(result) > 0:
                print(result)
        i += 1
        if i >= len(self.all_data['Player-'+str(1)])-1:
            return 0
        else:
            return self.check_cards(i) #ejemplo de recursividad  
        

# baraja = Cartas()
# baraja.tipo = ['Picas','Corazones','Diamantes','Tréboles']
# baraja.cartas = [1,2,3,4,5,6,7,8,9,10,11,12,13]
# baraja.icon = ['♤', '♥', '♦', '♣']
# baraja.mazo()
# baraja.barajar()

# baraja.repartir(4)

# rule.shifts() #turnos

# baraja.suggest_play('sum', [[1, 2], 1])

# baraja.all_data = {'flop': [[4, 'Diamantes', '♦'], [1, 'Picas', '♤'], [9, 'Diamantes', '♦'], [11, 'Corazones', '♥']], 'total': [[], [], [], []], 'Player-1': [[13, 'Picas', '♤'], [13, 'Corazones', '♥'], [6, 'Picas', '♤'], [6, 'Tréboles', '♣']], 'Player-2': [[8, 'Picas', '♤'], [3, 'Diamantes', '♦'], [3, 'Tréboles', '♣'], [9, 'Corazones', '♥']], 'Player-3': [[12, 'Picas', '♤'], [11, 'Picas', '♤'], [10, 'Corazones', '♥'], [12, 'Corazones', '♥']], 'Player-4': [[1, 'Corazones', '♥'], [12, 'Diamantes', '♦'], [13, 'Tréboles', '♣'], [1, 'Diamantes', '♦']]}

# baraja.new_flop('sum', [2, 3], 1)
# rule.shifts()
# baraja.new_flop('sum', [2, 1], 2)
# baraja.new_flop('sum', [[2, 3], 2], 2)
# baraja.new_flop('sum', [[2, 3], 2], 2)
# baraja.new_flop('get_card', [[1, 2], 1], 0)

# print(baraja.all_data)
