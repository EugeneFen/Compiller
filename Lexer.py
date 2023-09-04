import sys

class Lex:
    def __init__(self, row, col, type, value):
        self.row, self.col, self.type, self.value = row, col, type, value

    def __repr__(self):
        return f"Token: \tType: {self.type} \tValue: <{self.value}>"

class Lexer:
    eof: bool
    text: list
    row: int
    col: int
    curr_pos : int
    text_length: int
    curr_char: str

    START, NUM, ID, EOF, END, INTEGER, DOUBLE, STRING, CHAR,\
    BOOLEAN, FOR, NEXT, STEP, EACH, WHILE, DO, UNTIL, LOOP, IF,\
    LBR, RBR, PLUS, MINUS, MUL, DIVIDE, DEGREE, MORE, LESS, EQUAL,\
    NOTEQUALS, LCB, RCB, COMMA, AND, OR, NOT, THEN, ELSE, ELSEIF, \
    SELECT, CASE, FUNCTION, UPCOMMAS, RETURN, SUB, NEW, FROM, ADD, \
    REMOVE, INDEXOF, DIM, AS, TO, IN, TRUE, FALSE =  range(56) 

    SYMBOLS = {
        '(': LBR,
        ')': RBR,
        '+': PLUS,
        '-': MINUS,
        '*': MUL,
        '/': DIVIDE,
        '^': DEGREE,
        '>': MORE,
        '<': LESS,
        '=': EQUAL,
        '<>': NOTEQUALS,
        '{': LCB,
        '}': RCB,
        ',': COMMA,
        '"': UPCOMMAS
    }

    WORDS  = {
        'And': AND,
        'Or': OR,
        'Not': NOT,
        'End': END,
    
        'Integer': INTEGER, #не используется
        'Double': DOUBLE, #не используется
        'String': STRING, #не используется
        'Char': CHAR,
        'Boolean': BOOLEAN,
    
        'For': FOR,
        'Next': NEXT,
        'Step': STEP,
        'Each': EACH,
        'While': WHILE,
        'Do': DO,
        'Until': UNTIL,
        'Loop': LOOP,
        'If': IF,
        'Then': THEN,
        'Else': ELSE,
        'ElseIf': ELSEIF,
        'Select': SELECT,
        'Case': CASE,
        'Function': FUNCTION,
        'Return': RETURN,
        'Sub': SUB,
        'New': NEW,
        'From': FROM,
        'Add': ADD,
        'RemoveAt': REMOVE,
        'IndexOf':INDEXOF,
        'Dim': DIM,
        'As': AS,
        'To': TO,
        'In': IN,
        'true': TRUE,
        'false': FALSE,
    }

    def __init__(self, text) -> None:
        self.eof = False
        self.text = text
        self.row = 1
        self.col = 0
        self.text_length = len(text)
        self.curr_char = None
        self.curr_pos = 0
        self.get_char()
        
    def error(self, message):
        print("Lexer error:", message, f"at line {self.row}, index {self.col - 1}")
        sys.exit(1)

    def get_char(self) -> None:
        if self.curr_char == '\n':
            self.row += 1
            self.col = 0
        if self.curr_pos < self.text_length:
            self.curr_char = self.text[self.curr_pos]
            self.curr_pos += 1
            self.col += 1
        else:
            self.curr_char = ''
            
    def get_token(self):
        self.state = None
        self.value = None
        while self.state is None:
            #first step
            if self.curr_char is None:
                self.get_char()
            # end of file
            if self.curr_char == '':
                self.state = Lexer.EOF
            # comment
            elif self.curr_char == "'":
                start_comment = self.curr_char
                self.get_char()                
                while self.curr_char not in ['', '\n']:
                    self.get_char()
                if self.curr_char == "\n":
                    self.get_char()                
            # whitespaces
            elif self.curr_char in [' ', '\n']:
                self.get_char()
            # string and char   !!!!!!!!!!!!!!!!!!!!!!!
            elif self.curr_char == '"':                
                self.value = ""
                self.get_char()
                while self.curr_char != '"':
                    self.value += self.curr_char
                    self.get_char()
                self.get_char()
                if len(self.value) == 1:
                    self.state = Lexer.CHAR
                else:
                    self.state = Lexer.STRING
            # symbols
            elif self.curr_char in Lexer.SYMBOLS:                
                self.state = Lexer.SYMBOLS[self.curr_char]
                self.value = self.curr_char
                self.get_char()
            # numbers float(double) and integer
            elif self.curr_char.isdigit():
                number = 0
                while self.curr_char.isdigit():
                    number = number * 10 + int(self.curr_char)
                    self.get_char()
                if self.curr_char.isalpha() or self.curr_char == "_":
                    self.error(f'Invalid identifier')
                if self.curr_char == '.':
                    number = str(number)
                    number += '.'
                    self.get_char()
                    while self.curr_char.isdigit():
                        number += self.curr_char
                        self.get_char()
                    if self.curr_char.isdigit() == False and self.curr_char != ' ' or number[
                        len(number) - 1] == '.':
                        self.error(f'Invalid number ')

                    self.state = Lexer.DOUBLE
                else:
                    self.state = Lexer.INTEGER
                self.value = str(number)
            # identifiers, keywords and reserved names
            elif self.curr_char.isalpha():
                variable = ""
                while self.curr_char.isalpha() or self.curr_char.isdigit() or self.curr_char == '_':
                    variable += self.curr_char
                    self.get_char()
                if variable in Lexer.WORDS:
                    self.state = Lexer.WORDS[variable]
                    self.value = variable
                else:
                    self.state = Lexer.ID
                    self.value = variable
            else:
                self.error(f'Unexpected symbol: {self.curr_char}')

        token = Lex(self.row, self.col, self.state, self.value)
        return token


file = open('Readme.txt','r')
try:
    list = file.read()
    print(list)
    emp1 = Lexer(list)
    print(emp1.get_token().__repr__())
    print(emp1.get_token().__repr__())
finally:
   file.close()