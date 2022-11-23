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

def valueType(dir):
    

def memoryScope(dir):
    if dir >= 8000 and dir < 24000:
        return 'local'
    return 'global'

# def biOperands(memLocal, dirOpIzq, dirOpDer):
#     tipoOpIzq, valorOpIzq = 

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
        mainTempWorkspaceType = (mainTempWorkspace['int'], mainTempWorkspace['float'], mainTempWorkspace['bool'], mainTempWorkspace['string'])
        instructionPtr = currCuad[3]

    elif currCuad[0] == '=':
        assignType, assignValue = None, None
        assignType, assignValue = 