# PROBLEM 1:
# Write a decorator called 'banner' that prints a line of '=' before
# and after the decorated function runs.
# Apply it to a function show_menu() that prints "1. Start\n2. Exit".
# Expected output:
#   ==============================
#   1. Start
#   2. Exit
#   ==============================


def banner(func):
    def wrapper():
        print("="*30)
        func()
        print("="*30)
    return wrapper

@banner
def show_menu():
    print("1. Start")
    print("2. Exit")

show_menu()


# PROBLEM 2:
# Write a decorator 'announce' that prints "Calling..." before and "Done!" after.
# It must work on ALL of these without changing the decorator:
#   greet("Ayush")                 -> 1 positional arg
#   add(3, 5)                      -> 2 positional args
#   intro(name="Riya", age=22)     -> keyword args
#   ping()                         -> no args at all


def announce(func):
    def wrapper(*args, **kwargs):
        print("Calling....")
        func(*args, **kwargs)
        print("Done!")
    return wrapper

@announce
def greet(name):
    print(f"Hello {name}")

@announce
def add(a,b):
    print(a+b)

@announce
def intro(name,age):
    print(f"{name}, {age}")

@announce
def ping():
    print("pong")

greet("Ayush")
add(3, 5)
intro(name="Riya", age=22)
ping()


# PROBLEM 3:
# Write a decorator 'shout' that takes a function returning a string,
# and makes the result UPPERCASE with "!!!" added.
#   @shout
#   def greet(name): return f"hello {name}"
#   print(greet("ayush"))   ->  HELLO AYUSH!!!
# Also write a plain 'logger' decorator that just prints "Running..." but
# still correctly returns whatever the function returned.


def shout(func):
    def wrapper(*args,**kwargs):
        result=func(*args,**kwargs)
        return result.upper()+ "!!!"
    return wrapper

def logger(func):
    def wrapper(*args,**kwargs):
        print("Running...")
        return func(*args,**kwargs)
    return wrapper

@shout
def greet(name):
    return f"Hello {name}"

@logger
def add(a,b):
    return a+b

print(greet("ayush"))     # HELLO AYUSH!!!
print(add(3, 5))          # Running...  then  8


# PROBLEM 4:
# Write a decorator 'timer' that measures how long a function takes
# and prints "<function name> took 0.5023 seconds".
# Test it on a function slow_square(n) that sleeps for 1 second
# and returns n * n. Make sure the return value still works.

import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()          # stopwatch START
        result = func(*args, **kwargs)       # the real work
        end = time.perf_counter()            # stopwatch STOP
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result                        # don't lose the answer!
    return wrapper


@timer
def slow_square(n):
    time.sleep(1)
    return n * n


print(slow_square(5))
# slow_square took 1.0012 seconds
# 25



# PROBLEM 5:
# Take the 'logger' decorator from Problem 3 and apply it to a function
# that has a docstring:
#   @logger
#   def add(a, b):
#       """Adds two numbers."""
#       return a + b
# Now print add.__name__ and add.__doc__ . Something is wrong.
# Find out what, then fix it using functools.wraps.



# ---------- THE PROBLEM ----------
def logger_broken(func):
    def wrapper(*args, **kwargs):
        print("Running...")
        return func(*args, **kwargs)
    return wrapper


@logger_broken
def add(a, b):
    """Adds two numbers."""
    return a + b


print(add.__name__)   # wrapper           <- WRONG, expected 'add'
print(add.__doc__)    # None              <- WRONG, docstring gone


# ---------- THE FIX ----------
import functools

def logger(func):
    @functools.wraps(func)              # copies func's identity onto wrapper
    def wrapper(*args, **kwargs):
        print("Running...")
        return func(*args, **kwargs)
    return wrapper


@logger
def subtract(a, b):
    """Subtracts two numbers."""
    return a - b


print(subtract.__name__)   # subtract                 <- correct
print(subtract.__doc__)    # Subtracts two numbers.   <- correct



# PROBLEM 6:
# Improve your repeat(n) decorator from decorators_with_args.py so that:
#   - it works with ANY number of arguments (not just one)
#   - it COLLECTS all the return values into a list and returns that list
# Test:
#   @repeat(3)
#   def double(x): return x * 2
#   print(double(5))    ->  [10, 10, 10]
#
# Then write a second one: @tag("b") that wraps the returned string in <b>...</b>


import functools

def repeat(n):                                 # LAYER 1: takes the setting
    def decorator(func):                       # LAYER 2: takes the function
        @functools.wraps(func)
        def wrapper(*args, **kwargs):          # LAYER 3: takes the call's args
            results = []
            for _ in range(n):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator


def tag(name):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return f"<{name}>{func(*args, **kwargs)}</{name}>"
        return wrapper
    return decorator


@repeat(3)
def double(x):
    return x * 2

@repeat(2)
def add(a, b):
    return a + b

@tag("b")
def greet(name):
    return f"Hello {name}"


print(double(5))         # [10, 10, 10]
print(add(3, 4))         # [7, 7]        <- two args now work
print(greet("Ayush"))    # <b>Hello Ayush</b>



# PROBLEM 7:
# Write two decorators: bold (wraps result in <b>...</b>) and
# italic (wraps result in <i>...</i>).
# Apply BOTH to a function greet() that returns "hello".
# Predict the output BEFORE running, then swap their order and predict again.

import functools

def bold(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return "<b>" + func(*args, **kwargs) + "</b>"
    return wrapper

def italic(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return "<i>" + func(*args, **kwargs) + "</i>"
    return wrapper


@bold
@italic
def greet():
    return "hello"

@italic
@bold
def greet2():
    return "hello"


print(greet())    # <b><i>hello</i></b>
print(greet2())   # <i><b>hello</b></i>


# PROBLEM 8:
# Write a decorator 'count_calls' that tracks how many times a function
# has been called, printing "Call #1 to greet", "Call #2 to greet", etc.
# Also expose the total afterwards as greet.count
# Call greet() four times and then print greet.count.


import functools

def count_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.count += 1                    # the counter lives ON the wrapper
        print(f"Call #{wrapper.count} to {func.__name__}")
        return func(*args, **kwargs)
    wrapper.count = 0                         # set up the counter ONCE
    return wrapper


@count_calls
def greet(name):
    print(f"Hi {name}")


greet("Ayush")     # Call #1 to greet
greet("Riya")      # Call #2 to greet
greet("Karan")     # Call #3 to greet
greet("Zara")      # Call #4 to greet
print(greet.count) # 4


# PROBLEM 9:
# fib(35) computed recursively is painfully slow because it recomputes
# the same values millions of times.
# Write a decorator 'cache' that stores results in a dictionary so each
# input is computed only once.
# Time fib(35) with and without it.


import functools, time

def cache(func):
    stored = {}                            # created ONCE at decoration time

    @functools.wraps(func)
    def wrapper(*args):
        if args in stored:                 # seen this input before?
            return stored[args]            # hand back the saved answer
        result = func(*args)               # first time -> actually compute
        stored[args] = result              # ...and remember it
        return result
    return wrapper


def fib_slow(n):
    if n < 2:
        return n
    return fib_slow(n - 1) + fib_slow(n - 2)

@cache
def fib_fast(n):
    if n < 2:
        return n
    return fib_fast(n - 1) + fib_fast(n - 2)


start = time.perf_counter()
print(fib_slow(32), f"{time.perf_counter() - start:.4f}s")   # ~1.5 seconds

start = time.perf_counter()
print(fib_fast(32), f"{time.perf_counter() - start:.6f}s")   # ~0.00003 seconds



# PROBLEM 10 (final, combines everything):
# Write a decorator 'requires_role(role)' that only lets a function run if
# the user's role matches. Otherwise print "Access denied" and return None.
# The decorated functions take a 'user' dict as their first argument:
#   user = {"name": "Ayush", "role": "admin"}
#
# Then write @validate_positive that raises ValueError if any numeric
# argument is negative.
# Test both, including the failure cases.



import functools

def requires_role(role):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(user, *args, **kwargs):
            if user.get("role") != role:
                print(f"Access denied: {user['name']} is not a {role}")
                return None                         # short-circuit: func NEVER runs
            return func(user, *args, **kwargs)      # allowed -> proceed
        return wrapper
    return decorator


def validate_positive(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for value in args:
            if isinstance(value, (int, float)) and value < 0:
                raise ValueError(f"Negative value not allowed: {value}")
        return func(*args, **kwargs)
    return wrapper


@requires_role("admin")
def delete_database(user):
    print(f"{user['name']} deleted the database!")

@requires_role("admin")
def view_reports(user, month):
    print(f"{user['name']} is viewing reports for {month}")

@validate_positive
def area(length, width):
    return length * width


admin  = {"name": "Ayush", "role": "admin"}
normal = {"name": "Riya",  "role": "user"}

delete_database(admin)         # Ayush deleted the database!
delete_database(normal)        # Access denied: Riya is not a admin
view_reports(admin, "July")    # Ayush is viewing reports for July

print(area(4, 5))              # 20
# print(area(-4, 5))           # ValueError: Negative value not allowed: -4
