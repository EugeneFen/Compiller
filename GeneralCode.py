from parse import Parser
import sys

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

    def get_expression_list(self, VB_ast):
        java_code = ""
        for i in range(len(VB_ast.children)):
            java_code += self.general_statement(VB_ast.children[i])
        return java_code

    def general_statement(self, VB_ast):
        type_get = self.get_expression(VB_ast)
        if VB_ast.node_type == Parser.IF_STATEMENT:
            return self.general_if_statement(VB_ast)
        elif VB_ast.node_type == Parser.EXPRESSION_STATEMENT:
            code = ""
            #print(len(VB_ast.children))
            for i in range(len(VB_ast.children)):
                code += f" {self.get_expression_statement(VB_ast.children[i])}"
            return f"{code} \n"
        return f"{type_get} \n"

    def general_if_statement(self, VB_ast):
        java_code = ""
        condition = self.general_statement(VB_ast.children[0])
        if_body = self.get_expression_list(VB_ast.children[1]) #!!!!!!!!!!!!
        java_code += f"If ({condition}) \n"
        java_code += "{ \n"
        java_code += f"  {if_body}"
        java_code += "} \n"
        if len(VB_ast.children) > 2:
            else_body = self.general_statement(VB_ast.children[2].children[0]) #!!!!!!!!!!!!!
            java_code += f"Else \n"
            java_code += "{ \n"
            java_code += f"  {else_body}"
            java_code += "}"
        return java_code

    def get_expression(self, VB_ast):
        term = self.get_special_words(VB_ast)
        if VB_ast.node_type == Parser.ADDITION:
            if VB_ast.children[1].children:
                chill = self.get_expression(VB_ast.children[1])
                term = f"{VB_ast.children[0].value} + {chill}"
            else:
                term = f"{VB_ast.children[0].value} + {VB_ast.children[1].value}"
        elif VB_ast.node_type == Parser.SUBTRACTION:
            if VB_ast.children[1].children:
                chill = self.get_expression(VB_ast.children[1])
                term = f" {VB_ast.children[0].value} - {chill} "
            else:
                term = f" {VB_ast.children[0].value} - {VB_ast.children[1].value} "
        elif VB_ast.node_type == Parser.COMPARISON_EQ:
            if VB_ast.children[1].children:
                chill = self.get_expression(VB_ast.children[1])
                term = f" {VB_ast.children[0].value} = {chill} "
            else:
                term = f" {VB_ast.children[0].value} = {VB_ast.children[1].value} "
        elif VB_ast.node_type == Parser.COMPARISON_LE:
            if VB_ast.children[1].children:
                chill = self.get_expression(VB_ast.children[1])
                term = f" {VB_ast.children[0].value} < {chill} "
            else:
                term = f"{VB_ast.children[0].value} < {VB_ast.children[1].value}"
        elif VB_ast.node_type == Parser.COMPARISON_MO:
            if VB_ast.children[1].children:
                chill = self.get_expression(VB_ast.children[1])
                term = f" {VB_ast.children[0].value} > {chill} "
            else:
                term = f"{VB_ast.children[0].value} > {VB_ast.children[1].value}"
        elif VB_ast.node_type == Parser.COMPARISON_NOTEQ:
            if VB_ast.children[1].children:
                chill = self.get_expression(VB_ast.children[1])
                term = f" {VB_ast.children[0].value} <> {chill} "
            else:
                term = f" {VB_ast.children[0].value} <> {VB_ast.children[1].value} "
        elif VB_ast.node_type == Parser.MULTIPLICATION:
            if VB_ast.children[1].children:
                chill = self.get_expression(VB_ast.children[1])
                term = f" {VB_ast.children[0].value} * {chill} "
            else:
                term = f" {VB_ast.children[0].value} * {VB_ast.children[1].value} "
        elif VB_ast.node_type == Parser.DIVISION:
            if VB_ast.children[1].children:
                chill = self.get_expression(VB_ast.children[1])
                term = f" {VB_ast.children[0].value} / {chill} "
            else:
                term = f" {VB_ast.children[0].value} / {VB_ast.children[1].value} "
        return term

    def get_special_words(self, VB_ast):
        special_words = self.get_code_type(VB_ast)
        if VB_ast.node_type == Parser.AND:
            first_element = self.get_expression(VB_ast.children[0])
            second_element = self.get_expression(VB_ast.children[1])
            special_words = f"{first_element} and {second_element}"
        return special_words

    def get_expression_statement(self, VB_ast):
        expression = self.general_statement(VB_ast)
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
            code = f"{VB_ast.value}"
            return code
        return f"Not value {VB_ast.value}"






