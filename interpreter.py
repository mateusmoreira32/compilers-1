import operator


class Interpreter:

    def __init__(self, code):
        self.heap = [0] * 10
        self.stack = []
        self.code = code
        self.functions = {
            'ADD': (operator.add, 2),
            'SUB': (operator.sub, 2),
            'MUL': (operator.mul, 2),
            'DIV': (operator.truediv, 2),
            'PUSH': (self.push, 1),
            'POP': (self.pop, 1)
        }

    def start(self):
        for token in self.code:
            if type(token) is int:
                self.stack.append(token)
            else:
                params = []
                for _ in range(self.functions[token][1]):
                    params.insert(0, self.stack.pop())

                result = self.functions[token][0](*params)
                if result is not None:
                    self.stack.append(result)


    def push(self, s):
        self.heap[s] = self.stack.pop()

    def pop(self, s):
        self.stack.append(self.heap[s])