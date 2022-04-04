class Stack():
        
    def isEmpty(self):
        return self.size() == 0

    def push(self, letter):
        self.stack += letter

    def pop(self):
        self.stack = self.stack[:self.size()-1]

    def peek(self):
        return self.stack[self.size() - 1]

    def size(self):
        return len(self.stack)

    def execute(self, str):
        self.str = str
        self.stack = ''
        for letter in self.str:
            if self.isEmpty() and letter in [')', '}', ']']:
                return 'Несбалансированно'
            elif letter in ['(','{','[']:
                self.push(letter)
            elif (self.peek() == '(' and letter == ')') or (self.peek() == '[' and letter == ']') or (self.peek() == '{' and letter == '}'):
                self.pop()
            else:
                return 'Несбалансированно'
        
        if self.isEmpty():
            return 'Сбалансированно'
        else:
            return 'Несбалансированно'

stack_test = Stack()

print(stack_test.execute('(((([{}]))))'))
print(stack_test.execute('[([])((([[[]]])))]{()}'))
print(stack_test.execute('{{[()]}}'))
print(stack_test.execute('}{}'))
print(stack_test.execute('{{[(])]}}'))
print(stack_test.execute('[[{())}]'))