class BS(object):

    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

    def __imprimir__(self):
        print('A idade de {} é {}'.format(self.nome, self.idade))


class SBS(BS):

    def __init__(self, nome, idade, potencia):
        BS.__init__(self, nome, idade)
        self.potencia = potencia
