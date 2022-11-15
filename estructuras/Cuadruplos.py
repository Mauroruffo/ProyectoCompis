class Cuadruplos:
    def __init__(self, operador, opIzq, opDer, resultado):
        self.__operador = operador
        self.__opIzq = opIzq
        self.__opDer = opDer
        self.__resultado = resultado

    def operador(self):
        return self.__operador

    def opIzq(self):
        return self.__opIzq

    def opDer(self):
        return self.__opDer

    def resultado(self):
        return self.__resultado

    def set_resultado(self, newRes):
        self.__resultado = newRes

    def resolver(self):
        return self.__operador, self.__opIzq, self.__opDer, self.__resultado

    def print(self):
        print(f'{self.operador()} {self.opIzq()} {self.opDer()} {self.resultado()}')

