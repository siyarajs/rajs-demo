def calculator():
    def add(a, b):
     return a + b
def subtract(a, b):
    return a - b
def multiply(a, b):
    return a * b
def divide(a, b):
    if b == 0:
        return "Cannot divide by zero"
    return a / b
while True:
    expression = input("Enter a math expression: ")
    if expression== 'stop':
        break
    try:
        result = eval(expression)
        print(result)
    except:
        print("invalid")
calculator()
