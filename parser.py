import ply.yacc as yacc
from lx import tokens


symbol_table = dict()
global address
address = 0

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE')
)

def p_s(p):
    """statements : statement statements
                | empty
    """
    if p[1] is not None:
        q = p[2] if p[2] is not None else []
        p[0] = [p[1]] + q

def p_statement(p):
    """statement : attrib """
    p[0] = p[1]

def p_empty(p):
    """empty : """
    pass

def p_attrib(p):
    """attrib : ID ATTRIB expression SEMICOLON"""
    global address
    if p[1] not in symbol_table:
        symbol_table[p[1]] = address
        address += 1
    p[0] = (p[3], symbol_table[p[1]], 'PUSH')

def p_e(p):
    """expression : expression PLUS expression"""

    p[0] = (p[1], p[3], 'ADD')

def p_expression_minus(p):
    'expression : expression MINUS expression'

    p[0] = (p[1], p[3], 'SUB')

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term(p):
    'term : term TIMES term'

    p[0] = (p[1], p[3], 'MUL')


def p_term_div(p):
    'term : term DIVIDE term'

    p[0] = (p[1], p[3], 'DIV')

def p_term_number(p):
    'term : NUMBER'
    p[0] = p[1]

def p_term_id(p):
    'term : ID'
    if p[1] not in symbol_table:
        raise Exception('symbol not found')
    p[0] = (symbol_table[p[1]], 'POP')

def p_paren(p):
    'term : LPAREN expression RPAREN'
    p[0] = p[2]

def p_error(p):
    print('erro')
    print(p)

parser = yacc.yacc()