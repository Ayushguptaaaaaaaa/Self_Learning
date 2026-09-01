# ============================================================================
# Question 1: Basic Decorator
# ----------------------------------------------------------------------------
# Topic: Function decorators, closures, @ syntax
#
# Write a decorator named `logger` that wraps a function taking no arguments.
# Before the wrapped function runs, it should print "Function is being
# called...", and then call the original function.
#
# Apply this decorator using the @logger syntax to a function say_hello()
# that prints "Hello". Calling say_hello() should produce:
#     Function is being called...
#     Hello
#
# Concepts: A decorator is a function that takes a function and returns a
# replacement function. The inner `wrapper` closes over `func`. The line
# `@logger` is shorthand for `say_hello = logger(say_hello)`.
# ============================================================================

def logger(func):
    def wrapper():
        print("Function is being called...")
        func()
    return wrapper

@logger
def say_hello():
    print("Hello")


say_hello( )

# ============================================================================
# Question 2: Timing Decorator That Preserves the Return Value
# ----------------------------------------------------------------------------
# Topic: Decorators with arguments and return values, time.time()
#
# Write a decorator named `timer` that measures how long a function takes to
# execute. The wrapper must:
#   1. Record the start time using time() from the `time` module.
#   2. Call the decorated function with the argument it received (n).
#   3. Record the end time and print the elapsed seconds (t2 - t1).
#   4. RETURN the original function's result so the caller still gets a value.
#
# Then write a function sum_1m(n) that computes the sum of all integers from
# 1 to n using a for loop, decorate it with @timer, call it with 1000000,
# store the result in `a`, and print `a`.
#
# Concepts: The wrapper must accept the same parameters as the wrapped
# function, and it must `return result` -- otherwise the decorated function
# silently returns None.
# ============================================================================

from time import time

def timer(func):
    def wrapper(n):
        t1 = time()
        result = func(n)
        t2 = time()
        print(t2 - t1)
        return result
    return wrapper

@timer
def sum_1m(n):
    sum = 0
    for i in range(1, n+1):
        sum += i
    return sum

a = sum_1m(1000000)
print(a)

# ============================================================================
# Question 3: @property and Setter With Validation
# ----------------------------------------------------------------------------
# Topic: Encapsulation, getters/setters, @property, @<name>.setter
#
# Create a class `Employee` whose __init__ takes `salary` and stores it in a
# "protected" attribute self._salary.
#   - Expose a `salary` getter using the @property decorator that returns
#     self._salary.
#   - Add a corresponding @salary.setter that validates the new value: if the
#     value is negative, print "No Negative Salary!" and leave the salary
#     unchanged; otherwise assign it to self._salary.
#
# Demonstrate it: create e = Employee(3000), then assign e.salary = 4500 and
# print the stored value to confirm the setter ran.
#
# Concepts: @property lets attribute-style access (e.salary = 4500) run a
# method, so validation happens without changing the caller's syntax. The
# underscore prefix signals the backing attribute is internal.
# ============================================================================

class Employee:

    def __init__(self,salary):
        self._salary=salary

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self,value):
        if value<0:
            print("No Negative Salary!")
        else:
            self._salary=value

e=Employee(3000)
e.salary=4500
print(e._salary)


# ============================================================================
# Question 4: @staticmethod vs @classmethod
# ----------------------------------------------------------------------------
# Topic: Static methods, class methods, calling methods without an instance
#
# Create a utility class `MathUtils` containing:
#   - A STATIC method add(a, b) that returns a + b -- it needs neither `self`
#     nor `cls`.
#   - A CLASS method description(cls) that prints
#     "This is a utility class for Math Operations."
#
# Show that both can be called directly on the class, WITHOUT creating an
# object: call MathUtils.add(3, 6) and MathUtils.description().
#
# Note: below, `a = MathUtils` binds the class itself -- not an instance --
# so a.add(...) and a.description() are the same class-level calls. The empty
# __init__ with `pass` is unnecessary here.
#
# Concepts: The difference between instance, static, and class methods.
# Static methods are plain functions namespaced inside a class, while class
# methods receive the class as their first argument.
# ============================================================================

class MathUtils:
    def __init__(self):
        pass

    @staticmethod
    def add(a,b):
        return a+b


    @classmethod
    def description(cls):
        print("This is a utility class for Math Operations.")


a=MathUtils
print(a.add(3,54))
a.description()


# Without Creating an Object
MathUtils.description()
print(MathUtils.add(3,6))


# ============================================================================
# Question 5: Dunder Methods __str__ and __len__
# ----------------------------------------------------------------------------
# Topic: Magic/dunder methods, operator overloading
#
# Create a class `Book` with an __init__ that takes `title` and `author` and
# stores them as instance attributes. Then override two dunder methods:
#   - __str__ : returns a readable string in the format
#     "<title> by Author <author>", so that print(book) shows this instead of
#     the default <__main__.Book object at 0x...>.
#   - __len__ : returns the number of characters in the book's title, so that
#     len(book) works on a Book object.
#
# Create two books -- Book("Atomic Habits", "James Clear") and
# Book("The Hobbit", "J.R.R. Tolkien") -- then print each object and print
# len() of each.
#
# Concepts: Dunder methods let your own classes plug into built-in syntax
# (print(), len()). __len__ must return a non-negative int.
# ============================================================================

class Book:

    def __init__(self,title,author):
        self.title=title
        self.author=author

    def __str__(self):
         return f"{self.title} by Author {self.author}"

    def __len__(self):
        return len(self.title)


b1 = Book("Atomic Habits", "James Clear")
b2 = Book("The Hobbit", "J.R.R. Tolkien")


print(b1)
print(b2)
print(len(b1))
print(len(b2))

# ============================================================================
# Question 6: Custom Exception With Multiple except Blocks
# ----------------------------------------------------------------------------
# Topic: Custom exception classes, raise, multiple exception handlers
#
# Define your own exception class `NegativeNumberError` that inherits from
# Exception (with an empty body -- pass).
#
# Then write a program that:
#   1. Asks the user to enter a number and converts it with int().
#   2. If the number is negative, raise
#      NegativeNumberError("Negative numbers are not allowed!").
#   3. Otherwise, computes 45 / num and prints the result.
#
# Handle all three failure modes with separate except clauses:
#   - ValueError            -> print "Error: Please enter a proper number"
#                              (non-numeric input like "abc")
#   - ZeroDivisionError     -> print "Error: You cannot divide by zero!"
#                              (input 0)
#   - NegativeNumberError as e -> print an error message along with the
#                              exception object.
#
# Concepts: User-defined exceptions subclass Exception. `raise` triggers them
# manually. Each except catches one specific type, and `as e` captures the
# instance so its message can be printed.
# ============================================================================

class NegativeNumberError(Exception):
    pass

try:
    num=int(input("Enter a number: "))

    if num < 0:
        raise NegativeNumberError("Negative numbers are not allowed!")
    result=45/num
    print(f"The result is {result}")

except ValueError:
    print("Error: Please enter a proper number")
except ZeroDivisionError:
     print("Error: You cannot divide by zero!")
except NegativeNumberError as e:
    print(f"Error: THe number cannot be negative", e)


# ============================================================================
# Question 7: map, filter, reduce With Lambdas
# ----------------------------------------------------------------------------
# Topic: Functional programming, lambda, functools.reduce
#
# Solve three sub-tasks using anonymous (lambda) functions:
#
#   1. map    -- Given nums = [1, 2, 3, 4, 5], produce a list of the CUBE of
#                each element and print it.  Expected: [1, 8, 27, 64, 125]
#   2. filter -- Given nums2 = [10, 11, 12, 13, 14], produce a list containing
#                only the EVEN numbers and print it.  Expected: [10, 12, 14]
#   3. reduce -- Import reduce from functools. Given nums3 = [1, 2, 3, 4],
#                compute the PRODUCT of all elements by repeatedly multiplying
#                pairs, and print it.  Expected: 24
#
# Remember that map and filter return lazy iterators, so wrap them in list()
# to see the values.
#
# Concepts: map transforms every element, filter keeps elements matching a
# condition, reduce collapses a sequence to a single value. reduce must be
# imported from functools.
# ============================================================================

from functools import reduce

nums=[1,2,3,4,5]
cubes=list(map(lambda x:x**3, nums))
print(cubes)

nums2=[10,11,12,13,14]
even=list(filter(lambda x: x%2==0, nums2))
print(even)

nums3=[1,2,3,4]
product=reduce(lambda a,b: a*b, nums3)
print(product)

# ============================================================================
# Question 8: Walrus Operator :=
# ----------------------------------------------------------------------------
# Topic: Assignment expressions (Python 3.8+)
#
# Two sub-tasks using the walrus operator, which assigns a value AND
# evaluates to it in the same expression:
#
#   1. Input loop: Write a while loop that repeatedly asks "Enter something: "
#      and prints whatever the user typed, stopping when they type "quit".
#      Use the walrus operator so input() is captured into user_input and
#      compared against "quit" in the loop condition itself -- avoiding the
#      usual "read once before the loop, read again at the end" duplication.
#
#   2. List comprehension: Given words = ["python", "rocks", "ai"], build a
#      list of the LENGTHS of only the words whose length is 4 or more.
#      Compute each length once inside the if clause with (n := len(word)) and
#      reuse n as the output expression.  Expected: [6, 5]
#      The commented-out variant asks for the opposite: a list of
#      (word, length) tuples for words shorter than 4 characters.
#      Expected: [('ai', 2)]
#
# Concepts: := computes a value once and reuses it, keeping loops and
# comprehensions concise. The parentheses around (n := len(word)) are required
# in this context.
# ============================================================================

# 1. read input until "quit"

while (user_input := input("Enter something: ")) != "quit":
    print(user_input)


# 2. walrus in a list comprehension

words = ["python", "rocks", "ai"]

lengths = [n for word in words if (n := len(word)) >= 4]
print(lengths)
# short = [(word, n) for word in words if (n := len(word)) < 4]
# print(short)

# ============================================================================
# Question 9: *args and **kwargs
# ----------------------------------------------------------------------------
# Topic: Variable-length argument lists
#
#   1. Write a function sum_all(*args) that accepts ANY number of positional
#      arguments, loops over them accumulating a `total`, and returns the sum.
#      Test it with sum_all(1, 2, 3, 4, 5, 6, 7) -> 28
#
#   2. Write a function print_details(**kwargs) that accepts ANY number of
#      keyword arguments and prints each one on its own line in the format
#      "key: value". Iterate using kwargs.items() to get both the key and
#      value together. Test it with
#      print_details(name="Alice", age=25, city="Delhi"), producing:
#          name: Alice
#          age: 25
#          city: Delhi
#
# The commented-out alternative shows the same result by iterating keys only
# and indexing kwargs[key] -- both work, but .items() is the idiomatic form.
#
# Concepts: *args collects extra positional arguments into a tuple;
# **kwargs collects extra keyword arguments into a dict.
# ============================================================================

def sum_all(*args):
    total=0
    for i in args:
        total+=i
    return total

print(sum_all(1,2,3,4,5,6,7))

def print_details(**kwargs):
    # for key in kwargs:
    #     print(f"{key}: {kwargs[key]}")
    for key, value in kwargs.items():
        print(f"{key}: {value}")


print_details(name="Alice", age=25, city="Delhi")
