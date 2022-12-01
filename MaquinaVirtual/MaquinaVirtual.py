from adminObj import *
from MemoriaVirtual import * 
from TypeTranslate import *

TT = Translator()
obj = adminObj()

varWorkSpace = obj.varWorkspace('#global', '#global')
constSum = obj.constSum()

globalVarWorkSpace = (varWorkSpace['int'], varWorkSpace['float'], varWorkSpace['bool'], varWorkSpace['string'])
constWorkspace = (constSum['int'], constSum['float'], constSum['bool'], constSum['string'])

constTable = obj.constTable()

globalMemory = GlobalMemory(globalVarWorkSpace, constWorkspace, constTable)

cuads = obj.cuads

instructionPtr = 0
instructionPtrStack = []
memStack = []
futureMemory = []

def globalValueType(dir):
    type, value = globalMemory.getItem(dir)
    if not type:
        print('Not found')
        return(None, None)
    return(type, value)

def valueType(local_memory, dir):
    # Obtiene el tipo de dato y valor a partir de la direccion
    type, value = local_memory.getItem(dir)
    if not type:
        return globalValueType(dir)
    return (type, value)

def memoryScope(dir):
    if dir >= 8000 and dir < 24000:
        return 'local_memory'
    return 'global_memory'

def biOperands(memLocal, dirOpIzq, dirOpDer):
    # Convierte los valores recibidos por su tipo
    tipoOpIzq, valorOpIzq = valueType(memLocal, dirOpIzq)
    if not tipoOpIzq:
        raise Exception('Flop de direccionamiento de operador izquierdo')
    opIzq = TT.cast(valorOpIzq, tipoOpIzq)
    tipoOpDer, valorOpDer = valueType(memLocal, dirOpDer)
    if not tipoOpDer:
        raise Exception('Flop de direccionamiento de operador derecho')
    opDer = TT.cast(valorOpDer, tipoOpDer)
    return (opIzq, opDer)

def valorMemoria(dir, mem_local, valor):
    memScope = memoryScope(dir)
    if memScope == 'local_memory':
        mem_local.setValorDir(dir, valor)
    else:
        globalMemory.setValorDir(dir, valor)
    return mem_local

print("---------------------FLOP++---------------------")

while(instructionPtr < len(cuads)):
    currCuad = cuads[instructionPtr].copy()
    if len(memStack) > 100000:
        raise Exception('Stack OverFlop, demasiadas llamadas creadas')

    if currCuad[0] == 'GoToMain':
        # Obtenemos los workspaces del JSON (canitdades de cada tipo de dato)
        mainVarWorkSpace = obj.varWorkspace('#global', 'main')
        mainTempWorkspace = obj.tempWorkspace('#global', 'main')
        # Creamos un workspace para cada tipo de dato
        mainVarWorkSpaceType = (mainVarWorkSpace['int'], mainVarWorkSpace['float'], mainVarWorkSpace['bool'], mainVarWorkSpace['string'])
        mainTempWorkSpaceType = (mainTempWorkspace['int'], mainTempWorkspace['float'], mainTempWorkspace['bool'], mainTempWorkspace['string'])
        # Creamos un objeto con las cantidades de variables y temporales
        mainMem = LocalMemory(mainVarWorkSpaceType, mainTempWorkSpaceType)
        memStack.append(mainMem)
        instructionPtr = currCuad[3]
        continue

    elif currCuad[0] == '=':
        assignType, assignValue = None, None
        # Obtenemos el valor a asignar y su tipo
        assignType, assignValue = valueType(memStack[-1], currCuad[1])
        # Convertimos el valor de string a su tipo de dato
        assignValue = TT.cast(assignValue, assignType)
        # Actualizamos el objeto con el valor ubicado en la direccion
        memStack[-1] = valorMemoria(currCuad[3], memStack[-1], assignValue)
        

    elif currCuad[0] == '+':
        opIzq, opDer = None, None
        # Convierte los valores recibidos por su tipo
        opIzq, opDer = biOperands(memStack[-1], currCuad[1], currCuad[2])
        # Realizamos la operacion
        sum = opIzq + opDer
        memStack[-1] = valorMemoria(currCuad[3], memStack[-1], sum)

    elif currCuad[0] == '-':
        opIzq, opDer = None, None
        opIzq, opDer = biOperands(memStack[-1], currCuad[1], currCuad[2])
        sub = opIzq - opDer
        memStack[-1] = valorMemoria(currCuad[3], memStack[-1], sub)

    elif currCuad[0] == '*':
        opIzq, opDer = None, None
        opIzq, opDer = biOperands(memStack[-1], currCuad[1], currCuad[2])
        mult = opIzq * opDer
        memStack[-1] = valorMemoria(currCuad[3], memStack[-1], mult)

    elif currCuad[0] == '/':
        opIzq, opDer = None, None
        opIzq, opDer = biOperands(memStack[-1], currCuad[1], currCuad[2])
        div = opIzq / opDer
        memStack[-1] = valorMemoria(currCuad[3], memStack[-1], div)

    elif currCuad[0] == '>':
        opIzq, opDer = None, None
        opIzq, opDer = biOperands(memStack[-1], currCuad[1], currCuad[2])
        greater_than = opIzq > opDer
        memStack[-1] = valorMemoria(currCuad[3], memStack[-1], greater_than)
    
    elif currCuad[0] == '<':
        opIzq, opDer = None, None
        opIzq, opDer = biOperands(memStack[-1], currCuad[1], currCuad[2])
        less_than = opIzq < opDer
        memStack[-1] = valorMemoria(currCuad[3], memStack[-1], less_than)

    elif currCuad[0] == '==':
        opIzq, opDer = None, None
        opIzq, opDer = biOperands(memStack[-1], currCuad[1], currCuad[2])
        equal = opIzq == opDer
        memStack[-1] = valorMemoria(currCuad[3], memStack[-1], equal)

    elif currCuad[0] == '!=':
        opIzq, opDer = None, None
        opIzq, opDer = biOperands(memStack[-1], currCuad[1], currCuad[2])
        Not = opIzq != opDer
        memStack[-1] = valorMemoria(currCuad[3], memStack[-1], Not)

    elif currCuad[0] == '&&':
        opIzq, opDer = None, None
        opIzq, opDer = biOperands(memStack[-1], currCuad[1], currCuad[2])
        if opIzq and opIzq == True:
            And = True
        else:
            And =  False
        memStack[-1] = valorMemoria(currCuad[3], memStack[-1], And)

    elif currCuad[0] == '||':
        opIzq, opDer = None, None
        opIzq, opDer = biOperands(memStack[-1], currCuad[1], currCuad[2])
        if opIzq or opIzq == True:
            Or = True
        else:
            Or =  False
        memStack[-1] = valorMemoria(currCuad[3], memStack[-1], Or)

    elif currCuad[0] == 'WRITE':
        write_type, write_value = None, None
        write_type, write_value = valueType(memStack[-1], currCuad[3])
        # Imprimimos el valor
        print(write_value)

    elif currCuad[0] == 'READ':
        readType, readValue = None, None
        readType, readValue = valueType(memStack[-1], currCuad[3])
        # Recibimos como entrada el valor a asignar
        readValue = input()
        # Verificamos que tipo de dato es
        if readType == 'int':
            try:
                readValue = int(readValue)
                # Guardamos el valor en la memoria
                valorMemoria(currCuad[3], memStack[-1], readValue)
            except Exception:
                raise Exception("Flop de tipos, se esperaba " + readType)
        elif readType == 'float':
            try:
                if '.' not in readValue:
                    raise Exception('Flop de tipos se esperaba un . ' + readType)
                readValue = float(readValue)
                valorMemoria(currCuad[3], memStack[-1], readValue)
            except Exception:
                raise Exception("Flop de tipos, se esperaba " + readType)
        elif readType == 'bool':
            if readValue == 'true' or readValue == 'false':
                readValue = readValue == 'true'
                valorMemoria(currCuad[3], memStack[-1], readValue)
            else:
                raise Exception("Flop de entrada se esperaba un tipo " + readType)
        elif readType == 'string':
            valorMemoria(currCuad[3], memStack[-1], readValue)

    elif currCuad[0] == 'GoTo':
        instructionPtr = currCuad[3]
        continue

    elif currCuad[0] == 'GoToF':
        valorCond = None
        _, valorCond = valueType(memStack[-1], currCuad[1])
        if not valorCond:
            instructionPtr = currCuad[3]
            continue

    elif currCuad[0] == 'VER':
        dimSize = currCuad[1]
        indexType, indexValue = None, None
        indexType, indexValue = valueType(memStack[-1], currCuad[2])
        if indexValue < 0 and indexValue >= dimSize:
            raise Exception('Flop por tratar de acceder fuera de rangos!')

    elif currCuad[0] == 'GoSub':
        funcName = currCuad[1]
        funcStartCuad = currCuad[3]
        exeNewMem = futureMemory.pop()
        memStack.append(exeNewMem[0])
        instructionPtrStack.append(instructionPtr)
        instructionPtr = funcStartCuad
        continue            

    elif currCuad[0] == 'ERA':
        funcName = currCuad[3]
        funcVarWorkspace = obj.varWorkspace('#global', funcName)
        funcTempWorkspace = obj.tempWorkspace('#global', funcName)
        function_variable_workspace = (funcVarWorkspace['int'], funcVarWorkspace['float'], funcVarWorkspace['bool'], funcVarWorkspace['string'])
        function_temps_workspace = (funcTempWorkspace['int'], funcTempWorkspace['float'], funcTempWorkspace['bool'], funcTempWorkspace['string'])
        function_memory = LocalMemory(function_variable_workspace, function_temps_workspace)
        futureMemory.append([function_memory, {'int': 8000, 'float': 10000, 'bool': 12000, 'string': 14000}])

    elif currCuad[0] == 'PARAM':
        param_address = currCuad[1]
        param_index = currCuad[3]
        param_type, param_value = None, None
        param_type, param_value = valueType(memStack[-1], param_address)
        new_param_address = futureMemory[-1][1][param_type]
        futureMemory[-1][0].setValorDir(new_param_address, param_value)
        futureMemory[-1][1][param_type] += 1

    elif currCuad[0] == 'EndFunc':
        memStack.pop()
        instructionPtr = instructionPtrStack.pop()
        
    instructionPtr = instructionPtr + 1

print("---------------------Programa FLOP++ ejecutado sin Flopear!---------------------")