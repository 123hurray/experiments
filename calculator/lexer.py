class LeftBracketToken(object):
    def __repr__(self):
        return '('
class RightBracketToken(object):
    def __repr__(self):
        return ')'
class IntToken(int):
    def calc(self):
        return self
    pass
class AddToken(object):
    def __repr__(self):
        return '+'
class MinusToken(object):
    def __repr__(self):
        return '-'
class MultiplyToken(object):
    def __repr__(self):
        return '*'
class DivToken(object):
    def __repr__(self):
        return '/'
class Lexer(object):
    def __init__(self, text):
        self.instr = text
        self.backup = text
        self.lastTokenValid = False
    def reset(self):
        self.instr = self.backup
        self.lastTokenValid = False
    @staticmethod
    def isInt(string):
        try:
            int(string)
            return True
        except:
            return False
    def getRemains(self):
        if self.lastTokenValid:
            return str(self.lastToken) + self.instr
        return self.instr
    def back(self):
        self.lastTokenValid = True

    def nextToken(self):
        if self.lastTokenValid:
            self.lastTokenValid = False
            return self.lastToken
        instr = self.instr
        if instr == '':
            return None
        instr = instr.strip()
      
        if Lexer.isInt(instr[0]):
            i = 0
            num = 0
            while i < len(instr) and Lexer.isInt(instr[i]):
                num = num * 10 + int(instr[i])
                i += 1
            self.instr = instr[i:]
            token = IntToken(num)
        
        elif instr[0] == '(':
            self.instr = instr[1:]
            token = LeftBracketToken()
        elif instr[0] == ')':
            self.instr = instr[1:]
            token = RightBracketToken()
        elif instr[0] == '+':
            self.instr = instr[1:]
            token = AddToken()
        elif instr[0] == '*':
            self.instr = instr[1:]
            token = MultiplyToken()
        elif instr[0] == '-':
            self.instr = instr[1:]
            token = MinusToken()
        elif instr[0] == '/':
            self.instr = instr[1:]
            token = DivToken()
        else:
            raise Exception(instr)
        self.lastToken = token
        return token



