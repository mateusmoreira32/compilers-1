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

print('solved label code -------------------')
for c in code:
    print(c)


print('execution --------------')
interpreter = Interpreter(code=code, memorySize=10)

interpreter.start()

print(interpreter.stack)
print(interpreter.heap)


