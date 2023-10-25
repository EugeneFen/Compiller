from parse import Parser
from lexer import Lexer

class General_code:
    def generate_java_code(self, VB_ast):
        java_code = ""

        print(VB_ast.node_type, " \n")

        if VB_ast.node_type == Parser.PROGRAM:
            for i in range(len(VB_ast.children)):
                self.generate_java_code(VB_ast.children[i])

        elif VB_ast.node_type == Parser.IF_STATEMENT:
            condition = self.generate_java_code(VB_ast.children[0])
            if_body = self.generate_java_code(VB_ast.children[1])
            java_code += f"If ({condition}) \n"
            java_code += "{"
            java_code += f"{if_body}\n"
            java_code += "}"
            if len(VB_ast.children) > 2:
                else_body = self.generate_java_code(VB_ast.children[2])
                java_code += f" else \n"
                java_code += f"{else_body}\n"

        elif VB_ast.node_type == Parser.ID or \
              VB_ast.node_type == Parser.INTEGER or \
              VB_ast.node_type == Parser.DOUBLE or \
              VB_ast.node_type == Parser.STRING or \
              VB_ast.node_type == Parser.CHAR or \
              VB_ast.node_type == Parser.TRUE or \
              VB_ast.node_type == Parser.FALSE:
            java_code += f"{VB_ast.value}  "

        elif VB_ast.node_type == Parser.ADDITION:
            value_term = self.generate_java_code(VB_ast.children[0])
            value_right = self.generate_java_code(VB_ast.children[1])
            java_code += f"{value_term} + {value_right} \n"

        return java_code
