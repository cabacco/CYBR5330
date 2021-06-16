import hashlib
import time
import string

'''Beginning of functions needed to run program'''

#Function that compares hash values and prints desired output if a match is found
def FindMatch(guess, guess_hash, num_guess):
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
        match = FindMatch(guess, guess_hash, num_guess)
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

'''This function contains all the code for the dictionary method'''
def DictionaryCrack():
    global start_time
    count = 0 #Initialize guess counter
    while True:
        passlist = input('enter the file path: ') #enter the file path for the wordlist
        try: #Open and read the file
            password_file = open(passlist,'r')
            break
        except: #ask again if file not found
           print('File not found')
           continue
    
    start_time = time.monotonic() #Check start time for cracking session
    
    for word in password_file:        
        enc_word = word.strip().encode('utf-8') #utf-8 encoding 
        digest = str(hashlib.md5(enc_word.strip()).hexdigest()) #md5 hash is computed for the word,strip of white spaces,hexadecimal format 
        count += 1 #count is increased for every word check in the file
        if FindMatch(word.strip(), digest, count): #if hash is matched 
            return #End the for loop

    end_time = time.monotonic()
    elapsed_time = end_time - start_time
    print("Password not in dictionary :(")
    print(f'({count} passwords attempted in {elapsed_time} seconds)')
    return
    
'''This function contains the code for the brute force method'''
def BruteForceCrack():
    global possible_chars, start_time, num_guess
    num_guess = 0 #Initialize guess counter
    match = False #Initialize boolean that will become True when password is cracked
    
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
        
    #Ask user to choose maxmium password length (loop in case of invalid user entry)
    while True:
        #Prompt user for maximum length
        max_len = int(input("Enter max password length (1-5) for brute force attack: "))
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
            return
    elif max_len == 2:
        if BruteLenOne(""):
            return
        if BruteLenTwo(""):
            return
    elif max_len == 3:
        if BruteLenOne(""):
            return
        if BruteLenTwo(""):
            return
        if BruteLenThree(""):
            return
    elif max_len == 4:
        if BruteLenOne(""):
            return
        if BruteLenTwo(""):
            return
        if BruteLenThree(""):
            return
        if BruteLenFour(""):
            return
    elif max_len == 5:
        if BruteLenOne(""):
            return
        if BruteLenTwo(""):
            return
        if BruteLenThree(""):
            return
        if BruteLenFour(""):
            return
        if BruteLenFive():
            return
        
    #Message to display if no password match is found
    if not match:
        end_time = time.monotonic()
        elapsed_time = end_time - start_time
        print("unable to crack password :(")
        print(f'({num_guess} passwords attempted in {elapsed_time} seconds)')
        return
    
'''End of Functions'''

'''Main body of code runs as while loop to allow multiple cracking sessions'''
while True:
    #Give option to close program or run again
    run = input("Type 'close' to exit the program, or any other key to continue: ")
    if run == 'close':
        break

    #Get the hash of the password to be cracked
    pswd_hash = input("Enter the hash of the password you want to crack:")

    #Ask the user to choose dictionary or brute force method
    while True:
        method = input("Choose which cracking method to use\n1: Dictionary\n2: "
                       "Brute Force\n")
        if method != '1' and method != '2':#Error message if user does not choose 1 or 2
            print("Sorry, invalid option. Please try again")
            continue
        break

    if method == '1':
        DictionaryCrack()
    elif method == '2':
        BruteForceCrack()

    
