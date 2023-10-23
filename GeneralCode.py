def generate_java_code(VB_ast):
    java_code = ""

    if VB_ast.type == "PROGRAM":
        # Генерация заголовка программы
        program_name = VB_ast.children[0].value
        java_code += f"#include <iostream>\n\n"
        java_code += f"int main()\n"

        # Генерация остальной части программы
        statement_list = VB_ast.children[0]
        java_code += generate_java_code(statement_list)

        # Завершение программы
        java_code += f"\n    return 0;\n"

    elif VB_ast.type == "STATEMENT_LIST":
        for statement in VB_ast.children:
            java_code += generate_java_code(statement)

    elif VB_ast.type == "IF_STATEMENT":
        condition = generate_java_code(VB_ast.children[0])
        if_body = generate_java_code(VB_ast.children[1])
        else_body = generate_java_code(VB_ast.children[2])
        java_code += f"If ({condition}) \n"
        java_code += f"{if_body}\n"
        java_code += f"End If"
        if else_body:
            java_code += f" else \n"
            java_code += f"{else_body}\n"
            java_code += f"End If\n"

    elif VB_ast.type == "WHILE_STATEMENT":
        condition = generate_java_code(pascal_ast.children[0])
        loop_body = generate_java_code(pascal_ast.children[1])
        java_code += f"While ({condition}) \n"
        java_code += f"{loop_body}\n"
        java_code += f"End While\n"

        return java_code
