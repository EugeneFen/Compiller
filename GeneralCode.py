from parse import Parser
from lexer import Lexer

class General_code:
    def error(self, message):
        print("Error: ", message)
        sys.exit(1)

    def generate_java_code(self, VB_ast):
        java_code = ""

        #print(VB_ast.node_type, " \n")

        if VB_ast.node_type == Parser.PROGRAM:
            for i in range(len(VB_ast.children)):
                java_code += self.general_statement(VB_ast.children[i])
        print(java_code)

    def general_statement(self, VB_ast):
        type_get = self.get_code_type(VB_ast)
        if VB_ast.node_type == Parser.IF_STATEMENT:
            return self.general_if_statement(VB_ast)
        elif VB_ast.node_type == Parser.EXPRESSION_STATEMENT:
            code = ""
            print(len(VB_ast.children))
            for i in range(len(VB_ast.children)):
                code += f" {self.get_expression_statement(VB_ast.children[i])} \n"
            return code
        return f"{type_get} \n"

    def general_if_statement(self, VB_ast):
        java_code = ""
        condition = self.get_expression(VB_ast.children[0])
        if_body = self.general_statement(VB_ast.children[1].children[0])
        java_code += f"If ({condition}) \n"
        java_code += "{ \n"
        java_code += f"  {if_body}"
        java_code += "}"
        if len(VB_ast.children) > 2:
            else_body = self.general_statement(VB_ast.children[2])
            java_code += f" else \n"
            java_code += f"{else_body}\n"
        return java_code

    def get_expression(self, VB_ast):
        term = self.get_term(VB_ast)
        if VB_ast.node_type == Parser.ADDITION:
            term = f" {VB_ast.children[0].value} + {VB_ast.children[1].value} "
        elif VB_ast.node_type == Parser.SUBTRACTION:
            term = f" {VB_ast.children[0].value} - {VB_ast.children[1].value} "
        elif VB_ast.node_type == Parser.COMPARISON_EQ:
            term = f" {VB_ast.children[0].value} = {VB_ast.children[1].value} "
        elif VB_ast.node_type == Parser.COMPARISON_LE:
            term = f" {VB_ast.children[0].value} < {VB_ast.children[1].value} "
        elif VB_ast.node_type == Parser.COMPARISON_MO:
            term = f" {VB_ast.children[0].value} > {VB_ast.children[1].value} "
        elif VB_ast.node_type == Parser.COMPARISON_NOTEQ:
            term = f" {VB_ast.children[0].value} <> {VB_ast.children[1].value} "
        return term

    def get_term(self, VB_ast):
        factor = self.get_code_type(VB_ast)
        if VB_ast.node_type == Parser.MULTIPLICATION:
            factor = f" {VB_ast.children[0].value} * {VB_ast.children[1].value} "
        elif VB_ast.node_type == Parser.DIVISION:
            factor = f" {VB_ast.children[0].value} / {VB_ast.children[1].value} "
        return factor

    def parse_identifier(self):
        identifier = Node(self.ID, value=self.current_token.value)
        self.match(Lexer.ID)
        return identifier

    def get_expression_statement(self, VB_ast):
        expression = self.get_expression(VB_ast)
        return expression

    def get_code_type(self, VB_ast):
        if VB_ast.node_type == Parser.ID or \
              VB_ast.node_type == Parser.INTEGER or \
              VB_ast.node_type == Parser.DOUBLE or \
              VB_ast.node_type == Parser.STRING or \
              VB_ast.node_type == Parser.CHAR or \
              VB_ast.node_type == Parser.TRUE or \
              VB_ast.node_type == Parser.INTEGERT or \
              VB_ast.node_type == Parser.DOUBLET or \
              VB_ast.node_type == Parser.STRINGT or \
              VB_ast.node_type == Parser.CHART or \
              VB_ast.node_type == Parser.FALSE or \
              VB_ast.node_type == Parser.BOOLEANT:
            code = VB_ast.value
            print(VB_ast.value, "Type \n")
            return code






