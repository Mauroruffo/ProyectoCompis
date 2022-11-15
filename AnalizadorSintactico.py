import ply.yacc as yacc
import os
import codecs
import re
from AnalizadorLex import tokens
from AnalizadorSemantico import *
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
    p[0] = program(p[1], p[2], p[3], "program")
    print("program")

def p_vars(p):
    ''' vars : VAR varid COLON tipo SEMICOLON '''
    p[0] = vars(p[4], "vars")
    print("vars")

def p_varsEmpty(p):
    ''' vars : empty '''
    p[0] = Null()
    print("Nulo")

def p_varsid1(p):
    '''  varid : ID '''
    p[0] : varsid1(varsid1(p[1]), "varsid1")

def p_varsid2(p):
    ''' varid : ID COMMA ID '''
    p[0] : varsid2(varsid2(p[1]))

def p_varsidEmpty(p):
    ''' varid : empty '''
    p[0] = Null()

def p_tipo1(p):
    '''  tipo : INT '''

def p_tipo2(p):
    '''  tipo : FLOAT '''

def p_bloque(p):
    ''' bloque : LEFT_CURLYB estatutoRecursivo RIGHT_CURLYB '''
    p[0] = bloque(p[2], "bloque")
    print("bloque")

def p_estatutoRec1(p):
    ''' estatutoRecursivo : estatuto estatutoRecursivo '''
    p[0] = estatutoRec1(p[1], p[2], "estatutoRec1")

def p_estatutoRec2(p):
    ''' estatutoRecursivo : empty '''
    p[0] = Null()

def p_estatuto1(p):
    ''' estatuto : asignacion  '''
    p[0] = estatuto1(p[1], "estatuto1")
    print("estatuto")

def p_estatuto2(p):
    '''  estatuto : condicion '''
    p[0] = estatuto2(p[1], "estatuto2")

def p_estatuto3(p):
    '''  estatuto : write '''
    p[0] = estatuto3(p[1], "estatuto3")

def p_estatuto4(p):
    '''  estatuto : while '''
    p[0] = estatuto4(p[1], "estatuto4")

def p_estatuto5(p):
    '''  estatuto : read '''
    p[0] = estatuto5(p[1], "estatuto5")

def p_asignacion(p):
    ''' asignacion : ID EQUAL_ASSIGN expresion SEMICOLON '''
    p[0] = asignacion(p[3], "asignacion")
    print("asignacion")

def p_condicion(p):
    '''  condicion : IF LEFT_PARENTHESIS expresion RIGHT_PARENTHESIS bloque  '''
    p[0] = condicion(p[3], p[5], "condicion")
    print("condicion")

def p_condicion2(p):
    ''' condicion :  condicion ELSE bloque'''
    p[0] = condicion2(p[1], p[3], "condicion2")

def p_read(p):
    '''  read : READ VAR SEMICOLON '''
    print("read")

def p_while(p):
    '''  while : WHILE LEFT_PARENTHESIS expresion RIGHT_PARENTHESIS bloque '''
    p[0] = while_(p[3], p[5], "while")
    print("while")

def p_expresion1(p):
    '''  expresion : exp LESS_THAN exp '''
    p[0] = expresion1(p[1], LT(p[2]), p[3], "expresion1")
    print("expression")

def p_expresion2(p):
    ''' expresion : exp GREATER_THAN exp '''
    p[0] = expresion2(p[1], GT(p[2]), p[3], "expresion2")

def p_expresion3(p):
    ''' expresion : exp NOT_EQUAL exp '''
    p[0] = expresion3(p[1], NE(p[2]), p[3], "expresion3")

def p_exp1(p):
    ''' exp : termino PLUS termino  '''
    p[0] = exp1(p[1], p[3], "exp1")
    print("exp")

def p_exp2(p):
    ''' exp : termino MINUS termino '''
    p[0] = exp2(p[1], p[3], "exp2")

def p_termino1(p):
    '''  termino : factor MULTIPLICATION factor '''
    p[0] = termino1(p[1], Multiplication(p[2]), p[3], "termino1")
    print("termino")

def p_termino2(p):
    ''' termino : factor DIVISION factor '''
    p[0] = termino2(p[1], Division(p[2]), p[3], "termino2")

def p_factor1(p):
    '''  factor : LEFT_PARENTHESIS expresion RIGHT_PARENTHESIS '''
    p[0] = factor1(p[2], "factor1")
    print("factor")

def p_factor2(p):
    ''' factor : PLUS '''
    p[0] = factor2(Plus(p[1], "factor2"))

def p_factor3(p):
    ''' factor : MINUS '''
    p[0] = factor3(Minus(p[1]), "factor3")

def p_factor4(p):
    ''' factor : varcte '''
    p[0] = factor4(p[1], "factor4")

def p_varcte1(p):
    ''' varcte : ID '''
    p[0] = varcte1(ID(p[1], "varcte1"))

def p_varcte2(p):
    ''' varcte : CONST_INT '''
    p[0] = varcte2(Int(p[1]), "varcte2")

def p_varcte3(p):
    ''' varcte : CONST_FLOAT '''
    p[0] = varcte3(Float(p[1]), "varcte3")

def p_write(p):
    ''' write : WRITE LEFT_PARENTHESIS inside RIGHT_PARENTHESIS '''
    p[0] = write(p[3], "write")

def p_writeInside1(p):
    ''' inside : inside more inside '''
    p[0] = writeInside1(p[1], p[2], p[3], "wirteInside1")

def p_writeInside2(p):
    ''' inside : ID '''
    p[0] = writeInside2(ID(p[0]), "writeInside2")

def p_writeInside3(p):
    ''' inside : string '''
    p[0] = writeInside3(p[1], "writeInside3")

def p_writeInside4(p):
    ''' inside : empty '''
    p[0] = Null()

def p_more1(p):
    ''' more : MORE '''

def p_more2(p):
    ''' more : empty '''
    p[0] = Null()

def p_string(p):
    ''' string : CONST_STRING '''

def p_class(p):
    ''' class : CLASS ID LEFT_CURLYB vars method RIGHT_CURLYB '''
    p[0] = class_(p[4], p[5], "class")

def p_method(p):
    ''' method : tipo LEFT_PARENTHESIS varid RIGHT_PARENTHESIS bloquemetodo '''
    p[0] = method(p[1], p[3], "method")

def p_bloquemethod(p):
    ''' bloquemetodo : LEFT_CURLYB estatutoRecursivo RIGHT_CURLYB RETURN ID SEMICOLON '''
    p[0] = bloquemethod(p[2], "bloquemethod")

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

# result.imprimir(" ")
# print result.traducir()

# graphFile = open('graphviztrhee.vz', 'w')
# graphFile.write(result.traducir())
# graphFile.close()

print(result)