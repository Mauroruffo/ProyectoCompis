import ply.yacc as yacc
import os
import codecs
import re
from AnalizadorLex import tokens
from AnalizadorSemantico import *
from estructuras.VarsFuncs import *
from estructuras.Stack import *
from estructuras.Cuadruplos import *
from estructuras.CuboSemantico import *
from estructuras.Memoria import *
from sys import stdin

varTable = []
constTable = []
funcTable = []
quadList = []
operatorStack = []
operandStack = []
jumpStack = []
paramTable = []
controlTable = []
dim_stack = []
semantic_cube = Cubo()
cuads = Cuadruplos()
const = Constant()
memo = MemoriaVirtual()
func_dir = Function()


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


def p_main(p):
    ''' main : MAIN pn_internal_scope LEFT_PARENTHESIS RIGHT_PARENTHESIS LEFT_CURLYB vars_rec pn_gen_vartable pn_start_func bloque_rec RIGHT_CURLYB pn_end_main'''

def p_vars_rec(p):
    ''' vars_rec : var_dec vars_rec
                    | empty '''

def p_pn_internal_scope(p):
    ''' pn_internal_scope : empty '''

def p_pn_start_program(p):
    ''' pn_start_program : empty '''

def p_pn_start_func(p):
    ''' pn_start_func : empty '''
    global general_scope, internal_scope
    general_scope = '#global'
    internal_scope = '#global'
    func_dir.genScope(general_scope)
    func_dir.intScope(general_scope, internal_scope)
    func_dir.tipoFunc(general_scope, internal_scope, 'void')

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
                | pn_array_access1 LEFT_BRACKET pn_array_access2 all_logical pn_array_access3 RIGHT_BRACKET pn_access_return'''

def p_pn_array_access1(p):
    ''' pn_array_access1 : empty '''
    for x in varTable:
        if x.name() == p[-1]:
            varMap = func_dir.table['#global']['#global']['vars_table'][p[-1]]
            varDir, varType = varMap['var_virtual_address'], varMap['var_data_type']
            current_name = p[-1]
            operandStack.append((varDir, varType))
            # internal_scope = '#global'

    Exception("Flop de variable " + p[-1] + ", esta no fue definida!")

def p_pn_array_access2(p):
    ''' pn_array_access2 : empty '''
    listDir, _ = operandStack.pop()
    listDim = None
    if func_dir.varExists('#global', '#global', current_name):
        listDim = func_dir.get_group_dimensions('#global', '#global', current_name)

    if listDim > 0:
        dim = [listDir, 1, '#global', current_name]
        dim_stack.append(dim)
        operandStack.append('[')
    else: 
        Exception('Flop de arreglo ' + current_name + ', no tiene dimensiones!')
        

def p_pn_array_access3(p):
    ''' pn_array_access3 : empty '''
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
    auxDir1, _ = operandStack.pop()
    listDir = func_dir.varDir('#global', dim_stack[-1][2], dim_stack[-1][3])
    listType = func_dir.varType('#global', dim_stack[-1][2], dim_stack[-1][3])
    newDir = None
    if not const.const_exists('int', str(listDir)):
        newDir = memo.nueva_dir('int', 'constants')
        const.add_const('int', newDir, str(listDir))
    else:
        newDir = const.const_address('int', str(listDir))
    tempDir = memo.nueva_dir('int', str(listDir))
    cuads.gen_cuad('+', auxDir1, newDir, tempDir)
    pointerDir = '&' + str(tempDir)
    dim_stack.pop()
    operatorStack.pop()
    p[0] = (pointerDir, listType)

def p_var_dec(p):
    ''' var_dec :  VAR tipo pn_var_type  pn_value_type ID pn_current_name SEMICOLON pn_add_variable 
                | LIST tipo pn_var_type  pn_value_type ID pn_current_name pn_add_variable LEFT_BRACKET pn_add_dim_list cte_int pn_add_dim RIGHT_BRACKET SEMICOLON'''
    varTable.append(Variable(p[5], p[2]))
    
def p_pn_add_dim_list(p):
    ''' pn_add_dim_list : empty'''
    func_dir.add_dim1_list('#global', '#global', current_name)
    
def p_pn_add_dim(p):
    ''' pn_add_dim : empty'''
    size, _ = p[-1]
    size = int(size)
    func_dir.edit_dimSize('#global', '#global', current_name, 0, size)

    if not const.const_exists('int', p[-1][0]):
        const_dir = memo.nueva_dir('int', 'constants')
        const.add_const('int', const_dir, p[-1][0])

def p_pn_var_type(p):
    ''' pn_var_type : empty '''
    global var_type 
    var_type = p[-1]

def p_pn_value_type(p):
    ''' pn_value_type : empty '''
    global value_type
    value_type = p[-1]

def p_pn_current_name(p):
    ''' pn_current_name : empty '''
    global current_name
    current_name = p[-1]

def p_pn_add_variable(p):
    ''' pn_add_variable : empty '''
    var_dir = memo.nueva_dir(var_type, 'globals')
    func_dir.addVar('#global', '#global', current_name, var_type, value_type, var_dir)

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
                cuads.gen_cuad('=', all_logical_value, None, x.name() )
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
                | func_call '''
    p[0] = p[1]
    
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
                temp = ([x.name(), x.type()])
                print("La temp es:")
                print(temp)
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

    if not const.const_exists(constType, constValue):
        const_dir = memo.nueva_dir(constType, 'constants')
        const.add_const(constType, const_dir, constValue)
    
    p[0] = const.const_address(constType, constValue)


def p_pn_open_parenthesis(p):
    ''' pn_open_parenthesis : empty ''' 

def p_pn_close_parenthesis(p):
    ''' pn_close_parenthesis : empty '''

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

def p_pn_parametro_varTable(p):
    ''' pn_parametro_varTable : empty '''

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
    gotof_id = jumpStack.pop()
    cuad_return = jumpStack.pop()
    cuads.gen_cuad('GoTo', None, None, cuad_return)
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
    operandDir, _ = operandStack.pop()
    cuads.gen_cuad('WRITE', None, None, operandDir)

def p_func_call(p):
    ''' func_call : CALL ID pn_verify_func LEFT_PARENTHESIS pn_param_counter pn_open_parenthesis func_call_rec pn_close_parenthesis RIGHT_PARENTHESIS '''
    func_exists = False

    for x in funcTable:
        if x.name() == p[2]:
            func_exists = True
            break

    if (func_exists == False):
        Exception("La funcion " + p[2] + " no existe FLOP!")


def p_pn_verify_func(p):
    ''' pn_verify_func : empty '''

def p_pn_param_counter(p):
    ''' pn_param_counter : empty '''

def p_func_call_rec(p):
    ''' func_call_rec : all_logical pn_param_match func_call_rec1 '''

def p_func_call_rec1(p):
    ''' func_call_rec1 : COMMA all_logical pn_param_match func_call_rec
                        | empty '''

def p_pn_param_match(p):
    ''' pn_param_match : empty '''

def p_func_dec(p):
    ''' func_dec : FUNC return_module pn_return_type ID pn_add_func LEFT_PARENTHESIS parametro pn_add_param_vartable RIGHT_PARENTHESIS LEFT_CURLYB pn_gen_vartable pn_func_quad bloque_rec func_return RIGHT_CURLYB pn_end_func '''

    funcTable.append(Function1(p[4], p[2]))


def p_pn_add_param_vartable(p):
    ''' pn_add_param_vartable : empty '''
    parametros = p[-1]
    


def p_pn_gen_vartable(p):
    ''' pn_gen_vartable : empty '''

def p_pn_func_quad(p):
    ''' pn_func_quad : empty '''

def p_pn_end_main(p):
    ''' pn_end_main : empty'''

def p_pn_end_func(p):
    ''' pn_end_func : empty '''

def p_pn_add_func(p):
    ''' pn_add_func : empty '''

def p_pn_return_type(p):
    ''' pn_return_type : empty '''

def p_func_return(p):
    ''' func_return : RETURN all_logical SEMICOLON 
                    | RETURN SEMICOLON '''

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
        valor_der, tipo_der = operandStack.pop()
        valor_izq, tipo_izq = operandStack.pop()
        op = operatorStack.pop()
        result_type = semantic_cube.type_match(tipo_izq, tipo_der, op)
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