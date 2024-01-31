from parse import Parser
import sys

class General_code:
    def error(self, message):
        print("Error general code: ", message)
        sys.exit(1)

    def generate_java_code(self, VB_ast):
        java_code = ""

        #print(VB_ast.node_type, " \n")

        if VB_ast.type == Parser.PROGRAM:
            for i in range(len(VB_ast.children)):
                print(f"{VB_ast.children} 1")
                java_code += self.general_statement(VB_ast.children[i])
        print(java_code)

    def get_expression_list(self, VB_ast):
        java_code = ""
        for i in range(len(VB_ast.children)):
            print(f"{VB_ast.children} 2")
            java_code += self.general_statement(VB_ast.children[i])
        return java_code

    def general_statement(self, VB_ast):
        type_get = self.get_expression(VB_ast)
        if VB_ast.type == Parser.IF_STATEMENT:
            return self.general_if_statement(VB_ast)
        elif VB_ast.type == Parser.WHILE_STATEMENT:
            return self.general_while_statement(VB_ast)
        elif VB_ast.type == Parser.FOR:
            return self.general_for_statement(VB_ast)
        elif VB_ast.type == Parser.WRITE:
            return self.general_write_statement(VB_ast)
        elif VB_ast.type == Parser.WRITELINE:
            return self.general_writeline_statement(VB_ast)
        elif VB_ast.type == Parser.DIMV:
            return self.general_dim_statement(VB_ast)
        elif VB_ast.type == Parser.EXPRESSION_STATEMENT:
            code = ""
            #print(len(VB_ast.children))
            for i in range(len(VB_ast.children)):
                code += f"{self.get_expression_statement(VB_ast.children[i])}"
            return f"{code}"
        return f"{type_get}"

    def general_if_statement(self, VB_ast):
        condition = self.general_statement(VB_ast.children[0])
        if_body = self.get_expression_list(VB_ast.children[1]) #!!!!!!!!!!!!
        java_code = f"If ({condition}) \n"
        java_code += "{ \n"
        java_code += f"{if_body}"
        java_code += "} \n"
        if len(VB_ast.children) > 2:
            else_body = self.general_statement(VB_ast.children[2].children[0]) #!!!!!!!!!!!!!
            java_code += f"Else \n"
            java_code += "{ \n"
            java_code += f"{else_body}"
            java_code += "} \n"
        return java_code

    def general_while_statement(self, VB_ast):
        condition = self.general_statement(VB_ast.children[0])
        while_body = self.get_expression_list(VB_ast.children[1])
        java_code = f"While ({condition}) \n"
        java_code += "{ \n"
        java_code += f"{while_body}"
        java_code += "} \n"
        return java_code

    def general_for_statement(self, VB_ast):
        java_code = ""
        up_down = self.general_statement(VB_ast.children[0])
        condition = self.general_statement(VB_ast.children[1])
        if len(VB_ast.children) == 6:
            str_as = self.get_str_type(VB_ast.children[2])
            first_value = self.general_statement(VB_ast.children[3])
            second_value = self.general_statement(VB_ast.children[4])
            body_for = self.get_expression_list(VB_ast.children[5])
            if up_down == "up":
                java_code += f"For ({str_as} {condition} = {first_value}; {condition} < {second_value}; {condition}++) "
            else:
                java_code += f"For ({str_as} {condition} = {first_value}; {condition} > {second_value}; {condition}--) "
            java_code += "{ \n"
            java_code += f"{body_for} "
            java_code += "} \n"
        else:
            first_value = self.general_statement(VB_ast.children[2])
            second_value = self.general_statement(VB_ast.children[3])
            body_for = self.get_expression_list(VB_ast.children[4])
            str_as = self.get_str_type(VB_ast.children[2])
            if up_down == "up":
                java_code += f"For ({str_as} {condition} = {first_value}; {condition} < {second_value}; {condition}++) "
            else:
                java_code += f"For ({str_as} {condition} = {first_value}; {condition} > {second_value}; {condition}--) "
            java_code += "{ \n"
            java_code += f"{body_for} "
            java_code += "} \n"
        return java_code

    def get_str_type_more(self, VB_ast):
        str_type = self.get_str_type(VB_ast)
        if VB_ast.type == Parser.STRING or VB_ast.type == Parser.STRINGT:
            return "String"
        elif VB_ast.type == Parser.CHAR or VB_ast.type == Parser.CHART:
            return "char"
        elif VB_ast.type == Parser.BOOLEANT:
            return "boolean"
        return str_type

    def get_str_type(self, VB_ast):
        if VB_ast.type == Parser.INTEGERT or VB_ast.type == Parser.INTEGER:
            return "int"
        elif VB_ast.type == Parser.DOUBLET or VB_ast.type == Parser.DOUBLE:
            return "double"
        return self.error(f"Not type {VB_ast.value}")

    def general_write_statement(self, VB_ast): #more children
        return f"System.out.print({VB_ast.children[0].value});"

    def general_writeline_statement(self, VB_ast):
        return f"System.out.println({VB_ast.children[0].value});"

    def general_dim_statement(self, VB_ast):
        str_type = self.get_str_type_more(VB_ast.children[1])
        java_code = f"{str_type} {VB_ast.children[0].value}"
        if len(VB_ast.children) == 3:
            java_code += f" = {VB_ast.children[2].value}"
        java_code += ";"
        return java_code

    def get_expression(self, VB_ast):
        term = self.get_special_words(VB_ast)
        if VB_ast.type == Parser.ADDITION:
            if VB_ast.children[1].children:
                chill = self.get_expression(VB_ast.children[1])
                term = f"{VB_ast.children[0].value} + {chill}  "
            else:
                term = f"{VB_ast.children[0].value} + {VB_ast.children[1].value}  "
        elif VB_ast.type == Parser.SUBTRACTION:
            if VB_ast.children[1].children:
                chill = self.get_expression(VB_ast.children[1])
                term = f"{VB_ast.children[0].value} - {chill} \n"
            else:
                term = f"{VB_ast.children[0].value} - {VB_ast.children[1].value} \n"
        elif VB_ast.type == Parser.COMPARISON_EQ:
            if VB_ast.children[1].children:
                chill = self.get_expression(VB_ast.children[1])
                term = f"{VB_ast.children[0].value} = {chill} ;\n"
            else:
                term = f"{VB_ast.children[0].value} = {VB_ast.children[1].value} ;\n"
        elif VB_ast.type == Parser.COMPARISON_LE:
            if VB_ast.children[1].children:
                chill = self.get_expression(VB_ast.children[1])
                term = f"{VB_ast.children[0].value} < {chill}  "
            else:
                term = f"{VB_ast.children[0].value} < {VB_ast.children[1].value}  "
        elif VB_ast.type == Parser.COMPARISON_MO:
            if VB_ast.children[1].children:
                chill = self.get_expression(VB_ast.children[1])
                term = f"{VB_ast.children[0].value} > {chill}  "
            else:
                term = f"{VB_ast.children[0].value} > {VB_ast.children[1].value}  "
        elif VB_ast.type == Parser.COMPARISON_NOTEQ:
            if VB_ast.children[1].children:
                chill = self.get_expression(VB_ast.children[1])
                term = f"{VB_ast.children[0].value} <> {chill}  "
            else:
                term = f"{VB_ast.children[0].value} <> {VB_ast.children[1].value}  "
        elif VB_ast.type == Parser.MULTIPLICATION:
            if VB_ast.children[1].children:
                chill = self.get_expression(VB_ast.children[1])
                term = f"{VB_ast.children[0].value} * {chill} \n"
            else:
                term = f"{VB_ast.children[0].value} * {VB_ast.children[1].value} \n"
        elif VB_ast.type == Parser.DIVISION:
            if VB_ast.children[1].children:
                chill = self.get_expression(VB_ast.children[1])
                term = f"{VB_ast.children[0].value} / {chill} \n"
            else:
                term = f"{VB_ast.children[0].value} / {VB_ast.children[1].value} \n"
        return term

    def get_special_words(self, VB_ast):
        special_words = self.get_code_type(VB_ast)
        if VB_ast.type == Parser.AND:
            first_element = self.get_expression(VB_ast.children[0])
            second_element = self.get_expression(VB_ast.children[1])
            special_words = f"{first_element} and {second_element}"
        return special_words

    def get_expression_statement(self, VB_ast):
        expression = self.general_statement(VB_ast)
        return expression

    def get_code_type(self, VB_ast):
        if VB_ast.type == Parser.ID or \
              VB_ast.type == Parser.INTEGER or \
              VB_ast.type == Parser.DOUBLE or \
              VB_ast.type == Parser.STRING or \
              VB_ast.type == Parser.CHAR or \
              VB_ast.type == Parser.TRUE or \
              VB_ast.type == Parser.INTEGERT or \
              VB_ast.type == Parser.DOUBLET or \
              VB_ast.type == Parser.STRINGT or \
              VB_ast.type == Parser.CHART or \
              VB_ast.type == Parser.FALSE or \
              VB_ast.type == Parser.BOOLEANT:
            code = VB_ast.value
            return code
        return f"Not value type {VB_ast.value}"
