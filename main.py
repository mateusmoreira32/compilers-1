from interpreter import Interpreter
from parser import parser
from lx import lexer

with open('code.m', 'r') as f:
    t = parser.parse(f.read())

print('tree ----------------------------')
for q in t:
    print(q)

def dps(tree, w):
    if tree[0] in ['ADD', 'DIV', 'LT']:
        dps(tree[1], w)
        dps(tree[2], w)
        w.append((tree[0], ))
    elif tree[0] in ['PUSH', 'POP']:
        if tree[1] == 'CONSTANT':
            w.append(tree)
        else:
            if len(tree) < 4:
                w.append(tree)
            else:
                dps(tree[3], w)
                w.append((tree[0], tree[1], tree[2]))

    elif tree[0] == 'IF':
        dps(tree[1], w)
        w.append(tree[2])
        for s in tree[3]:
            dps(s, w)
        w.append(tree[4])

    elif tree[0] == 'WHILE':
        w.append(tree[1])
        dps(tree[2], w)
        w.append(tree[3])
        for s in tree[4]:
            dps(s, w)
        w.append(tree[5])
        w.append(tree[6])
    elif tree[0] == 'FUNC':
        w.append(('LABEL', tree[1]))
        w.append(('PUSH', 'CONSTANT', 0))
        w.append(('POP', 'STATIC', 0))
        w.append(('LABEL', tree[1] + '-local-start'))
        w.append(('PUSH', 'STATIC', 0))
        w.append(('PUSH', 'CONSTANT', tree[2]))
        w.append(('LT',))
        w.append(('JUMP', 'NOT', tree[1] + '-local-end'))
        w.append(('PUSH', 'STATIC', 0))
        w.append(('PUSH', 'CONSTANT', 1))
        w.append(('ADD',))
        w.append(('POP', 'STATIC', 0))
        w.append(('PUSH', 'CONSTANT', 0))
        w.append(('JUMP', 'TO', tree[1] + '-local-start'))
        w.append(('LABEL', tree[1] + '-local-end'))
        for s in tree[3]:
            dps(s, w)
        w.append(('RETURN', 'VOID'))

    elif tree[0] == 'CALL':
        for s in tree[2]:
            dps(s, w)
        w.append(('CALL', tree[1], len(tree[2])))

    elif tree[0] == 'RETURN':
        dps(tree[1], w)

        if len(tree[1]) <= 0:
            w.append(('RETURN', 'VOID'))
        else:
            w.append(('RETURN', 'VALUE'))

code = []

for s in t:
    q = []
    dps(s, q)
    code.extend(q)

print('code -------------------')
for c in code:
    print(c)

label_dict = dict()
i = 0
while i < len(code):
    if code[i][0] == 'LABEL':
        label_dict[code[i][1]] = i
        code.pop(i)
        i -= 1

    i += 1

for i in range(len(code)):
    if code[i][0] == 'JUMP':
        code[i] = (code[i][0], code[i][1], label_dict[code[i][2]])

    elif code[i][0] == 'CALL':
        code[i] = (code[i][0], label_dict[code[i][1]], code[i][2])

print('solved label code -------------------')
for c in code:
    print(c)


print('execution --------------')
interpreter = Interpreter(code=code, memorySize=10)

interpreter.start()

print(interpreter.stack)
print(interpreter.heap)


