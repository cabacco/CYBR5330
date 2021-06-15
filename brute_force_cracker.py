import hashlib
import time
import string

'''Beginning of functions needed to run program'''

#Function that compares hash values and prints desired output if a match is found
def FindMatch(guess, guess_hash):
    if guess_hash == pswd_hash: #hash strings match
        end_time = time.monotonic()
        elapsed_time = end_time - start_time
        print('Password cracked!')
        print(f'Password is: {guess}')
        print(f'({num_guess} passwords attempted in {elapsed_time} seconds)')
        return(True)
    else: #hash strings do not match
        return(False)

'''These functions generate all possible combinations of guesses. Each function calls
the next lower function.BruteLenOne() is the only function that actually checks guesses
against the password. Since we know password length is < 6 we can manually construct
functions for each possibility'''
def BruteLenOne(stem):
    global num_guess, match
    #print('executing BruteLenOne()')
    for i in range(len(possible_chars)):
        num_guess += 1
        guess = stem + possible_chars[i]
        #print("current guess ", guess, "\n")
        guess_hash = str(hashlib.md5(str.encode(guess)).hexdigest())
        match = FindMatch(guess, guess_hash)
        if match:
            break
    return match

def BruteLenTwo(stem):
    global match
    for i in range(len(possible_chars)):
        match = BruteLenOne(stem + possible_chars[i])
        if match:
            break
    return match

def BruteLenThree(stem):
    global match
    for i in range(len(possible_chars)):
        match = BruteLenTwo(stem + possible_chars[i])
        if match:
            break
    return match

def BruteLenFour(stem):
    global match
    for i in range(len(possible_chars)):
        match = BruteLenThree(stem + possible_chars[i])
        if match:
            break
    return match

def BruteLenFive():
    global match
    for i in range(len(possible_chars)):
        match = BruteLenFour(possible_chars[i])
        if match:
            break
    return match
'''End of Functions'''

'''Main body of code runs as while loop to allow multiple cracking sessions'''
while True:
    #Give option to close program or run again
    run = input("Type 'close' to exit the program, or any other key to continue:")
    if run == 'close':
        break

    #Get the password to be cracked (for testing purposes)
    #Final implementation will ask for hash directly
    word = input("Enter the word to hash:")
    #Compute the md5 hash and convert to string format
    pswd_hash = str(hashlib.md5(str.encode(word)).hexdigest())
    #print("MD5 hash of ", word ," is: ", pswd_hash) #Debug

    #Ask user to choose character set to use (loop in case of invalid user entry)
    while True:
        #Prompt user for choice
        print("Choose character set for brute force attack from the following options")
        char_set = input("1: [a-z]\n2: [A-Z]\n3: [a-z, A-Z]\n4: [0-9]\n5: [a-z, A-Z, 0-9]\n"
                         "6: all non-whitespace characters\n")
        #Set possible characters according to user selection
        if char_set == '1':
            possible_chars = string.ascii_lowercase
            break
        elif char_set == '2':
            possible_chars = string.ascii_uppercase
            break
        elif char_set == '3':
            possible_chars = string.ascii_letters
            break
        elif char_set == '4':
            possible_chars = string.digits
            break
        elif char_set == '5':
            possible_chars = string.ascii_letters + string.digits
            break
        elif char_set == '6':
            possible_chars = string.ascii_letters + string.digits + string.punctuation
            break
        else: #Error message if user does not choose 1-6
            print("Sorry, invalid option. Please try again")
            continue

    num_guess = 0 #Initialize guess counter
    match = False #Initialize boolean that will become True when password is cracked

    #Ask user to choose maxmium password length (loop in case of invalid user entry)
    while True:
        #Prompt user for maximum length
        max_len = int(input("Enter max password length (1-5) for brute force attack:"))
        if max_len < 1 or max_len > 5: #Error message if user does not choose 1-5
            print("Sorry, invalid option. Please try again")
            continue
        else:
            break
        
    start_time = time.monotonic() #Check start time for cracking session

    #Call successive cracking functions based on maximum length
    #Program will try all single-characters, then all 2-character combos, and so on
    #Program will stop cracking as soon as match is found
    if max_len == 1:
        if BruteLenOne(""):
            continue
    elif max_len == 2:
        if BruteLenOne(""):
            continue
        if BruteLenTwo(""):
            continue
    elif max_len == 3:
        if BruteLenOne(""):
            continue
        if BruteLenTwo(""):
            continue
        if BruteLenThree(""):
            continue
    elif max_len == 4:
        if BruteLenOne(""):
            continue
        if BruteLenTwo(""):
            continue
        if BruteLenThree(""):
            continue
        if BruteLenFour(""):
            continue
    elif max_len == 5:
        if BruteLenOne(""):
            continue
        if BruteLenTwo(""):
            continue
        if BruteLenThree(""):
            continue
        if BruteLenFour(""):
            continue
        if BruteLenFive():
            continue
    #Message to display if no password match is found
    if not match:
        end_time = time.monotonic()
        elapsed_time = end_time - start_time
        print("unable to crack password :(")
        print(f'({num_guess} passwords attempted in {elapsed_time} seconds)')
        continue
