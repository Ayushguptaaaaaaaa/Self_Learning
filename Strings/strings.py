# ============================================================
#                  PYTHON STRINGS - MUST KNOW NOTES
# ============================================================

# ------------------------------------------------------------
# 1. WHAT IS A STRING?
# ------------------------------------------------------------
# A string is a sequence of characters inside quotes.
# Single or double quotes both work. Triple quotes = multi-line.
#
#   s = 'hello'
#   s = "hello"
#   s = """multi
#          line"""
#
# IMPORTANT: Strings are IMMUTABLE - you cannot change them in place.
#   s[0] = 'H'   # ERROR! TypeError
# Instead, build a NEW string:  s = 'H' + s[1:]

# ------------------------------------------------------------
# 2. INDEXING (accessing single characters)
# ------------------------------------------------------------
#   s = "python"
#
#   Index:      p   y   t   h   o   n
#   Positive:   0   1   2   3   4   5
#   Negative:  -6  -5  -4  -3  -2  -1
#
#   s[0]   -> 'p'   (first character)
#   s[5]   -> 'n'   (last character)
#   s[-1]  -> 'n'   (NEGATIVE INDEXING: last character)
#   s[-2]  -> 'o'   (second from the end)
#   s[6]   -> ERROR! IndexError (out of range)

# ------------------------------------------------------------
# 3. SLICING  ->  s[start : stop : step]
# ------------------------------------------------------------
# Takes a piece of the string. 'stop' is NOT included!
#
#   s = "python"
#   s[0:3]    -> 'pyt'    (index 0,1,2 - stops BEFORE 3)
#   s[2:]     -> 'thon'   (from index 2 to the end)
#   s[:4]     -> 'pyth'   (from start up to index 3)
#   s[:]      -> 'python' (full copy)
#   s[1:-1]   -> 'ytho'   (without first & last char)
#   s[::2]    -> 'pto'    (every 2nd character)
#   s[::-1]   -> 'nohtyp' (REVERSED! step -1 goes backwards)

# ------------------------------------------------------------
# 4. len() - length of a string
# ------------------------------------------------------------
#   len("hello")  -> 5
#   len("")       -> 0
# Last valid index is always len(s) - 1

# ------------------------------------------------------------
# 5. CHANGING CASE
# ------------------------------------------------------------
#   s = "Hello World"
#   s.upper()      -> 'HELLO WORLD'
#   s.lower()      -> 'hello world'
#   s.title()      -> 'Hello World'   (Each Word Capitalized)
#   s.capitalize() -> 'Hello world'   (only first letter)
#   s.swapcase()   -> 'hELLO wORLD'   (flips every letter's case)

# ------------------------------------------------------------
# 6. strip() - removing unwanted spaces/characters
# ------------------------------------------------------------
# Removes characters from BOTH ends (default: whitespace).
#
#   s = "   hello   "
#   s.strip()   -> 'hello'      (spaces removed from both sides)
#   s.lstrip()  -> 'hello   '   (left side only)
#   s.rstrip()  -> '   hello'   (right side only)
#
# Can also strip specific characters:
#   "###python###".strip('#')  -> 'python'
#
# VERY useful for cleaning user input:  name = input().strip()

# ------------------------------------------------------------
# 7. replace() - replacing text
# ------------------------------------------------------------
#   s = "I like Java"
#   s.replace("Java", "Python")  -> 'I like Python'
#
#   "aaa".replace("a", "b")      -> 'bbb'   (replaces ALL by default)
#   "aaa".replace("a", "b", 1)   -> 'baa'   (replace only first 1)
#
# Remember: it returns a NEW string, original stays unchanged!

# ------------------------------------------------------------
# 8. split() and join() - string <-> list
# ------------------------------------------------------------
#   s = "I love Python"
#   s.split()          -> ['I', 'love', 'Python']   (splits on spaces)
#   "a,b,c".split(",") -> ['a', 'b', 'c']           (split on comma)
#
#   words = ['I', 'love', 'Python']
#   " ".join(words)  -> 'I love Python'   (glue list back with " ")
#   "-".join("abc")  -> 'a-b-c'

# ------------------------------------------------------------
# 9. SEARCHING inside a string
# ------------------------------------------------------------
#   s = "hello world"
#
#   "world" in s        -> True    (membership check - most used!)
#   "xyz" not in s      -> True
#
#   s.find("world")     -> 6       (index where it starts)
#   s.find("xyz")       -> -1      (NOT found returns -1, no error)
#   s.index("world")    -> 6       (same, but ERROR if not found)
#
#   s.count("l")        -> 3       (how many times 'l' appears)

# ------------------------------------------------------------
# 10. startswith() and endswith() - checking beginnings/ends
# ------------------------------------------------------------
# Both return True/False. Great for validation checks!
#
#   s = "hello world"
#   s.startswith("hello")   -> True
#   s.startswith("world")   -> False
#   s.endswith("world")     -> True
#   s.endswith("hello")     -> False
#
# Real-world examples:
#   filename = "report.pdf"
#   filename.endswith(".pdf")        -> True   (check file type)
#
#   url = "https://example.com"
#   url.startswith("https://")       -> True   (check secure link)
#
# BONUS: can check MULTIPLE options at once using a tuple:
#   filename.endswith((".jpg", ".png", ".gif"))  -> is it an image?
#   name.startswith(("Mr.", "Mrs.", "Dr."))      -> has a title?
#
# Both are case-sensitive:
#   "Hello".startswith("hello")  -> False
#   Use s.lower().startswith("hello") to ignore case.

# ------------------------------------------------------------
# 11. CHECKING string content (all return True/False)
# ------------------------------------------------------------
#   "abc".isalpha()    -> True   (only letters)
#   "123".isdigit()    -> True   (only digits)
#   "abc123".isalnum() -> True   (letters and/or digits)
#   "   ".isspace()    -> True   (only whitespace)
#   "ABC".isupper()    -> True   (all uppercase)
#   "abc".islower()    -> True   (all lowercase)

# ------------------------------------------------------------
# 12. CONCATENATION and REPETITION
# ------------------------------------------------------------
#   "py" + "thon"   -> 'python'        (+ joins strings)
#   "ha" * 3        -> 'hahaha'        (* repeats)
#   "5" + 5         -> ERROR! Can't add string + number
#   "5" + str(5)    -> '55'            (convert number first)
#   int("5") + 5    -> 10              (or convert string to int)

# ------------------------------------------------------------
# 13. f-STRINGS (modern formatting - MUST KNOW!)
# ------------------------------------------------------------
#   name = "Sam"
#   age = 20
#   print(f"My name is {name} and I am {age}")
#   -> My name is Sam and I am 20
#
#   price = 49.987
#   print(f"Price: {price:.2f}")   -> Price: 49.99  (2 decimals)

# ------------------------------------------------------------
# 14. LOOPING through a string
# ------------------------------------------------------------
#   for char in "abc":        # directly over characters (preferred)
#       print(char)
#
#   for i in range(len(s)):   # by index (when you NEED the position)
#       print(i, s[i])

# ------------------------------------------------------------
# QUICK REFERENCE TABLE
# ------------------------------------------------------------
#   s[i]          -> character at index i
#   s[-1]         -> last character
#   s[a:b]        -> slice from a to b-1
#   s[::-1]       -> reversed string
#   len(s)        -> length
#   s.upper()     -> uppercase        s.lower()   -> lowercase
#   s.strip()     -> trim whitespace  s.replace(old, new)
#   s.split()     -> string to list   sep.join(list) -> list to string
#   s.find(x)     -> index or -1      s.count(x)  -> occurrences
#   x in s        -> True/False       s.startswith / s.endswith
# ============================================================


# 1. Length without len()

# user=input()
# count=0

# for i in user:
#     count+=1

# print(count)

# 2. First and last

# user=input()
# print(user[0])
# print(user[len(user)-1])

# 3. Uppercase / lowercase split
# Given a string like "HeLLo WoRLd", count how many letters are uppercase and how many are lowercase. (Hint: .isupper() and .islower().)

# user=input()
# low=0
# up=0

# for i in user:
#     if i.islower():
#         low+=1
#     elif i.isupper():
#         up+=1

# print(f"{up} and {low}")


# 4. Character frequency
# Ask the user for a word and a letter, then count how many times that letter appears in the word — first with a loop, then check your answer with .count().

# user_word=input()
# user_letter=input().lower()
# count=0

# for i in user_word:
#     if i == user_letter:
#         count+=1

# print(count)

# 5. Palindrome checker

# user=input()
# is_palindrome=True

# for i in range(len(user)//2):
#     if user[i] != user[len(user)-1-i]:
#         is_palindrome=False
#         break
 
# if is_palindrome:
#     print("Yes")
# else:
#     print("No")


# Vowel Remover:-

# user=input().lower()

# new=""

# for i in user:
#     if i != 'a' and i!= 'e' and i != 'i'and i!= 'o' and i != 'u':
#         new+=i


# print(new)

# 7. Word Count:-

# user=input()
# words=user.split()
# print(len(words))


# 8. Capitalize every word (without .title()):-

# user=input()
# words=user.split()
# new=[]

# for word in words:
#     new.append(word[0].upper() + word[1:].lower())

# print(" ".join(new))
# print(user.title())          # verify - should match the line above


# 9. Swap case (without .swapcase()):-

# user=input()
# new=""

# for ch in user:
#     if ch.isupper():
#         new += ch.lower()
#     elif ch.islower():
#         new += ch.upper()
#     else:
#         new += ch          # keep spaces, digits, symbols unchanged

# print(new)


# 10. First non-repeating character:-

user=input()
answer=""

for ch in user:
    if user.count(ch) == 1:
        answer = ch
        break

if answer:
    print(answer)
else:
    print("No non-repeating character")