class Variable:
    def __init__(self, varName, varType):
        self.__varName = varName
        self.__varType = varType
        self.__varValue = None
        self.__varSize = None

    def name(self):
        return self.__varName

    def type(self):
        return self.__varType

    def value(self):
        return self.__varValue

    def size(self):
        return self.__varSize

    def __repr__(self):
        print(self.__varName + ' ' + self.__varType + ' ' + self.__varValue + ' ' + self.__varSize)

class Function:
    def __init__(self, funcName, funcType):
        self.__funcName = funcName
        self.__funcType = funcType

    def name(self):
        return self.__funcName

    def type(self):
        return self.__funcType

class Constant:
    def __init__(self):

    # Tabla seccionada por los tipos de datos int, float, bool, string
    # cada seccion tiene un diccionario con las constantes y su direccion virtual
        self.table = {'int': {}, 'float': {}, 'bool': {}, 'string': {}}

    # funcion para agregar una constante a la tabla de constantes
    # entradas: tipo de dato de la constante, su direccion virtual y su valor
    def add_const(self, type, virtual_address, constant):
        self.table[type][constant] = virtual_address

    # funcion para verificar si una constante ya se encuentra en la tabla
    # entradas: tipo de dato de la constante y su valor
    # salidas: valor booleano de acuerdo a la existencia de la variable a buscar en la tabla
    def const_exists(self, type, constant):
        return constant in self.table[type].keys()

    # funcion para obtener la direccion virtual de alguna constante
    # entradas: tipo de dato de la constante y su valor
    # salida: su direccion virtual asignada
    def const_address(self, type, constant):
        return self.table[type][constant]