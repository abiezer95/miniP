import cartas
import time, os
# import engine

# server = engine.Server()
# rule = engine.Server()
game = cartas.Cartas()
game.tipo = ['Picas','Corazones','Diamantes','Tréboles']
game.cartas = [1,2,3,4,5,6,7,8,9,10,11,12,13]

definitions = {
    'welcome': 'bienvenido a casino en python console',
    'n_players': 'Elige cuantos jugaran: ',
    'n_player_error': 'Solo puedes jugar con 4 jugadores y no puedes jugar con un solo jugador',
    'inning': 'Es el turno del jugador $n',
    'player': 'Jugador $n estas son sus cartas: ',
    'choose': 'Que vas a elegir: ',
    'suggestions1': 'En este caso puedes sumar tu carta $n con $y',
    'suggestions2': 'En este caso puedes llevarte la carta $n'
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
    piece_text(10, '/', definitions['welcome'].upper())
    n_player = get_input(definitions['n_players'])
    cartas.server.limit_player = n_player
    if int(n_player) <= 1 or int(n_player) > 4:
        print(definitions['n_player_error'])
        time.sleep(3), cls(), load_game()
    else:
        time.sleep(2), cls()
        setTimeOut([[1, 'game.mazo()'], [1, 'game.barajar()'], [1, 'game.repartir('+n_player+')']])
        time.sleep(2), cls()
        flop()

def flop():
    river = ""
    player_card = ""
    cartas.rule.shifts()
    inning = cartas.rule.inning

    for cards in game.all_data['flop']:
        river = river +"/"+ str(cards[0])+"-"+cards[1][0].upper()+"/   "
    
    for cards in game.all_data['Player-'+str(inning)]:
        player_card = player_card +"/"+ str(cards[0])+"-"+cards[1][0].upper()+"/   "
    
    
    piece_text(5, '⚄ ', definitions['inning'].replace('$n', 'Player-'+str(inning)))
    print('\n')
    piece_text(5, ' ', river+'\n\n')
    print(definitions['player'].replace('$n', str(inning))+player_card)
    
load_game()