#!/usr/bin/env python3
"""
MiniLang - A Mini Programming Language
Complete interpreter implemented with PLY (Python Lex-Yacc)

Features:
- Lexical and syntactic analysis
- Data types: int, float, string, list
- Variables and scopes (local/global)
- Arithmetic and logical operations
- Control structures: if/else, while, for
- Functions with parameters and return
- Simple and compound assignments
"""

import ply.lex as lex
import ply.yacc as yacc
import sys
from typing import Any, Dict, List, Optional, Union

# =============================================================================
# LEXICAL ANALYSIS (LEXER)
# =============================================================================


class MiniLangLexer:
    """Lexical analyzer for MiniLang"""

    # Tokens
    # Define tokens used by the lexer
    tokens = (
        "NUMBER",  # Integer numbers (e.g., 42, 123)
        "FLOAT",  # Floating point numbers (e.g., 3.14, 2.5)
        "STRING",  # String literals (e.g., "hello", "world")
        "IDENTIFIER",  # Variable/function names (e.g., x, my_var)
        "PLUS",  # Addition operator (+)
        "MINUS",  # Subtraction operator (-)
        "TIMES",  # Multiplication operator (*)
        "DIVIDE",  # Division operator (/)
        "MODULO",  # Modulo operator (%)
        "ASSIGN",  # Assignment operator (=)
        "PLUS_ASSIGN",  # Compound assignment (+=)
        "MINUS_ASSIGN",  # Compound assignment (-=)
        "TIMES_ASSIGN",  # Compound assignment (*=)
        "POWER_ASSIGN"  # Compound assignment (**=)
        "DIVIDE_ASSIGN",  # Compound assignment (/=)
        "EQ",  # Equality operator (==)
        "NE",  # Not equal operator (!=)
        "LT",  # Less than operator (<)
        "LE",  # Less than or equal operator (<=)
        "GT",  # Greater than operator (>)
        "GE",  # Greater than or equal operator (>=)
        "AND",  # Logical AND operator (and)
        "OR",  # Logical OR operator (or)
        "NOT",  # Logical NOT operator (not)
        "LPAREN",  # Left parenthesis (()
        "RPAREN",  # Right parenthesis ())
        "LBRACKET",  # Left square bracket ([)
        "RBRACKET",  # Right square bracket (])
        "COMMA",  # Comma separator (,)
        "COLON",  # Colon (:)
        "NEWLINE",  # Newline character (\n)
        "IF",  # if keyword
        "ELSE",  # else keyword
        "WHILE",  # while keyword
        "FOR",  # for keyword
        "IN",  # in keyword
        "DEF",  # def keyword (function definition)
        "RETURN",  # return keyword
        "TRUE",  # True boolean literal
        "FALSE",  # False boolean literal
        "PRINT",  # print built-in function
        "LEN",  # len built-in function
    )

    # Reserved words
    reserved = {
        "if": "IF",
        "else": "ELSE",
        "while": "WHILE",
        "for": "FOR",
        "in": "IN",
        "def": "DEF",
        "return": "RETURN",
        "True": "TRUE",
        "False": "FALSE",
        "print": "PRINT",
        "len": "LEN",
        "and": "AND",
        "or": "OR",
        "not": "NOT",
    }

    # Token rules
    t_PLUS = r"\+"
    t_MINUS = r"-"
    t_TIMES = r"\*"
    t_POWER = r"\*\*"
    t_DIVIDE = r"/"
    t_MODULO = r"%"
    t_ASSIGN = r"="
    t_PLUS_ASSIGN = r"\+="
    t_MINUS_ASSIGN = r"-="
    t_TIMES_ASSIGN = r"\*="
    t_DIVIDE_ASSIGN = r"/="
    t_EQ = r"=="
    t_NE = r"!="
    t_LT = r"<"
    t_LE = r"<="
    t_GT = r">"
    t_GE = r">="
    t_LPAREN = r"\("
    t_RPAREN = r"\)"
    t_LBRACKET = r"\["
    t_RBRACKET = r"\]"
    t_COMMA = r","
    t_COLON = r":"

    # Ignore spaces and tabs
    t_ignore = " \t"

    def t_FLOAT(self, t):
        r"\d+\.\d+"
        t.value = float(t.value)
        return t

    def t_NUMBER(self, t):
        r"\d+"
        t.value = int(t.value)
        return t

    def t_STRING(self, t):
        r'"([^"\\]|\\.)*"'
        t.value = t.value[1:-1]  # Remove quotes
        return t

    def t_IDENTIFIER(self, t):
        r"[a-zA-Z_][a-zA-Z_0-9]*"
        t.type = self.reserved.get(t.value, "IDENTIFIER")
        return t

    def t_NEWLINE(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value)
        return t

    def t_COMMENT(self, t):
        r"\#.*"
        pass  # Ignore comments

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        return self.lexer


# =============================================================================
# SYNTACTIC ANALYSIS (PARSER) AND INTERPRETER
# =============================================================================


class Environment:
    """Execution environment for variables and functions"""

    def __init__(self, parent=None):
        self.parent = parent
        self.variables = {}
        self.functions = {}

    def get(self, name):
        if name in self.variables:
            return self.variables[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise NameError(f"Variable '{name}' not defined")

    def set(self, name, value):
        self.variables[name] = value

    def define_function(self, name, func):
        self.functions[name] = func

    def get_function(self, name):
        if name in self.functions:
            return self.functions[name]
        elif self.parent:
            return self.parent.get_function(name)
        else:
            raise NameError(f"Function '{name}' not defined")


class Function:
    """Represents a user-defined function"""

    def __init__(self, name, params, body, env):
        self.name = name
        self.params = params
        self.body = body
        self.closure_env = env


class ReturnException(Exception):
    """Exception to implement return in functions"""

    def __init__(self, value):
        self.value = value


class MiniLangParser:
    """Syntactic analyzer and interpreter for MiniLang"""

    def __init__(self):
        self.lexer = MiniLangLexer()
        self.lexer.build()
        self.tokens = self.lexer.tokens
        self.global_env = Environment()
        self.current_env = self.global_env
        self.parser = yacc.yacc(module=self, debug=False, write_tables=False)

    # Operator precedence
    precedence = (
        ("left", "OR"),
        ("left", "AND"),
        ("left", "EQ", "NE"),
        ("left", "LT", "LE", "GT", "GE"),
        ("left", "PLUS", "MINUS"),
        ("left", "TIMES", "DIVIDE", "MODULO"),
        ("right", "POWER"),
        ("right", "UMINUS", "NOT"),
    )

    # Grammar rules
    def p_program(self, p):
        """program : statement_list"""
        p[0] = p[1]

    def p_statement_list(self, p):
        """statement_list : statement_list statement
        | statement"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_statement(self, p):
        """statement : assignment_stmt
        | expression_stmt
        | if_stmt
        | while_stmt
        | for_stmt
        | function_def
        | return_stmt
        | print_stmt
        | NEWLINE"""
        p[0] = p[1]

    def p_assignment_stmt(self, p):
        """assignment_stmt : IDENTIFIER ASSIGN expression NEWLINE
        | IDENTIFIER PLUS_ASSIGN expression NEWLINE
        | IDENTIFIER MINUS_ASSIGN expression NEWLINE
        | IDENTIFIER TIMES_ASSIGN expression NEWLINE
        | IDENTIFIER DIVIDE_ASSIGN expression NEWLINE"""
        var_name = p[1]
        operator = p[2]
        value = self.evaluate(p[3])

        if operator == "=":
            self.current_env.set(var_name, value)
        elif operator == "+=":
            old_value = self.current_env.get(var_name)
            self.current_env.set(var_name, old_value + value)
        elif operator == "-=":
            old_value = self.current_env.get(var_name)
            self.current_env.set(var_name, old_value - value)
        elif operator == "*=":
            old_value = self.current_env.get(var_name)
            self.current_env.set(var_name, old_value * value)
        elif operator == "/=":
            old_value = self.current_env.get(var_name)
            self.current_env.set(var_name, old_value / value)
        elif operator == "**=":
            old_value = self.current_env.get(var_name)
            self.current_env.set(var_name, old_value**value)

        p[0] = ("assign", var_name, value)

    def p_expression_stmt(self, p):
        """expression_stmt : expression NEWLINE"""
        result = self.evaluate(p[1])
        if result is not None:
            print(self.format_value(result))
        p[0] = ("expr_stmt", p[1])

    def p_if_stmt(self, p):
        """if_stmt : IF expression COLON NEWLINE statement_list
        | IF expression COLON NEWLINE statement_list ELSE COLON NEWLINE statement_list
        """
        condition = self.evaluate(p[2])
        if condition:
            self.execute_statements(p[5])
        elif len(p) == 10:  # has else
            self.execute_statements(p[9])
        p[0] = ("if", p[2], p[5], p[9] if len(p) == 10 else None)

    def p_while_stmt(self, p):
        """while_stmt : WHILE expression COLON NEWLINE statement_list"""
        while self.evaluate(p[2]):
            try:
                self.execute_statements(p[5])
            except ReturnException:
                break
        p[0] = ("while", p[2], p[5])

    def p_for_stmt(self, p):
        """for_stmt : FOR IDENTIFIER IN expression COLON NEWLINE statement_list"""
        var_name = p[2]
        iterable = self.evaluate(p[4])

        if not isinstance(iterable, list):
            raise TypeError("Object is not iterable")

        for item in iterable:
            self.current_env.set(var_name, item)
            try:
                self.execute_statements(p[7])
            except ReturnException:
                break

        p[0] = ("for", var_name, p[4], p[7])

    def p_function_def(self, p):
        """function_def : DEF IDENTIFIER LPAREN parameter_list RPAREN COLON NEWLINE statement_list
        | DEF IDENTIFIER LPAREN RPAREN COLON NEWLINE statement_list"""
        func_name = p[2]
        params = p[4] if len(p) == 9 else []
        body = p[8] if len(p) == 9 else p[7]

        func = Function(func_name, params, body, self.current_env)
        self.current_env.define_function(func_name, func)
        p[0] = ("function_def", func_name, params, body)

    def p_parameter_list(self, p):
        """parameter_list : parameter_list COMMA IDENTIFIER
        | IDENTIFIER"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_return_stmt(self, p):
        """return_stmt : RETURN expression NEWLINE
        | RETURN NEWLINE"""
        value = self.evaluate(p[2]) if len(p) == 4 else None
        raise ReturnException(value)

    def p_print_stmt(self, p):
        """print_stmt : PRINT LPAREN expression RPAREN NEWLINE"""
        value = self.evaluate(p[3])
        print(self.format_value(value))
        p[0] = ("print", p[3])

    def p_expression_binop(self, p):
        """expression : expression PLUS expression
        | expression MINUS expression
        | expression TIMES expression
        | expression DIVIDE expression
        | expression MODULO expression
        | expression EQ expression
        | expression NE expression
        | expression LT expression
        | expression LE expression
        | expression GT expression
        | expression GE expression
        | expression AND expression
        | expression OR expression"""
        p[0] = (p[2], p[1], p[3])

    def p_expression_unary(self, p):
        """expression : MINUS expression %prec UMINUS
        | NOT expression"""
        p[0] = (p[1], p[2])

    def p_expression_group(self, p):
        """expression : LPAREN expression RPAREN"""
        p[0] = p[2]

    def p_expression_number(self, p):
        """expression : NUMBER
        | FLOAT"""
        p[0] = p[1]

    def p_expression_string(self, p):
        """expression : STRING"""
        p[0] = p[1]

    def p_expression_boolean(self, p):
        """expression : TRUE
        | FALSE"""
        p[0] = True if p[1] == "True" else False

    def p_expression_identifier(self, p):
        """expression : IDENTIFIER"""
        p[0] = ("var", p[1])

    def p_expression_list(self, p):
        """expression : LBRACKET expression_list RBRACKET
        | LBRACKET RBRACKET"""
        p[0] = ("list", p[2] if len(p) == 4 else [])

    def p_expression_list_items(self, p):
        """expression_list : expression_list COMMA expression
        | expression"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_expression_function_call(self, p):
        """expression : IDENTIFIER LPAREN argument_list RPAREN
        | IDENTIFIER LPAREN RPAREN
        | LEN LPAREN expression RPAREN"""
        func_name = p[1]
        args = p[3] if len(p) == 5 and isinstance(p[3], list) else []

        if func_name == "len":
            p[0] = ("builtin_len", p[3])
        else:
            p[0] = ("call", func_name, args)

    def p_argument_list(self, p):
        """argument_list : argument_list COMMA expression
        | expression"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_error(self, p):
        if p:
            print(f"Syntax error at token '{p.value}' on line {p.lineno}")
        else:
            print("Syntax error at end of file")

    def evaluate(self, node):
        """Evaluates an expression and returns its value"""
        if node is None:
            return None

        if isinstance(node, (int, float, str, bool)):
            return node

        if isinstance(node, tuple):
            op = node[0]

            if op == "var":
                return self.current_env.get(node[1])

            elif op == "list":
                return [self.evaluate(item) for item in node[1]]

            elif op == "call":
                func_name = node[1]
                args = [self.evaluate(arg) for arg in node[2]]
                return self.call_function(func_name, args)

            elif op == "builtin_len":
                value = self.evaluate(node[1])
                if isinstance(value, (list, str)):
                    return len(value)
                else:
                    raise TypeError("len() only works with lists and strings")

            elif op in ["+", "-", "*", "/", "%"]:
                left = self.evaluate(node[1])
                right = self.evaluate(node[2])
                return self.apply_arithmetic(op, left, right)

            elif op in ["==", "!=", "<", "<=", ">", ">="]:
                left = self.evaluate(node[1])
                right = self.evaluate(node[2])
                return self.apply_comparison(op, left, right)

            elif op == "and":
                left = self.evaluate(node[1])
                if not left:
                    return False
                return self.evaluate(node[2])

            elif op == "or":
                left = self.evaluate(node[1])
                if left:
                    return True
                return self.evaluate(node[2])

            elif op == "not":
                return not self.evaluate(node[1])

            elif op == "-" and len(node) == 2:  # Unary
                return -self.evaluate(node[1])

        return node

    def apply_arithmetic(self, op, left, right):
        """Applies arithmetic operations"""
        if op == "+":
            return left + right
        elif op == "-":
            return left - right
        elif op == "*":
            return left * right
        elif op == "/":
            if right == 0:
                raise ZeroDivisionError("Division by zero")
            return left / right
        elif op == "%":
            return left % right

    def apply_comparison(self, op, left, right):
        """Applies comparison operations"""
        if op == "==":
            return left == right
        elif op == "!=":
            return left != right
        elif op == "<":
            return left < right
        elif op == "<=":
            return left <= right
        elif op == ">":
            return left > right
        elif op == ">=":
            return left >= right

    def call_function(self, func_name, args):
        """Calls a function"""
        func = self.current_env.get_function(func_name)

        if len(args) != len(func.params):
            raise TypeError(
                f"Function '{func_name}' expects {len(func.params)} arguments, but {len(args)} were given"
            )

        # Create new environment for the function
        func_env = Environment(func.closure_env)

        # Bind parameters to arguments
        for param, arg in zip(func.params, args):
            func_env.set(param, arg)

        # Save current environment
        old_env = self.current_env
        self.current_env = func_env

        try:
            self.execute_statements(func.body)
            result = None  # Function without explicit return
        except ReturnException as e:
            result = e.value
        finally:
            self.current_env = old_env

        return result

    def execute_statements(self, statements):
        """Executes a list of statements"""
        for stmt in statements:
            if stmt is not None and stmt != "\n":
                # The statement was already executed during parsing
                pass

    def format_value(self, value):
        """Formats a value for printing"""
        if isinstance(value, bool):
            return "True" if value else "False"
        elif isinstance(value, list):
            return "[" + ", ".join(self.format_value(item) for item in value) + "]"
        elif isinstance(value, str):
            return value
        else:
            return str(value)

    def parse(self, input_text):
        """Parses and executes the code"""
        try:
            result = self.parser.parse(input_text, lexer=self.lexer.lexer)
            return result
        except Exception as e:
            print(f"Error during execution: {e}")
            return None


# =============================================================================
# MAIN INTERFACE
# =============================================================================


def main():
    """Main function - Interactive REPL"""
    print("=== MiniLang Interpreter ===")
    print("Type 'exit' to quit")
    print("Type 'help' for help")
    print()

    interpreter = MiniLangParser()

    while True:
        try:
            user_input = input(">>> ")

            if user_input.strip() == "exit":
                print("Exiting...")
                break
            elif user_input.strip() == "help":
                print_help()
                continue
            elif user_input.strip() == "":
                continue

            # Add newline if it doesn't have one
            if not user_input.endswith("\n"):
                user_input += "\n"

            # If it's just an expression without explicit newline, treat as expression
            if not any(
                keyword in user_input
                for keyword in ["=", "if", "while", "for", "def", "print"]
            ):
                # It's probably a simple expression
                try:
                    # Try to evaluate directly as expression
                    result = interpreter.parser.parse(
                        user_input, lexer=interpreter.lexer.lexer
                    )
                except:
                    print("Syntax error")
            else:
                interpreter.parse(user_input)

        except KeyboardInterrupt:
            print("\nUse 'exit' to quit")
        except EOFError:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")


def print_help():
    """Prints help about the language"""
    help_text = """
MiniLang - Available Commands:

VARIABLES:
  x = 10              # Simple assignment
  x += 5              # Compound assignment
  
DATA TYPES:
  42                  # Integer
  3.14                # Float
  "hello"             # String
  [1, 2, 3]           # List
  True, False         # Booleans

OPERATIONS:
  +, -, *, /, %       # Arithmetic
  ==, !=, <, <=, >, >= # Comparison
  and, or, not        # Logical

CONTROL FLOW:
  if x > 0:
      print("positive")
  else:
      print("not positive")
      
  while x < 10:
      x += 1
      
  for item in [1, 2, 3]:
      print(item)

FUNCTIONS:
  def sum(a, b):
      return a + b
      
  result = sum(5, 3)

BUILT-INS:
  print(value)        # Prints value
  len(list)          # Size of list/string
"""
    print(help_text)


def run_file(filename):
    """Executes a MiniLang file"""
    try:
        with open(filename, "r") as f:
            content = f.read()

        interpreter = MiniLangParser()
        interpreter.parse(content)

    except FileNotFoundError:
        print(f"File '{filename}' not found")
    except Exception as e:
        print(f"Error executing file: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Execute file
        run_file(sys.argv[1])
    else:
        # Interactive REPL
        main()
