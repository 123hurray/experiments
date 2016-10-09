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
class MultiplyToken(object):
    def __repr__(self):
        return '*'
class Lexer(object):
    def __init__(self, text):
        self.instr = text
    @staticmethod
    def isInt(string):
        try:
            int(string)
            return True
        except:
            return False


    def getTokens(self):
        instr = self.instr
        tokens = []
        num = None
        while instr != '':
            if Lexer.isInt(instr[0]):
                if num == None:
                    num = 0
                num = num * 10 + int(instr[0])
                instr = instr[1:]
                continue
            elif num != None:
                tokens.append(IntToken(num))
                num = None
                
            if instr[0] == '(':
                tokens.append(LeftBracketToken())
                instr = instr[1:]
            elif instr[0] == ')':
                tokens.append(RightBracketToken())
                instr = instr[1:]
            elif instr[0] == '+':
                tokens.append(AddToken())
                instr = instr[1:]
            elif instr[0] == '*':
                tokens.append(MultiplyToken())
                instr = instr[1:]
            else:
                raise Exception()
        if num != None:
            tokens.append(IntToken(num))
        return tokens


