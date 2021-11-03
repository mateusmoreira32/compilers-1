import operator


class Interpreter:

    def __init__(self, code, memorySize):
        self.heap = [0] * memorySize
        self.static = [0] * 10
        self.args = 0
        self.local = 0
        self.stack = []
        self.code = code
        self.pc = 0
        self.functions = {
            'ADD': self.add,
            'SUB': self.sub,
            'MUL': self.mul,
            'DIV': self.div,
            'PUSH': self.push,
            'POP': self.pop,
            'LT': self.lt,
            'JUMP': self.jump,
            'RETURN': self.ret,
            'CALL': self.call
        }

    def start(self):
        while self.pc < len(self.code):
            line = self.code[self.pc]
            self.pc += 1
            self.functions[line[0]](line)

    def push(self, s):
        if s[1] == 'CONSTANT':
            self.stack.append(s[2])
        elif s[1] == 'LOCAL':
            self.stack.append(self.stack[self.local + s[2]])
        elif s[1] == 'STATIC':
            self.stack.append(self.static[s[2]])
        elif s[1] == 'ARG':
            self.stack.append(self.stack[self.args + s[2]])

    def pop(self, s):
        if s[1] == 'LOCAL':
            self.stack[self.local + s[2]] = self.stack.pop()
        elif s[1] == 'STATIC':
            self.static[s[2]] = self.stack.pop()
        elif s[1] == 'ARG':
            self.stack[self.args + s[2]] = self.stack.pop()

    def add(self, s):
        a2 = self.stack.pop()
        a1 = self.stack.pop()
        self.stack.append(a1 + a2)

    def sub(self, s):
        a2 = self.stack.pop()
        a1 = self.stack.pop()
        self.stack.append(a1 - a2)

    def mul(self, s):
        a2 = self.stack.pop()
        a1 = self.stack.pop()
        self.stack.append(a1 * a2)

    def div(self, s):
        a2 = self.stack.pop()
        a1 = self.stack.pop()
        self.stack.append(a1 / a2)

    def lt(self, s):
        a2 = self.stack.pop()
        a1 = self.stack.pop()
        self.stack.append(a1 < a2)

    def jump(self, s):
        if s[1] == 'NOT':
            v = self.stack.pop()
            if not v:
                self.pc = s[2]

        elif s[1] == 'TO':
            self.pc = s[2]

    def ret(self, s):
        if s[1] == 'VOID':
            if self.args - 1 < 0:
                self.pc = len(self.code)
                return
            pc = self.stack[self.args - 1]
            self.pc = pc
        elif s[1] == 'VALUE':
            value = self.stack.pop()
            pc = self.stack[self.local - 1]
            args = self.args
            self.args = self.stack[self.local - 3]
            self.local = self.stack[self.local - 2]
            self.pc = pc
            self.stack = self.stack[:args]
            self.stack.append(value)

    def call(self, s):
        self.stack.append(self.local)
        self.stack.append(self.args)
        self.stack.append(self.pc)
        self.args = len(self.stack) - 3 - s[2]
        self.local = len(self.stack)
        self.pc = s[1]
