class Movie:
    hello = ['asasd', 'asdas']
    def __init__(self, name, age):
        self.name = name
        self.age = age


class Serie(Movie):
    def _init_(self, name, age, apellido):
        Movie.__init__(self, name, age)
        # self.lastname = apellido
        


# lol = Movie('abiezer', '15')
lols = Serie('antonio', '15')

print(lols.name)


