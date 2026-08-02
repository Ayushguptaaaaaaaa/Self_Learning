try:
    a=int(input("Enter a number: "))
    b=int(input("Enter another number: "))

    print("Please select an operation to perform:")
    print("+. Addition")
    print("-. Subtraction")
    print("*. Multiplication")
    print("/. Division")

    operation=input("Enter the operation you want to perform: ")

    if operation == "+":
        print(f"The result of {a}+{b} is: {a+b}")
    elif operation == "-":
        print(f"The result of {a}-{b} is: {a-b}")
    elif operation == "*":
        print(f"The result of {a}*{b} is: {a*b}")
    elif operation == "/":
        if b == 0:
            print("Error: Division by zero is not allowed.")
        else:
            print(f"The result of {a}/{b} is: {a/b}")

except Exception as e:
    print("Invalid input. Please enter valid integers.")
    exit()