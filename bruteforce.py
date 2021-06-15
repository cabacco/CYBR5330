# brute force password cracking for unsalted MD5 hash

import hashlib

word = input("enter the word to hash: ")
word_bytes = str.encode(word)
md5 = hashlib.md5(word_bytes)
result = md5.hexdigest()
result_string = str(result)

print("MD5 has of ", word ," is: ", result_string)

# create a list of characters to try in the password
possible_chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
pass_len = len(word) # the length of the password we are trying to guess

# Create and initialize structure to keep track of which char in which position
# we are testing; initally all 0 which equates to the first letter in possible_chars
indexes = []
for i in range(0, pass_len):
    indexes.insert(i, 0)
#    print(indexes[i]) #debug


# Since we know password length is < 6 manually construct functions for each possibility
def BruteLenOne(stem):
    i = 0
    while i < len(possible_chars):
        print("current guess ", stem + possible_chars[i], "\n")
        encoded_guess = str.encode(stem + possible_chars[i])
        if hashlib.md5(encoded_guess).hexdigest() == result:
            print("match found: ", stem + possible_chars[i])
            return True
        else:
            i = i + 1
    # if we get this far we didn't find a match
    return False

def BruteLenTwo(stem):
    print("2") # debug
    matchFound = False
    current_stem = ""
    i = 0
    while ((i < len(possible_chars)) and (not matchFound)):
        print("in 2 loop")
        current_stem = possible_chars[i]
        matchFound = BruteLenOne(stem + current_stem)
        i = i + 1
    return matchFound

def BruteLenThree(stem):
    print("3") # debug
    matchFound = False
    current_stem = ""
    i = 0
    while ((i < len(possible_chars)) and (not matchFound)):
        print("in 3 loop")
        current_stem = possible_chars[i]
        matchFound = BruteLenTwo(stem + current_stem)
        i = i + 1
    return matchFound

def BruteLenFour(stem):
    print("4")
    matchFound = False
    current_stem = ""
    i = 0
    while ((i < len(possible_chars)) and (not matchFound)):
        print("in 4 loop")
        current_stem = possible_chars[i]
        matchFound = BruteLenThree(stem + current_stem)
        i = i + 1
    return matchFound

def BruteLenFive(stem):
    print("5")
    matchFound = False
    current_stem = ""
    i = 0
    while ((i < len(possible_chars)) and (not matchFound)):
        print("in 5 loop")
        current_stem = possible_chars[i]
        matchFound = BruteLenFour(stem + current_stem)
        i = i + 1
    return matchFound


# Initialize matchFound
matchFound = False

if pass_len == 1:
    matchFound = BruteLenOne("")
elif pass_len == 2:
    matchFound = BruteLenTwo("")
elif pass_len == 3:
    matchFound = BruteLenThree("")
elif pass_len == 4:
    matchFound = BruteLenFour("")
elif pass_len == 5:
    matchFound = BruteLenFive("")
else:
    print("invalid password length")

if matchFound:
    print("yeah!")
else:
    print("fail")
