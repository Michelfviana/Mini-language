from lark import Transformer
from lexer import create_lexer


class MiniLangTransformer(Transformer):
    def start(self, items):
        return {"type": "program", "statements": items}

    def number(self, items):
        value = items[0]
        if "." in str(value):
            return {"type": "number", "value": float(value)}
        else:
            return {"type": "number", "value": int(value)}

    def string(self, items):
        # Remove aspas da string
        value = str(items[0])[1:-1]  # Remove primeira e última aspas
        return {"type": "string", "value": value}

    def variable(self, items):
        return {"type": "variable", "name": str(items[0])}

    def list(self, items):
        return {"type": "list", "elements": list(items)}

    def assignment(self, items):
        var_name = str(items[0])
        value = items[1]
        return {"type": "assignment", "var_name": var_name, "value": value}

    def compound_assignment(self, items):
        var_name = str(items[0])
        op = str(items[1])
        value = items[2]
        return {
            "type": "compound_assignment",
            "var_name": var_name,
            "op": op,
            "value": value,
        }

    def if_stmt(self, items):
        condition = items[0]
        then_block = items[1]
        else_block = items[2] if len(items) > 2 else None
        return {
            "type": "if",
            "condition": condition,
            "then": then_block,
            "else": else_block,
        }

    def while_stmt(self, items):
        condition = items[0]
        body = items[1]
        return {"type": "while", "condition": condition, "body": body}

    def for_stmt(self, items):
        var_name = str(items[0])
        iterable = items[1]
        body = items[2]
        return {"type": "for", "var": var_name, "iterable": iterable, "body": body}

    def func_def(self, items):
        name = str(items[0])
        params = [str(param) for param in items[1:-1]]
        body = items[-1]
        return {"type": "function_def", "name": name, "params": params, "body": body}

    def func_call(self, items):
        name = str(items[0])
        args = list(items[1:]) if len(items) > 1 else []
        return {"type": "function_call", "name": name, "args": args}

    def print_stmt(self, items):
        value = items[0]
        return {"type": "print", "value": value}

    def return_stmt(self, items):
        value = items[0] if items else None
        return {"type": "return", "value": value}

    def block(self, items):
        return {"type": "block", "statements": items}

    def or_expr(self, items):
        if len(items) == 1:
            return items[0]
        left = items[0]
        for i in range(1, len(items)):
            right = items[i]
            left = {"type": "binary_op", "left": left, "op": "or", "right": right}
        return left

    def and_expr(self, items):
        if len(items) == 1:
            return items[0]
        left = items[0]
        for i in range(1, len(items)):
            right = items[i]
            left = {"type": "binary_op", "left": left, "op": "and", "right": right}
        return left

    def not_expr(self, items):
        if len(items) == 1:
            return items[0]
        return {"type": "unary_op", "op": "not", "operand": items[1]}

    def comparison(self, items):
        if len(items) == 1:
            return items[0]
        left = items[0]
        op = str(items[1])
        right = items[2]
        return {"type": "binary_op", "left": left, "op": op, "right": right}

    def add_expr(self, items):
        if len(items) == 1:
            return items[0]
        result = items[0]
        for i in range(1, len(items), 2):
            op = str(items[i])
            right = items[i + 1]
            result = {"type": "binary_op", "left": result, "op": op, "right": right}
        return result

    def mul_expr(self, items):
        if len(items) == 1:
            return items[0]
        result = items[0]
        for i in range(1, len(items), 2):
            op = str(items[i])
            right = items[i + 1]
            result = {"type": "binary_op", "left": result, "op": op, "right": right}
        return result

    def unary_expr(self, items):
        if len(items) == 1:
            return items[0]
        op = str(items[0])
        operand = items[1]
        return {"type": "unary_op", "op": op, "operand": operand}


class Parser:
    def __init__(self):
        self.lexer, self.transformer = create_parser()

    def parse(self, code):
        tree = self.lexer.parse(code)
        ast = self.transformer.transform(tree)
        return ast


def create_parser():
    lexer = create_lexer()
    transformer = MiniLangTransformer()
    return lexer, transformer


def parse_code(code):
    lexer, transformer = create_parser()
    tree = lexer.parse(code)
    ast = transformer.transform(tree)
    return ast
