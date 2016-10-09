'''

BNF of calculator

    expr = term expr2
    
    expr2 = ('+'|'-') term
          | ('+'|'-') term expr2
          | e

    term = factor term2
    
    term2 = ('*'|'/') factor
          | ('*'|'/') factor term2
          | e

    factor = [0-9]
          | '(' expr ')'
'''

import random
import md5
from lexer import *
isDebug = False 
class Expr2(object):
    def __init__(self, token, term, expr2):
        self.token = token
        self.term = term
        self.expr2 = expr2
    def calc(self, expr):
        if isinstance(self.token, AddToken):
            tmp = expr.calc() + self.term.calc()
        elif isinstance(self.token, MinusToken):
            tmp = expr.calc() - self.term.calc()
        if self.expr2 == None:
            return tmp
        return self.expr2.calc(IntToken(tmp))
    def __str__(self):
        return str(self.token) + str(self.term) + (str(self.expr2) if self.expr2 != None else '')
class Expr(object):
    def __init__(self, term, expr2):
        self.term = term
        self.expr2 = expr2
    def calc(self):
        if self.expr2 == None:
            return self.term.calc()
        else:
            return self.expr2.calc(self.term)
    def __str__(self):
        return str(self.term) + (str(self.expr2) if self.expr2 != None else '')


class Term(object):
    def __init__(self, factor, term):
        self.factor = factor
        self.term = term
    def calc(self):
        if self.term == None:
            return self.factor.calc()
        else:
            return self.term.calc(self.factor)
    def __str__(self):
        return str(self.factor) + (str(self.term) if self.term != None else '')

class Term2(object):
    def __init__(self, token, factor, term2):
        self.token = token
        self.factor = factor
        self.term2 = term2
    def calc(self, factor):
        if isinstance(self.token, MultiplyToken):
            tmp = factor.calc() * self.factor.calc()
        elif isinstance(self.token, DivToken):
            tmp = factor.calc() / self.factor.calc()
        if self.term2 == None:
            return tmp
        return self.term2.calc(IntToken(tmp))

    def __str__(self):
        return str(self.token) + str(self.factor) + (str(self.term2) if self.term2 != None else '')



class Factor(object):
    def __init__(self, t):
        self.t = t
    def calc(self):
        return self.t.calc()

    def __str__(self):
        if isinstance(self.t, IntToken):
            return str(self.t)
        else:
            return '(' + str(self.t) + ')'



def debug(func):
    def _debug(self):
        tag = md5.md5(str(random.random())).hexdigest()[:8]
        if isDebug: print func.func_name, tag, self.lexer.getRemains(), "start"
        ret = func(self)
        if isDebug: print func.func_name, tag, "end"
        return ret
    return _debug


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
    @debug
    def matchFactor(self):
        token = self.lexer.nextToken() 
        if token == None:
            raise Exception('Unexpected EOF!')
        if isinstance(token, IntToken):
            return Factor(token)
        elif isinstance(token, LeftBracketToken):
            expr = self.matchExpr()
            right = self.lexer.nextToken()
            if not isinstance(right, RightBracketToken):
                raise Exception('Bracket mismatch!')
            return Factor(expr)
        else:
            raise Exception('Unexpected token: ' + str(token))
    @debug
    def matchTerm2(self):
        token = self.lexer.nextToken()
        if token == None:
            return None
        if not (isinstance(token, MultiplyToken) or isinstance(token, DivToken)):
            self.lexer.back()
            return None
        factor = self.matchFactor()
        term2 = self.matchTerm2()
        return Term2(token, factor, term2)
    @debug
    def matchTerm(self):
        factor = self.matchFactor()
        term2 = self.matchTerm2()
        return Term(factor, term2)
    @debug
    def matchExpr2(self):
        token = self.lexer.nextToken()
        if token == None:
            return None
        if not (isinstance(token, AddToken) or isinstance(token, MinusToken)):
            self.lexer.back()
            return None
        term = self.matchTerm()
        expr2 = self.matchExpr2()

        return Expr2(token, term, expr2)
    @debug
    def matchExpr(self):
        term = self.matchTerm()
        expr2 = self.matchExpr2()
        return Expr(term, expr2)

    def match(self):
        if self.lexer.nextToken() == None:
            return None
        self.lexer.back()
        ret = self.matchExpr()
        if self.lexer.nextToken() != None:
            raise Exception('Syntax Error!')
        return ret
