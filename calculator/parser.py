'''
    expr = term expr2
    
    expr2 = ('+'|'-') term
          | e

    term = factor term2
    
    term2 = ('*'|'/') term
          | e

    factor = [0-9]
          | '(' expr ')'
'''


from lexer import *
isDebug = False
class Expr2(object):
    def __init__(self, token, expr):
        self.token = token
        self.expr = expr
    def calc(self, expr):
        if isinstance(self.token, AddToken):
            return expr.calc() + self.expr.calc()
    def __str__(self):
        return str(self.token) + str(self.expr)
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
    def __init__(self, token, term2):
        self.token = token
        self.term2 = term2
    def calc(self, factor):
        if self.term2 == None:
            return factor.calc()
        if isinstance(self.token, MultiplyToken):
            return factor.calc() * self.term2.calc()

    def __str__(self):
        return str(self.token) + (str(self.term2) if self.term2 != None else '')



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
        if isDebug: print func.func_name, self.lexer.getRemains(), "start"
        ret = func(self)
        if isDebug: print func.func_name, self.lexer.getRemains(), "end"
        return ret
    return _debug


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
    @debug
    def matchFactor(self):
        token = self.lexer.nextToken() 
        if isinstance(token, IntToken):
            return Factor(token)
        elif isinstance(token, LeftBracketToken):
            expr = self.matchExpr()
            self.lexer.nextToken()
            return Factor(expr)
        else:
            raise Exception(token)
    @debug
    def matchTerm2(self):
        token = self.lexer.nextToken()
        if token == None:
            return None
        if not isinstance(token, MultiplyToken):
            self.lexer.back()
            return None
        term = self.matchTerm()
        return Term2(token, term)
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
        if not isinstance(token, AddToken):
            self.lexer.back()
            return None
        expr = self.matchExpr()
        return Expr2(token, expr)
    @debug
    def matchExpr(self):
        term = self.matchTerm()
        expr2 = self.matchExpr2()
        return Expr(term, expr2)


