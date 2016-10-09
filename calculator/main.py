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
        try:
            print 'Correct result: %d' % eval(instr)
        except:
            print 'Syntax error'
        lexer = Lexer(instr)
        print 'Lexer result: ',
        while True:
            token = lexer.nextToken()
            if token != None:
                print token,
            else:
                break
        print
        lexer.reset()
        parser = Parser(lexer)
        expr = parser.match()
        if expr == None:
           break 
        print 'Parser result: ', expr
        print 'Execute result:', expr.calc()
