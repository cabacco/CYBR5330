import hashlib #Library for computing hash values
import re #Library for using regular expressions
import string #Library for manipulating strings
import os

'''Define magic numbers'''
PNG_SOF_string = '89504e470d0a1a0a'
PNG_EOF_string = '49454e44ae426082'
JPG_SOF_string = 'ffd8ffe[01]'
JPG_EOF_string = 'ffd900'
PDF_SOF_string = '25504446'
PDF_EOF_string = '[0ad]{2,4}2525454f46[0ad]{0,4}00'

'''Function definitions needed to run program'''

'''Function to get user input for binary file and directory for writing results'''
def GetUserInput():
    #Ask for path of binary file
    #Ask for path of directory to write to
#    binary_path = 'carve.lab' #debug
    binary_path = 'midterm.dd' #debug
#    output_directory = 'carveFiles' #debug
    output_directory = 'midtermFiles' #debug
    return(binary_path, output_directory)

'''Function to calculates the hash of a carved file and write it to "hashes.txt"'''
def WriteHash(output_directory, hash_file_name):
    #Calculate MD5 hash of file
    #Open hash file
    #with open(hash_file_name, 'a'):
        #Write hash to hash file
    return

'''Function to display file type, location, and size (size is calculated using offsets)'''
def DisplayFileInfo(file_type, SOF, EOF):
    #Print file type
    #Print memory offsets for SOF and EOF
    #Print file size (calculate using EOF-SOF)
    return

'''Function to carve a file from the given binary data. This function will copy the data between
the SOF and EOF and write that data to a new file.'''
def CarveFile(file_type, SOF, EOF, type_counter, binary_data, output_directory):
    #Copy data from binary_data between SOF and EOF
    file_data = binary_data[int(SOF, 16):int(EOF, 16)]

    #Open new file for writing with name <type>-<type counter> (ex. “png-1”)
    #and write data to file
    newFileName = output_directory + "/" + file_type + '-' + str(type_counter)
#    print(newFileName) # debug
    file_newfile = open(newFileName, 'wb')
    file_newfile.write(file_data)
    file_newfile.close()

    #Display file info
    DisplayFileInfo(file_type, SOF, EOF)

    return

'''Function to search binary file for carveable files. This function executes most of the
program. If a file is found, the function will call the necessary functions to carve the file,
store the hash, and display file info.'''
def LocateFiles(file_type, SOF_string, EOF_string, hex_dump, output_directory, hash_file_name, binary_data):
    count = 0
    if file_type == 'png':
        modifier = 0
    else:
        modifier = 2
    regex = re.compile(SOF_string + r'\w+?' + EOF_string)
    locations = regex.finditer(hex_dump)
    for file in locations:
        count += 1
        SOF_offset = hex((file.start()+1) // 2)
        EOF_offset = hex((file.end()-1-modifier) // 2)
        CarveFile(file_type, SOF_offset, EOF_offset, count, binary_data, output_directory)
        #DisplayFileInfo(file_type, SOF_offset, EOF_offset)
        #WriteHash(output_dir, hash_file_name)
    return

'''End of Functions'''

'''Main body of code'''
while True:
    #Give option to close program or run again
    run = input("Type 'close' to exit the program, or any other key to continue: ")
    if run == 'close':
        break

    #Get binary file and output directory from user
    binary_path, output_dir = GetUserInput()
    #Create path for hash file
    hash_file_name = output_dir + 'hashes.txt'
    #Open the binary file
    with open(binary_path, 'rb') as binary_file:
        #Read the binary data into memory
        binary_data = binary_file.read()
        #Convert the binary to hex
        hex_dump = binary_data.hex()

        #Call the LocateFiles function 3 times, one for each type
        print('\n') #Print new line to make output look better
        LocateFiles('png', PNG_SOF_string, PNG_EOF_string, hex_dump, output_dir, hash_file_name, binary_data)
        print('\n')
        LocateFiles('jpg', JPG_SOF_string, JPG_EOF_string, hex_dump, output_dir, hash_file_name, binary_data)
        print('\n')
        LocateFiles('pdf', PDF_SOF_string, PDF_EOF_string, hex_dump, output_dir, hash_file_name, binary_data)

    #Display results
        #Print number of each file type
        #Print directory where files are saved

'''End of code'''
