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

    def mazo(self): #creating deck of cards
        i = 0
        for card in self.__cartas:
            for x in self.__tipo:
                self.__cards.append([card, x, self.icon[i]])
                i += 1
                if i == 4:
                    i = 0
        print('Mazo de cartas listo...')

    def barajar(self):
        random.shuffle(self.__cards) #shuffle deck of cards
        print('Cartas barajadas ...')

    def repartir(self, step):
        limit = self._limit
        if step == False:
            for i in range(limit): #adding the player id in desk flop
                server.online_player()
                self.all_data[server._id_player] = [] 
                self.all_data['total'].append([]) 
                ############
        i = 0
        e = 1
        delete = []
        flop = limit*4
        for card in self.__cards: #spreading, distributing cards
            if i >= flop: #last cards spreading in desk
                if step == False:
                    self.all_data['flop'].append(card)
                    self.__cards.pop(0)
                if i >= flop+3:
                    break
            else:
                self.all_data['Player-'+str(e)].append(card)
                e = 1 if e == limit else e + 1 #starting to spreading from first player then second even
                delete.append(i) #to prevent the error of bad cards spreading
            i += 1
        [self.__cards.pop(0) for i in delete]       
        
        print('Cartas repartidas ...')
        
    #adding new desk flop, updating #polimorfismo de dos funciones :)
    def new_flop(self, action, cards, shifts): #new card of flop
        flop = self.all_data['flop']
        player = self.all_data['Player-'+str(shifts)]

        if action == 'sum':
            i = 1
            river = rule.rule_sum(self.all_data, cards)
            if not river[0] >= 15:    #if you adding up a greter digit  of 14
                try:
                    if isinstance(cards[0], list): #if you add a card up more than a card flop and one your
                        for card in cards[0]:
                            flop.pop(int(card)-i)
                            i += 1
                        flop.insert(int(cards[0][0])-1, river)
                    else: # if you add a card up with one of the desk flop
                        flop.pop(int(cards[0])-1)
                        flop.insert(int(cards[0])-1, river)
                    player.pop(int(cards[-1])-1) #removing card of my deck
                except IndexError:
                    return False
            else:
                return True #error
            
        if action == 'get_card':
            river = rule.rule_get(self.all_data, cards, player)
            if river == False: #error
                return True

            if cards != 'success': #if doesnt all cards
                [self.all_data['total'][shifts-1].append(i) for i in river] #adding cards to total
                player.pop(int(cards[-1])-1)
            else:
                [self.all_data['total'][rule.player_finish-1].append(i) for i in river] #total of desk flop when all is finished

            print('Carta obtenida')

        if action == 'leave_card':
            try:
                flop.append(player[int(cards[0])-1])
                player.pop(int(cards[0])-1)
            except IndexError:
                return True #error

        if rule.inning == self._limit and len(player) == 0: #spreading new inning
            return 'turn_finished'
                
    def check(self, total, card, player_get):
        text = ''
        player = self.all_data['Player-'+str(1)]
        for __cards in player:
            if total == __cards[0]:
                text = 'Suma: /'+str(player_get)+'/ + /'+text+str(card[0])+card[2]+'/ = '+str(__cards[0])+__cards[2]
                
        return text


    def check_cards(self, i): #for suggestions
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
            return self.check_cards(i) #example of recursividad  