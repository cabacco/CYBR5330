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

    #debug begin
    print('Image dimensions: ', carrier_image.shape)
    cv2.imshow('Carrier image', carrier_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #debug end

    #Check number of bits in secret_binary
    lenSecret = len(secret_binary)
    print("bits in message = ", lenSecret) #debug
    #Calculate number of pixels in carrier_image
    numBitsCarrier = carrier_image.shape[0] * carrier_image.shape[1] * 3
    print("bits in carrier = ", numBitsCarrier) #debug
    #If number of bits in secret_binary > number of pixels*3, output error message
    if lenSecret > numBitsCarrier:
        raise ValueError("The carrier image is too small to hide the message provided!")
    else:
        print("Carrier file is large enough to hide message, proceeding...") #debug

    #Embed the secret binary data in the LSBs of each pixel in carrier_image
    pixelCount = 0
    for row in carrier_image:
        print("shape of row: ", row.shape) #debug
        print("pixelCount ", pixelCount, " lenSecret ", lenSecret) #debug
        cv2.imshow('Carrier image', carrier_image) #debug
        cv2.waitKey(0) #debug
        cv2.destroyAllWindows() #debug
        for currentPixel in row:
            print("pixelCount ", pixelCount, " lenSecret ", lenSecret) #debug
            red, green, blue = [format(i, "08b") for i in currentPixel]
            print("BEFORE: red ", red, ", green ", green, ", blue ", blue) #debug
            if pixelCount < lenSecret:
                #stuff data from secret message into LSB of "red"
                currentPixel[0] = int(red[:-1] + secret_binary[pixelCount], 2)

                print("shape is: ", currentPixel[0].shape) #debug
                print("value is: ", currentPixel[0]) #debug
                print("pixelCount is: ", pixelCount) #debug
                red, green, blue = [format(i, "08b") for i in currentPixel]
                print("R AFTER, hid (", secret_binary[pixelCount], ")", ": red ", red, ", green ", green, ", blue ", blue) #debug

                pixelCount += 1
            if pixelCount < lenSecret:
                #stuff data from secret message into LSB of "green"
                currentPixel[1] = int(green[:-1] + secret_binary[pixelCount], 2)

                red, green, blue = [format(i, "08b") for i in currentPixel]
                print("G AFTER, hid (", secret_binary[pixelCount], ")", ": red ", red, ", green ", green, ", blue ", blue) #debug

                pixelCount += 1
            if pixelCount < lenSecret:
                #stuff data from secret message into LSB of "blue"
                currentPixel[2] = int(blue[:-1] + secret_binary[pixelCount], 2)

                red, green, blue = [format(i, "08b") for i in currentPixel]
                print("B AFTER, hid (", secret_binary[pixelCount], ")", ": red ", red, ", green ", green, ", blue ", blue) #debug

                pixelCount += 1

            if pixelCount >= lenSecret:
                break
        if pixelCount >= lenSecret: #allows us to break out early for short message
            break

    #debug begin
    print('Image dimensions: ', carrier_image.shape)
    print("Has the image changed?")
    cv2.imshow('Carrier image', carrier_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #debug end

    #Store the new image as a new file (i.e. <carrier file name> + "-steg.jpg"
    #NOTE: the extension with the file type, e.g. ".jpg" is required by cv2
    new_file_name = "jpg-1-steg.jpg"
    wasWritten = cv2.imwrite(new_file_name, carrier_image)
    if wasWritten:
        print("Image with secret message written to file: ", new_file_name)
    else:
        print("ERROR WRITING IMAGE!")

    #Print original and new file name, size, MD5 hash
    DisplayInfo()

    return

''''''
def ExtractSecret(steg_image):

    #Extract the secret binary data from the LSBs of each pixel in steg_image
        #Loop through pixel values in steg_image
        #Record the LSB for each color in each pixel as the next bit of secret_binary

    #Change the secret_binary into ASCII text
    #Print the secret text

    return

'''Function to get secret data from user and return it in binary form'''
def ChooseSecret():
    while True:
        #Get user input selection
        print('\nYou may enter a secret message directly or choose a file to hide.')
        choice = input('\n1: Enter message\n2: Choose file\nPlease enter "1" or "2": ')

        #Get user message if choice is "1"
        if choice == '1':
            secret = input('\nPlease enter the message to hide: ')
            print('Length of message: ', len(secret)) #debug

            #Convert message to binary
            secret_binary = ''.join([format(ord(character), "08b") for character in secret])

        #Get file name if choice is "2"
        elif choice == '2':
            secret_file = input('\nPlease enter name of file to hide: ')
            secret_binary = GetFileBinary(secret_file)

        #Append delimiter '$$$$$$$' to binary string
        for i in range(7):
            secret_binary += '00100100'

        print('length of binary message: ', len(secret_binary)) #debug
        #print('type of binary message: ', type(secret_binary)) #debug
        print('binary message: ', secret_binary) #debug, NOTE: this is reversed from expected

        return(secret_binary)

'''Function to compute MD5 hash of a file'''
def ComputeHash(file_name):

    with open(file_name, "rb") as f:
        data = f.read()
    md5 = hashlib.md5(data).hexdigest()
    return(md5)

''''''
def DisplayInfo():

    carrier_hash = ComputeHash(carrier_file)
    stego_hash = ComputeHash(steg_file)

    carrier_size = os.path.getsize(carrier_file)
    stego_size = os.path.getsize(steg_file)

    #Print
    print(f'\nOriginal Carrier Image:\nName: {carrier_file}\nSize:{carrier_size}\nMD5: {carrier_hash}')
    print(f'\nStego Image:\nName: {steg_file}\nSize:{steg_size}\nMD5: {steg_hash}')

    return

'''Function to open file and convert to binary string'''
def GetFileBinary(file_name):

    #Open file and convert to binary string
    with open(file_name, 'rb') as file:
        file_data = file.read()
        file_binary = ''.join([format(character, '08b') for character in file_data])

    return(file_binary)

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
        steg_file = input('\nPlease enter the name of the stego image in which the message is hidden: ')
        steg_image = cv2.imread(steg_file)
        ExtractSecret(steg_image)

'''End of program'''
