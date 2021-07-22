from cs50 import get_string
import re

# prompt user for input
text = get_string("Text: ")

# set number of letters to 0
letters = 0

# initialize text length
length = len(text)

# initialize number of words
words = 0

# initialize number of sentences
sentences = 0

# count each letter
i = 0
while i < length:
    if text[i].isalpha():
        letters += 1

    if (i == 0 and text[i] != " ") or (i != length and text[i] == " " and text[i + 1] != " "):
        words += 1

    if text[i] == "." or text[i] == "!" or text[i] == "?":
        sentences += 1
    i += 1

# average number of letters per 100 words
L = (letters / words) * 100

# average number of sentences per 100 words
S = (sentences / words) * 100

# Coleman-Liau index
index = round(0.0588 * L - 0.296 * S - 15.8)

if index < 1:
    print("Before Grade 1")

elif index >= 16:
    print("Grade 16+")

else:
    print(f"Grade {index}")
    
