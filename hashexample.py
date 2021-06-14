#Simple python code to generate and display an md5 hash from user input (from Isaac)
import hashlib

word = input("enter the word to hash:")
word_bytes = str.encode(word)
md5 = hashlib.md5(word_bytes)
result = md5.hexdigest()
result_string = str(result)
print(result_string)
