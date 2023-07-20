import fire

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b != 0:
        return a / b
    else:
        return "Error: Division by zero is undefined"

def main():
    fire.Fire({
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide,
    })

if __name__ == '__main__':
    main()
