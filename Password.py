import hashlib           #import hashlib module
flag=0                   #flag will be set to zero :If password  matched flag is set to 1 and if it is zero there is no password match in the list
count=0                  #password guess count is set to zero
input_hash = input('enter md5 hash: ')          #enter the md5 hash
passlist = input('enter the file path: ')       #enter the file path for the wordlist

try:                                            #Open and read the file
        #password_file = open ('C:\\Users\\imran\\AppData\\Local\\Programs\\Python\\Python35\\Pass.txt.txt','r')
        password_file = open ('passlist','r')
except:                                          #quit if file not found
   quit(0)

for word in password_file:                              #for loop to check the words in input file
  enc_word = word.encode('utf-8')                       #utf-8 encoding 
  digest = hashlib.md5(enc_word.strip()).hexdigest()    #md5 hash is computed for the word,strip of white spaces,hexadecimal format 
  print(digest)                                         #print the hash
  count +=1                                             #count is increased for every word check in the file
  print(count)                                          #print the number of guesses             

  if digest == input_hash:                              #if hash is matched 
      print("password found")                           #Print password found
      print("password is  " + word)                     #print password
      flag=1                                            #flag is set to 1 if password is cracked
      break                                             #End the for loop

    
if flag==0:                                             #if flag is zero
    print("Password not in the file")                   #Print password is not in the file
    print(count)                                        #print the number of guesses  
                                               
