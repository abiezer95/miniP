import cartas
import time, os

game = cartas.Cartas()
game.tipo = ['Picas','Corazones','Diamantes','Tréboles']
game.cartas = [1,2,3,4,5,6,7,8,9,10,11,12,13]
game.icon = ['♤', '♥', '♦', '♣']

definitions = {
    'welcome': 'bienvenido a casino en python console',
    'n_players': 'Elige cuantos jugaran: ',
    'n_player_error': 'Solo puedes jugar con 4 jugadores y no puedes jugar con un solo jugador',
    'inning': 'Es el turno del jugador $n',
    'player': 'Jugador $n estas son sus cartas: ',
    'choose': 'Que vas a elegir: ',
    'playing': 'Que jugaras \nSumar(1), Obtener(2), Dejar Carta (3): ',
    'suggestions': '\nEscribe ej. 1+2 para sumar donde 1 es la 1ra carta de las principales del frente (flop) y 2 para la 2da de tu mazo\nLlevate una carta escribiendo 1=2 siguiendo la misma estructura y 1,2+3 para sumar \nla 1ra y 2da carta del flop con la 3ra de tu mazo',
}

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

def load_game():
    setTimeOut([[0, 'game.mazo()'], [0, 'game.barajar()'], [0, 'game.repartir(4, False)']])
    flop(0)
    
    # piece_text(10, '/', definitions['welcome'].upper())
    # n_player = get_input(definitions['n_players'])
    # cartas.server.limit_player = n_player
    # if int(n_player) <= 1 or int(n_player) > 4:
    #     print(definitions['n_player_error'])
    #     time.sleep(3), cls(), load_game()
    # else:
    #     time.sleep(2), cls()
    #     setTimeOut([[1, 'game.mazo()'], [1, 'game.barajar()'], [1, 'game.repartir('+n_player+')']])
    #     time.sleep(2), cls()
    #     flop()

def flop(suggested): #jugabilidad y textos
    cls()
    # print(game.all_data)
    river = ""
    player_card = ""
    inning = 1 if cartas.rule.inning == 0 else cartas.rule.inning
    
    # game.all_data = {'flop': [[7, [1, 'Corazones', '♥'], [6, 'Diamantes', '♦']], [12, 'Corazones', '♥'], [2, 'Tréboles', '♣'], [6, 'Tréboles', '♣']], 'total': [[], [], [], []], 'Player-1': [[6, 'Diamantes', '♦'], [8, 'Diamantes', '♦'], [11, 'Corazones', '♥'], [1, 'Picas', '♤']], 'Player-2': [[5, 'Tréboles', '♣'], [13, 'Picas', '♤'], [12, 'Picas', '♤'], [4, 'Picas', '♤']], 'Player-3': [[10, 'Picas', '♤'], [8, 'Picas', '♤'], [13, 'Diamantes', '♦'], [9, 'Corazones', '♥']], 'Player-4': [[12, 'Diamantes', '♦'], [10, 'Corazones', '♥'], [9, 'Picas', '♤'], [7, 'Tréboles', '♣']]}
    
    icons = ''
    for cards in game.all_data['flop']:
        if isinstance(cards[1], list) or isinstance(cards[2], list):
            icons = [i[2] if isinstance(i, list) else '' for i in cards] #si es array en flop
            river = river +"/"+ str(cards[0])+"-"+str(''.join(icons))+"/ "
        else:
            river = river +"/"+ str(cards[0])+"-"+str(cards[2])+"/ " 
    
    for cards in game.all_data['Player-'+str(inning)]:
        player_card = player_card +"/"+ str(cards[0])+"-"+cards[2].upper()+"/   "
    
    
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

    
def suggestion():
    print('Puedes jugar de esta forma: ')
    game.check_cards(0)
    
    print(definitions['suggestions'])
    get_input('\nPreciona ENTER para continuar')
    flop(True)
        

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
        get = get_input('Objeter: ')
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

    back_page(play) #volver a lo mismo

    cartas.rule.shifts() #nuevo turno
    # print(action)
    print('Listo, ahora es turno del jugador '+str(cartas.rule.inning))
    setTimeOut([[3, 'cls(),flop(False)']])

    # print(game.all_data)
    # flop(True)
    
def back_page(play):
    if play not in ['1', '2', '3']:
        flop(True), player_play()

def make_card_play(card):
    river = card.replace('=', '-').split('-')
    flop = []
    if len(river) >= 3:
        river.pop(-1)
        flop.extend((river, card[-1]))
        card = flop
    else:
        card = river
    return card

load_game()