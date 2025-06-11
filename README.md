# MiniLang - Mini Programming Language

## Integrated Practical Work: "Building your Mini Programming Language"

## Installation and Usage

### Prerequisites

Make sure you have Python 3.6+ installed on your system and install the required PLY library.

### Platform-Specific Installation

**Windows:**

```cmd
pip install ply
```

**macOS:**

```bash
pip3 install ply
# or if using Homebrew Python
pip install ply
```

**Linux (Ubuntu/Debian):**

```bash
# Using system Python
sudo apt update
sudo apt install python3-pip
pip3 install ply

# Or using package manager
sudo apt install python3-ply
```

**Linux (Fedora/RHEL):**

```bash
sudo dnf install python3-pip
pip3 install ply
```

**Linux (Arch/Manjaro):**

```bash
sudo pacman -S python-pip
pip install ply

# Or using AUR package manager
yay -S python-ply
```

### How to Use

**Interactive Mode (REPL):**

```bash
python3 minilang.py
```

**Run File:**

```bash
python3 minilang.py example.ml
```

### REPL Usage Examples

```python
>>> 4 + 6
10
>>> x = 5
>>> x * 2
10
>>> print("Hello World")
Hello World
>>> quit()  # To exit REPL
```

## 1. Language Objectives and Audience (Chapters 1-3)

**Objective:** MiniLang is an educational programming language designed to teach fundamental programming concepts in a simple and intuitive way.

**Target audience:**

- Programming beginners
- People who want to understand how languages work internally
- Educators who need a simple tool for teaching

**Main features:**

- Simple and clean syntax inspired by Python
- Basic data types (int, float, string, list, bool)
- Essential control structures
- Support for functions with local scope
- Interactive interpreter (REPL) with custom prompt
- Robust error handling

## 2. Lexical and Syntactic Analysis (Chapter 4)

The interpreter uses PLY (Python Lex-Yacc) to implement complete lexical and syntactic analysis.

### Recognized Tokens (25 types)

**Literals and Identifiers:**

- `NUMBER`: Integer and decimal numbers (regex: `\d+\.?\d*`)
- `STRING`: Strings delimited by double quotes
- `ID`: Identifiers for variables and functions
- `COMMENT`: Comments starting with # (ignored)

**Arithmetic Operators:**

- `PLUS` (+), `MINUS` (-), `TIMES` (*), `DIVIDE` (/), `MODULO` (%), `POWER` (**)

**Assignment Operators:**

- `ASSIGN` (=), `PLUS_ASSIGN` (+=), `MINUS_ASSIGN` (-=)
- `TIMES_ASSIGN` (*=), `DIVIDE_ASSIGN` (/=)

**Comparison Operators:**

- `EQ` (==), `NE` (!=), `LT` (<), `GT` (>), `LE` (<=), `GE` (>=)

**Logical Operators:**

- `AND`, `OR`, `NOT`

**Reserved Words:**

- Control: `IF`, `ELSE`, `WHILE`, `FOR`, `IN`
- Functions: `DEF`, `RETURN`
- Values: `TRUE`, `FALSE`
- Built-ins: `PRINT`, `LEN`

**Delimiters:**

- `LPAREN` ((), `RPAREN` ()), `LBRACKET` ([), `RBRACKET` (])
- `COLON` (:), `COMMA` (,)

### Syntactic Analysis (Parser)

**Operator Precedence (from lowest to highest):**

```python
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('left', 'EQ', 'NE'),
    ('left', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
    ('right', 'POWER'),
    ('right', 'UMINUS'),
)
```

**Main Grammar Rules:**

- `program`: List of statements
- `statement`: Assignments, expressions, control structures, function definitions
- `expression`: Arithmetic, logical operations, function calls
- `assignment`: Simple and compound assignments
- `if_statement`: Conditional structures with optional else
- `while_statement`: While loops
- `for_statement`: For loops with iteration over lists/strings
- `function_def`: Function definition with parameters

## 3. Names, Bindings and Scopes (Chapter 5)

### Scope Implementation with Environment

```python
class Environment:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent
    
    def get(self, name):
        # Hierarchical search: local → global
        if name in self.vars:
            return self.vars[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise NameError(f"Variable '{name}' is not defined")
    
    def set(self, name, value):
        # Define or update variable in current scope
        self.vars[name] = value
    
    def define(self, name, value):
        # Define new variable in current scope
        self.vars[name] = value
```

**Usage Example:**

```python
# Global scope
x = 10

def test():
    # Function local scope
    y = 20
    return x + y  # Access global variable

result = test()  # result = 30
```

**Characteristics:**

- Initial global environment created in parser
- Local environment created on each function call
- Automatic hierarchical search
- Error handling for undefined variables

## 4. Data Types (Chapter 6)

### Supported Types

```python
# Integers
age = 25

# Floats  
height = 1.75

# Strings
name = "John"
message = "Hello, World!"

# Lists (heterogeneous)
numbers = [1, 2, 3, 4, 5]
mixed = [1, "text", 3.14, True]

# Booleans
active = True
inactive = False
```

### Operations by Type

**Numbers (int/float):**

- Arithmetic: `+`, `-`, `*`, `/`, `%`, `**` (exponentiation)
- Comparisons: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Unary: `-` (negation)

**Strings:**

- Concatenation: `+`
- Comparisons: `==`, `!=`
- Iteration in for loops
- len() function for length

**Lists:**

- Concatenation: `+`
- Index access: `list[0]`
- Comparisons: `==`, `!=`
- Iteration in for loops
- len() function for length

**Booleans:**

- Logical operations: `and`, `or`, `not`
- Literal values: `True`, `False`

## 5. Assignments (Chapter 7)

### Implemented Assignment Types

```python
# Simple assignment
x = 10
name = "John"
list = [1, 2, 3]

# Compound assignments
x += 5   # x = x + 5
x -= 2   # x = x - 2  
x *= 3   # x = x * 3
x /= 2   # x = x / 2

# List assignment with concatenation
list += [4, 5]  # list = list + [4, 5]

# Power assignment
x **= 2  # x = x ** 2
```

### Parser Implementation

```python
def p_assignment_compound(p):
    '''assignment : ID PLUS_ASSIGN expression
                  | ID MINUS_ASSIGN expression
                  | ID TIMES_ASSIGN expression
                  | ID DIVIDE_ASSIGN expression'''
    var_name = p[1]
    operator = p[2]
    value = p[3]
    
    current_val = p.parser.env.get(var_name)
    
    if operator == '+=':
        result = current_val + value
    elif operator == '-=':
        result = current_val - value
    # ... etc
```

## 6. Control Flow (Chapter 8)

### Conditional Structure

```python
if age >= 18:
    print("Adult")
else:
    print("Minor")

# Nested conditions
if grade >= 90:
    print("A")
else:
    if grade >= 80:
        print("B")
    else:
        print("C")
```

### While Loop

```python
counter = 0
while counter < 5:
    print(counter)
    counter += 1

# With complex conditions
while x > 0 and y < 10:
    x -= 1
    y += 2
```

### For Loop

```python
# Iteration over list
for number in [1, 2, 3, 4, 5]:
    print(number)

# Iteration over string
for char in "Hello":
    print(char)

# Iteration over list variable
numbers = [10, 20, 30]
for n in numbers:
    print(n * 2)
```

**Implementation:** The parser automatically converts strings and lists into iterables, creating a local environment for the loop variable.

## 7. Subprograms (Chapters 9 and 10)

### Function Definition and Calling

```python
# Simple function
def greeting():
    print("Hello, world!")

# Function with parameters
def sum(a, b):
    return a + b

# Function with multiple parameters
def calculate_average(list):
    total = 0
    for num in list:
        total += num
    return total / len(list)

# Function with power operation
def power_of_two(x):
    return x ** 2

# Calls
greeting()
result = sum(10, 5)
average = calculate_average([1, 2, 3, 4, 5])
squared = power_of_two(8)  # Returns 64
```

### Function Class Implementation

```python
class Function:
    def __init__(self, params, body, closure_env):
        self.params = params      # Parameter list
        self.body = body         # Statement list of body
        self.closure_env = closure_env  # Definition environment
    
    def call(self, args, parser):
        # Create new local environment
        call_env = Environment(self.closure_env)
        
        # Bind parameters to arguments
        for i, param in enumerate(self.params):
            if i < len(args):
                call_env.define(param, args[i])
        
        # Execute function body
        old_env = parser.env
        parser.env = call_env
        
        result = None
        for stmt in self.body:
            result = stmt
            if parser.return_value is not None:
                result = parser.return_value
                parser.return_value = None
                break
        
        parser.env = old_env
        return result
```

### Function Characteristics

- Support for multiple parameters
- Return values with `return`
- Automatic local scope for variables
- Closure: access to variables from definition scope
- Handling of missing arguments (None)

## 8. Built-in Functions

### print(*args)

Displays values in output, separated by space:

```python
print("Hello World")          # Hello World
print(42)                     # 42
print([1, 2, 3])             # [1, 2, 3]
print("Result:", 10 + 5)      # Result: 15
print("Power of 2^3:", 2**3)  # Power of 2^3: 8
```

### len(obj)

Returns the length of lists and strings:

```python
len([1, 2, 3, 4])     # 4
len("Hello")          # 5
len([])               # 0
```

### quit()

Terminates the interpreter (REPL only):

```python
>>> quit()
# Exits the program
```

## Complete Examples

### Example 1: Advanced Calculator

```python
def calculator(a, b, operation):
    if operation == "+":
        return a + b
    else:
        if operation == "-":
            return a - b
        else:
            if operation == "*":
                return a * b
            else:
                if operation == "/":
                    if b != 0:
                        return a / b
                    else:
                        return "Error: division by zero"
                else:
                    if operation == "%":
                        return a % b
                    else:
                        if operation == "**":
                            return a ** b
                        else:
                            return "Invalid operation"

# Tests
print(calculator(10, 5, "+"))   # 15
print(calculator(10, 5, "/"))   # 2.0
print(calculator(10, 3, "%"))   # 1
print(calculator(2, 8, "**"))   # 256
print(calculator(10, 0, "/"))   # Error: division by zero
```

### Example 2: List Processing

```python
def process_numbers(limit):
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    evens = []
    for i in numbers:
        if i <= limit:
            if i % 2 == 0:
                evens += [i]
    return evens

def sum_list(list):
    total = 0
    for num in list:
        total += num
    return total

result = process_numbers(8)
print("Evens up to 8:", result)        # [2, 4, 6, 8]
print("Sum:", sum_list(result))        # 20
```

### Example 3: Mathematical Algorithms

```python
def factorial(n):
    if n <= 1:
        return 1
    else:
        result = 1
        counter = 2
        while counter <= n:
            result *= counter
            counter += 1
        return result

def fibonacci(n):
    if n <= 0:
        return 0
    else:
        if n == 1:
            return 1
        else:
            a = 0
            b = 1
            counter = 2
            while counter <= n:
                temp = a + b
                a = b
                b = temp
                counter += 1
            return b

def power_table(base, max_exp):
    exponents = [1, 2, 3, 4, 5]
    for i in exponents:
        if i <= max_exp:
            result = base ** i
            print("Power calculation:", base, "^", i, "=", result)

print("Factorial of 5:", factorial(5))    # 120
print("Fibonacci 10:", fibonacci(10))     # 55
print("Power table for base 2:")
power_table(2, 4)  # Shows: 2^1=2, 2^2=4, 2^3=8, 2^4=16
```

## Interpreter Architecture

### Main Components

#### 1. MiniLangLexer

- **Tokenization**: Uses PLY (Python Lex-Yacc)
- **25 token types** recognized
- **Regex patterns** for numbers, strings, identifiers
- **Reserved words** mapped automatically
- **Comment handling** (ignored)
- **Ignored characters**: spaces, tabs, line breaks

#### 2. MiniLangParser

- **Grammar rules** for language constructs
- **Operator precedence** explicitly defined
- **Interpreted execution** during parsing (tree-walking interpreter)
- **Error handling** with `p_error` and informative messages
- **State management**: current environment, return value

#### 3. Environment (Scope Management)

- **Hierarchical chaining** of environments
- **Main methods**: `get()`, `set()`, `define()`
- **Automatic search**: local → parent → global
- **Error handling**: NameError for non-existent variables

#### 4. Function (Function Representation)

- **Closure**: stores definition environment
- **Parameters and body** of function
- **call() method**: execution with new local environment
- **Argument binding** to parameters

### Execution Flow

```text
Source Code → Tokenization (PLY) → Parsing (PLY) → Direct Execution
                     ↓                    ↓              ↓
                  Tokens            Grammar Rules    Evaluation
                                                        ↓
                                                 Result/Effect
```

1. **Lexical Analysis**: Source code converted to tokens via PLY
2. **Syntactic Analysis**: Tokens processed by grammar rules
3. **Execution**: Semantic actions executed during parsing
4. **Evaluation**: Operations calculated and effects applied immediately

### Error Handling

**Handled Error Types:**

```python
# Lexical error
>>> 4 @ 5
Illegal character '@'

# Syntax error  
>>> if x
Syntax error on line X

# Semantic error
>>> print(nonexistent_variable)
Variable 'nonexistent_variable' is not defined

# Type error
>>> 5 + "text"
TypeError: Invalid operation between types

# Division by zero
>>> 10 / 0
ZeroDivisionError: Division by zero

# Power operation errors
>>> 2 ** "text"
TypeError: Invalid exponent type
```

### REPL Mode (Read-Eval-Print Loop)

**Features:**

- Custom prompt `>>>`
- Line-by-line evaluation
- Command history
- `quit()` command to exit
- Error handling without crashes
- State maintenance between commands

**REPL Examples with Power Operator:**

```python
>>> 2 ** 3
8
>>> base = 5
>>> exponent = 2
>>> result = base ** exponent
>>> print("Result:", result)
Result: 25
>>> x = 2
>>> x **= 3
>>> print(x)
8
```

## Current Limitations and Future Extensions

### Current Limitations

**Data Types:**

- No dictionaries/maps
- No sets
- No immutable tuples

**Control Structures:**

- No break/continue in loops
- No try/catch for exceptions
- No switch/case

**Module System:**

- No import/export
- No external libraries
- No namespaces

**Advanced Programming:**

- No classes/objects
- No inheritance
- No decorators
- No generators/yield

**I/O and System:**

- No file operations
- Limited user input capabilities
- No operating system access

### Possible Extensions

**Short Term:**

- Add break/continue in loops
- Implement basic dictionaries
- Improve error messages with line numbers
- Add more built-in functions (input, range, etc.)

**Medium Term:**

- Basic module system
- Structured exception handling
- Simple class support
- Basic file operations

**Long Term:**

- Bytecode compilation
- Performance optimizations
- Integrated debugger
- Optional static type system
- GUI development interface

## Conclusion

MiniLang represents a complete and functional educational implementation of a programming language. Using the **tree-walking interpreter** pattern with PLY, it clearly demonstrates fundamental concepts:

**Highlighted Technical Aspects:**

- Robust lexical and syntactic analysis
- Hierarchical scope management
- Dynamic type system
- Complete function support with closure
- Functional interactive REPL
- **Power operator support** for mathematical operations

**Educational Value:**

- Clean and well-structured code
- Modular implementation facilitating extensions
- Practical demonstration of theoretical concepts
- Solid foundation for understanding more complex languages

The chosen architecture (direct interpreter) prioritizes simplicity and clarity over performance, making the code accessible for study and an excellent learning tool for understanding programming language implementation.
