import ply.yacc as yacc
import os
import codecs
import re
from AnalizadorLex import tokens
from sys import stdin

precedence = (
    ('right', 'EQUAL_ASSIGN'),
    ('left', 'LEFT_CURLYB', 'RIGHT_CURLYB'),
    ('left', 'LEFT_BRACKET', 'RIGHT_BRACKET'),
    ('left', 'LESS_THAN', 'GREATER_THAN', 'NOT_EQUAL', 'LESS_EQUAL', 'GREATER_EQUAL', 'EQUAL_COMPARE'),
    ('left', 'AND', 'OR', 'NEGATION'),
    ('left', 'MINUS', 'PLUS'),
    ('left', 'MULTIPLICATION', 'DIVISION'),
    ('left', 'LEFT_PARENTHESIS', 'RIGHT_PARENTHESIS'),
)

def p_program(p):
    ''' program : PROGRAM ID SEMICOLON vars class bloque '''
    #p[0] = program(p[1], "program")
    print("program")

def p_vars(p):
    ''' vars : VAR varid COLON tipo SEMICOLON '''
    #p[0] = vars(p[4])
    print("vars")

def p_varsEmpty(p):
    ''' vars : empty '''
    print("Nulo")

def p_varsid1(p0):
    '''  varid : ID '''

def p_varsid2(p):
    ''' varid : ID COMMA ID '''

def p_varsidEmpty(p):
    ''' varid : empty '''

def p_tipo1(p):
    '''  tipo : INT '''

def p_tipo2(p):
    '''  tipo : FLOAT '''

def p_bloque(p):
    ''' bloque : LEFT_CURLYB estatutoRecursivo RIGHT_CURLYB '''
    #p[0] = bloque(p[2])
    print("bloque")

def p_estatutoRec1(p):
    ''' estatutoRecursivo : estatuto estatutoRecursivo '''

def p_estatutoRec2(p):
    ''' estatutoRecursivo : empty '''

def p_estatuto1(p):
    ''' estatuto : asignacion  '''
    #p[0] = 
    print("estatuto")

def p_estatuto2(p):
    '''  estatuto : condicion '''

def p_estatuto3(p):
    '''  estatuto : write '''

def p_estatuto4(p):
    '''  estatuto : while '''

def p_estatuto5(p):
    '''  estatuto : read '''

def p_asignacion(p):
    ''' asignacion : ID EQUAL_ASSIGN expresion SEMICOLON '''
    print("asignacion")

def p_condicion(p):
    '''  condicion : IF LEFT_PARENTHESIS expresion RIGHT_PARENTHESIS bloque  '''
    print("condicion")

def p_condicion2(p):
    ''' condicion :  condicion ELSE bloque'''

def p_read(p):
    '''  read : READ VAR SEMICOLON '''
    print("read")

def p_while(p):
    '''  while : WHILE LEFT_PARENTHESIS expresion RIGHT_PARENTHESIS bloque '''
    print("while")

def p_expresion1(p):
    '''  expresion : exp LESS_THAN exp '''
    print("expression")

def p_expresion2(p):
    ''' expresion : exp GREATER_THAN exp '''

def p_expresion3(p):
    ''' expresion : exp NOT_EQUAL exp '''

def p_exp1(p):
    ''' exp : termino PLUS termino  '''
    print("exp")

def p_exp2(p):
    ''' exp : termino MINUS termino '''

def p_termino1(p):
    '''  termino : factor MULTIPLICATION factor '''
    print("termino")

def p_termino2(p):
    ''' termino : factor DIVISION factor '''

def p_factor1(p):
    '''  factor : LEFT_PARENTHESIS expresion RIGHT_PARENTHESIS '''
    print("factor")

def p_factor2(p):
    ''' factor : PLUS '''

def p_factor3(p):
    ''' factor : MINUS '''

def p_factor4(p):
    ''' factor : varcte '''

def p_varcte1(p):
    ''' varcte : ID '''

def p_varcte2(p):
    ''' varcte : CONST_INT '''

def p_varcte3(p):
    ''' varcte : CONST_FLOAT '''

def p_write(p):
    ''' write : WRITE LEFT_PARENTHESIS inside RIGHT_PARENTHESIS '''

def p_writeInside1(p):
    ''' inside : inside more inside '''

def p_writeInside2(p):
    ''' inside : ID '''

def p_writeInside3(p):
    ''' inside : string '''

def p_writeInside4(p):
    ''' inside : empty '''

def p_more1(p):
    ''' more : MORE '''

def p_more2(p):
    ''' more : empty '''

def p_string(p):
    ''' string : DOUBLE_QUOTES CONST_STRING DOUBLE_QUOTES '''

def p_class(p):
    ''' class : CLASS LEFT_CURLYB vars method RIGHT_CURLYB '''

def p_method(p):
    ''' method : DEF LEFT_PARENTHESIS varid RIGHT_PARENTHESIS bloquemetodo '''

def p_bloquemethod(p):
    ''' bloquemetodo : LEFT_CURLYB estatutoRecursivo RIGHT_CURLYB RETURN ID SEMICOLON '''

def p_empty(p):
    ''' empty :  '''
    pass

def p_error(p):
    print("Error de sintaxis" , p)
    print("Error en la linea " + str(p.lineno))

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