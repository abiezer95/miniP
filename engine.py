class Server:
    __all_players, _id_player = 0, 0
    limit_players = 0

    def online_player(self):
        self.__all_players =  self.__all_players + 1
        self._id_player = 'Player-'+str(self.__all_players) #creating id of player
    
    def limit_player(self):
        return False if self.limit_players <= 1 or self.limit_player > 4 else True

class RulesGame():
    inning = 1 #innings
    new_flop = 0
    player_finish = 0
    turn = []
    recursivity = []

    def shifts(self, limit): #inning system
        self.inning = 1 if self.inning == limit else self.inning + 1
        return self.inning
    
    def rule_sum(self, data, cards): #working
        self.turn = []
        player = data['Player-'+str(self.inning)] #getting turn or inning
        flop = data['flop'] #getting cards of desk flop

        try:    
            if isinstance(cards[0], list): #if you added one of your cards up between a group in desk flop
                for card in cards[0]:
                    self.new_flop = self.new_flop + flop[int(card)-1][0] #adding cards ading up
                    self.turn.append(flop[int(card)-1])
                    
                self.turn.append(player[int(cards[1])-1])
            else: 
                getted = flop[int(cards[0])-1]
                self.new_flop = getted[0] #card of desk flop
                self.turn.extend((getted, player[int(cards[1])-1]))

                if isinstance(getted[1], list): #removing first digit
                    self.turn = []
                    for card in getted:
                        if isinstance(card, list): #if there is two or more cards join in the desk flop
                            self.turn.append(card)
                    self.turn.append(player[int(cards[1])-1])

            self.turn.insert(0, self.new_flop+player[int(cards[1])-1][0])
        except IndexError:
            return [15] #sending error

        return self.turn
    
    def rule_get(self, data, cards, player):
        river = []
        flop = data['flop']

        if cards == 'success': #who plays the last time
            e = 0
            if len(flop) != 0:
                for card in flop:
                    if isinstance(card[1], list): #if there were already cards added up
                        flop[e].pop(0) #deleting first digit useless
                        [river.append(i) for i in flop[e]] #flop
                    else:
                        river.append(card) #flop
                    e += 1
    
            return river
        ################
        if not isinstance(cards[0], list): #if not adding up cards of desk flop
            try:
                card1 = int(cards[0]) #flop
                card2 = int(cards[1]) #player card
                
                if flop[card1-1][0] ==  player[card2-1][0]:
                    self.player_finish = self.inning
                    if isinstance(flop[card1-1][1], list): #if there is cards added up
                        flop[card1-1].pop(0) #deleting first digit useless
                        [river.append(i) for i in flop[card1-1]] #flop
                        river.append(player[card2-1]) #player
                    else:
                        river.extend((flop[card1-1], player[card2-1])) #adding
                        
                    flop.pop(card1-1) #deliting degits useless
                    [data['total'][self.inning-1].append(i) for i in river]
                else:
                    return False
                # self.turn = flop
            except IndexError:
                    return False
        else: #if you will get a card adding up two or more of in desk flop
            total = 0
            save = False
            for i in cards[0]:
                try:
                    if flop[int(i)-1][0] == player[int(cards[-1])-1][0]:
                        save = True
                    else:
                        total = total + int(flop[int(i)-1][0])
                except IndexError:
                    return False
            
            if total == player[int(cards[-1])-1][0] or save == True:
                self.player_finish = self.inning
                cards[0].sort(reverse = True)

                for i in cards[0]:
                    river.append(flop[int(i)-1]) #flop
                river.append(player[int(cards[-1])-1]) #player
                
                [flop.pop(int(i)-1) for i in cards[0]] 
                # player.pop(int(cards[1]-1))

                self.turn = flop     
            else:
                river = False
        return river

    #2 picas = 1. ases=1, 10 diamante = 2, mas picas o trebol = 2
    def rule_winner(self, data, limit, i):
        self.__get_result_winner(data, limit, i)
        i = 0
        max_cards = 0
        players = []
        for winner in self.recursivity:
            if winner['maxCards'] >= max_cards:
                i += 1
            players.append(winner['max'])
        
        winner = 0
        players[i-1] = players[i-1]+3 #greater number of cards

        return players
    
    def __get_result_winner(self, data, limit, i):
        black = ['tréboles', 'picas'] 
        total = {'maxCards': 0, 'max': 0} 

        for cards in data['total'][i]:
            if cards[0] == 2 and cards[1].lower() == 'picas' or cards[0] == 1: #2picas #ases 
                total['max'] += 1
            if cards[0] == 10 and cards[1].lower() == 'diamantes': #10 diamond
                total['max'] += 2  
            if cards[1].lower() in black: #who has the total wins 2 points
                total['maxCards'] += 1
        
        self.recursivity.append(total)

        if i < limit-1:
            self.__get_result_winner(data, limit, i+1) #recursivity 