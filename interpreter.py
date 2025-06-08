from typing import Dict, Any, List, Callable
from dataclasses import dataclass
from enum import Enum, auto


class ValueType(Enum):
    NUMBER = auto()
    STRING = auto()
    BOOLEAN = auto()
    LIST = auto()
    FUNCTION = auto()
    NONE = auto()


@dataclass
class Value:
    type: ValueType
    value: Any

    def __str__(self):
        if self.type == ValueType.STRING:
            return str(self.value)
        elif self.type == ValueType.LIST:
            return "[" + ", ".join(str(item) for item in self.value) + "]"
        elif self.type == ValueType.NONE:
            return "None"
        elif self.type == ValueType.BOOLEAN:
            return "True" if self.value else "False"
        else:
            return str(self.value)


class ReturnException(Exception):
    def __init__(self, value):
        self.value = value


class Interpreter:
    def __init__(self):
        self.variables: Dict[str, Value] = {}
        self.functions: Dict[str, Callable] = {}
        self.current_scope = self.variables
        self.scopes: List[Dict[str, Value]] = [self.variables]

    def enter_scope(self):
        new_scope = {}
        self.scopes.append(new_scope)
        self.current_scope = new_scope

    def exit_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()
            self.current_scope = self.scopes[-1]

    def get_variable(self, name: str) -> Value:
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise NameError(f"Variable '{name}' is not defined")

    def set_variable(self, name: str, value: Value):
        self.current_scope[name] = value

    def interpret(self, ast):
        if isinstance(ast, list):
            result = None
            for node in ast:
                result = self.interpret(node)
                if isinstance(result, dict) and result.get("type") == "return":
                    return result
            return result

        elif isinstance(ast, dict):
            node_type = ast.get("type")

            # Valores básicos
            if node_type == "number":
                return Value(ValueType.NUMBER, ast["value"])
            elif node_type == "string":
                return Value(ValueType.STRING, ast["value"])
            elif node_type == "variable":
                return self.get_variable(ast["name"])
            elif node_type == "list":
                elements = [self.interpret(elem) for elem in ast["elements"]]
                return Value(ValueType.LIST, [elem.value for elem in elements])

            # Programa principal
            elif node_type == "program":
                return self.interpret(ast["statements"])

            # Bloco de código
            elif node_type == "block":
                return self.interpret(ast["statements"])

            # Atribuições
            elif node_type == "assignment":
                var_name = ast["var_name"]
                value = self.interpret(ast["value"])
                self.set_variable(var_name, value)
                return value

            elif node_type == "compound_assignment":
                var_name = ast["var_name"]
                current = self.get_variable(var_name)
                new_value = self.interpret(ast["value"])
                op = ast["op"].rstrip("=")  # Remove '=' from '+=' etc.
                result = self.evaluate_binary_op(current, new_value, op)
                self.set_variable(var_name, result)
                return result

            # Operações
            elif node_type == "binary_op":
                left = self.interpret(ast["left"])
                right = self.interpret(ast["right"])
                op = ast["op"]
                return self.evaluate_binary_op(left, right, op)

            elif node_type == "unary_op":
                operand = self.interpret(ast["operand"])
                op = ast["op"]
                return self.evaluate_unary_op(operand, op)

            # Estruturas de controle
            elif node_type == "if":
                condition = self.interpret(ast["condition"])
                if self.is_truthy(condition):
                    return self.interpret(ast["then"])
                elif ast.get("else"):
                    return self.interpret(ast["else"])

            elif node_type == "while":
                while True:
                    condition = self.interpret(ast["condition"])
                    if not self.is_truthy(condition):
                        break
                    result = self.interpret(ast["body"])
                    if isinstance(result, dict) and result.get("type") == "return":
                        return result

            elif node_type == "for":
                var_name = ast["var"]
                iterable = self.interpret(ast["iterable"])

                if iterable.type != ValueType.LIST:
                    raise TypeError(f"'{iterable.type}' object is not iterable")

                for item in iterable.value:
                    self.set_variable(var_name, Value(self._infer_type(item), item))
                    result = self.interpret(ast["body"])
                    if isinstance(result, dict) and result.get("type") == "return":
                        return result

            # Funções
            elif node_type == "function_def":
                name = ast["name"]
                params = ast["params"]
                body = ast["body"]
                self.functions[name] = {"params": params, "body": body}
                return Value(ValueType.FUNCTION, name)

            elif node_type == "function_call":
                name = ast["name"]
                args = [self.interpret(arg) for arg in ast["args"]]
                return self.call_function(name, args)

            elif node_type == "return":
                value = (
                    self.interpret(ast["value"])
                    if ast.get("value")
                    else Value(ValueType.NONE, None)
                )
                return {"type": "return", "value": value}

            # Print
            elif node_type == "print":
                value = self.interpret(ast["value"])
                print(value)
                return value

        return Value(ValueType.NONE, None)

    def evaluate_binary_op(self, left: Value, right: Value, op: str) -> Value:
        # Operações aritméticas
        if op == "+":
            if left.type == ValueType.NUMBER and right.type == ValueType.NUMBER:
                return Value(ValueType.NUMBER, left.value + right.value)
            elif left.type == ValueType.STRING and right.type == ValueType.STRING:
                return Value(ValueType.STRING, left.value + right.value)
            elif left.type == ValueType.LIST and right.type == ValueType.LIST:
                return Value(ValueType.LIST, left.value + right.value)
        elif op == "-":
            if left.type == ValueType.NUMBER and right.type == ValueType.NUMBER:
                return Value(ValueType.NUMBER, left.value - right.value)
        elif op == "*":
            if left.type == ValueType.NUMBER and right.type == ValueType.NUMBER:
                return Value(ValueType.NUMBER, left.value * right.value)
        elif op == "/":
            if left.type == ValueType.NUMBER and right.type == ValueType.NUMBER:
                if right.value == 0:
                    raise ZeroDivisionError("Division by zero")
                return Value(ValueType.NUMBER, left.value / right.value)

        # Operações de comparação
        elif op == "==":
            return Value(ValueType.BOOLEAN, left.value == right.value)
        elif op == "!=":
            return Value(ValueType.BOOLEAN, left.value != right.value)
        elif op == "<":
            return Value(ValueType.BOOLEAN, left.value < right.value)
        elif op == ">":
            return Value(ValueType.BOOLEAN, left.value > right.value)
        elif op == "<=":
            return Value(ValueType.BOOLEAN, left.value <= right.value)
        elif op == ">=":
            return Value(ValueType.BOOLEAN, left.value >= right.value)

        # Operações lógicas
        elif op == "and":
            return Value(
                ValueType.BOOLEAN, self.is_truthy(left) and self.is_truthy(right)
            )
        elif op == "or":
            return Value(
                ValueType.BOOLEAN, self.is_truthy(left) or self.is_truthy(right)
            )

        raise TypeError(f"Invalid operation {op} between {left.type} and {right.type}")

    def evaluate_unary_op(self, operand: Value, op: str) -> Value:
        if op == "not":
            return Value(ValueType.BOOLEAN, not self.is_truthy(operand))
        elif op == "-":
            if operand.type == ValueType.NUMBER:
                return Value(ValueType.NUMBER, -operand.value)
        elif op == "+":
            if operand.type == ValueType.NUMBER:
                return Value(ValueType.NUMBER, +operand.value)

        raise TypeError(f"Invalid unary operation {op} on {operand.type}")

    def is_truthy(self, value: Value) -> bool:
        if value.type == ValueType.BOOLEAN:
            return value.value
        elif value.type == ValueType.NUMBER:
            return value.value != 0
        elif value.type == ValueType.STRING:
            return len(value.value) > 0
        elif value.type == ValueType.LIST:
            return len(value.value) > 0
        elif value.type == ValueType.NONE:
            return False
        return True

    def _infer_type(self, value) -> ValueType:
        if isinstance(value, (int, float)):
            return ValueType.NUMBER
        elif isinstance(value, str):
            return ValueType.STRING
        elif isinstance(value, list):
            return ValueType.LIST
        elif isinstance(value, bool):
            return ValueType.BOOLEAN
        else:
            return ValueType.NONE

    def call_function(self, name: str, args: List[Value]) -> Value:
        if name not in self.functions:
            raise NameError(f"Function '{name}' is not defined")

        func_def = self.functions[name]
        params = func_def["params"]
        body = func_def["body"]

        if len(params) != len(args):
            raise TypeError(
                f"Function '{name}' expects {len(params)} arguments, got {len(args)}"
            )

        self.enter_scope()
        try:
            # Bind parameters to arguments
            for param, arg in zip(params, args):
                self.set_variable(param, arg)

            # Execute function body
            result = self.interpret(body)

            # Handle return value
            if isinstance(result, dict) and result.get("type") == "return":
                return result["value"]
            else:
                return Value(ValueType.NONE, None)

        finally:
            self.exit_scope()


if __name__ == "__main__":
    # Test the interpreter
    from parser import parse_code

    interpreter = Interpreter()

    test_code = """
def add(a, b):
    return a + b

x = 5
y = 10
z = add(x, y)
print(z)
"""

    try:
        ast = parse_code(test_code)
        result = interpreter.interpret(ast)
        print("Variables:", {k: str(v) for k, v in interpreter.variables.items()})
    except Exception as e:
        print(f"Error: {e}")
