import hashlib #Library for computing hash values
import re #Library for using regular expressions
import string #Library for manipulating strings

'''Function definitions needed to run program'''

'''Function to get user input for binary file and direcotry for writing results'''
def GetUserInput():
    #Ask for path of binary file
    #Ask for path of directory to write to
    return(binary_path, output_directory)

'''Function to calculates the hash of a carved file and write it to "hashes.txt"'''
def WriteHash(output_directory, hash_file):
    #Calculate MD5 hash of file
    #Open hash file
    with open(hash_file_name, 'a'):
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
def CarveFile(file_type, SOF, EOF, type_counter):
    #Open new file for writing with name <type>-<type counter> (ex. “png-1”)
    #Copy data between SOF and EOF
    #Write data to file
    return

'''Function to search binary file for carveable files. This function executes most of the
program. If a file is found, the function will call the necessary functions to carve the file,
store the hash, and display file info.'''
def LocateFiles(binary_file, output_directory, hash_file):
    #Initialize file type counters
    #Search magic numbers for SOF
    #Loop
        #Search for PNG SOF from last offset
        #If found:
            #SOF = offset of first match byte
            #Search for PNG EOF magic number (from SOF location)
            #EOF = offset
            #Try CarveFile(file_type, SOF, EOF, type_counter)
            #DisplayFileInfo(file_type, SOF, EOF)
            #WriteHash(output_directory, hash_file)
            #Continue (repeat loop from EOF)
    #Loop
        #Search for JPEG SOF
        #If found:
            #SOF = offset of first match byte
            #Search for JPEG EOF magic number (from SOF location)
            #EOF = offset
            #Try CarveFile(file_type, SOF, EOF, type_counter)
            #DisplayFileInfo(file_type, SOF, EOF)
            #Continue (repeat loop from EOF)
    #Loop
        #Search for PDF SOF
        #If found:
            #SOF = offset of first match byte
            #Search for PDF EOF magic number (from SOF location)
            #EOF = offset
            #Try CarveFile(file_type, SOF, EOF, type_counter)
            #DisplayFileInfo(file_type, SOF, EOF)
            #Continue (repeat loop from EOF)
    
    #Display results
        #Print number of each file type
        #Print directory where files are saved
    return

'''End of Functions'''

'''Main body of code'''
while True:
    #Give option to close program or run again
    run = input("Type 'close' to exit the program, or any other key to continue: ")
    if run == 'close':
        break
    
    #Get binary file and output directory from user
    binary_path, output_directory = GetUserInput()
    #Open the binary file and create the hash file
    OpenFiles(binary_path, output_directory)
    #Search the binary for files to be carved
    Locate Files(binary_file, output_directory, hash_file)
