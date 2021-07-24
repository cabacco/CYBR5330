'''
Steganographer.py

The use of the cv2 image processing library for LSB steganography was informed by an article
in "Towards Data Science" by Rupali Roy
(https://towardsdatascience.com/hiding-data-in-an-image-image-steganography-using-python-e491b68b1372)
'''

'''Import Statements'''
import cv2 #Library to enable reading of images
import numpy as np #Library to enable the matrices used by cv2
import hashlib #Library to enable calculation of hash values
import os #Library to enable checking file size
import re #Library to enable regular expressions

'''Function block'''

'''Function to get user input for mode'''
def ChooseMode():

    while True:
        #Print user prompt
        print('\nWelcome to Steganographer!\n\nThe program runs in two modes: "Embed" and "Extract"'
              '\nChoose Embed if you wish to hide a message in the carrier image file'
              '\nChoose Extract if you wish to retrieve a previously hidden file')
        #Receive user input to select mode
        mode = input('\n1: Embed\n2: Extract\n\nPlease enter your choice: ')
        #Return choice if valid
        if mode == '1' or mode == '2':
            return(mode)
        #Print error message if selection is not 1 or 2
        print('\nSorry, that is not a valid choice. Please enter "1" or "2" to select a mode.')

'''Function to embed a given binary string into the LSB of each pixel in an image'''
def EmbedSecret(carrier_image):

    #Get the secret data as a binary string
    secret_binary = ChooseSecret()

    #Check number of bits in secret_binary
    lenSecret = len(secret_binary)
    #Calculate number of pixels in carrier_image
    numBitsCarrier = carrier_image.shape[0] * carrier_image.shape[1] * 3
    #If number of bits in secret_binary > number of pixels*3, output error message
    if lenSecret > numBitsCarrier:
        print("The carrier image is too small to hide the message provided!")
        return
    else:
        print("Carrier file is large enough to hide message, proceeding...")
    
    #Embed the secret binary data in the LSBs of each pixel in carrier_image
    #until all of the message plus deliminater has been inserted; the end could
    #be reached part way through a pixel so we check for each channel (red,
    #green, blue)
    #Code template taken from link listed above
    pixelCount = 0
    for row in carrier_image:
        for currentPixel in row:
            #Retrieve current values to be modified
            blue, green, red = [format(i, "08b") for i in currentPixel]
            if pixelCount < lenSecret:
                #stuff data from secret message into LSB of "red"
                currentPixel[0] = int(blue[:-1] + secret_binary[pixelCount], 2)
                pixelCount += 1
            if pixelCount < lenSecret:
                #stuff data from secret message into LSB of "green"
                currentPixel[1] = int(green[:-1] + secret_binary[pixelCount], 2)
                pixelCount += 1
            if pixelCount < lenSecret:
                #stuff data from secret message into LSB of "blue"
                currentPixel[2] = int(red[:-1] + secret_binary[pixelCount], 2)
                pixelCount += 1
            if pixelCount >= lenSecret:
                break
            red, green, blue = [format(i, "08b") for i in currentPixel]            
        if pixelCount >= lenSecret: #allows us to break out early for short message
            break

    #regex to grab file name without extension
    regex = re.compile('(\S+)(?:[.])')
    carrier_name = regex.match(carrier_file).group(1)
    #Store the modified image as a new file (i.e. <carrier file name> + "-steg.png"        
    #NOTE: the extension with the file type, e.g. ".png" is required by cv2
    new_file_name = carrier_name + "-steg.png"
    wasWritten = cv2.imwrite(new_file_name, carrier_image)
    if not wasWritten:
        print("ERROR WRITING IMAGE!")

    #Print original and new file name, size, MD5 hash
    DisplayInfo(new_file_name)

    return

'''Function to exctract binary data from the LSB of each pixel in an image and print
it to the screen'''
def ExtractSecret(steg_image):

    #Extract the secret binary data from the LSBs of each pixel in steg_image
    #Code template taken from link listed above
    encoded_data = ""
    for row in steg_image:
        for pixel in row:
            r, g, b = [format(i, "08b") for i in pixel]
            encoded_data += r[-1]
            encoded_data += g[-1]
            encoded_data += b[-1]
            
    # split into bytes
    all_bytes = [ encoded_data[i:i+8] for i in range(0, len(encoded_data), 8) ]
    
    #String bytes together until delimiter is reached
    decoded_data = ""
    for byte in all_bytes:
        #Append ASCII character to decoded string
        decoded_data += chr(int(byte, 2))
        #Stop when delimiter is found
        if decoded_data[-5:] == "$$$$$":
            break

    #Print the extracted message
    print(f'\nSecret message: "{decoded_data[:-5]}"')
    
    return
    

'''Function to get secret data from user and return it in binary form'''
def ChooseSecret():
    while True:
        #Get user input selection
        print('\nYou may enter a secret message directly or choose a file to hide.')
        choice = input('\n1: Enter message\n2: Choose file\n\nPlease enter "1" or "2": ')

        #Get user message if choice is "1"
        if choice == '1':
            secret = input('\nPlease enter the message to hide: ')
            #print('Length of message: ', len(secret)) #debug

            #Convert message to binary
            secret_binary = ''.join([format(ord(character), "08b") for character in secret])

        #Get file name if choice is "2"
        elif choice == '2':
            secret_file = input('\nPlease enter name of file to hide: ')
            secret_binary = GetFileBinary(secret_file)
            
        #If user input not valid, prompt for new entry
        else:
            print('\nSorry, that is not a valid choice. Please enter "1" or "2"')
            continue
        
        #Append delimiter '$$$$$' to binary string
        for i in range(5):
            secret_binary += '00100100'

        return(secret_binary)

'''Function to compute MD5 hash of a file'''
def ComputeHash(file_name):
    #Read in file data and compute MD5 hash
    with open(file_name, "rb") as f:
        data = f.read()
    md5 = hashlib.md5(data).hexdigest()
    return(md5)

'''Function to print info to screen about carrier file and stego file'''
def DisplayInfo(steg_file):

    #Compute hash of original and new files
    carrier_hash = ComputeHash(carrier_file)
    steg_hash = ComputeHash(steg_file)

    #Get size of original and new files
    carrier_size = round(os.path.getsize(carrier_file) / 1024, 2)
    steg_size = round(os.path.getsize(steg_file) / 1024, 2)

    #Print file info to screen
    print(f'\nOriginal Carrier Image:\nName: {carrier_file}\nSize:{carrier_size} KB\nMD5: {carrier_hash}')
    print(f'\nStego Image:\nName: {steg_file}\nSize:{steg_size} KB\nMD5: {steg_hash}')

    return

'''Function to open file and convert to binary string'''
def GetFileBinary(file_name):

    #Open file and convert to binary string
    with open(file_name, 'rb') as file:
        file_data = file.read()
        file_binary = ''.join([format(character, '08b') for character in file_data])

    return(file_binary)

'''End of function block'''

'''Main body of program'''
while True:

    #Give option to close program or run again
    run = input('\nType "close" to exit the program, or any other key to continue: ')
    if run == 'close':
        break

    #Run Embed mode
    if int(ChooseMode()) == 1:
        #Ask user for name carrier PNG
        carrier_file = input('\nEnter the name of the carrier PNG (Must be in program directory): ')
        #Open the image using the OpenCV module
        carrier_image = cv2.imread(carrier_file)
        #Call EmbedSecret()
        EmbedSecret(carrier_image)

    #Run Extract mode
    else:
        #Ask user for name of stego image
        steg_file = input('\nPlease enter the name of the stego image in which the message is hidden: ')
        #Open the image using the OpenCV module
        steg_image = cv2.imread(steg_file)
        #Call ExtractSecret()
        ExtractSecret(steg_image)

'''End of program'''
