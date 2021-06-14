import hashlib
import time

"""Function that compares hash values and prints desired output if a match
is found"""
def FindMatch():
    if guess_hash == pswd_hash: #hash strings match
        end_time = time.monotonic()
        elapsed_time = end_time - start_time
        print('Password cracked!')
        print(f'Password is: {guess}')
        print(f'({num_guess} passwords attempted in {elapsed_time} seconds)')
        return(True)
    else: #hash strings do not match
        return(False)

#Get user input for hash of password to be cracked
pswd_hash = input("Enter the md5 hash of password to crack:")
#Get user input for dictionary file (wordlist) to use for cracking
wordfile = input("Enter the full path of dictionary file:")

wordlist = open(wordfile) #Open dictionary file for reading
start_time = time.monotonic() #Check start time for cracking session
num_guess = 0 #Initialize guess counter
match = False #Initialize boolean that will become True when password is cracked
for guess in wordlist: #Loop through the wordlist one word (line) at a time
    num_guess += 1 #Increment guess counter
    guess = guess.rstrip('\n') #Strip newline character from word
    #Compute the md5 hash and convert to string format
    guess_hash = str(hashlib.md5(str.encode(guess)).hexdigest())
    match = FindMatch() #Call FindMatch function to check if passwords match
    if match: #Password is cracked
        break #End the For loop
    
if match == False: #For loop terminated but no match was found
    print('Password not found in dictionary :(')
