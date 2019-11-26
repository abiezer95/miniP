import cartas
import time, os
import re as regex

game = cartas.Cartas(
    ['Picas','Corazones','Diamantes','Tréboles'],
    [1,2,3,4,5,6,7,8,9,10,11,12,13],
    ['♤', '♥', '♦', '♣']
)

definitions = {
    'welcome': 'bienvenido a casino en python console',
    'n_players': 'Elige cuantos jugaran: ',
    'n_player_error': 'Solo puedes jugar con 4 jugadores y no puedes jugar con un solo jugador',
    'inning': 'Es el turno del jugador $n',
    'player': 'Jugador $n estas son sus cartas: ',
    'choose': 'Que vas a elegir: ',
    'playing': 'Que jugaras \nSumar(1), Obtener(2), Dejar Carta (3), Sugerencias (4): ',
    'suggestions': '\nPara (obtener, sumar o dejar carta escribir el numero que se indica)\nEscribe ej. (1+2) para sumar la (1ra) carta de la mesa (flop) y la (2da) de tu mazo.\nLlevate una carta escribiendo (1=2) siguiendo la misma estructura y 1+2=3 para sumar \nla 3ra carta de tu mazo con 2 sumadas de la mesa. También puedes dejar una carta escribiendo \nla posición de esta ej. 3',
}

def load_game():

    n_player = get_input(definitions['n_players'])

    try:
       n_player = int(n_player)
    except:
        n_player = ''

    if n_player != '':
        cartas.rule.inning = 1
        game._limit = int(n_player)
    else:
        cls()
        load_game()

    if int(n_player) <= 1 or int(n_player) > 4:
        print(definitions['n_player_error'])
        time.sleep(3), cls(), load_game()
    else:
        time.sleep(2), cls()
        setTimeOut([[1, 'game.mazo()'], [1, 'game.barajar()'], [1, 'game.repartir(False)']])
        time.sleep(2), cls()
        flop(0)
    

def flop(suggested): #jugabilidad y textos
    cls()
    river = ""
    player_card = ""
    icons = ""
    inning = 1 if cartas.rule.inning == 0 else cartas.rule.inning

    for cards in game.all_data['flop']: #cards of desk
        if isinstance(cards[1], list) or isinstance(cards[2], list):
            icons = [i[2] if isinstance(i, list) else '' for i in cards] #if there are an array in flop
            river = river +"/"+ str(cards[0])+"-"+str(''.join(icons))+"/ "
        else:
            river = river +"/"+ str(cards[0])+"-"+str(cards[2])+"/ " 
    
    for cards in game.all_data['Player-'+str(inning)]: #the player cards
        player_card = player_card +"/"+ str(cards[0])+"-"+cards[2].upper()+"/  "
    
    
    piece_text(5, '⚄ ', definitions['inning'].replace('$n', 'Player-'+str(inning))) #title and turn of player #titulo y turno del jugador
    
    print('\n')
    
    piece_text(5, ' ', river+'\n\n') #this is the flop
    
    print(definitions['player'].replace('$n', str(inning))+player_card) #cards of player
        
    if suggested == False:
        flop(True) #overwriting the flop
        player_play() #playing
    

def player_play(): #when the player is playing
    play = get_input(definitions['playing'])

    if play == '4':
        suggestion()

    action = False #action of new_flop

    if play == '1':
        flop(True)
        print('Para volver preciona ENTER')
        get = get_input('Sumar: ')
        try:
            get = make_card_play(get)
            if not get == ['']:
                    action = game.new_flop('sum', [i for i in get], cartas.rule.inning)
            else: 
                play = 0
        except:
            print('Error: no puedes usar letras')
            time.sleep(2)
            play = 0
        
         
    if play == '2':
        flop(True)
        print('Para volver preciona ENTER')
        get = get_input('Obtener: ')
        try:
            get = make_card_play(get)
            if not get == ['']:
                action = game.new_flop('get_card', [i for i in get], cartas.rule.inning)
            else:
                play = 0
        except:
            print('Para volver preciona ENTER')
            print('Error: no puedes usar letras')
            time.sleep(2)
            play = 0
    
    if play == '3':
        flop(True)
        print('Para volver preciona ENTER')
        get = get_input('Dejar carta: ')
        try:
            get = make_card_play(get)
            if not get == ['']:
                action = game.new_flop('leave_card', [i for i in get], cartas.rule.inning)
            else:
                play = 0
        except:
            print('Error: no puedes usar letras')
            time.sleep(2)
            play = 0
    
    if action == True: #error of cards
        print('Error cartas no coinciden o las sumaste más de 14')
        time.sleep(2)
        play = 0
        flop(0)

    if len(game._Cartas__cards) == 0 and action == 'turn_finished': # if the gane finished
        game.new_flop('get_card', 'success', cartas.rule.inning) #getting all from the desk if you are the last in get a card
        cls()
        piece_text(7, '❤ ', 'CONGRATULATIONS')
        all_finished() #counting for get the winner
        return #
    else:
        back_page(play) #back to the start

        cartas.rule.shifts(game._limit) #new turn
        
        if action == 'turn_finished': #deal cards
            cls()
            print('Ahora comenzara la nueva mano..')
            time.sleep(1)
            game.repartir(True)
            print('Quedan '+str(len(game._Cartas__cards))+' por repartir') #access to private element
            time.sleep(2)
            back_page(0)
        
        print('Listo, ahora es turno del jugador '+str(cartas.rule.inning))
        setTimeOut([[3, 'cls(),flop(False)']])

def all_finished(): #when all finish
    time.sleep(2)
    cls()
    _max = cartas.rule.rule_winner(game.all_data, game._limit, 0)
    winner = [i for i, j in enumerate(_max) if j == max(_max)][0]+1
    piece_text(7, '❤ ', 'The winner is the '+'PLAYER-'+str(winner))
    print('Estas son las estadisticas: \n')
    i = 1
    for winner in _max:
        print('Player-'+str(i)+': '+str(winner))
        i += 1

    print('\n')
    piece_text(10, '❤ ', 'Winner')
    input('\nContinuar Press ENTER')
    exit()

def back_page(play):
    if play not in ['1', '2', '3']:
        flop(True), player_play()

def make_card_play(card):
    river = regex.sub(r'[=,+ ]', '-', card).split('-')
    flop = []
    if len(river) >= 3:
        river.pop(-1)
        flop.extend((river, card[-1]))
        card = flop
    else:
        card = river

    return [''] if True in [True if i == '' else False for i in river] else card #error y value


def suggestion():
    print('Puedes jugar de esta forma: ')
    game.check_cards(0)
    
    print(definitions['suggestions'])
    get_input('\nPreciona ENTER para continuar')
    flop(True)

def piece_text(n, piece, text):
    slash = ''
    slash = ''
    i = 0
    while i <= n:
        slash = slash+piece
        i += 1
    print(slash+' '+text+' '+slash)

def setTimeOut(function):
    for f in function:
        time.sleep(f[0])
        eval(f[1])

def get_input(text):
    var = input(text)
    return var

def cls():
    # os.system ("clear") #this is for linux
    os.system ("cls") 

piece_text(10, '/', definitions['welcome'].upper())
load_game() 