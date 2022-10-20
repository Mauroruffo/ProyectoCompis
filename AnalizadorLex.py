from importlib.metadata import files
import ply.lex as lex
import re
import codecs
import os
import sys

tokens = ['LEFT_PARENTHESIS', 'RIGHT_PARENTHESIS', 'LEFT_BRACKET', 'RIGHT_BRACKET', 'LEFT_CURLYB', 'RIGHT_CURLYB', 'COLON', 'SEMICOLON', 
        'COMMA', 'PERIOD', 'LESS_THAN', 'GREATER_THAN', 'EQUAL_ASSIGN', 'NOT_EQUAL', 'LESS_EQUAL', 'GREATER_EQUAL', 'EQUAL_COMPARE', 'NUMBER',
        'MINUS', 'PLUS', 'MULTIPLICATION', 'DIVISION', 'AND', 'OR', 'NEGATION', 'ID', 'CONST_INT', 'CONST_FLOAT', 'CONST_CHAR', 'CONST_STRING']

reservadas = {
    'program' : 'PROGRAM',
    'var' : 'VAR',
    'class' : 'CLASS',
    'main' : 'MAIN',
    'if' : 'IF',
    'elseif' : 'ELSEIF',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'do' : 'DO',
    'function' : 'FUNCTION',
    'return' : 'RETURN',
    'read' : 'READ',
    'write' : 'WRITE',
    'int' : 'INT',
    'float' : 'FLOAT',
    'char' : 'CHAR',
    'void' : 'VOID',
    'attributes' : 'ATTRIBUTES',
    'methods' : 'METHODS'
}

tokens = tokens + list(reservadas.values())

t_ignore = ' \t'
t_EQUAL_ASSIGN = r'='
t_LEFT_PARENTHESIS = r'\('
t_RIGHT_PARENTHESIS = r'\)'
t_LEFT_BRACKET = r'\['
t_RIGHT_BRACKET = r'\]'
t_LEFT_CURLYB = r'\{'
t_RIGHT_CURLYB = r'\}'
t_COLON = r':'
t_SEMICOLON = r';'
t_COMMA = r','
t_PERIOD = r'\.'
t_LESS_THAN = r'<'
t_GREATER_THAN = r'>'
t_EQUAL_COMPARE = r'=='
t_NOT_EQUAL = r'!='
t_LESS_EQUAL = r'<='
t_GREATER_EQUAL = r'>='
t_MINUS = r'-'
t_PLUS = r'\+'
t_MULTIPLICATION = r'\*'
t_DIVISION = r'/'
t_AND = r'&'
t_OR = r'\|\|'
t_NEGATION = r'!'
t_CONST_INT = r'[1-9][0-9]*|0'
t_CONST_FLOAT = r'[+-]?([0-9]*[.])?[0-9]+'
t_CONST_CHAR = r'[_(a-zA-Z0-9)]'
t_CONST_STRING = r'[[_(a-zA-Z0-9)+]*]'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_ID(t):
    r'[a-zA-Z][_(a-zA-Z0-9)+]*'
    if t.value.upper() in reservadas:
        t.value = t.value.upper()
        t.type = t.value
    
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    print("Caracter Ilegal! '%s'" % t.value[0] )
    t.lexer.skip(1)

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


directorio = 'C:/Users/mauro/OneDrive/Documents/9no Semestre/Compiladores/ProyectoFinal/test/'
archivo = buscarFicheros(directorio)
test = directorio + archivo
fp = codecs.open(test,"r","utf-8")
cadena = fp.read()
fp.close()

print("Sam Raimi")

analizador = lex.lex()
analizador.input(cadena)

while True:
    tok = analizador.token()
    if not tok : break
    print(tok)
