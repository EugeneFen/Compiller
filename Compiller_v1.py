from lexer import Lexer
from parse import Parser

file = open('Readme.txt','r')
try:
    list = file.read()
    print(list)
    emp1 = Lexer(list)
    prt1 = Parser(emp1)
    print(prt1.parse().children)
    #emp2 = emp1.get_token()
    #print(emp2.__repr__())
    """while emp2.type != Lexer.EOF:
        emp2 = emp1.get_token()
        print(emp2.__repr__())"""
    prt1.close_f()
finally:
    file.close()
