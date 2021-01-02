# Parser to to recognize PGN (Portable Game Notation) files.
# Usage: pgn_parser.py [PGN_file_name]
 
import sys
import ply.yacc as yacc
 
# Get the token map from the lexer.  This is required.
from lexer import tokens


# S : <array<capture>,num>
def p_S(p):
    '''S : SPRIMA'''
    print(p[1])


# SPRIMA : <array<capture>>
def p_SPRIMA_DMS(p):
    '''SPRIMA : D M SPRIMA'''
    p[0] = []
    p[0].append(p[2][0])
    p[0] = p[0]+p[3]


def p_empty(p):
     'empty :'
     pass 

def p_SPRIMA_empty(p):
    '''SPRIMA : empty'''
    p[0] = []
         

def p_D(p):
    '''D : MATCHDESCRIPTOR D
         | empty'''

# M : <captura,num>
#match: recursion only if black doesnt give up
def p_M_NRW(p):
    '''M : ROUNDNUMBERDOT R W'''
    p[0] = (p[2] + p[3][0], p[1])
    if p[3][1] != None:
        if p[1] != p[3][1]:
            print('#ERROR: Incorrect round number.')

def p_M_empty(p):
    '''M : FINALSCORE'''
    p[0] = (0,None)
   
# R : <captura>         
#real movement
def p_R_M(p):
    '''R : MOVE'''
    p[0] = p[1]

def p_R_Q(p):
    '''R : QUEENSIDECASTLING'''
    p[0] = 0

def p_R_K(p):
    '''R : KINGSIDECASTLING'''
    p[0] = 0

# C : <captura>
#comment
def p_C_B(p):
    '''C : BRACKETCOMMENT'''
    p[0] = p[1]

def p_C_P(p):
    '''C : PARENTHESESCOMMENT'''
    p[0] = p[1]

# O : <captura>
#opcional comment
def p_O_C(p):
    '''O : C'''
    p[0] = p[1]

def p_O_empty(p):
    '''O : empty'''
    p[0] = 0

# W : <captura,num>
#white comment
#1) white comment + black turn after white comment 
#2) black turn and recursion on M 3) black gives up
def p_W_CF(p):
    '''W : C F'''
    p[0] = (p[1] + p[2][0], p[2][1])

def p_W_BM(p):
    '''W : B M '''
    if p[2][1] != None:
        p[0] = (p[1] + p[2][0], p[2][1] - 1)
    else: 
        p[0] = (p[1] + p[2][0],None)

def p_W_F(p):
    '''W : FINALSCORE'''
    p[0] = (0,None)
          
# F : <captura,num> 
# after white comment, black turn:
# 1) black movement and recursion on M 2) black gives up          
def p_F_NBM(p):
    '''F : ROUNDNUMBERTHREEDOT B M'''
    p[0] = (p[2] + p[3][0],p[1])
    if p[3][1] != None:
        if p[3][1] != p[1] + 1:
            print('#ERROR: Incorrect round number.')
    
           
def p_F_F(p):
    '''F : FINALSCORE'''
    p[0] = (0,None)

# B : <captura>
#black movement: real movement + optional comment
def p_B(p):
    '''B : R O'''
    p[0] = p[1] + p[2]
    
# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")
 
# Build the parser
parser = yacc.yacc()
 

# try:
#     s = ''''''

# except EOFError:
#     print('error')
# parser.parse(s)
    

if __name__ == '__main__':
    
    with open(sys.argv[1], 'r') as file:
        data = file.read()

parser.parse(data)


