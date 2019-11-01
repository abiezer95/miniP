import random
import re as regex
import json
import engine

server = engine.Server()
rule = engine.RulesGame({'n_player': 2})

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

    def repartir(self, playerlimit, step):
        if step == False:
            for i in range(playerlimit): #añadimos el id de jugador a la mesa
                server.online_player()
                self.all_data[server.id_player] = [] 
                self.all_data['total'].append([]) 
                ############
        i = 0
        e = 1
        flop = playerlimit*4
        for card in self.cards: #repartiendo
            if i >= flop:
                if step == False:
                    self.all_data['flop'].append(card)
                    if i >= flop+3:
                        break
            else:
                self.all_data['Player-'+str(e)].append(card)
            self.cards.pop(i)
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
            if not river[0] >= 15:    #si lo que sumas es mayor que 14 
                if isinstance(cards[0], list): #si se suma una o mas cartas del flop y una tuya
                    for card in cards[0]:
                        flop.pop(int(card)-i)
                        i += 1
                    flop.insert(int(cards[0][0])-1, river)
                else: # si se suma una carta tuya y del flop
                    flop.pop(int(cards[0])-1)
                    flop.insert(int(cards[0])-1, river)
                player.pop(int(cards[-1])-1) #quitando carta de mi mazo
            else:
                return True #error
            
        if action == 'get_card':
            river = rule.rule_get(self.all_data, cards, player)
            if river == False: #error
                return True

            [self.all_data['total'][shifts-1].append(i) for i in river] #agregando cartas a total
            print('Carta obtenida')

        if action == 'leave_card':
            flop.append(player[int(cards[0])-1])
            player.pop(int(cards[0])-1)

        limit = rule.serverData['n_player'] #si se quedan sin cartas
        if rule.inning == limit and len(player) == 0:
            return 'turn_finished'
                
    def check(self, total, card, player_get):
        text = ''
        player = self.all_data['Player-'+str(1)]
        for cards in player:
            if total == cards[0]:
                text = 'Suma: /'+str(player_get)+'/ + /'+text+str(card[0])+card[2]+'/ = '+str(cards[0])+cards[2]
        return text


    def check_cards(self, i): #para las sugerencias
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

# baraja.repartir(2, False)

# rule.shifts() #turnos

# baraja.suggest_play('sum', [[1, 2], 1])

# baraja.all_data = {'flop': [[4, 'Diamantes', '♦'], [1, 'Picas', '♤'], [1, 'Diamantes', '♦'], [11, 'Corazones', '♥']], 'total': [[], [], [], []], 'Player-1': [[4, 'Picas', '♤'], [1, 'Corazones', '♥'], [1, 'Corazones', '♤'], [6, 'Tréboles', '♣']], 'Player-2': [[4, 'Picas', '♤'], [3, 'Diamantes', '♦'], [6, 'Tréboles', '♣'], [9, 'Corazones', '♥']], 'Player-3': [[12, 'Picas', '♤'], [11, 'Picas', '♤'], [10, 'Corazones', '♥'], [12, 'Corazones', '♥']], 'Player-4': [[1, 'Corazones', '♥'], [12, 'Diamantes', '♦'], [13, 'Tréboles', '♣'], [1, 'Diamantes', '♦']]}

# baraja.new_flop('sum', [[1, 2], 2], 1)
# rule.shifts()
# baraja.new_flop('get_card', [1, 1], 2)
# 
# baraja.new_flop('leave_card', [1], 2)
# baraja.new_flop('sum', [[2, 3], 2], 2)
# baraja.new_flop('sum', [[2, 3], 2], 2)
# baraja.new_flop('get_card', [[1, 2], 1], 0)

# print(baraja.all_data)
