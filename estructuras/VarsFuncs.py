class Variable:
    def __init__(self, varName, varType, varScope):
        self.__varName = varName
        self.__varType = varType
        self.__varValue = None
        self.__varSize = None
        self.__varScope = varScope

    def name(self):
        return self.__varName

    def type(self):
        return self.__varType

    def value(self):
        return self.__varValue

    def size(self):
        return self.__varSize

    def scope(self):
        return self.__varScope

class Function:
    def __init__(self, funcName, funcType, parameters=[]):
        self.__funcName = funcName
        self.__funcType = funcType
        self.__funcParameters = parameters

    def name(self):
        return self.__funcName

    def type(self):
        return self.__funcType

    def parameters(self):
        return self.__funcParameters