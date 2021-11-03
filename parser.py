import ply.yacc as yacc
from lx import tokens

class Scope:
    def __init__(self):
        self.address = 0
        self.arg_address = 0
        self.symbol_table = dict()
        self.args = dict()

    def add_arg(self, arg):
        self.args[arg] = self.arg_address
        self.arg_address += 1

    def add_symbol(self, symbol):
        self.symbol_table[symbol] = self.address
        self.address += 1

scopes = []

global label_count
label_count = 0

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE')
)

def p_func(p):
    """functions : function functions
                | empty
    """
    if len(p) > 2:
        p[0] = [p[1]] + p[2]
    elif p[1] is not None:
        p[0] = [p[1]]
    else:
        p[0] = []


def p_function(p):
    """function : FUNC ID LPAREN params RPAREN LBR statements RBR"""
    p[0] = ('FUNC', p[2], len(scopes[-1].symbol_table), p[7])
    scopes.pop()


def p_params_call(p):
    """pcall : logic pclist
             | empty
    """
    if p[1] is None:
        p[0] = []
        return
    p[0] = [p[1]] + p[2]


def p_pclist(p):
    """ pclist : COMMA logic pclist
             | empty
    """
    if p[1] == ',':
        p[0] = [p[2]] + p[3]
    else:
        p[0] = []

def p_params(p):
    """params : ID plist
              | empty
    """
    if p[1] is None:
        p[0] = []
        return

    p[0] = [p[1]] + p[2]
    scopes.append(Scope())
    for a in p[0]:
        scopes[-1].add_arg(a)

def p_plist(p):
    """ plist : COMMA ID plist
             | empty
    """
    if p[1] == ',':
        p[0] = [p[2]] + p[3]
    else:
        p[0] = []

def p_s(p):
    """statements : statement statements
                | empty
    """
    if p[1] is not None:
        q = p[2] if p[2] is not None else []
        p[0] = [p[1]] + q

def p_statement(p):
    """statement : attrib
                | if
                | while
                | return
                """
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
    label_count += 1

def p_while(p):
    """while : WHILE LPAREN logic RPAREN LBR statements RBR"""
    global label_count

    while_start = ('LABEL', 'while-start' + str(label_count))
    while_end = ('LABEL', 'while-end-' + str(label_count))
    jump = ('JUMP', 'NOT', while_end[1])
    jump_to = ('JUMP', 'TO', while_start[1])
    p[0] = ('WHILE', while_start, p[3], jump, p[6], jump_to, while_end)
    label_count += 1


def p_return(p):
    """return : RETURN logic SEMICOLON"""
    p[0] = ('RETURN', p[2])

def p_attrib(p):
    """attrib : ID ATTRIB logic SEMICOLON"""
    scope = scopes[-1]
    if p[1] in scope.args:
        p[0] = ('POP', 'ARG', scope.args[p[1]], p[3])
    else:
        if p[1] not in scope.symbol_table:
            scope.add_symbol(p[1])
        p[0] = ('POP', 'LOCAL', scope.symbol_table[p[1]], p[3])

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

def p_term_call(p):
    """term : call"""
    p[0] = p[1]

def p_term_number(p):
    'term : NUMBER'
    p[0] = ('PUSH', 'CONSTANT', p[1])

def p_term_id(p):
    'term : ID'
    scope = scopes[-1]
    if p[1] in scope.symbol_table:
        p[0] = ('PUSH', 'LOCAL', scope.symbol_table[p[1]])
    elif p[1] in scope.args:
        p[0] = ('PUSH', 'ARG', scope.args[p[1]])
    else:
        raise Exception('symbol not found')

def p_call(p):
    'call : ID LPAREN pcall RPAREN '
    p[0] = ('CALL', p[1], p[3])

def p_paren(p):
    'term : LPAREN expression RPAREN'
    p[0] = p[2]

def p_error(p):
    print('erro')
    print(p)

parser = yacc.yacc()