from lark import Lark

grammar = """
    start: statement+

    ?statement: assignment
              | expr
              | if_stmt
              | while_stmt
              | for_stmt
              | func_def
              | func_call
              | print_stmt
              | return_stmt

    ?assignment: NAME "=" expr
               | NAME compound_op expr -> compound_assignment

    compound_op: "+=" | "-=" | "*=" | "/="

    if_stmt: "if" expr ":" block ("else" ":" block)?
    while_stmt: "while" expr ":" block
    for_stmt: "for" NAME "in" expr ":" block
    func_def: "def" NAME "(" [NAME ("," NAME)*] ")" ":" block
    func_call: NAME "(" [expr ("," expr)*] ")"
    print_stmt: "print" "(" expr ")"
    return_stmt: "return" expr?

    // Simplificar o bloco para não usar INDENT/DEDENT por enquanto
    block: statement
         | "{" statement+ "}"

    ?expr: or_expr
    ?or_expr: and_expr ("or" and_expr)*
    ?and_expr: not_expr ("and" not_expr)*
    ?not_expr: "not" not_expr | comparison
    ?comparison: add_expr (comp_op add_expr)*
    comp_op: "==" | "!=" | "<" | ">" | "<=" | ">="
    ?add_expr: mul_expr (("+" | "-") mul_expr)*
    ?mul_expr: unary_expr (("*" | "/") unary_expr)*
    ?unary_expr: ("+" | "-") unary_expr | primary
    ?primary: atom
    ?atom: NUMBER -> number
         | STRING -> string
         | NAME -> variable
         | list
         | "(" expr ")"
    
    list: "[" [expr ("," expr)*] "]"

    %import common.CNAME -> NAME
    %import common.NUMBER
    %import common.ESCAPED_STRING -> STRING
    %import common.WS
    %ignore WS
"""

def create_lexer():
    return Lark(grammar, parser='lalr')