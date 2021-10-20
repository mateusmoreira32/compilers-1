import operator


class Interpreter:

    def __init__(self, code, memorySize):
        self.heap = [0] * memorySize
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
            'JUMP': self.jump
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
            self.stack.append(self.heap[s[2]])


    def pop(self, s):
        if s[1] == 'LOCAL':
            self.heap[s[2]] = self.stack.pop()

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