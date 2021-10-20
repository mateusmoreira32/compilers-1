import ply.yacc as yacc
from lx import tokens

symbol_table = dict()
global address
address = 0

global label_count
label_count = 0

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
    """statement : attrib
                | if """
    p[0] = p[1]

def p_empty(p):
    """empty : """
    pass

def p_if(p):
    """if : IF LPAREN logic RPAREN LBR statements RBR"""
    global label_count
    if_end = ('LABEL', 'if-end-' + str(label_count))
    jump = ('JUMP', 'NOT', if_end[1])
    p[0] = ('IF', p[3], jump, p[6], if_end)

def p_attrib(p):
    """attrib : ID ATTRIB logic SEMICOLON"""
    global address
    if p[1] not in symbol_table:
        symbol_table[p[1]] = address
        address += 1
    p[0] = ('POP', 'LOCAL', symbol_table[p[1]], p[3])

def p_logic(p):
    """logic : logic LT logic"""
    p[0] = ('LT', p[1], p[3])

def p_logic_expression(p):
    """logic : expression"""
    p[0] = p[1]

def p_e(p):
    """expression : expression PLUS expression"""
    p[0] = ('ADD', p[1], p[3])

def p_expression_minus(p):
    'expression : expression MINUS expression'

    p[0] = ('SUB', p[1], p[3])

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term(p):
    'term : term TIMES term'

    p[0] = ('MUL', p[1], p[3])


def p_term_div(p):
    'term : term DIVIDE term'

    p[0] = ('DIV', p[1], p[3])

def p_term_number(p):
    'term : NUMBER'
    p[0] = ('PUSH', 'CONSTANT', p[1])

def p_term_id(p):
    'term : ID'
    if p[1] not in symbol_table:
        raise Exception('symbol not found')
    p[0] = ('PUSH', 'LOCAL', symbol_table[p[1]])

def p_paren(p):
    'term : LPAREN expression RPAREN'
    p[0] = p[2]

def p_error(p):
    print('erro')
    print(p)

parser = yacc.yacc()