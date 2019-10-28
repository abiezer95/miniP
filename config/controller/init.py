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
    os.system ("clear")
    os.system ("cls") 

def load_game():
    setTimeOut([[0, 'game.mazo()'], [0, 'game.barajar()'], [0, 'game.repartir(4)']])
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
    river = ""
    player_card = ""
    inning = 1 if cartas.rule.inning == 0 else cartas.rule.inning
    
    game.all_data = {'flop': [[7, [1, 'Corazones', '♥'], [6, 'Diamantes', '♦']], [12, 'Corazones', '♥'], [2, 'Tréboles', '♣'], [6, 'Tréboles', '♣']], 'total': [[], [], [], []], 'Player-1': [[6, 'Diamantes', '♦'], [8, 'Diamantes', '♦'], [11, 'Corazones', '♥'], [1, 'Picas', '♤']], 'Player-2': [[5, 'Tréboles', '♣'], [13, 'Picas', '♤'], [12, 'Picas', '♤'], [4, 'Picas', '♤']], 'Player-3': [[10, 'Picas', '♤'], [8, 'Picas', '♤'], [13, 'Diamantes', '♦'], [9, 'Corazones', '♥']], 'Player-4': [[12, 'Diamantes', '♦'], [10, 'Corazones', '♥'], [9, 'Picas', '♤'], [7, 'Tréboles', '♣']]}
    
    icons = ''
    for cards in game.all_data['flop']:
        if isinstance(cards[1], list):
            icons = icons + str([i[2] if isinstance(i, list) else ':' for i in cards])
            print(icons)
            # print(icons)
            river = river +"/"+ str(cards[0])+"-"+icons+"/ "
        # else:
        #     river = river +"/"+ str(cards[0])+"-"+cards[2].upper()+"/ " 
    # print(river)
    
    for cards in game.all_data['Player-'+str(inning)]:
        player_card = player_card +"/"+ str(cards[0])+"-"+cards[2].upper()+"/   "
    
    #titulo y turno del jugador
    piece_text(5, '⚄ ', definitions['inning'].replace('$n', 'Player-'+str(inning)))
    
    print('\n')
    
    piece_text(5, ' ', river+'\n\n') #este es el flop
    
    print(definitions['player'].replace('$n', str(inning))+player_card) #cartas del jugador
    
    suggest = get_input('\nVer sugerencias (y/n): ').upper() if suggested == False else True

    if suggest == 'Y':
        suggestion()
        
    if suggested == False:
        flop(True) #sobreescribiendo el flop
        player_play() #jugando
        
    # print(game.sum_play('sum', [[1, 2], 1]))
    
def suggestion():
    print('Puedes jugar de esta forma: ')
    game.check_cards(0)
    
    print(definitions['suggestions'])
    get_input('\nPreciona ENTER para continuar')
    flop(True)
        

def player_play():
    cartas.rule.shifts() #nuevo turno
    play = get_input('Que jugaras \n Sumar(1), Obtener(2): ')
    if play == '1':
        flop(True)
        get = get_input('Sumar: ')
        get = get.replace(' ', '').split('-')
        get = [int(i) for i in get]
        print(get)
        game.new_flop('sum', get, cartas.rule.inning)
    
    print(game.all_data)
    # flop(True)
    

load_game()