from interpreter import Interpreter
from parser import parser
from lx import lexer

with open('code.m', 'r') as f:
    t = parser.parse(f.read())
# for q in t:
#     print(q)

def dps(tree, w):
    if type(tree) is not tuple:
        w.append(tree)
        return
    dps(tree[0], w)
    dps(tree[1], w)
    if len(tree) > 2:
        w.append(tree[2])

code = []

for s in t:
    q = []
    dps(s, q)
    code.extend(q)

print('code ---------------')
for c in code:
    print(c)

print('execution --------------')
interpreter = Interpreter(code=code)

interpreter.start()

print(interpreter.stack)
print(interpreter.heap)


