import random
import re as regex
import json
import engine

server = engine.Server()
rule = engine.RulesGame()

class Cartas:

    __cards = []
    _limit = 0

    def __init__(self, tipo, cartas, icon):
        self.__tipo = tipo #private
        self.__cartas = cartas 
        self.icon = icon
        self.all_data = {'flop': [], 'total': []}

    def mazo(self): #creamos el mazo normal de cartas
        i = 0
        for card in self.__cartas:
            for x in self.__tipo:
                self.__cards.append([card, x, self.icon[i]])
                i += 1
                if i == 4:
                    i = 0
        print('Mazo de cartas listo...')

    def barajar(self):
        random.shuffle(self.__cards) #barajando de forma aleatoria
        print('Cartas barajadas ...')

    def repartir(self, step):
        limit = self._limit
        if step == False:
            for i in range(limit): #añadimos el id de jugador a la mesa
                server.online_player()
                self.all_data[server._id_player] = [] 
                self.all_data['total'].append([]) 
                ############
        i = 0
        e = 1
        flop = limit*4
        for card in self.__cards: #repartiendo
            if i >= flop: #ultimas cartas repartidas en mesa
                if step == False:
                    self.all_data['flop'].append(card)
                if i >= flop+3:
                    self.__cards.pop(i)
                    break
            else: #repartiendo a jugadores
                self.all_data['Player-'+str(e)].append(card)
                e = 1 if e == limit else e + 1 #comienza a repartir desde el primer jugador
                if i == flop and step == True:
                    break
            self.__cards.pop(i)
        
            i += 1
        # print(len(self.__cards))
        print('Cartas repartidas ...')
        
    #agregando nuevo flop, updating #polimorfismo de dos funciones :)
    def new_flop(self, action, cards, shifts): #nueva baraja del flop
        flop = self.all_data['flop']
        player = self.all_data['Player-'+str(shifts)]

        if action == 'sum':
            i = 1
            river = rule.rule_sum(self.all_data, cards)
            if not river[0] >= 15:    #si lo que sumas es mayor que 14 
                try:
                    if isinstance(cards[0], list): #si se suma una o mas cartas del flop y una tuya
                        for card in cards[0]:
                            flop.pop(int(card)-i)
                            i += 1
                        flop.insert(int(cards[0][0])-1, river)
                    else: # si se suma una carta tuya y del flop
                        flop.pop(int(cards[0])-1)
                        flop.insert(int(cards[0])-1, river)
                    player.pop(int(cards[-1])-1) #quitando carta de mi mazo
                except IndexError:
                    return False
            else:
                return True #error
            
        if action == 'get_card':
            river = rule.rule_get(self.all_data, cards, player)
            if river == False: #error
                return True

            [self.all_data['total'][shifts-1].append(i) for i in river] #agregando cartas a total
            player.pop(int(cards[-1])-1)
            print('Carta obtenida')

        if action == 'leave_card':
            try:
                flop.append(player[int(cards[0])-1])
                player.pop(int(cards[0])-1)
            except IndexError:
                return True #error

        if rule.inning == self._limit and len(player) == 0: #repartir nueva mano
            return 'turn_finished'
                
    def check(self, total, card, player_get):
        text = ''
        player = self.all_data['Player-'+str(1)]
        for __cards in player:
            if total == __cards[0]:
                text = 'Suma: /'+str(player_get)+'/ + /'+text+str(card[0])+card[2]+'/ = '+str(__cards[0])+__cards[2]
                
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