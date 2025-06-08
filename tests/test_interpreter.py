import pytest
from interpreter import Interpreter
from parser import Parser

@pytest.fixture
def interpreter():
    return Interpreter()

@pytest.fixture
def parser():
    return Parser()

def test_basic_arithmetic(interpreter, parser):
    code = """
    x = 5
    y = 10
    z = x + y
    """
    ast = parser.parse(code)
    interpreter.interpret(ast)
    assert interpreter.get_variable("z").value == 15

def test_compound_assignments(interpreter, parser):
    code = """
    x = 5
    x += 3
    x *= 2
    """
    ast = parser.parse(code)
    interpreter.interpret(ast)
    assert interpreter.get_variable("x").value == 16

def test_string_operations(interpreter, parser):
    code = """
    name = "John"
    greeting = "Hello, " + name
    """
    ast = parser.parse(code)
    interpreter.interpret(ast)
    assert interpreter.get_variable("greeting").value == "Hello, John"

def test_list_operations(interpreter, parser):
    code = """
    numbers = [1, 2, 3, 4, 5]
    sum = 0
    for num in numbers:
        sum += num
    """
    ast = parser.parse(code)
    interpreter.interpret(ast)
    assert interpreter.get_variable("sum").value == 15

def test_function_definition_and_call(interpreter, parser):
    code = """
    def add(a, b):
        return a + b
    
    result = add(5, 3)
    """
    ast = parser.parse(code)
    interpreter.interpret(ast)
    assert interpreter.get_variable("result").value == 8

def test_if_statement(interpreter, parser):
    code = """
    x = 10
    if x > 5:
        y = 20
    else:
        y = 30
    """
    ast = parser.parse(code)
    interpreter.interpret(ast)
    assert interpreter.get_variable("y").value == 20

def test_while_loop(interpreter, parser):
    code = """
    i = 0
    sum = 0
    while i < 5:
        sum += i
        i += 1
    """
    ast = parser.parse(code)
    interpreter.interpret(ast)
    assert interpreter.get_variable("sum").value == 10

def test_scope(interpreter, parser):
    code = """
    x = 5
    def test():
        x = 10
        return x
    
    result = test()
    """
    ast = parser.parse(code)
    interpreter.interpret(ast)
    assert interpreter.get_variable("x").value == 5
    assert interpreter.get_variable("result").value == 10

def test_error_handling(interpreter, parser):
    code = """
    x = 5
    y = x + undefined
    """
    ast = parser.parse(code)
    with pytest.raises(NameError):
        interpreter.interpret(ast) 