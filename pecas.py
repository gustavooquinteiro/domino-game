class Peca():
    def __init__(self, numerador, denominador):
        self.numerador = numerador
        self.denominador = denominador
    
    def __repr__(self):
        return "{} | {}" .format(self.numerador, self.denominador)

    
 
p = Peca(1, 2)
print(p)
