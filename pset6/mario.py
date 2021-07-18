from cs50 import get_int

# prompt user for height of half-pyramid
while True:
    height = get_int("Height: ")
    if height >= 1 and height <=8:
        break

# print half-pyramid
for i in range(height):
    print(" " * (height - 1 - i), end = "")
    print("#" * (i + 1))
    
