from cs50 import get_float

# prompt user for input
while True:
    change = get_float("Change owed: ")
    if change > 0:
        break

cents = change * 100
coins = 0

# quarters
while cents >= 25:
    coins += 1
    cents -= 25

# dimes
while cents >= 10:
    coins += 1
    cents -= 10

# nickels
while cents >= 5:
    coins += 1
    cents -= 5

# pennies
while cents >= 1:
    coins += 1
    cents -= 1

if cents == 0:
    print(f"{coins}")
    
