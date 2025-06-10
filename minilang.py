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
    """
    Lexical analyzer for MiniLang

    This class implements the tokenization phase of compilation, breaking
    the input source code into meaningful tokens that can be processed
    by the parser. It uses PLY's lex module for token recognition.
    """

    # Define all tokens that the lexer can recognize
    # Each token represents a fundamental unit of the language syntax
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
        "POWER",  # Exponentiation operator (**)
        "ASSIGN",  # Assignment operator (=)
        "PLUS_ASSIGN",  # Compound assignment (+=)
        "MINUS_ASSIGN",  # Compound assignment (-=)
        "TIMES_ASSIGN",  # Compound assignment (*=)
        "POWER_ASSIGN",  # Compound assignment (**=)
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

    # Dictionary mapping reserved words to their corresponding token types
    # This ensures keywords are recognized as special tokens rather than identifiers
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

    # Regular expression rules for simple tokens
    # These use PLY's convention of t_TOKENNAME for token rules
    t_PLUS = r"\+"  # Match the + character
    t_MINUS = r"-"  # Match the - character
    t_TIMES = r"\*"  # Match the * character (escaped for regex)
    t_POWER = r"\*\*"  # Match ** for exponentiation
    t_DIVIDE = r"/"  # Match the / character
    t_MODULO = r"%"  # Match the % character
    t_ASSIGN = r"="  # Match the = character
    t_PLUS_ASSIGN = r"\+="  # Match += compound assignment
    t_MINUS_ASSIGN = r"-="  # Match -= compound assignment
    t_TIMES_ASSIGN = r"\*="  # Match *= compound assignment
    t_POWER_ASSIGN = r"\*\*="  # Match **= compound assignment
    t_DIVIDE_ASSIGN = r"/="  # Match /= compound assignment
    t_EQ = r"=="  # Match == equality operator
    t_NE = r"!="  # Match != not equal operator
    t_LT = r"<"  # Match < less than operator
    t_LE = r"<="  # Match <= less than or equal operator
    t_GT = r">"  # Match > greater than operator
    t_GE = r">="  # Match >= greater than or equal operator
    t_LPAREN = r"\("  # Match ( left parenthesis
    t_RPAREN = r"\)"  # Match ) right parenthesis
    t_LBRACKET = r"\["  # Match [ left bracket
    t_RBRACKET = r"\]"  # Match ] right bracket
    t_COMMA = r","  # Match , comma
    t_COLON = r":"  # Match : colon

    # Characters to ignore (whitespace)
    t_ignore = " \t"

    def t_FLOAT(self, t):
        r"\d+\.\d+"
        """
        Token rule for floating-point numbers.
        Matches one or more digits, followed by a dot, followed by one or more digits.
        Converts the matched string to a Python float.
        """
        t.value = float(t.value)
        return t

    def t_NUMBER(self, t):
        r"\d+"
        """
        Token rule for integer numbers.
        Matches one or more digits.
        Converts the matched string to a Python integer.
        """
        t.value = int(t.value)
        return t

    def t_STRING(self, t):
        r'"([^"\\]|\\.)*"'
        """
        Token rule for string literals.
        Matches text enclosed in double quotes, handling escaped characters.
        Removes the surrounding quotes from the token value.
        """
        t.value = t.value[1:-1]  # Remove surrounding quotes
        return t

    def t_IDENTIFIER(self, t):
        r"[a-zA-Z_][a-zA-Z_0-9]*"
        """
        Token rule for identifiers (variable names, function names).
        Matches a letter or underscore followed by any number of letters, digits, or underscores.
        Checks if the identifier is a reserved word and sets the token type accordingly.
        """
        t.type = self.reserved.get(t.value, "IDENTIFIER")
        return t

    def t_NEWLINE(self, t):
        r"\n+"
        """
        Token rule for newlines.
        Matches one or more newline characters.
        Updates the line number counter for error reporting.
        """
        t.lexer.lineno += len(t.value)
        return t

    def t_COMMENT(self, t):
        r"\#.*"
        """
        Token rule for comments.
        Matches a # character followed by any characters until end of line.
        Comments are ignored (not returned as tokens).
        """
        pass  # Ignore comments

    def t_error(self, t):
        """
        Error handling function called when an illegal character is encountered.
        Prints an error message and skips the problematic character.
        """
        print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
        t.lexer.skip(1)

    def build(self, **kwargs):
        """
        Builds and returns the lexer object.
        This method initializes the PLY lexer with the defined rules.
        """
        self.lexer = lex.lex(module=self, **kwargs)
        return self.lexer


# =============================================================================
# SYNTACTIC ANALYSIS (PARSER) AND INTERPRETER
# =============================================================================


class Environment:
    """
    Execution environment for variables and functions.

    This class implements a scope chain for variable and function resolution.
    Each environment can have a parent environment, creating nested scopes.
    Variables are looked up in the current environment first, then in parent environments.
    """

    def __init__(self, parent=None):
        """
        Initialize a new environment.

        Args:
            parent: Parent environment for scope chaining (None for global scope)
        """
        self.parent = parent
        self.variables = {}  # Dictionary to store variable name -> value mappings
        self.functions = (
            {}
        )  # Dictionary to store function name -> Function object mappings

    def get(self, name):
        """
        Retrieve a variable's value from this environment or parent environments.

        Args:
            name: Variable name to look up

        Returns:
            The variable's value

        Raises:
            NameError: If the variable is not found in any scope
        """
        if name in self.variables:
            return self.variables[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise NameError(f"Variable '{name}' not defined")

    def set(self, name, value):
        """
        Set a variable's value in the current environment.

        Args:
            name: Variable name
            value: Value to assign
        """
        self.variables[name] = value

    def define_function(self, name, func):
        """
        Define a function in the current environment.

        Args:
            name: Function name
            func: Function object to store
        """
        self.functions[name] = func

    def get_function(self, name):
        """
        Retrieve a function from this environment or parent environments.

        Args:
            name: Function name to look up

        Returns:
            The Function object

        Raises:
            NameError: If the function is not found in any scope
        """
        if name in self.functions:
            return self.functions[name]
        elif self.parent:
            return self.parent.get_function(name)
        else:
            raise NameError(f"Function '{name}' not defined")


class Function:
    """
    Represents a user-defined function.

    Stores the function's name, parameters, body (list of statements),
    and the environment where it was defined (for closures).
    """

    def __init__(self, name, params, body, env):
        """
        Initialize a new function.

        Args:
            name: Function name
            params: List of parameter names
            body: List of statements that make up the function body
            env: Environment where the function was defined (closure environment)
        """
        self.name = name
        self.params = params
        self.body = body
        self.closure_env = env  # Environment for lexical scoping


class ReturnException(Exception):
    """
    Exception used to implement return statements in functions.

    When a return statement is executed, this exception is thrown
    with the return value, allowing control to jump out of nested
    statement execution back to the function call site.
    """

    def __init__(self, value):
        """
        Initialize return exception with a value.

        Args:
            value: The value to return from the function
        """
        self.value = value


class MiniLangParser:
    """
    Syntactic analyzer and interpreter for MiniLang.

    This class implements both the parser (using PLY's yacc) and the interpreter.
    It uses a syntax-directed translation approach where semantic actions
    are executed during parsing, making it a single-pass interpreter.
    """

    def __init__(self):
        """
        Initialize the parser/interpreter.
        Creates the lexer, sets up the global environment, and builds the parser.
        """
        self.lexer = MiniLangLexer()
        self.lexer.build()
        self.tokens = self.lexer.tokens
        self.global_env = Environment()  # Global scope environment
        self.current_env = self.global_env  # Current execution environment
        self.parser = yacc.yacc(module=self, debug=False, write_tables=False)

    # Operator precedence and associativity rules
    # Lower entries have higher precedence
    precedence = (
        ("left", "OR"),  # Logical OR has lowest precedence
        ("left", "AND"),  # Logical AND
        ("left", "EQ", "NE"),  # Equality and inequality
        ("left", "LT", "LE", "GT", "GE"),  # Comparison operators
        ("left", "PLUS", "MINUS"),  # Addition and subtraction
        ("left", "TIMES", "DIVIDE", "MODULO"),  # Multiplication, division, modulo
        ("right", "POWER"),  # Exponentiation (right associative)
        ("right", "UMINUS", "NOT"),  # Unary minus and logical NOT (highest precedence)
    )

    # Grammar rules and semantic actions
    # Each p_* method defines a grammar rule and its corresponding semantic action

    def p_program(self, p):
        """program : statement_list"""
        """
        Top-level grammar rule for a complete program.
        A program consists of a list of statements.
        """
        p[0] = p[1]

    def p_statement_list(self, p):
        """statement_list : statement_list statement
        | statement"""
        """
        Grammar rule for a list of statements.
        Can be a single statement or multiple statements.
        Builds a list of all statements in the program.
        """
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
        """
        Grammar rule for individual statements.
        A statement can be any of the listed statement types or just a newline.
        """
        p[0] = p[1]

    def p_assignment_stmt(self, p):
        """assignment_stmt : IDENTIFIER ASSIGN expression NEWLINE
        | IDENTIFIER PLUS_ASSIGN expression NEWLINE
        | IDENTIFIER MINUS_ASSIGN expression NEWLINE
        | IDENTIFIER TIMES_ASSIGN expression NEWLINE
        | IDENTIFIER DIVIDE_ASSIGN expression NEWLINE
        | IDENTIFIER POWER_ASSIGN expression NEWLINE"""
        """
        Grammar rule for assignment statements.
        Handles both simple assignment (=) and compound assignments (+=, -=, etc.).
        Semantic action: Evaluates the expression and stores the result in the variable.
        """
        var_name = p[1]
        operator = p[2]
        value = self.evaluate(p[3])

        if operator == "=":
            # Simple assignment
            self.current_env.set(var_name, value)
        elif operator == "+=":
            # Add and assign
            old_value = self.current_env.get(var_name)
            self.current_env.set(var_name, old_value + value)
        elif operator == "-=":
            # Subtract and assign
            old_value = self.current_env.get(var_name)
            self.current_env.set(var_name, old_value - value)
        elif operator == "*=":
            # Multiply and assign
            old_value = self.current_env.get(var_name)
            self.current_env.set(var_name, old_value * value)
        elif operator == "/=":
            # Divide and assign
            old_value = self.current_env.get(var_name)
            self.current_env.set(var_name, old_value / value)
        elif operator == "**=":
            # Power and assign
            old_value = self.current_env.get(var_name)
            self.current_env.set(var_name, old_value**value)

        p[0] = ("assign", var_name, value)

    def p_expression_stmt(self, p):
        """expression_stmt : expression NEWLINE"""
        """
        Grammar rule for expression statements.
        An expression followed by a newline (e.g., standalone expressions in REPL).
        Semantic action: Evaluates the expression and prints the result if it's not None.
        """
        result = self.evaluate(p[1])
        if result is not None:
            print(self.format_value(result))
        p[0] = ("expr_stmt", p[1])

    def p_if_stmt(self, p):
        """if_stmt : IF expression COLON NEWLINE statement_list
        | IF expression COLON NEWLINE statement_list ELSE COLON NEWLINE statement_list
        """
        """
        Grammar rule for if statements.
        Supports both if-only and if-else forms.
        Semantic action: Evaluates the condition and executes the appropriate branch.
        """
        condition = self.evaluate(p[2])
        if condition:
            self.execute_statements(p[5])
        elif len(p) == 10:  # has else clause
            self.execute_statements(p[9])
        p[0] = ("if", p[2], p[5], p[9] if len(p) == 10 else None)

    def p_while_stmt(self, p):
        """while_stmt : WHILE expression COLON NEWLINE statement_list"""
        """
        Grammar rule for while loops.
        Semantic action: Repeatedly evaluates the condition and executes the body while true.
        Handles return statements that might break out of the loop.
        """
        while self.evaluate(p[2]):
            try:
                self.execute_statements(p[5])
            except ReturnException:
                break  # Return statement breaks the loop
        p[0] = ("while", p[2], p[5])

    def p_for_stmt(self, p):
        """for_stmt : FOR IDENTIFIER IN expression COLON NEWLINE statement_list"""
        """
        Grammar rule for for loops.
        Iterates over the elements of a list or string.
        Semantic action: Sets the loop variable to each element and executes the body.
        """
        var_name = p[2]
        iterable = self.evaluate(p[4])

        if not isinstance(iterable, list):
            raise TypeError("Object is not iterable")

        for item in iterable:
            self.current_env.set(var_name, item)
            try:
                self.execute_statements(p[7])
            except ReturnException:
                break  # Return statement breaks the loop

        p[0] = ("for", var_name, p[4], p[7])

    def p_function_def(self, p):
        """function_def : DEF IDENTIFIER LPAREN parameter_list RPAREN COLON NEWLINE statement_list
        | DEF IDENTIFIER LPAREN RPAREN COLON NEWLINE statement_list"""
        """
        Grammar rule for function definitions.
        Supports functions with parameters or no parameters.
        Semantic action: Creates a Function object and stores it in the current environment.
        """
        func_name = p[2]
        params = p[4] if len(p) == 9 else []
        body = p[8] if len(p) == 9 else p[7]

        func = Function(func_name, params, body, self.current_env)
        self.current_env.define_function(func_name, func)
        p[0] = ("function_def", func_name, params, body)

    def p_parameter_list(self, p):
        """parameter_list : parameter_list COMMA IDENTIFIER
        | IDENTIFIER"""
        """
        Grammar rule for function parameter lists.
        Builds a list of parameter names.
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_return_stmt(self, p):
        """return_stmt : RETURN expression NEWLINE
        | RETURN NEWLINE"""
        """
        Grammar rule for return statements.
        Can return a value or return without a value (None).
        Semantic action: Throws a ReturnException to implement the return mechanism.
        """
        value = self.evaluate(p[2]) if len(p) == 4 else None
        raise ReturnException(value)

    def p_print_stmt(self, p):
        """print_stmt : PRINT LPAREN expression RPAREN NEWLINE"""
        """
        Grammar rule for print statements.
        Semantic action: Evaluates the expression and prints its formatted value.
        """
        value = self.evaluate(p[3])
        print(self.format_value(value))
        p[0] = ("print", p[3])

    def p_expression_binop(self, p):
        """expression : expression PLUS expression
        | expression MINUS expression
        | expression TIMES expression
        | expression POWER expression
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
        """
        Grammar rule for binary operators.
        Creates an AST node representing the binary operation.
        The actual evaluation is deferred to the evaluate() method.
        """
        p[0] = (p[2], p[1], p[3])

    def p_expression_unary(self, p):
        """expression : MINUS expression %prec UMINUS
        | NOT expression"""
        """
        Grammar rule for unary operators.
        Handles unary minus and logical NOT.
        Uses %prec UMINUS to give unary minus higher precedence than binary minus.
        """
        p[0] = (p[1], p[2])

    def p_expression_group(self, p):
        """expression : LPAREN expression RPAREN"""
        """
        Grammar rule for parenthesized expressions.
        Parentheses are used for grouping and don't change the expression's value.
        """
        p[0] = p[2]

    def p_expression_number(self, p):
        """expression : NUMBER
        | FLOAT"""
        """
        Grammar rule for numeric literals.
        Numbers are already converted to Python int/float by the lexer.
        """
        p[0] = p[1]

    def p_expression_string(self, p):
        """expression : STRING"""
        """
        Grammar rule for string literals.
        Strings are already processed by the lexer (quotes removed).
        """
        p[0] = p[1]

    def p_expression_boolean(self, p):
        """expression : TRUE
        | FALSE"""
        """
        Grammar rule for boolean literals.
        Converts the string tokens "True"/"False" to Python boolean values.
        """
        p[0] = True if p[1] == "True" else False

    def p_expression_identifier(self, p):
        """expression : IDENTIFIER"""
        """
        Grammar rule for variable references.
        Creates an AST node that will be resolved during evaluation.
        """
        p[0] = ("var", p[1])

    def p_expression_list(self, p):
        """expression : LBRACKET expression_list RBRACKET
        | LBRACKET RBRACKET"""
        """
        Grammar rule for list literals.
        Supports both empty lists and lists with elements.
        """
        p[0] = ("list", p[2] if len(p) == 4 else [])

    def p_expression_list_items(self, p):
        """expression_list : expression_list COMMA expression
        | expression"""
        """
        Grammar rule for list elements.
        Builds a list of expressions that will be evaluated to create the list.
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_expression_function_call(self, p):
        """expression : IDENTIFIER LPAREN argument_list RPAREN
        | IDENTIFIER LPAREN RPAREN
        | LEN LPAREN expression RPAREN"""
        """
        Grammar rule for function calls.
        Handles user-defined functions and the built-in len() function.
        """
        func_name = p[1]
        args = p[3] if len(p) == 5 and isinstance(p[3], list) else []

        if func_name == "len":
            # Built-in len() function
            p[0] = ("builtin_len", p[3])
        else:
            # User-defined function call
            p[0] = ("call", func_name, args)

    def p_argument_list(self, p):
        """argument_list : argument_list COMMA expression
        | expression"""
        """
        Grammar rule for function call arguments.
        Builds a list of argument expressions.
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_error(self, p):
        """
        Error handling for syntax errors.
        Called by PLY when the parser encounters a syntax error.
        """
        if p:
            print(f"Syntax error at token '{p.value}' on line {p.lineno}")
        else:
            print("Syntax error at end of file")

    def evaluate(self, node):
        """
        Evaluates an expression and returns its value.

        This method implements the interpreter's evaluation engine.
        It recursively evaluates AST nodes and returns their computed values.

        Args:
            node: AST node to evaluate (can be a literal value or tuple representing an operation)

        Returns:
            The computed value of the expression
        """
        if node is None:
            return None

        # Literal values (already computed)
        if isinstance(node, (int, float, str, bool)):
            return node

        if isinstance(node, tuple):
            op = node[0]

            if op == "var":
                # Variable reference - look up in current environment
                return self.current_env.get(node[1])

            elif op == "list":
                # List literal - evaluate all elements
                return [self.evaluate(item) for item in node[1]]

            elif op == "call":
                # Function call - evaluate arguments and call function
                func_name = node[1]
                args = [self.evaluate(arg) for arg in node[2]]
                return self.call_function(func_name, args)

            elif op == "builtin_len":
                # Built-in len() function
                value = self.evaluate(node[1])
                if isinstance(value, (list, str)):
                    return len(value)
                else:
                    raise TypeError("len() only works with lists and strings")

            elif op in ["+", "-", "*", "**", "/", "%"]:
                # Arithmetic operations
                left = self.evaluate(node[1])
                right = self.evaluate(node[2])
                return self.apply_arithmetic(op, left, right)

            elif op in ["==", "!=", "<", "<=", ">", ">="]:
                # Comparison operations
                left = self.evaluate(node[1])
                right = self.evaluate(node[2])
                return self.apply_comparison(op, left, right)

            elif op == "and":
                # Logical AND with short-circuit evaluation
                left = self.evaluate(node[1])
                if not left:
                    return False
                return self.evaluate(node[2])

            elif op == "or":
                # Logical OR with short-circuit evaluation
                left = self.evaluate(node[1])
                if left:
                    return True
                return self.evaluate(node[2])

            elif op == "not":
                # Logical NOT
                return not self.evaluate(node[1])

            elif op == "-" and len(node) == 2:  # Unary minus
                return -self.evaluate(node[1])

        return node

    def apply_arithmetic(self, op, left, right):
        """
        Applies arithmetic operations to two operands.

        Args:
            op: Operator string ("+", "-", "*", "**", "/", "%")
            left: Left operand
            right: Right operand

        Returns:
            Result of the arithmetic operation

        Raises:
            ZeroDivisionError: For division by zero
        """
        if op == "+":
            return left + right
        elif op == "-":
            return left - right
        elif op == "*":
            return left * right
        elif op == "**":
            return left**right
        elif op == "/":
            if right == 0:
                raise ZeroDivisionError("Division by zero")
            return left / right
        elif op == "%":
            return left % right

    def apply_comparison(self, op, left, right):
        """
        Applies comparison operations to two operands.

        Args:
            op: Comparison operator string ("==", "!=", "<", "<=", ">", ">=")
            left: Left operand
            right: Right operand

        Returns:
            Boolean result of the comparison
        """
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
        """
        Calls a user-defined function with the given arguments.

        This method implements function calls by:
        1. Looking up the function definition
        2. Checking argument count matches parameter count
        3. Creating a new environment for the function execution
        4. Binding arguments to parameters
        5. Executing the function body
        6. Handling return values via ReturnException

        Args:
            func_name: Name of the function to call
            args: List of argument values

        Returns:
            The function's return value (None if no explicit return)

        Raises:
            TypeError: If argument count doesn't match parameter count
        """
        func = self.current_env.get_function(func_name)

        # Check argument count
        if len(args) != len(func.params):
            raise TypeError(
                f"Function '{func_name}' expects {len(func.params)} arguments, but {len(args)} were given"
            )

        # Create new environment for function execution (lexical scoping)
        func_env = Environment(func.closure_env)

        # Bind parameters to argument values
        for param, arg in zip(func.params, args):
            func_env.set(param, arg)

        # Save current environment and switch to function environment
        old_env = self.current_env
        self.current_env = func_env

        try:
            # Execute function body
            self.execute_statements(func.body)
            result = None  # Function without explicit return returns None
        except ReturnException as e:
            # Function returned a value
            result = e.value
        finally:
            # Restore previous environment
            self.current_env = old_env

        return result

    def execute_statements(self, statements):
        """
        Executes a list of statements.

        This method is called to execute the body of control structures
        (if, while, for) and functions. Since this is a syntax-directed
        interpreter, most statements are already executed during parsing,
        so this method primarily serves as a placeholder.

        Args:
            statements: List of statement AST nodes
        """
        for stmt in statements:
            if stmt is not None and stmt != "\n":
                # Statements are already executed during parsing
                # This is mainly for consistency with the AST structure
                pass

    def format_value(self, value):
        """
        Formats a value for printing.

        Converts Python values to their string representation in MiniLang format.

        Args:
            value: Value to format

        Returns:
            String representation of the value
        """
        if isinstance(value, bool):
            return "True" if value else "False"
        elif isinstance(value, list):
            return "[" + ", ".join(self.format_value(item) for item in value) + "]"
        elif isinstance(value, str):
            return value
        else:
            return str(value)

    def parse(self, input_text):
        """
        Parses and executes the given code.

        This is the main entry point for code execution.

        Args:
            input_text: MiniLang source code to parse and execute

        Returns:
            Parse result (usually None for statements)
        """
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
    """
    Main function - Interactive REPL (Read-Eval-Print Loop).

    Provides an interactive command-line interface for MiniLang.
    Users can enter statements and expressions line by line.
    """
    print("=== MiniLang Interpreter ===")
    print("Type 'exit' to quit")
    print("Type 'help' for help")
    print()

    interpreter = MiniLangParser()

    while True:
        try:
            user_input = input(">>> ")

            # Handle special commands
            if user_input.strip() == "exit":
                print("Exiting...")
                break
            elif user_input.strip() == "help":
                print_help()
                continue
            elif user_input.strip() == "":
                continue

            # Ensure input ends with newline for proper parsing
            if not user_input.endswith("\n"):
                user_input += "\n"

            # Check if it's a simple expression (for REPL convenience)
            if not any(
                keyword in user_input
                for keyword in ["=", "if", "while", "for", "def", "print"]
            ):
                # Treat as simple expression for evaluation
                try:
                    result = interpreter.parser.parse(
                        user_input, lexer=interpreter.lexer.lexer
                    )
                except:
                    print("Syntax error")
            else:
                # Parse and execute as statement(s)
                interpreter.parse(user_input)

        except KeyboardInterrupt:
            print("\nUse 'exit' to quit")
        except EOFError:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")


def print_help():
    """
    Prints help information about MiniLang syntax and features.

    Displays a comprehensive guide to using the language,
    including examples of all major features.
    """
    help_text = """
MiniLang - Available Commands:

VARIABLES:
  x = 10              # Simple assignment
  x += 5              # Compound assignment
  x **= 2             # Power assignment
  
DATA TYPES:
  42                  # Integer
  3.14                # Float
  "hello"             # String
  [1, 2, 3]           # List
  True, False         # Booleans

OPERATIONS:
  +, -, *, /, %       # Arithmetic
  **                  # Exponentiation
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

EXAMPLES:
  2 ** 3              # Returns 8
  x = 5
  x **= 2             # x becomes 25
"""
    print(help_text)


def run_file(filename):
    """
    Executes a MiniLang source file.

    Reads the entire file and passes it to the interpreter for execution.

    Args:
        filename: Path to the MiniLang source file
    """
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
    # Entry point - can run files or start interactive REPL
    if len(sys.argv) > 1:
        # Command line argument provided - execute file
        run_file(sys.argv[1])
    else:
        # No arguments - start interactive REPL
        main()
