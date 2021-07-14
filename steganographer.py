'''Steganographer.py'''

'''Import Statements'''
import cv2 #Library to enable reading of images
import numpy as np #Library to enable the matrices used by cv2

'''Function block'''

'''Function to get user input for mode'''
def ChooseMode():

    while True:
        #Print user prompt
        print('\nWelcome to Steganographer! The program runs in two modes: "Embed" and "Extract". '
              'Choose Embed if you wish to hide a message in the carrier image file. '
              'Choose Extract if you wish to retrieve a previously hidden file.')
        #Receive user input to select mode
        mode = input('\n1: Embed\n2: Extract\n\nPlease enter your choice: ')
        #Return choice if valid
        if mode == '1' or mode == '2':
            return(mode)
        #Print error message if selection is not 1 or 2
        print('\nSorry, that is not a valid choice. Please enter "1" or "2" to select a mode.')

''''''
def EmbedSecret(carrier_image):

    #Get the secret data as a binary string
    secret_binary = ChooseSecret()
    #Add delimiter at the end of secret_binary
    #Check number of bits in secret_binary

    #Calculate number of pixels in carrier_image
    #If number of bits in secret_binary > number of pixels*3, output error message

    #Embed the secret binary data in the LSBs of each pixel in carrier_image
        #Loop through pixel values in carrier_image
        #Change the LSB for each color in each pixel to the next bit of secret_binary

    #Store the new image as a new file (i.e. <carrier file name> + "-steg"

    ComputeHash(carrier_file)
    ComputeHash(new_file)

    #Print original and new file name, size, MD5 hash
    
    
    return

''''''
def ExtractSecret(steg_image):

    #Extract the secret binary data from the LSBs of each pixel in steg_image
        #Loop through pixel values in steg_image
        #Record the LSB for each color in each pixel as the next bit of secret_binary

    #Change the secret_binary into ASCII text
    #Print the secret text

    return

''''''
def ComputeHash():

    #

    return(md5)

''''''
def DisplayInfo():

    #

    return

'''Function to open file and convert to binary string'''
def GetFileBinary(file_name):

    #Open file and convert to binary string
    with open(file_name, 'rb') as file:
        file_data = file.read()
        file_binary = ''.join([format(character, '08b') for character in file_data])
    return(file_binary)

'''Function to get secret data from user and return it in binary form'''
def ChooseSecret():
    while True:
        #Get user input selection
        print('\nYou may enter a secret message directly or choose a file to hide.')
        choice = input('\n1: Enter message\n2: Choose file\nPlease enter "1" or "2": ')

        #Get user message if choice is "1"
        if choice == '1':
            secret = input('\nPlease enter the message to hide: ')
            #Convert message to binary
            secret_binary = ''.join([format(ord(character), '08b') for character in secret])
            
        #Get file name if choice is "2"
        elif choice == '2':
            secret_file = input('\nPlease enter name of file to hide: ')
            secret_binary = GetFileBinary(secret_file)

        return(secret_binary)
        
''''''
def Function():

    #

    return

'''End of function block'''

'''Main body of program'''
while True:

    #Give option to close program or run again
    run = input('\nType "close" to exit the program, or any other key to continue: ')
    if run == 'close':
        break

    if int(ChooseMode()) == 1:
        #Specify carrier file
        carrier_file = 'jpg-1'
        #Option to ask user for carrier file instead of hardcoding the file name, if desired
        #carrier_file = input('Enter the name of the carrier file (Must be in program directory): ')
        carrier_image = cv2.imread(carrier_file)
        EmbedSecret(carrier_image)
        
    else:
        steg_file = input('\nPlease enter the name of the ')
        steg_image = cv2.imread(steg_file)
        ExtractSecret(steg_image)

'''End of program'''
