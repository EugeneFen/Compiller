import sys
from enum import Enum
from lexer import Lexer
from symboltable import SymbolTable

class Node:
    def __init__(self, node_type, value=None, children=None):
        self.node_type = node_type
        self.value = value
        self.children = children if children else []

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self):
        return f"Node: Type={self.node_type}, Value={self.value}, Children={self.children}"

class Parser:
    START, MODULE, ELSE_STATEMENT, IF_STATEMENT, THEN_STATEMENT, WHILE_STATEMENT, PROGRAM, ADDITION, SUBTRACTION, DIVISION, \
    MULTIPLICATION, EXPRESSION_STATEMENT, ID_LPAREN, INTEGER, DOUBLE, CHAR, STRING, TRUE, FALSE, ID, \
    COMPARISON_EQ, COMPARISON_LE, COMPARISON_MO, COMPARISON_NOTEQ, FUNCT_STATEMENT, FUNCTIONCALL, LISTF, EOF, INTEGERT, DOUBLET, \
    STRINGT, CHART, BOOLEANT, DIMV, PROGRAM, AND = range(36) #?

    def __init__(self, lexer):
        self.file = open('Debugging.txt','w')
        self.lexer = lexer
        self.current_token = self.lexer.get_token() #take the first token (row, col, type, value)

        self.file.write(str(self.current_token.type))
        self.file.write(" , ")
        self.file.write(self.current_token.value)
        self.file.write("\n")

        self.symbol_table = SymbolTable()

    def close_f(self):
        self.file.close()

    def error(self, message):
        print("Parser error: ", message)
        sys.exit(1)

    def match(self, expected_type): #requests a new token from the lexer
        if self.current_token.type == expected_type:
                self.current_token = self.lexer.get_token()

                self.file.write(str(self.current_token.type))
                self.file.write(" , ")
                self.file.write(str(self.current_token.value))
                self.file.write("\n")
        else:
            self.error(f"Unexpected token: {self.current_token.type}  {self.current_token.value}")
            
    def parse(self): # start
        return self.parse_program()

    def parse_program(self):

        statement_list = self.parse_statement_list()
        return Node(self.PROGRAM, value = "Program", children=[statement_list])

    def parse_statement_list(self):
        statement = self.parse_statement()
        if self.current_token.type != Lexer.EOF and \
            self.current_token.type != Lexer.ELSE and \
            self.current_token.type != Lexer.ENDIF and \
            self.current_token.type != Lexer.RETURN and \
            self.current_token.type != Lexer.ENDFUNC and \
            self.current_token.type != Lexer.ENDWHILE:
                statement_list = self.parse_statement_list()
                statement.add_child(statement_list) 
        return statement


    def parse_statement(self):
        if self.current_token.type == Lexer.IF: 
            return self.parse_if_statement()
        elif self.current_token.type == Lexer.WHILE:
            return self.parse_while_statement()
        elif self.current_token.type == Lexer.FUNCTION:
            return self.parse_function_statement()
        elif self.current_token.type == Lexer.DIM:
            return self.parse_dim_statement()
        else:
            return self.parse_expression_statement()

    def parse_if_statement(self):
        self.match(Lexer.IF) # if if then step
        self.match(Lexer.LBR)
        expression = self.parse_expression()
        self.match(Lexer.RBR)
        self.match(Lexer.THEN)
        statement_list = Node(self.THEN_STATEMENT, value="Then", children=[self.parse_statement_list()])
        if self.current_token.type == Lexer.ELSE:
            self.match(Lexer.ELSE)
            else_statement = Node(self.ELSE_STATEMENT, value="Else", children=[self.parse_statement_list()])
            self.match(Lexer.ENDIF)
            return Node(self.IF_STATEMENT, value="If", children=[expression, statement_list, else_statement])
        self.match(Lexer.ENDIF) #!!!!!!!!!!!!
        return Node(self.IF_STATEMENT, value="If", children=[expression, statement_list])

    def parse_while_statement(self):
        self.match(Lexer.WHILE)
        self.match(Lexer.LBR)
        expression = self.parse_expression()
        self.match(Lexer.RBR)
        statement_list = self.parse_statement_list()
        self.match(Lexer.ENDWHILE)
        return Node(self.WHILE_STATEMENT, value="While", children=[expression, statement_list])


    def parse_function_statement(self):
        self.match(Lexer.FUNCTION)
        id_value = Node(self.FUNCTIONCALL, value=self.current_token.value)
        self.match(Lexer.FUNCTIONCALL)
        self.match(Lexer.AS)
        ptype = self.parse_type_str()
        statement_list = self.parse_statement_list()        
        self.match(Lexer.RETURN)
        statement_list_ret = self.parse_statement_list()
        self.match(Lexer.ENDFUNC)
        return Node(self.FUNCT_STATEMENT, value="Function", children=[id_value, ptype, statement_list, statement_list_ret])

    def parse_dim_statement(self):
        self.match(Lexer.DIM)
        value = self.parse_identifier()
        if self.symbol_table.check(value.value):
            
            self.match(Lexer.AS)
            if self.current_token.type == Lexer.NEW:
                self.match(Lexer.NEW)        
                self.match(Lexer.LISTF)
                self.match(Lexer.LBR)
                self.match(Lexer.OF)
                type_list = self.parse_type_str()
                self.match(Lexer.RBR)
                self.match(Lexer.LBR)
                count_list = Node(self.INTEGER, value=self.current_token.value)
                self.match(Lexer.INTEGER)
                self.match(Lexer.RBR)
                self.symbol_table.set(value.value, "List", type_list.value)
                return Node(self.LISTF, value="List", children=[value, type_list, count_list])
            else:
                type_list = self.parse_type_str()
                self.symbol_table.set(value.value, type_list.value)
                if self.current_token.type == Lexer.EQUAL:
                    self.match(Lexer.EQUAL)
                    ptype = self.parse_type()
                    return Node(self.DIMV, value="DIMVAL", children=[value, type_list, ptype])
                return Node(self.DIMV, value="DIMVAL", children=[value, type_list])
        self.error(f"This variable already exists: {value.value}")

    def parse_expression(self):
        term = self.parse_factor()
        if self.current_token.type == Lexer.PLUS:
            self.match(Lexer.PLUS)
            return Node(self.ADDITION, value = "PLUS", children=[term, self.parse_expression()])
        elif self.current_token.type == Lexer.MINUS:
            self.match(Lexer.MINUS)
            return Node(self.SUBTRACTION, value = "MINUS", children=[term, self.parse_expression()])
        elif self.current_token.type == Lexer.EQUAL:
            self.match(Lexer.EQUAL)
            return Node(self.COMPARISON_EQ, value = "EQUAL", children=[term, self.parse_expression()])
        elif self.current_token.type == Lexer.LESS:
            self.match(Lexer.LESS)
            return Node(self.COMPARISON_LE, value = "LESS", children=[term, self.parse_expression()])
        elif self.current_token.type == Lexer.MORE:
            self.match(Lexer.MORE)
            return Node(self.COMPARISON_MO, value = "MORE", children=[term, self.parse_expression()])
        elif self.current_token.type == Lexer.NOTEQUALS:
            self.match(Lexer.NOTEQUALS)
            return Node(self.COMPARISON_NOTEQ, value = "NOTEQUALS", children=[term, self.parse_expression()])
        elif self.current_token.type == Lexer.AND:
            self.match(Lexer.AND)
            return Node(self.AND, value="AND", children=[term, self.parse_expression()])
        elif self.current_token.type == Lexer.MUL:
            self.match(Lexer.MUL)
            return Node(self.MULTIPLICATION, children=[term, self.parse_expression()])
        elif self.current_token.type == Lexer.DIVIDE:
            self.match(Lexer.DIVIDE)
            return Node(self.DIVISION, children=[term, self.parse_expression()])
        return term

    def parse_factor(self):
        ptype = self.parse_type()
        if self.current_token.type == Lexer.LBR:          
            self.match(Lexer.LBR)
            type_lbrrbr = self.parse_expression()
            self.match(Lexer.RBR)
            return type_lbrrbr
        return ptype

    def parse_type(self):
        if self.current_token.type == Lexer.INTEGER:
            int_value = Node(self.INTEGER, value=self.current_token.value)
            self.match(Lexer.INTEGER)
            return int_value
        elif self.current_token.type == Lexer.DOUBLE:
            double_value = Node(self.DOUBLE, value=self.current_token.value)
            self.match(Lexer.DOUBLE)
            return double_value
        elif self.current_token.type == Lexer.STRING:
            string_value = Node(self.STRING, value=self.current_token.value)
            self.match(Lexer.STRING)
            return string_value
        elif self.current_token.type == Lexer.CHAR:
            char_value = Node(self.CHAR, value=self.current_token.value)
            self.match(Lexer.CHAR)
            return char_value
        elif self.current_token.type == Lexer.TRUE:
            true_value = Node(self.TRUE, value=self.current_token.value)
            self.match(Lexer.TRUE)
            return true_value
        elif self.current_token.type == Lexer.FALSE:
            false_value = Node(self.FALSE, value=self.current_token.value)
            self.match(Lexer.FALSE)
            return false_value
        elif self.current_token.type == Lexer.ID:
            return self.parse_identifier()
        return Node(self.EOF, value="Not good")

    def parse_type_str(self):
        if self.current_token.type == Lexer.INTEGERT:
            int_value = Node(self.INTEGERT, value=self.current_token.value)
            self.match(Lexer.INTEGERT)
            return int_value
        elif self.current_token.type == Lexer.DOUBLET:
            double_value = Node(self.DOUBLET, value=self.current_token.value)
            self.match(Lexer.DOUBLET)
            return double_value
        elif self.current_token.type == Lexer.STRINGT:
            string_value = Node(self.STRINGT, value=self.current_token.value)
            self.match(Lexer.STRINGT)
            return string_value
        elif self.current_token.type == Lexer.CHART:
            char_value = Node(self.CHART, value=self.current_token.value)
            self.match(Lexer.CHART)
            return char_value   
        elif self.current_token.type == Lexer.BOOLEANT:
            bolean_value = Node(self.BOOLEANT, value=self.current_token.value)
            self.match(Lexer.BOOLEANT)
            return bolean_value
        return Node(self.EOF, value="Not good")

    def parse_identifier(self):
        identifier = Node(self.ID, value=self.current_token.value)
        self.match(Lexer.ID)
        return identifier

    def parse_expression_statement(self):
        expression = self.parse_expression()
        return Node(self.EXPRESSION_STATEMENT, value = "EXPRESSION", children=[expression])
