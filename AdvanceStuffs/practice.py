# numbers=[1,2,3,4,5]
# squares=[]

# for i in numbers:
#     square=i*i
#     squares.append(square)

# print(squares)
# ---------OR--------
# squares=[i*i for i in numbers]


# numbers=[1,2,3,4,5,6,7,8,9,10]
# even=[]

# for i in numbers:
    # if i%2==0:
        # even.append(i)

# print(even)
# ----------OR-----------

# evens=[i for i in numbers if i%2==0]

# Convert to Uppsercase
# names=["ram", "shyam", "ghanshyam"]

# results=[i.upper() for i in names]

# print(results)



#ENUMERATE FUNCTION-returns result plus index number

# Names plus indexing number:-

# names=["Aman", "Neha", "Ravi"]

# for i in range(len(names)):
#     print(i, names[i])


    # ---------OR-------

# for index, name in enumerate(names, start=1):
    # print(index, name)



# ZIP and UNZIP:-

names=["Aman", "Neha", "Ravi"]
marks=[80,90,70]

# for i in range(len(marks)):
#     print(names[i], marks[i])


# ---------OR----------

for name,mark in zip(names, marks):
    print(name, mark)

# Unzip is a concept not a function:-
data=[("Aman",80),("Neha",90),("Ravi",70)]

names, marks=zip(*data)
print(list(names))
print(marks) 