from parser import parse_code
from interpreter import Interpreter


def main():
    interpreter = Interpreter()

    print("Mini Language Interpreter")
    print("Type 'exit' to quit")

    while True:
        try:
            code = input(">>> ")
            if code.strip().lower() == "exit":
                break

            if code.strip():
                ast = parse_code(code)
                result = interpreter.interpret(ast)
                if result and result.type != interpreter.ValueType.NONE:
                    print(result)

        except EOFError:
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
