class Fichas:
    def _init_(self, fichas):
        self.fichas = fichas

    def recargar(self):
        self.fichas = 1000

    def actual(self, fichas):
        self.fichas = fichas


i = 1
        e = 0
        for cards in self.cards:
            if e == playerlimit*4:
                break
            else:
                if i >= playerlimit:
                    i = 1
                else:
                    self.player['Player-'+str(i)].append(cards)
            i += i
            e += e