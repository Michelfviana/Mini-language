# Basic arithmetic operations
x = 5
y = 10
z = x + y
print(z)  # Should print 15

# Compound assignments
x += 5
print(x)  # Should print 10

# String operations
name = "John"
greeting = "Hello, " + name
print(greeting)  # Should print "Hello, John"

# List operations
numbers = [1, 2, 3, 4, 5]
sum = 0
for num in numbers:
    sum += num
print(sum)  # Should print 15

# Function definition and call
def add(a, b):
    return a + b

result = add(5, 3)
print(result)  # Should print 8

# If statement
if x > 5:
    print("x is greater than 5")
else:
    print("x is less than or equal to 5")

# While loop
i = 0
while i < 5:
    print(i)
    i += 1 