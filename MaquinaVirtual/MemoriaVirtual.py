from TypeTranslate import *

class GlobalMemory:
    def __init__(self, varSize, constSize, constTable):
        # Cantidades que existen por cada tipo de dato
        varInt, varFloat, varBool, varString = varSize
        constInt, constFloat, constBool, constString = constSize

        self.TT = Translator()
        self.table = {
            'vars': {'int': [0] * (varInt + 1), 'float': [0.0] * (varFloat + 1), 'bool': [False] * (varBool + 1), 'string': [''] * (varString + 1)},
            'constants': {'int': [0] * (constInt + 1), 'float': [0.0] * (constFloat + 1), 'bool': [False] * (constBool + 1) , 'string': [''] * (constString + 1)}
        }

        for type, dictValue in constTable.items():
            for item, dir in dictValue.items():
                self.constDir(dir, item)

    def constDir(self, dir, item):
        # FUncion para agregar una constante en una direccion virtual
        tableScope, dataType, index = self.tableKeys(dir)
        item = self.TT.cast(item, dataType)
        self.table[tableScope][dataType][index] = item

    def setValorDir(self, dir, item):
        # Funcion para agregar un valor en una direccion virtual
        tableScope, dataType, index = self.tableKeys(dir)
        while(len(self.table[tableScope][dataType]) < index + 1):
            self.table[tableScope][dataType].append(0)
        self.table[tableScope][dataType][index] = item

    def getItem(self, dir):
        # Funcion que regresa el valor y su tipo de dato
        tableScope, dataType, index = self.tableKeys(dir)
        item  = self.table[tableScope][dataType][index]
        return (dataType, item)

    def tableKeys(self, dir):
        # Funcion que regresa las llaves del diccionario para una direccion virtual
        scopeKey = self.scopeKey(dir)
        if scopeKey == 'vars':
            dir = dir - 0
        else:
            dir = dir - 24000
        dataType, index = self.dataType(dir)
        return (scopeKey, dataType, index)
    
    def scopeKey(self, dir):
        # Funcion para la llave de diccionario de un tipo de dato para una direccion
        if dir >= 0 and dir < 8000:
            return 'vars'
        else:
            return 'constants'

    def dataType(self, dir):
        # Funcion que regresa el tipo de dato para una direccion
        dataType = 0
        if dir >= 0 and dir < 2000:
            dataType = 'int'
            dir = dir - 0
        elif dir >= 2000 and dir < 4000:
            dataType = 'float'
            dir = dir - 2000
        elif dir >= 4000 and dir < 6000:
            dataType = 'bool'
            dir = dir - 4000
        else:
            dataType = 'string'
            dir = dir - 6000
        return (dataType, dir)
    
class LocalMemory:
    def __init__(self, varSize, tempSize):
        varInt, varFloat, varBool, varString = varSize
        tempInt, tempFloat, tempBool, tempString = tempSize

        self.table = {
            'vars': {'int': [0] * (varInt + 1), 'float': [0.0] * (varFloat + 1), 'bool': [False] * (varBool + 1), 'string': [''] * (varString + 1)},
            'temps': {'int': [0] * (tempInt + 1), 'float': [0.0] * (tempFloat + 1), 'bool': [False] * (tempBool + 1), 'string': [''] * (tempString + 1)}
        }

    def scopeKey(self, dir):
        if dir >= 8000 and dir < 16000:
            return 'locals'
        elif dir >= 16000 and dir < 24000:
            return 'temps'
        
    def dataType(self, dir):
        if dir >= 0 and dir < 2000:
            return ('int', 0)
        elif dir >= 2000 and dir < 4000:
            return ('float', 2000)
        elif dir >= 4000 and dir < 6000:
            return ('bool', 4000)
        elif dir >= 6000:
            return ('string', 6000)
    
    def tableKeys(self, dir):
        scopeKey = self.scopeKey(dir)
        if not scopeKey:
            return (None, None, None)
        tableScope = None
        dataType = None

        if scopeKey == 'temps':
            tableScope = 'temps'
            dir = dir - 16000
        else:
            tableScope = 'vars'
            dir = dir - 8000
        
        dataType, offSet = self.dataType(dir)

        return (tableScope, dataType, (dir - offSet))

    def setValorDir(self, dir, valor):
        tableScope, dataType, index = self.tableKeys(dir)
        if not tableScope:
            return None
        while(len(self.table[tableScope][dataType]) < index + 1):
            self.table[tableScope][dataType].append(0)
        self.table[tableScope][dataType][index] = valor

    def getItem(self, dir):
        tableScope, dataType, index = self.tableKeys(dir)
        if not tableScope:
            return (None, None)
        else:
            return (dataType, self.table[tableScope][dataType][index])