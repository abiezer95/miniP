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
    'playing': 'Que jugaras \nSumar(1), Obtener(2), Dejar Carta (3): ',
    'suggestions': '\nPara (obtener, sumar o dejar carta escribir el numero que se indica)\nEscribe ej. (1+2) para sumar la (1ra) carta de la mesa (flop) y la (2da) de tu mazo.\nLlevate una carta escribiendo (1=2) siguiendo la misma estructura y 1+2=3 para sumar \nla 3ra carta de tu mazo con 2 sumadas de la mesa. También puedes dejar una carta escribiendo \nla posición de esta ej. 3',
}

def load_game():
    piece_text(10, '/', definitions['welcome'].upper())
    n_player = get_input(definitions['n_players'])
    game._limit = int(n_player)
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

    for cards in game.all_data['flop']: #cartas de la mesa
        if isinstance(cards[1], list) or isinstance(cards[2], list):
            icons = [i[2] if isinstance(i, list) else '' for i in cards] #si es array en flop
            river = river +"/"+ str(cards[0])+"-"+str(''.join(icons))+"/ "
        else:
            river = river +"/"+ str(cards[0])+"-"+str(cards[2])+"/ " 
    
    for cards in game.all_data['Player-'+str(inning)]: #cartas del jugador
        player_card = player_card +"/"+ str(cards[0])+"-"+cards[2].upper()+"/  "
    
    
    piece_text(5, '⚄ ', definitions['inning'].replace('$n', 'Player-'+str(inning))) #titulo y turno del jugador
    
    print('\n')
    
    piece_text(5, ' ', river+'\n\n') #este es el flop
    
    print(definitions['player'].replace('$n', str(inning))+player_card) #cartas del jugador
    
    suggest = get_input('\nVer sugerencias (y/n): ').upper() if suggested == False else True

    if suggest == 'Y':
        suggestion()
        
    if suggested == False:
        flop(True) #sobreescribiendo el flop
        player_play() #jugando
    

def player_play(): #cuando el jugador va a jugar
    play = get_input(definitions['playing'])
    action = False #accion del new_flop

    if play == '1':
        flop(True)
        get = get_input('Sumar: ')
        get = make_card_play(get)
        if not get == ['']:
            action = game.new_flop('sum', [i for i in get], cartas.rule.inning)
        else: 
            play = 0
            
    if play == '2':
        flop(True)
        get = get_input('Obtener: ')
        get = make_card_play(get)
        if not get == ['']:
            action = game.new_flop('get_card', [i for i in get], cartas.rule.inning)
        else:
            play = 0
    
    if play == '3':
        flop(True)
        get = get_input('Dejar carta: ')
        get = make_card_play(get)
        if not get == ['']:
            action = game.new_flop('leave_card', [i for i in get], cartas.rule.inning)
        else:
            play = 0
    
    if action == True: #error de cartas
        print('Error cartas no coinciden o las sumaste más de 14')
        time.sleep(2)
        play = 0

    if len(game._Cartas__cards) == 0 and action == 'turn_finished': # si ya acabo todo el juego

        all_finished()

    back_page(play) #volver al principio

    cartas.rule.shifts(game._limit) #nuevo turno
    
    if action == 'turn_finished': #para repartir mas cartas
        cls()
        print('Ahora comenzara la nueva mano..')
        time.sleep(1)
        game.repartir(True)
        print('Quedan '+str(len(game._Cartas__cards))+' por repartir') #accediendo a elemento privado
        time.sleep(2)
        back_page(0)
    
    print(game.all_data)
    print('Listo, ahora es turno del jugador '+str(cartas.rule.inning))
    setTimeOut([[3, 'cls(),flop(False)']])

def all_finished(): #cuando acabas todo
    _max = cartas.rule.rule_winner(game.all_data, game._limit, 0)
    winner = [i for i, j in enumerate(_max) if j == max(_max)][0]+1
    piece_text(7, '❤ ', 'The winner is the '+'Player-'+str(winner))
    print('Estas son las estadisticas: \n')
    i = 1
    for winner in _max:
        print('Player-'+str(i)+': '+str(winner))
        i += 1
    press = input('\nEmpezar otra partida? (Y/N): ')
    if press.upper() == 'Y':
        load_game()

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

    return [''] if True in [True if i == '' else False for i in river] else card #error y valor


def suggestion():
    print('Puedes jugar de esta forma: ')
    game.check_cards(0)
    
    print(definitions['suggestions'])
    get_input('\nPreciona ENTER para continuar')
    flop(True)

def piece_text(n, piece, text):
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
    # os.system ("clear")
    os.system ("cls") 

load_game()