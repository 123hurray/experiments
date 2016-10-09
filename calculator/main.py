from lexer import *
from parser import *


if __name__ == '__main__':
    while True:
        try:
            instr = raw_input()
        except:
            break
        print '************************************'
        print 'Raw line:' + instr
        print 'Correct result:%d' % eval(instr)
        tokens = Lexer(instr).getTokens()
        print 'Lexer result: ', tokens
        expr, tokens = matchExpr(tokens)
        print 'Parser result: ', expr
        print 'Execute result:', expr.calc()
