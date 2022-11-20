import ply.yacc as yacc
import os
import codecs
import re
from AnalizadorLex import tokens
from AnalizadorSemantico import *
from estructuras.VarsFuncs import *
from estructuras.stack import *
from estructuras.Cuadruplos import *
from estructuras.CuboSemantico import *
from sys import stdin

varTable = []
funcTable = []
quadList = []

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
    p[0] = program(p[1], p[2], p[3], "program")
    funcTable.append(Function(p[2], "program"))
    print("program")


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
    print(p[1])

def p_varArray(p):
    ''' varArray :  empty 
                | pn_array_access1 LEFT_BRACKET pn_array_access2 all_logical pn_array_access3 RIGHT_BRACKET '''

def p_pn_array_access1(p):
    ''' pn_array_access1 : empty '''

def p_pn_array_access2(p):
    ''' pn_array_access2 : empty '''

def p_pn_array_access3(p):
    ''' pn_array_access3 : empty '''

def p_var_dec(p):
    ''' var_dec :  VAR tipo pn_var_type pn_value_type ID pn_current_name SEMICOLON pn_add_variable '''
    varTable.append(Variable(p[5], p[2]))
    #print(len(varTable))

def p_pn_var_type(p):
    ''' pn_var_type : empty '''

def p_pn_value_type(p):
    ''' pn_value_type : empty '''

def p_pn_current_name(p):
    ''' pn_current_name : empty '''

def p_pn_add_variable(p):
    ''' pn_add_variable : empty '''

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
        print(x.name())
        if x.name() == p[1]:
            print("La variable " + p[1] + " si existe!")
            variable_exists = True
            break

    if (variable_exists == False):
        print("La variable " + p[1] + " no existe FLOP!")
        quit()

def p_pn_var_asignacion(p):
    ''' pn_var_assign : empty '''

def p_pn_operator(p):
    ''' pn_operator : empty '''

def p_all_logical(p):
    ''' all_logical : logical_exp pn_all_logical all_logical_rec '''

def p_all_logical_rec(p):
    ''' all_logical_rec : AND pn_operator logical_exp pn_all_logical all_logical_rec 
                        | OR pn_operator logical_exp pn_all_logical all_logical_rec 
                        | empty'''

def p_pn_all_logical(p):
    ''' pn_all_logical : empty '''

def p_logical_exp(p):
    ''' logical_exp : exp pn_logical_exp logical_exp_rec '''

def p_logical_exp_rec(p):
    ''' logical_exp_rec : GREATER_THAN pn_operator exp pn_logical_exp logical_exp_rec 
                        | LESS_THAN pn_operator exp pn_logical_exp logical_exp_rec 
                        | EQUAL_COMPARE pn_operator exp pn_logical_exp logical_exp_rec 
                        | NOT_EQUAL pn_operator exp pn_logical_exp logical_exp_rec 
                        | empty'''

def p_pn_logical_exp(p):
    ''' pn_logical_exp : empty '''

def p_exp(p):
    ''' exp : termino pn_exp exp_rec '''

def p_pn_exp(p):
    ''' pn_exp : empty '''

def p_exp_rec(p):
    ''' exp_rec : PLUS pn_operator termino pn_exp exp_rec 
                | MINUS pn_operator termino pn_exp exp_rec 
                | empty'''

def p_termino(p):
    ''' termino :  factor pn_termino termino_rec '''

def p_termino_rec(p):
    ''' termino_rec : MULTIPLICATION pn_operator factor pn_termino termino_rec 
                    | DIVISION pn_operator factor pn_termino termino_rec 
                    | empty'''

def p_pn_termino(p):
    ''' pn_termino : empty '''

def p_factor(p):
    ''' factor : varcte 
                | LEFT_PARENTHESIS pn_open_parenthesis all_logical  RIGHT_PARENTHESIS pn_close_parenthesis 
                | func_call '''

def p_varcte(p):
    ''' varcte : cte_int pn_add_constant 
                | cte_float pn_add_constant 
                | CONST_BOOL pn_add_constant 
                | CONST_STRING pn_add_constant 
                | var '''


def p_cte_int(p):
    ''' cte_int : CONST_INT 
                | MINUS CONST_INT '''

def p_cte_float(p):
    ''' cte_float : CONST_FLOAT 
                | MINUS CONST_FLOAT '''    

def p_pn_add_constant(p):
    ''' pn_add_constant : empty '''   

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

def p_parametro_rec(p):
    ''' parametro_rec : COMMA tipo ID parametro_rec 
                        | empty '''

def p_pn_parametro_varTable(p):
    ''' pn_parametro_varTable : empty '''

def p_condicional(p):
    ''' condicional : IF LEFT_PARENTHESIS all_logical RIGHT_PARENTHESIS pn_condicional LEFT_CURLYB bloque_rec RIGHT_CURLYB condicional_else '''

def p_condicional_else(p):
    ''' condicional_else : ELSE pn_condicional_else LEFT_CURLYB bloque_rec RIGHT_CURLYB pn_condicional_final 
                        | pn_condicional_final '''

def p_pn_condicional(p):
    ''' pn_condicional : empty '''

def p_pn_condicional_else(p):
    ''' pn_condicional_else : empty '''

def p_pn_condicional_final(p):
    ''' pn_condicional_final : empty '''

def p_while(p):
    ''' while : WHILE pn_while LEFT_PARENTHESIS all_logical RIGHT_PARENTHESIS pn_while_jump while_loop'''

def p_while_loop(p):
    ''' while_loop : LEFT_CURLYB bloque_rec RIGHT_CURLYB pn_while_jump1 '''

def p_pn_while(p):
    ''' pn_while : empty '''

def p_pn_while_jump(p):
    ''' pn_while_jump : empty '''

def p_pn_while_jump1(p):
    ''' pn_while_jump1 : empty '''

def p_read(p):
    ''' read : READ LEFT_PARENTHESIS var RIGHT_PARENTHESIS SEMICOLON '''

def p_write(p):
    ''' write : WRITE LEFT_PARENTHESIS write_rec RIGHT_PARENTHESIS SEMICOLON '''

def p_write_rec(p):
    ''' write_rec : all_logical pn_write_quad write_rec1 '''

def p_write_rec1(p):
    ''' write_rec1 : MORE all_logical pn_write_quad write_rec1 
                    | empty '''

def p_pn_write_quad(p):
    ''' pn_write_quad : empty '''

def p_func_call(p):
    ''' func_call : CALL ID pn_verify_func LEFT_PARENTHESIS pn_param_counter pn_open_parenthesis func_call_rec pn_close_parenthesis RIGHT_PARENTHESIS '''
    func_exists = False

    for x in funcTable:
        print(x.name())
        if x.name() == p[2]:
            print("La funcion " + p[2] + " si existe!")
            func_exists = True
            break

    if (func_exists == False):
        print("La funcion " + p[2] + " no existe FLOP!")
        quit()

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

    funcTable.append(Function(p[4], p[2]))

def p_pn_add_param_vartable(p):
    ''' pn_add_param_vartable : empty '''

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
    print("Error en la linea " + str(p.lineno - 10))

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

# result.imprimir(" ")
# print result.traducir()

# graphFile = open('graphviztrhee.vz', 'w')
# graphFile.write(result.traducir())
# graphFile.close()

print(result)
print (varTable)
print([Variable.name for Variable in varTable])