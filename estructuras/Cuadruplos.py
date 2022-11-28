class Cuadruplos:
    def __init__(self):
        # Inicializamos con una lista vacia y el contador de cuadruplos que sirven para los GoTo
        self.counter = 0
        self.list = []

    def gen_cuad(self, operador, opIzq, opDer, resultado):
        # Genera cuadruplo
        cuad = [operador, opIzq, opDer, resultado]
        self.list.append(cuad)
        print(cuad)
        self.counter += 1

    def fill_quad(self, rellena_cuad, index_cuad, valor):
        # Funcion para llenar un goto
        self.list[rellena_cuad][index_cuad] = valor
        print(self.list[rellena_cuad])

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

