import ply.yacc as yacc
import os
import codecs
import re
from AnalizadorLex import tokens
from estructuras.VarsFuncs import *
from estructuras.Stack import *
from estructuras.Cuadruplos import *
from estructuras.CuboSemantico import *
from estructuras.Memoria import *
import json
from sys import stdin

varTable = []
vars_table = {}
constTable = []
funcTable = []
quadList = []
operatorStack = []
operandStack = []
jumpStack = []
paramTable = []
controlTable = []
constructors  = []
dim_stack = []
semantic_cube = Cubo()
cuads = Cuadruplos()
func_dir = None


precedence = (
    ('right', 'EQUAL_ASSIGN'),
    ('left', 'ID'),
    ('left', 'LEFT_CURLYB', 'RIGHT_CURLYB'),
    ('left', 'LEFT_BRACKET', 'RIGHT_BRACKET'),
    ('left', 'LESS_THAN', 'GREATER_THAN', 'NOT_EQUAL', 'LESS_EQUAL', 'GREATER_EQUAL', 'EQUAL_COMPARE'),
    ('left', 'AND', 'OR', 'NEGATION'),
    ('left', 'MINUS', 'PLUS'),
    ('left', 'MULTIPLICATION', 'DIVISION'),
    ('left', 'LEFT_PARENTHESIS', 'RIGHT_PARENTHESIS'),
)

def p_program(p):
    ''' program : PROGRAM pn_start_program pn_start_func ID SEMICOLON init_dec main '''
    funcTable.append(Function1(p[2], "program"))

    constTable = memo.cont_info('constants')
    func_dir.genVarInfo('#global', '#global', vars_table)
    
    # Generar JSON a partir de toda la informacion que se guardo (variables, direcciones, temporales...)
    obj = {"function_directory": func_dir.table, "quads": cuads.list, "constants_summary": constTable, "constants_table": const.table, "global_objects_constructors_start_quads": constructors}
    with open('obj.json', "w") as output_file:
        json.dump(obj, output_file, indent = 2)

def p_main(p):
    ''' main : MAIN pn_internal_scope LEFT_PARENTHESIS RIGHT_PARENTHESIS LEFT_CURLYB vars_rec pn_gen_vartable bloque_rec RIGHT_CURLYB pn_end_main'''
    global curr_intScope
    curr_intScope = '#global'
    memo.resetLocalMem()

def p_vars_rec(p):
    ''' vars_rec : var_dec vars_rec
                    | empty '''

def p_pn_internal_scope(p):
    ''' pn_internal_scope : empty '''
    global curr_intScope
    curr_intScope = 'main'
    func_dir.intScope(curr_genScope, curr_intScope)
    cuads.fill_quad(0, 3, cuads.counter)

def p_pn_start_program(p):
    ''' pn_start_program : empty '''
    global func_dir, curr_listIntScope, curr_funcCallStack, funcParamCountStack
    global memo, const, funcParamCount
    funcParamCount = None
    curr_listIntScope = None
    memo = MemoriaVirtual()
    func_dir = Function()
    const = Constant()
    cuads.gen_cuad('GoToMain', None, None, None)
    curr_funcCallStack = []
    funcParamCountStack = []

def p_pn_start_func(p):
    ''' pn_start_func : empty '''
    global curr_genScope, curr_intScope
    curr_genScope = '#global'
    curr_intScope = '#global'
    func_dir.genScope(curr_genScope)
    func_dir.intScope(curr_genScope, curr_intScope)
    func_dir.tipoFunc(curr_genScope, curr_intScope, 'void')

def p_init_dec(p):
    ''' init_dec : empty 
                | dec init_dec '''

def p_dec(p):
    ''' dec :  var_dec 
            | func_dec 
            | class_dec '''

def p_class_dec(p):
    ''' class_dec : empty'''

def p_var(p):
    ''' var : ID varArray'''
    p[0] = p[1]

def p_varArray(p):
    ''' varArray :  empty 
                | pn_array_access1 LEFT_BRACKET pn_array_access2 all_logical pn_array_access3 RIGHT_BRACKET pn_access_return '''

def p_pn_array_access1(p):
    ''' pn_array_access1 : empty '''
    global current_name, curr_listIntScope
    # for varName in vars_table.keys():
    #     if 'group_size' in vars_table[varName]:
    #         func_dir.table['#global']['#global']['vars_table'][varName] = {'var_type': vars_table[varName]['var_type'], 'var_data_type': vars_table[varName]['var_data_type'], 'var_virtual_address': vars_table[varName]['var_virtual_address'], 'dim_list': vars_table[varName]['dim_list'], 'r': vars_table[varName]['r']}
    #     else:
    #         func_dir.table['#global']['#global']['vars_table'][varName] = {'var_type': vars_table[varName]['var_type'], 'var_data_type': vars_table[varName]['var_data_type'], 'var_virtual_address': vars_table[varName]['var_virtual_address']}
    if (func_dir.varExistsInScope(curr_genScope, curr_intScope, p[-1])):
        varMap = func_dir.table[curr_genScope][curr_intScope]['vars_table'][p[-1]]
        varDir, varType = varMap['var_virtual_address'], varMap['var_data_type']
        curr_listIntScope = curr_intScope
    elif (func_dir.varExistsInScope('#global', '#global', p[-1])):
        varMap = func_dir.table['#global']['#global']['vars_table'][p[-1]]
        varDir, varType = varMap['var_virtual_address'], varMap['var_data_type']
        curr_listIntScope = '#global'
    else: 
        Exception("Flop de variable " + p[-1] + ", esta no fue definida!")
    current_name = p[-1]
    operandStack.append((varDir, varType))
    

def p_pn_array_access2(p):
    ''' pn_array_access2 : empty '''
    listDir, _ = operandStack.pop()
    listDim = None
    if (func_dir.varExistsInScope(curr_genScope, curr_intScope, current_name)):
        listDim = func_dir.get_group_dimensions(curr_genScope, curr_intScope, current_name)
    elif (func_dir.varExistsInScope('#global', '#global', current_name)):
        listDim = func_dir.get_group_dimensions('#global', '#global', current_name)

    if listDim > 0:
        dim = [listDir, 1, curr_listIntScope, current_name]
        dim_stack.append(dim)
        operatorStack.append('[')
    else: 
        Exception('Flop de arreglo ' + current_name + ', no tiene dimensiones!')
        

def p_pn_array_access3(p):
    ''' pn_array_access3 : empty '''
    if (func_dir.varExistsInScope(curr_genScope, curr_intScope, current_name)):
        general_scope = curr_genScope
    else:
        general_scope = '#global'
    dimSize = func_dir.dimSize(general_scope, dim_stack[-1][2], dim_stack[-1][3], dim_stack[-1][1])
    index = operandStack[-1][0]

    cuads.gen_cuad('VER', dimSize, index, None)

    auxDir, auxType = operandStack.pop()
    if auxType != 'int':
        raise Exception('Flop de indexamiento por variable ' + dim_stack[-1][3] + ' por su tipo ' + auxType)
    else:
        dimM = func_dir.dimM(general_scope, dim_stack[-1][2], dim_stack[-1][3], dim_stack[-1][1])
        dir = const.const_address('int', str(int(dimM)))
        tempDir = memo.nueva_dir('int', 'temps')
        cuads.gen_cuad('*', auxDir, dir, tempDir)
        operandStack.append((tempDir, 'int'))

def p_pn_access_return(p):
    ''' pn_access_return : empty '''
    if (func_dir.varExistsInScope(curr_genScope, dim_stack[-1][2], dim_stack[-1][3])):
        general_scope = curr_genScope
    else:
        general_scope = '#global'
    auxDir1, _ = operandStack.pop()
    listDir = func_dir.varDir(general_scope, dim_stack[-1][2], dim_stack[-1][3])
    listType = func_dir.varType(general_scope, dim_stack[-1][2], dim_stack[-1][3])
    newDir = None
    if not const.const_exists('int', str(listDir)):
        newDir = memo.nueva_dir('int', 'constants')
        const.add_const('int', newDir, str(listDir))
    else:
        newDir = const.const_address('int', str(listDir))
    tempDir = memo.nueva_dir('int', 'temps')
    cuads.gen_cuad('+', auxDir1, newDir, tempDir)
    pointerDir = '&' + str(tempDir)
    dim_stack.pop()
    operatorStack.pop()
    p[0] = (pointerDir, listType)

def p_var_dec(p):
    ''' var_dec :  VAR tipo pn_var_type  pn_value_type ID pn_current_name SEMICOLON pn_add_variable 
                | LIST tipo pn_var_type  pn_value_type ID pn_current_name LEFT_BRACKET  cte_int pn_add_variable pn_add_dim_list pn_add_dim RIGHT_BRACKET list1 SEMICOLON'''

def p_list1(p):
    ''' list1 : empty '''
    func_dir.genDimMs(curr_genScope, curr_intScope, current_name)
    if (curr_genScope == '#global'):
        listScope = 'globals'
    else:
        listScope ='locals'

    size = func_dir.groupSize(curr_genScope, curr_intScope, current_name)
    memo.getListDir(var_type, listScope, size - 1)

def p_pn_add_dim_list(p):
    ''' pn_add_dim_list : empty'''
    func_dir.add_dim1_list(curr_genScope, curr_intScope, vars_table, current_name)
    vars_table[current_name]['dim_list'] = [{'dim': 1, 'size': None}]
    vars_table[current_name]['r'] = 1
    
def p_pn_add_dim(p):
    ''' pn_add_dim : empty'''
    size, _ = p[-3]
    size = int(size)
    func_dir.editSizeAndR(curr_genScope, curr_intScope, current_name, 0, size)

    if not const.const_exists('int', p[-3][0]):
        const_dir = memo.nueva_dir('int', 'constants')
        const.add_const('int', const_dir, p[-3][0])

def p_pn_var_type(p):
    ''' pn_var_type : empty '''
    global var_type 
    var_type = p[-1]

def p_pn_value_type(p):
    ''' pn_value_type : empty '''
    global value_type
    value_type = p[-3]

def p_pn_current_name(p):
    ''' pn_current_name : empty '''
    global current_name
    current_name = p[-1]

def p_pn_add_variable(p):
    ''' pn_add_variable : empty '''
    if(curr_intScope == '#global'):
        var_dir = memo.nueva_dir(var_type, 'globals')
    else:
        var_dir = memo.nueva_dir(var_type, 'locals')
    if p[-7] == 'var':
        vars_table[p[-3]] = {'var_type': p[-7], 'var_data_type': var_type, 'var_virtual_address': var_dir, 'general_scope': '#global', 'internal_scope': '#global'}
        varTable.append(Variable(current_name, var_type, var_dir ))
        func_dir.addVar(curr_genScope, curr_intScope, current_name, value_type, var_type, var_dir)
    else:
        size, _ = p[-1]
        size = int(size)
        vars_table[p[-4]] = {'var_type': value_type, 'var_data_type': var_type, 'var_virtual_address': var_dir, 'group_size': size, 'general_scope': '#global', 'internal_scope': '#global'}
        varTable.append(Variable(current_name, var_type, var_dir ))
        func_dir.addVar(curr_genScope, curr_intScope, current_name, value_type, var_type, var_dir)

def p_bloque(p):
    ''' bloque : asignacion 
                | condicional 
                | while 
                | read 
                | write 
                | func_call SEMICOLON '''

def p_asignacion(p):
    ''' asignacion : var pn_var_assign EQUAL_ASSIGN all_logical SEMICOLON '''
    variable_exists = False

    for x in varTable:
        if x.name() == p[1]:
            variable_exists = True
            all_logical_value, all_logical_type = operandStack.pop()
            result_type = semantic_cube.type_match(x.type(), all_logical_type, '=')
            if(result_type):
                cuads.gen_cuad('=', all_logical_value, None, x.varDir() )
            else:
                Exception("Flop de asignacion entre " + x.type() + " and " + all_logical_type + " en linea " + str(p.lineno(3) - 10))
            break

    if (variable_exists == False):
        Exception("La variable " + p[1] + " no existe FLOP!")

def p_pn_var_asignacion(p):
    ''' pn_var_assign : empty '''

def p_pn_operator(p):
    ''' pn_operator : empty '''
    operatorStack.append(p[-1])

def p_all_logical(p):
    ''' all_logical : logical_exp pn_all_logical all_logical_rec '''
    p[0] = p[1]

def p_all_logical_rec(p):
    ''' all_logical_rec : AND pn_operator logical_exp pn_all_logical all_logical_rec 
                        | OR pn_operator logical_exp pn_all_logical all_logical_rec 
                        | empty'''

def p_pn_all_logical(p):
    ''' pn_all_logical : empty '''
    exp_cuad(['&&', '||'], p.lineno(1))

def p_logical_exp(p):
    ''' logical_exp : exp pn_logical_exp logical_exp_rec '''
    p[0] = p[1]

def p_logical_exp_rec(p):
    ''' logical_exp_rec : GREATER_THAN pn_operator exp pn_logical_exp logical_exp_rec 
                        | LESS_THAN pn_operator exp pn_logical_exp logical_exp_rec 
                        | EQUAL_COMPARE pn_operator exp pn_logical_exp logical_exp_rec 
                        | NOT_EQUAL pn_operator exp pn_logical_exp logical_exp_rec 
                        | empty'''

def p_pn_logical_exp(p):
    ''' pn_logical_exp : empty '''
    exp_cuad(['>', '<', '==', '!='], p.lineno(1))

def p_exp(p):
    ''' exp : termino pn_exp exp_rec '''
    p[0] = p[1]

def p_pn_exp(p):
    ''' pn_exp : empty '''
    exp_cuad(['+', '-'], p.lineno(1))

def p_exp_rec(p):
    ''' exp_rec : PLUS pn_operator termino pn_exp exp_rec 
                | MINUS pn_operator termino pn_exp exp_rec 
                | empty'''

def p_termino(p):
    ''' termino :  factor pn_termino termino_rec '''
    p[0] = p[1]

def p_termino_rec(p):
    ''' termino_rec : MULTIPLICATION pn_operator factor pn_termino termino_rec 
                    | DIVISION pn_operator factor pn_termino termino_rec 
                    | empty'''

def p_pn_termino(p):
    ''' pn_termino : empty '''
    exp_cuad(['*', '/'], p.lineno(1))

def p_factor(p):
    ''' factor : varcte 
                | LEFT_PARENTHESIS pn_open_parenthesis all_logical  RIGHT_PARENTHESIS pn_close_parenthesis 
                | func_call empty'''
    p[0] = p[1]
    if len(p) == 3:
        temp = p[1]
        operandStack.append(temp)
    
def p_varcte(p):
    ''' varcte : cte_int pn_add_constant 
                | cte_float pn_add_constant 
                | CONST_BOOL pn_add_constant 
                | CONST_STRING empty empty
                | var '''
    if len(p) == 3:
        _, constType = p[1]
        temp = (p[2], constType)
        operandStack.append(temp)
    elif len(p) == 2:
        p[0] = p[1]
        temp = p[1]
        for x in varTable:
            if x.name() == temp:
                temp = ([x.varDir(), x.type()])
                operandStack.append(temp)

def p_cte_int(p):
    ''' cte_int : CONST_INT 
                | MINUS CONST_INT '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('-' + p[2][0], p[2][1])

def p_cte_float(p):
    ''' cte_float : CONST_FLOAT 
                | MINUS CONST_FLOAT '''    
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('-' + p[2][0], p[2][1])

def p_pn_add_constant(p):
    ''' pn_add_constant : empty '''   
    constValue, constType = p[-1]
    # Agrega la direccion de constante constante junto a su tipo
    if not const.const_exists(constType, constValue):
        const_dir = memo.nueva_dir(constType, 'constants')
        const.add_const(constType, const_dir, constValue)
    
    p[0] = const.const_address(constType, constValue)


def p_pn_open_parenthesis(p):
    ''' pn_open_parenthesis : empty ''' 
    operatorStack.append('(')

def p_pn_close_parenthesis(p):
    ''' pn_close_parenthesis : empty '''
    operatorStack.pop()

def p_tipo(p):
    ''' tipo : INT 
            | FLOAT 
            | BOOL 
            | STRING '''
    p[0] = p[1]

def p_return_module(p):
    ''' return_module : tipo 
                | VOID '''
    p[0] = p[1]

def p_parametro(p):
    ''' parametro : tipo ID parametro_rec 
                    | empty '''
    if len(p) == 4:
        p[0] = [(p[1], p[2])] + p[3]
    else:
        p[0] = []

def p_parametro_rec(p):
    ''' parametro_rec : COMMA tipo ID parametro_rec 
                        | empty '''
    if len(p) == 5:
        p[0] = [(p[2], p[3])] + p[4]
    else:
        p[0] = []
            
def p_condicional(p):
    ''' condicional : IF LEFT_PARENTHESIS all_logical RIGHT_PARENTHESIS pn_condicional LEFT_CURLYB bloque_rec RIGHT_CURLYB condicional_else '''

def p_condicional_else(p):
    ''' condicional_else : ELSE pn_condicional_else LEFT_CURLYB bloque_rec RIGHT_CURLYB pn_condicional_final 
                        | pn_condicional_final '''

def p_pn_condicional(p):
    ''' pn_condicional : empty '''
    direccion, tipo = operandStack.pop()
    if tipo == 'bool':
        cuads.gen_cuad('GoToF', direccion, None, None)
        jumpStack.append(cuads.counter - 1)
    else:
        Exception("Flop de condicion por expresion recibida " + tipo + " en linea " + str(p.lineno(1)))

def p_pn_condicional_else(p):
    ''' pn_condicional_else : empty '''
    cuads.gen_cuad('GoTo', None, None, None)
    id_cuad_falso = jumpStack.pop()
    jumpStack.append(cuads.counter - 1)
    cuads.fill_quad(id_cuad_falso, 3, cuads.counter)

def p_pn_condicional_final(p):
    ''' pn_condicional_final : empty '''
    if_final = jumpStack.pop()
    cuads.fill_quad(if_final, 3, cuads.counter)

def p_while(p):
    ''' while : WHILE pn_while LEFT_PARENTHESIS all_logical RIGHT_PARENTHESIS pn_while_jump while_loop'''

def p_while_loop(p):
    ''' while_loop : LEFT_CURLYB bloque_rec RIGHT_CURLYB pn_while_jump1 '''

def p_pn_while(p):
    ''' pn_while : empty '''
    jumpStack.append(cuads.counter)

def p_pn_while_jump(p):
    ''' pn_while_jump : empty '''

    direccion, tipo = operandStack.pop()
    if tipo == 'bool':
        cuads.gen_cuad('GoToF', direccion, None, None)
        jumpStack.append(cuads.counter - 1)
    else:
        Exception("Flop de condicion por expresion recibida " + tipo + " en linea " + str(p.lineno(1)))

def p_pn_while_jump1(p):
    ''' pn_while_jump1 : empty '''
    # Obtiene la direccion de la pila de saltos
    gotof_id = jumpStack.pop()
    cuad_return = jumpStack.pop()
    cuads.gen_cuad('GoTo', None, None, cuad_return)
    # Modifica el cuadruplo que fue generado sin un destion
    cuads.fill_quad(gotof_id, 3, cuads.counter)

def p_read(p):
    ''' read : READ LEFT_PARENTHESIS var RIGHT_PARENTHESIS SEMICOLON '''
    for var in p[3]:
        dir_var = var
        cuads.gen_cuad('READ', None, None, dir_var)

def p_write(p):
    ''' write : WRITE LEFT_PARENTHESIS write_rec RIGHT_PARENTHESIS SEMICOLON '''

def p_write_rec(p):
    ''' write_rec : all_logical pn_write_quad write_rec1 '''

def p_write_rec1(p):
    ''' write_rec1 : MORE all_logical pn_write_quad write_rec1 
                    | empty '''

def p_pn_write_quad(p):
    ''' pn_write_quad : empty '''
    # Obtenemos la direccion de la variable para pode desplegar
    operandDir, _ = operandStack.pop()
    for x in varTable:
        if x.varDir() == operandDir:
            cuads.gen_cuad('WRITE', None, None, x.varDir())
    
def p_func_call(p):
    ''' func_call : CALL ID pn_verify_func LEFT_PARENTHESIS pn_param_counter pn_open_parenthesis func_call_rec pn_close_parenthesis RIGHT_PARENTHESIS '''
    genName = None
    intName = None

    genName = '#global'
    intName = curr_funcCallStack[-1]
    lenFirmaParam = func_dir.lenFirmaParam(genName, intName)
    if lenFirmaParam != funcParamCountStack[-1]:
        raise Exception("Flop por cantidades de parametros ingresados, se recibieron " + str(funcParamCountStack[-1]) + " y se esperaban " + str(lenFirmaParam))
    else:
        funcStartCuad = func_dir.getCuadFuncInicial(genName, intName)
        cuads.gen_cuad('GoSub', intName, None, funcStartCuad)
        funcType = func_dir.getTipoFunc(genName, intName)
        if funcType != 'void':
            funcDir = func_dir.funcDir('#global', '#global', curr_funcCallStack[-1])
            nuevaDir, _ = memo.nuevo_temp(funcType)
            p[0] = (nuevaDir, funcType)
            cuads.gen_cuad('=', funcDir, None, nuevaDir)
    curr_funcCallStack.pop()
    funcParamCountStack.pop()


def p_pn_verify_func(p):
    ''' pn_verify_func : empty '''
    global currFuncCallName
    # Verificamos que la funcion exista
    curr_funcCallName = p[-1]
    curr_funcCallStack.append(curr_funcCallName)
    if not func_dir.internalScopeExists('#global', curr_funcCallStack[-1]):
        raise Exception("Flop de llamada a la funcion " + curr_funcCallStack[-1] + " no existe!")
    else:
        cuads.gen_cuad('ERA', None, None, curr_funcCallStack[-1])

def p_pn_param_counter(p):
    ''' pn_param_counter : empty '''
    funcParamCount = 0
    funcParamCountStack.append(funcParamCount)

def p_func_call_rec(p):
    ''' func_call_rec : all_logical pn_param_match func_call_rec1 '''

def p_func_call_rec1(p):
    ''' func_call_rec1 : COMMA all_logical pn_param_match func_call_rec1
                        | empty '''

def p_pn_param_match(p):
    ''' pn_param_match : empty '''
    global funcParamCountStack
    genName = None
    intName = None

    genName = '#global'
    intName = curr_funcCallStack[-1]

    paramDir, paramType = operandStack.pop()
    numTipoFirma = func_dir.numTipoFirma(genName, intName, funcParamCountStack[-1])
    if numTipoFirma != paramType:
        raise Exception("Flop por orden de tipos de parametros!")
    else:
        cuads.gen_cuad('PARAM', paramDir, None, funcParamCountStack[-1])
        # Agregar al contador de parametros
        funcParamCountStack[-1] += 1

def p_func_dec(p):
    ''' func_dec : FUNC return_module ID pn_add_func LEFT_PARENTHESIS parametro pn_add_param_vartable pn_return_type RIGHT_PARENTHESIS LEFT_CURLYB vars_rec pn_gen_vartable pn_func_quad bloque_rec func_return RIGHT_CURLYB pn_end_func '''
    global curr_intScope
    curr_intScope = '#global'
    memo.resetLocalMem()
    funcTable.append(Function1(p[4], p[2]))

def p_pn_add_param_vartable(p):
    ''' pn_add_param_vartable : empty '''
    parametros = p[-1]
    for parametro in parametros:
        paramType, paramName = parametro
        if (func_dir.varExistsInScope(curr_genScope, curr_intScope, paramName)):
            raise Exception("Flop de parametro llamado " + paramName + " ya fue declarado en la linea " + str(p.lineno(1) -10))
        else:
            paramDir = memo.nueva_dir(paramType, 'locals')
            func_dir.addVar(curr_genScope, curr_intScope, paramName, 'var', paramType, paramDir)
            func_dir.agregarFirma(curr_genScope, curr_intScope, paramType)

def p_pn_gen_vartable(p):
    ''' pn_gen_vartable : empty '''
    func_dir.genVarInfo(curr_genScope, curr_intScope, vars_table)

def p_pn_func_quad(p):
    ''' pn_func_quad : empty '''
    func_dir.cuadInicial(curr_genScope, curr_intScope, cuads.counter)

def p_pn_end_main(p):
    ''' pn_end_main : empty'''
    tempWorkSpace = memo.cont_info('temps')
    func_dir.tempInfo(curr_genScope, curr_intScope, tempWorkSpace)

def p_pn_end_func(p):
    ''' pn_end_func : empty '''
    # func_dir.table[curr_genScope][curr_intScope]['vars_table'] = {}
    cuads.gen_cuad('EndFunc', None, None, None)
    tempsInfo = memo.cont_info('temps')
    func_dir.tempInfo(curr_genScope, curr_intScope, tempsInfo)

def p_pn_add_func(p):
    ''' pn_add_func : empty '''
    global curr_intScope
    curr_intScope = p[-1]
    func_dir.intScope(curr_genScope, curr_intScope)

def p_pn_return_type(p):
    ''' pn_return_type : empty '''
    funcType = p[-6]
    func_dir.setFuncType(curr_genScope, curr_intScope, funcType)
    if funcType != 'void':
        nuevaDir = memo.nueva_dir(funcType, 'globals')
        func_dir.addVar('#global', '#global', curr_intScope, 'var', funcType, nuevaDir)

def p_func_return(p):
    ''' func_return : RETURN all_logical SEMICOLON 
                    | RETURN SEMICOLON '''
    funcType = func_dir.table[curr_genScope][curr_intScope]['function_type']
    if len(p) == 4:
        returnDir, returnType = operandStack.pop()
        if returnType != funcType:
            raise Exception("Flop de retorno de tipo de variable, se esperaba " + funcType + " y se recibio un tipo " + returnType)
        else:
            globalVarFuncName = None
            if curr_genScope == '#global':
                globalVarFuncName = curr_intScope
            else:
                globalVarFuncName = curr_genScope + '#' + curr_intScope
            funcDir = func_dir.funcDir('#global', '#global', globalVarFuncName)
            cuads.gen_cuad('=', returnDir, None, funcDir)
    else:
        if funcType != 'void':
            raise Exception("Flop de tipos de retorno, se esperaba un " + returnType)

def p_bloque_rec(p):
    ''' bloque_rec : bloque bloque_rec 
                    | empty'''


def p_empty(p):
    ''' empty :  '''
    pass

def p_error(p):
    print("Error de sintaxis" , p)
    Exception("Error en la linea " + str(p.lineno - 10))

def exp_cuad(op_list, line_no = 'Undefined'):
    if operatorStack and operatorStack[-1] in op_list:
        # Obtiene los valores y tipos de dato para los operandos izquierda y derecha
        valor_der, tipo_der = operandStack.pop()
        valor_izq, tipo_izq = operandStack.pop()
        # Obtiene el operador del stacke
        op = operatorStack.pop()
        # Verifica el operador y los operandos son compatibles
        result_type = semantic_cube.type_match(tipo_izq, tipo_der, op)
        # Si es compatible guardamos la direccion de la temporal 
        if result_type:
            temp_dir, temp_type = memo.nuevo_temp(result_type)
            cuads.gen_cuad(op, valor_izq, valor_der, temp_dir)
            operandStack.append((temp_dir, temp_type))
        else:
            Exception("Flop de operador " + op + " entre " + tipo_izq + " y " + tipo_der + " en linea " + str(line_no - 10))
 

def buscarFicheros(directorio):
    ficheros = []
    numArchivo = ''
    respuesta = False
    cont = 1

    for base, dirs, files in os.walk(directorio):
        ficheros.append(files)

    for file in files:
        print(str(cont) + ". " + file)   
        cont = cont + 1

    while respuesta == False:
        numArchivo = eval(input('\nNumero del Test: '))
        for file in files:
            if file == files[int(numArchivo)-1]:
                respuesta = True
                break
    
    print("Has escogido {} \n".format(files[int(numArchivo) - 1]))

    return files[int(numArchivo) - 1]

directorio = 'C:/Users/mauro/OneDrive/Documents/9no Semestre/Compiladores/ProyectoFinalOOP/test/'
archivo = buscarFicheros(directorio)
test = directorio + archivo
fp = codecs.open(test,"r","utf-8")
cadena = fp.read()
fp.close()

parser = yacc.yacc()
result = parser.parse(cadena)

print(result)