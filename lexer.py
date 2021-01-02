# ------------------------------------------------------------
# lexer.py
#
# Tokenizer to recognize PGN (Portable Game Notation) files.
# ------------------------------------------------------------
import sys
import re
import ply.lex as lex

# List of token names.
tokens = (
   'FINALSCORE',
   'MATCHDESCRIPTOR',
   'QUEENSIDECASTLING',
   'KINGSIDECASTLING',
   'ROUNDNUMBERTHREEDOT',
   'ROUNDNUMBERDOT',
   'MOVE',
   'BRACKETCOMMENT',
   'BRACKETCOMMENT_lbrace',
   'BRACKETCOMMENT_rbrace',
   'PARENTHESESCOMMENT',
   'PARENTHESESCOMMENT_lparent',
   'PARENTHESESCOMMENT_rparent',
   'BRACKETCOMMENT_nonspace',
   'PARENTHESESCOMMENT_nonspace',
   'PARENTHESESCOMMENT_rbrace',
   'PARENTHESESCOMMENT_lbrace',
   'BRACKETCOMMENT_lparent',
   'BRACKETCOMMENT_rparent'
)

# Regular expression rules for simple tokens
t_QUEENSIDECASTLING = r'O-O-O'
t_KINGSIDECASTLING = r'O-O'


t_MATCHDESCRIPTOR = r'\[[a-zA-Z0-9\u00f1\u00d1]+\s"[^\[|\]]+"\](\n|$)'

def t_FINALSCORE(t):
	r'([0]-[1])|([1]-[0])|([1]/[2]-[1]/[2])'
	return t

def t_MOVE(t):
  r'(P|N|B|Q|K|R)?([a-h])?([1-8])?(x)?[a-h][1-8][+#?!]?'
  m = re.findall('x', t.value)
  t.value = len(m)
  return t


def t_ROUNDNUMBERTHREEDOT(t):
    r'\d+\.{3}'
    t.value = int(t.value[:-3])
    # t.lexer.lexpos = t.lexer.lexpos
    # r'\.{3}'
    return t


def t_ROUNDNUMBERDOT(t):
    r'\d+\.{1}'
    t.value = int(t.value[:-1])
    # t.lexer.lexpos = t.lexer.lexpos
    # r'\.{1}'
    return t
    
# -----------------------------------------
# Manage nested comments, based on example available at:
# https://ply.readthedocs.io/en/latest/ply.html#lex

 # Declare the state
states = (
  ('BRACKETCOMMENT','exclusive'), 
  ('PARENTHESESCOMMENT', 'exclusive'),
)
 
 
 # Match the first {. Enter BRACKETCOMMENT state.
def t_BRACKETCOMMENT(t):
   r'\{'
   t.lexer.code_start = t.lexer.lexpos        # Record the starting position
   t.lexer.level = 1                          # Initial brace level
   t.lexer.push_state('BRACKETCOMMENT')                     # Enter 'BRACKET_COMMENT' state


# Rules for the BRACKETCOMMENT state
def t_BRACKETCOMMENT_lbrace(t):     
   r'\{'
   t.lexer.level +=1
   t.lexer.push_state('BRACKETCOMMENT')              

def t_BRACKETCOMMENT_rbrace(t):
   r'\}'
   t.lexer.level -=1
   t.lexer.pop_state()  
   # If closing brace, return the code fragment
   if t.lexer.level == 0:
    t.value = t.lexer.lexdata[t.lexer.code_start-1:t.lexer.lexpos+1]
    t.type = "BRACKETCOMMENT"
    t.lexer.lineno += t.value.count('\n')         
    m = re.findall('(P|N|B|Q|K|R)?([a-h])?([1-8])?(x)[a-h][1-8][+#?!]?', t.value)
    t.value = len(m)
    return t


 # Match the first (. Enter PARENTHESESCOMMENT state.
def t_PARENTHESESCOMMENT(t):
   r'\('
   t.lexer.code_start = t.lexer.lexpos        # Record the starting position
   t.lexer.level = 1                          # Initial brace level
   t.lexer.push_state('PARENTHESESCOMMENT')                     # Enter 'BRACKET_COMMENT' state


# Rules for the PARENTHESESCOMMENT state
def t_PARENTHESESCOMMENT_lparent(t):     
    r'\('
    t.lexer.level +=1 
    t.lexer.push_state('PARENTHESESCOMMENT')                

def t_PARENTHESESCOMMENT_rparent(t):
   r'\)'
   t.lexer.level -=1
   t.lexer.pop_state() 
   # If closing brace, return the code fragment
   if t.lexer.level == 0:
    t.value = t.lexer.lexdata[t.lexer.code_start-1:t.lexer.lexpos+1]
    t.type = "PARENTHESESCOMMENT"
    t.lexer.lineno += t.value.count('\n')         
    m = re.findall('(P|N|B|Q|K|R)?([a-h])?([1-8])?(x)[a-h][1-8][+#?!]?', t.value)
    t.value = len(m)
    return t

def t_PARENTHESESCOMMENT_lbrace(t):
    r'\{'
    t.lexer.level += 1               
    t.lexer.push_state('BRACKETCOMMENT') 
    
def t_BRACKETCOMMENT_lparent(t):
    r'\('
    t.lexer.level += 1               
    t.lexer.push_state('PARENTHESESCOMMENT') 
  
  
def t_PARENTHESESCOMMENT_rbrace(t):
    r'\}'
    t.lexer.level -= 1
    t.lexer.pop_state()
    print('#ERROR: Cant close parentheses comment with brackets')    

def t_BRACKETCOMMENT_rparent(t):
    r'\)'
    t.lexer.level -= 1
    t.lexer.pop_state()
    print('#ERROR: Cant close bracket comment with parentheses')    

# -------------------------------------------------------------

# Any sequence of non-whitespace characters (not braces, strings)
def t_BRACKETCOMMENT_nonspace(t):
    r'[^(\{\}\)\(\n)]+'


def t_PARENTHESESCOMMENT_nonspace(t):
    r'[^(\(\)\}\{\n)]+'


#End of file by state
def t_PARENTHESESCOMMENT_eof(t):
    if t.lexer.level != 0:
        print('#ERROR: Invalid comment! Unclosed parentheses comment found.')

def t_BRACKETCOMMENT_eof(t):
    if t.lexer.level != 0:
        print('#ERROR: Invalid comment! Unclosed bracket comment found.')


# Error handling rule by state
def t_BRACKETCOMMENT_error(t):
    print("#ERROR: Invalid character in bracket comment '%s'" % t.value[0])
    t.lexer.skip(1)

def t_PARENTHESESCOMMENT_error(t):
    print("#ERROR: Invalid character in parentheses comment '%s'" % t.value[0])
    t.lexer.skip(1)

def t_error(t):
    print("#ERROR: Invalid character '%s'" % t.value[0])
    t.lexer.skip(1)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t\n'
t_PARENTHESESCOMMENT_ignore  = '\n'
t_BRACKETCOMMENT_ignore  = '\n'

# Build the lexer
lexer = lex.lex()


# lexer.input(data)
'''
if __name__ == '__main__':
	
    with open(sys.argv[1], 'r') as file:
        data = file.read().replace('\n', '')
# Give the lexer some input
'''

# while True:
#     tok = lexer.token()
#     if not tok:
#         break     
#     print(tok)

    
    
    


