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
    def _debug(tokens):
        if isDebug: print func.func_name, tokens, "start"
        a, b = func(tokens)
        if isDebug: print func.func_name, tokens, "end"
        return a, b
    return _debug



@debug
def matchFactor(tokens):
    token = tokens[0]
    if isinstance(token, IntToken):
        return Factor(token), tokens[1:]
    elif isinstance(token, LeftBracketToken):
        expr, tokens = matchExpr(tokens[1:])
        return Factor(expr), tokens[1:]
    else:
        raise Exception(token)
@debug
def matchTerm2(tokens):
    if tokens == None or len(tokens) == 0:
        return None, None
    token = tokens[0]
    if not isinstance(token, MultiplyToken):
        return None, tokens
    term2, tokens = matchTerm(tokens[1:])
    return Term2(token, term2), tokens
@debug
def matchTerm(tokens):
    factor, tokens = matchFactor(tokens)
    term2, tokens = matchTerm2(tokens)
    return Term(factor, term2), tokens
@debug
def matchExpr2(tokens):
    if tokens == None or len(tokens) == 0:
        return None, None
    token = tokens[0]
    if not isinstance(token, AddToken):
        return None, tokens
    term, tokens = matchExpr(tokens[1:])
    return Expr2(token, term), tokens
@debug
def matchExpr(tokens):
    term, tokens = matchTerm(tokens)
    expr2, tokens = matchExpr2(tokens)
    return Expr(term, expr2), tokens


