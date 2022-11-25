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
    type, value = local_memory.valorDir(dir)
    if not type:
        return globalValueType(dir)
    return (type, value)

def memoryScope(dir):
    if dir >= 8000 and dir < 24000:
        return 'local'
    return 'global'

def biOperands(memLocal, dirOpIzq, dirOpDer):
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
        mem_local.getItem(dir, valor)
    else:
        globalMemory.getItem(dir, valor)
    return mem_local
    
    

# def resetCuadDir(current_quad, memory):
#     for i, element in enumerate(current_quad):
#         if element is not None and str(element)[0] == '&':
#             # make the check for && operand
#             if len(str(element)) > 1 and str(element)[1] == '&':
#                 continue
#             element = element[1:]
#             element = int(element)
#             _, new_address = get_type_and_value(memory, element)
#             current_quad[i] = new_address
#     return current_quad

print("---------------------FLOP++---------------------")

while(instructionPtr < len(cuads)):
    currCuad = cuads[instructionPtr].copy()
    if len(memStack) > 100000:
        raise Exception('Stack overFLop, demasiadas llamadas creadas')
    if currCuad[0] == 'GoToMain':
        mainVarWorkSpace = obj.varWorkspace('#global', 'main')
        mainTempWorkspace = obj.tempWorkspace('#global', 'main')
        mainVarWorkSpaceType = (mainVarWorkSpace['int'], mainVarWorkSpace['float'], mainVarWorkSpace['bool'], mainVarWorkSpace['string'])
        mainTempWorkSpaceType = (mainTempWorkspace['int'], mainTempWorkspace['float'], mainTempWorkspace['bool'], mainTempWorkspace['string'])
        mainMem = LocalMemory(mainVarWorkSpaceType, mainTempWorkSpaceType)
        memStack.append(mainMem)
        instructionPtr = currCuad[3]

    elif currCuad[0] == '=':
        assignType, assignValue = None, None
        assignType, assignValue = valueType(memStack[-1], currCuad[1])
        assignValue = TT.cast(assignValue, assignType)
        memStack[-1] = valorMemoria(currCuad[3], memStack[-1], assignValue)

    elif currCuad[0] == '+':
        opIzq, opDer = None, None
        opIzq, opDer = biOperands(memStack[-1], currCuad[1], currCuad[2])
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
        print(write_value)

    elif currCuad[0] == 'READ':
        readType, readValue = None, None
        readType, readValue = valueType(memStack[-1], currCuad[3])
        readValue = input()
        if readType == 'int':
            try:
                readValue = int(readValue)
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
        if valorCond == False:
            instructionPtr = currCuad[3]
            continue
    
    elif currCuad[0] == 'GoToV':
        valorCond = None
        _, valorCond = valueType(memStack[-1], currCuad[1])
        if valorCond == True:
            instructionPtr = currCuad[3]
            continue

    instructionPtr += 1

print("---------------------Programa Flop++ ejecutado sin Flopear!---------------------")