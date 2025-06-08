# Mini Language Interpreter

A simple interpreter for a custom programming language, implemented in Python. This project serves as an educational tool to illustrate the core concepts of language design and interpreter construction.

## ✨ Features

- **Arithmetic operations:** `+`, `-`, `*`, `/`
- **Variable assignments:** Standard and compound (`=`, `+=`, `-=`, `*=`, `/=`)
- **Control flow:** `if` statements, `while` loops
- **Functions:** Definition and invocation with parameters and return values
- **Data types:** 
    - Numbers (integers, floats)
    - Strings
    - Lists
- **Scope:** Local and global variable management
- **Error handling:** Informative runtime and syntax errors

## 🚀 Installation

1. **Clone the repository:**
     ```bash
     git clone <repository-url>
     cd Mini-language
     ```
2. **Create a virtual environment:**
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     ```
3. **Install dependencies:**
     ```bash
     pip install -r requirements.txt
     ```

## 🛠️ Usage

You can use the interpreter in two ways:

### 1. Interactive Mode (Python API)

```python
from interpreter import Interpreter
from parser import Parser

interpreter = Interpreter()
parser = Parser()

code = """
x = 5
y = 10
z = x + y
"""

ast = parser.parse(code)
result = interpreter.interpret(ast)
print(result)
```

### 2. Command Line

```bash
python interpreter.py
```
You can then enter code interactively or run scripts.

## 📄 Example Code

```python
# Arithmetic
x = 5
y = 10
z = x + y

# If statement
if x > 3:
        y = 20
else:
        y = 30

# While loop
i = 0
while i < 5:
        i += 1

# Function definition and call
def add(a, b):
        return a + b

result = add(5, 3)
```

## 📁 Project Structure

- `lexer.py` — Lexical analysis (tokenization) using Lark
- `parser.py` — Syntax analysis and AST generation
- `interpreter.py` — AST execution logic
- `requirements.txt` — Python dependencies
- `examples/` — Example programs
- `tests/` — Unit tests

## 🤝 Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements and new features.

---

**License:** MIT (see `LICENSE` file for details)
