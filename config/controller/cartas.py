import random
import motor

motor = motor.Server()

class Cartas:
    tipo = []
    cartas, cards, player = [], [], {}

    # def _init_(self):
    #     self.tipo
    #     self.cartas

    def mazo(self):
        for card in self.cartas:
            for x in self.tipo:
                self.cards.append([card, x])

    def barajar(self):
        random.shuffle(self.cards)

    def repartir(self, playerlimit):
        for i in range(playerlimit):
            motor.online_player()
            self.player[motor.id_player] = [] #añadimos el id de jugador a la mesa
            #
        i = 0
        e = 1
        for card in self.cards:
            if i >= playerlimit*4:
                break
            else:
                self.player['Player-'+str(e)].append(card)
            e = 1 if e == playerlimit else e + 1 #si llega al limite de jugadores comienza a repartir desde el primer jugador
            i += 1                

baraja = Cartas()
baraja.tipo = ['Picas','Corazones','Diamantes','Tréboles']
baraja.cartas = ['1','2','3','4','5','6','7','8','9','10','11','12','13']
baraja.mazo()
baraja.barajar()
baraja.repartir(4)

print(baraja.player)
