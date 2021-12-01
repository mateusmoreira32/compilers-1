import ply.lex as lex

resul_lexema = []

reservada = (

    'INCLUDE',
    'USING',
    'NAMEESPACE',
    'STD',
    'COUT',
    'CIN',
    'GET',
    'CADENA',
    'RETURN',
    'VOID',
    'INT',
    'ENDL',
)
tokens = reservada + (

    'IDENTIFICADOR',
    'ENTERO',
    'ASIGNAR',

    'SUMA',
    'RESTA',
    'MULT',
    'DIV',
    'POTENCIA',
    'MODULO',

    'MINUSMINUS',
    'PLUSPLUS',

    'SE',
    'SINO'
    'MIENTRAS'
    'PARA',
    'AND',
    'OR',
    'NOT',
    'MENORQUE',
    'MENORIGUAL',
    'MAYORQUE',
    'MAYORIGUAL',
    'IGUAL',
    'DISTINTO',
    'NUMERAL',
    'PARIZQ',
    'PARDER',
    'CORIZQ',
    'CORDER',
    'LLAIZQ',
    'LLADER',
    'PUNTOCOMA',
    'COMA',
    'COMDOB',
    'MAYORDER', #>>
    'MAYORIZO', #<<
)
t_SUMA = r'\+'
t_RESTA = r'-'
t_MINUSMINUS = r'\-\-'
t_MULT = r'\*'
t_DIV = r'/'
t_MODULO = r'\%'
t_POTENCIA = r'(\*{2} | \^)'
t_ASIGNAR = r'='
t_AND = r'\&\&'
t_OR = r'\|{2}'
t_NOT = r'\!'
t_MENORQUE = r'<'
t_MAYORQUE = r'>'
t_PUNTOCOMA = ';'
t_COMA = r','
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_CORIZQ = r'\['
t_CORDER = r'\]'
t_LLAIZQ = r'{'
t_LLADER = r'}'
t_COMDOB = r'\"'

def t_INCLUDE(t):
    r'include'
    return t
def t_USING(t):
    r'using'
    return t
def t_NAMESPACE(t):
    r'namespace'
    return t
def t_STD(t):
    r'std'
    return t
def t_COUT(t):
    r'cout'
    return t
def t_CIN(t):
    r'cin'
    return t
def t_GET(t):
    r'get'
    return t
def t_ENDL(t):
    r'endl'
    return t
def t_SINO(t):
    r'else'
    return t
def t_SI(t):
    r'if'
    return t
def t_RETURN(t):
    r'return'
    return t
def t_VOID(t):
    r'void'
    return t
def t_MIENTRAS(t):
    r'while'
    return t
def t_PARA(t):
    r'for'
    return t
def t_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t
def t_IDENTIFICADOR(t):
    r'\w+(_\d\w)*'
    return t
def t_CADENA(t):
    r'\"?(\w+ \ *\w*\d* \ *)"?'
    return t
def t_NUMERAL(t):
    r'\#'
    return t
def t_PLUSPLUS(t):
    r'\+\+'
    return t
def t_MENORIGUAL(t):
    r'<='
    return t
def t_MAYORIGUAL(t):
    r'>='
    return t
def t_IGUAL(t):
    r'=='
    return t
def t_MAYORDER(t):
    r'<<'
    return t
def t_MAYORIZO(t):
    r'>>'
    return t

def t_comments_ONELine(t):
    r'\/\/(.)*\n'
    t.lexer.lineno += 1
    print("Comentario de uma linha")
t_ignore = ' \t'
def t_error(t):
    global resul_lexema
    estado = "** Token Invalido na linha {:4} valor {:16} Posição {:4}".format(str(t.lineno),str(t.value),
                                                                               str(t.lexpos))
    resul_lexema.append(estado)
    t.lexer.skip(1)
def prueba(data):
    global resul_lexema
    analizador = lex.lex()
    analizador.input(data)
    resul_lexema.clear()
    while True:
        tok = analizador.token()
        if  not tok:
            break
        estado = "Linha {:4} Tipo {:16} Valor {:16} Posição {:4} ".format(str(tok.lineno),str(tok.type),
                                                                           str(tok.value),str(tok.lexpos))
        resul_lexema.append(estado)
    return resul_lexema
analizador = lex.lex()
if __name__ == '__main__':
    while True:
        data = input("Entre com os dados: ")
        prueba(data)
        print(resul_lexema)

