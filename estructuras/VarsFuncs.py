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