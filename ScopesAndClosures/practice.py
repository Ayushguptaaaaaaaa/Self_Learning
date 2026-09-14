# ============================================================
# SCOPES AND CLOSURES - Short Notes
# ============================================================


# ------------------------------------------------------------
# WHAT IS SCOPE?
# ------------------------------------------------------------
# Scope means "where a variable can be seen/used" in your code.
# A variable made inside a function is NOT visible outside it.


# ------------------------------------------------------------
# TYPES OF SCOPE (LEGB Rule)
# ------------------------------------------------------------
# Python looks for a variable in this order:
#   L - Local     -> inside the current function
#   E - Enclosing -> inside the outer function (for nested functions)
#   G - Global    -> at the top level of the file
#   B - Built-in  -> names Python already gives us (print, len, etc.)


# ------------------------------------------------------------
# 1. LOCAL SCOPE
# ------------------------------------------------------------
# 'x' lives ONLY inside the function. Outside, it does not exist.

# def my_func():
#     x = 10          # local variable
#     print(x)

# my_func()           # works -> 10
# print(x)            # ERROR -> x is not defined outside


# ------------------------------------------------------------
# 2. GLOBAL SCOPE
# ------------------------------------------------------------
# 'y' is made at the top, so any function can READ it.

# y = 5

# def show():
#     print(y)        # can read global y -> 5

# show()


# ------------------------------------------------------------
# 3. 'global' KEYWORD
# ------------------------------------------------------------
# To CHANGE a global variable inside a function, use 'global'.

# count = 0

# def increase():
#     global count    # now we can change the global 'count'
#     count = count + 1

# increase()
# print(count)        # 1


# ------------------------------------------------------------
# 4. ENCLOSING SCOPE + 'nonlocal' KEYWORD
# ------------------------------------------------------------
# Inner function can see the outer function's variable.
# Use 'nonlocal' to CHANGE the outer (enclosing) variable.

# def outer():
#     msg = "hi"
#     def inner():
#         nonlocal msg
#         msg = "hello"     # changes outer's msg
#     inner()
#     print(msg)            # hello

# outer()


# ============================================================
# WHAT IS A CLOSURE?
# ============================================================
# A closure is when an INNER function REMEMBERS the variables
# of its OUTER function, even AFTER the outer function is done.
#
# In simple words: the inner function "carries" data with it.


# ------------------------------------------------------------
# EXAMPLE 1: Basic Closure
# ------------------------------------------------------------
# def greet(name):
#     def message():
#         print(f"Hello {name}!")   # remembers 'name'
#     return message                # return the inner function

# say_hi = greet("Ayush")
# say_hi()                          # Hello Ayush!
# Even though greet() finished, 'name' is still remembered.


# ------------------------------------------------------------
# EXAMPLE 2: Closure that keeps a value (multiplier)
# ------------------------------------------------------------
# def multiplier(n):
#     def multiply(x):
#         return x * n              # 'n' is remembered
#     return multiply

# times3 = multiplier(3)
# times5 = multiplier(5)

# print(times3(10))                 # 30
# print(times5(10))                 # 50


# ------------------------------------------------------------
# EXAMPLE 3: Closure as a counter (keeps its own memory)
# ------------------------------------------------------------
# def counter():
#     count = 0
#     def increase():
#         nonlocal count
#         count += 1
#         return count
#     return increase

# c = counter()
# print(c())                        # 1
# print(c())                        # 2
# print(c())                        # 3
# The 'count' stays alive between calls -> closure remembers it.


# ------------------------------------------------------------
# QUICK SUMMARY
# ------------------------------------------------------------
# Scope   -> where a variable can be used (LEGB rule).
# global  -> change a global variable inside a function.
# nonlocal-> change an outer function's variable from inside.
# Closure -> inner function that remembers outer variables,
#            even after the outer function has finished.
