import hashlib #Library for computing hash values
import re #Library for using regular expressions
import os #Library to enable creation of directories

'''Define magic numbers using regex notation'''
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
    binary_path = input("Enter target file path: ")
    #Ask for path of directory to write to
    output_dir_name = input("Enter a name for the output directory: ")
    #Add path notation to directory name
    output_dir = output_dir_name + '/'
    
    return (binary_path, output_dir)

'''Function to calculates the hash of a carved file and write it to "hashes.txt"'''
def WriteHash(new_file_name, hash_file_name):
    
    #Open the carved file and read the data
    with open(output_dir + new_file_name, "rb") as f:
     data = f.read()
     
     #Calculate the hash of the data
     md5hash = hashlib.md5(data).hexdigest()
     print("MD5 Hash :", md5hash)
     
     #Open the hash file and append the new hash
     with open(hash_file_name, 'a') as m:
        m.write(new_file_name + ' :' + md5hash + '\n')
        
    return

'''Function to display file type, location, and size (size is calculated using offsets)'''
def DisplayFileInfo(file_type, SOF, EOF, new_file_name):
    
    #Print file type
    print("\nNew", file_type, "file found")
    
    #Print memory offsets for SOF and EOF
    print("Name :", new_file_name)
    print("File SOF :" ,SOF)
    print("File EOF :" ,EOF)
    
    #Print file size (calculate using EOF-SOF)
    file_size= (int(EOF, 16) - int(SOF, 16))
    print("File Size :" ,file_size ,"bytes")
    
    return

'''Function to carve a file from the given binary data. This function will copy the data between
the SOF and EOF and write that data to a new file.'''
def CarveFile(file_type, SOF, EOF, type_counter, output_dir, hash_file_name):
    
    #Copy data from binary_data between SOF and EOF
    file_data = binary_data[int(SOF, 16):int(EOF, 16)]

    #Open new file for writing with name <type>-<type counter> (ex. “png-1”)    
    new_file_name = file_type + '-' + str(type_counter)
    new_file_path = output_dir + new_file_name
    file_newfile = open(new_file_path, 'wb')
    
    #Write data to file
    file_newfile.write(file_data)
    file_newfile.close()

    #Display file info
    DisplayFileInfo(file_type, SOF, EOF, new_file_name)

    #Compute and save the hash of the file
    WriteHash(new_file_name, hash_file_name)

    return

'''Function to search binary file for carveable files. If a file is found, the function will call a
function to carve the file.'''
def LocateFiles(file_type, SOF_string, EOF_string, hex_dump, output_dir, hash_file_name):
    
    #Initialize counter for number of files found
    count = 0
    
    #If statement to modify EOF offset for JPEG and PDF files since the regex includes a null byte
    if file_type == 'png':
        modifier = 0
    else:
        modifier = 2

    #Compile the regex using the SOF and EOF strings passed from the main code
    #The regex captures the SOF and EOF magic numbers and any amount of content between
    regex = re.compile(SOF_string + r'\w+?' + EOF_string)
    
    #Use re.finditer() to create iterable objects of each match
    locations = regex.finditer(hex_dump)
    
    #For each match found, calculate the memory offsets and call CarveFile()
    for file in locations:
        #Increment file counter
        count += 1
        #Calculate memory offsets in hex
        SOF_offset = hex((file.start()+1) // 2)
        EOF_offset = hex((file.end()-1-modifier) // 2)
        #Carve the file
        CarveFile(file_type, SOF_offset, EOF_offset, count, output_dir, hash_file_name)

    return(count)

'''End of Functions'''

'''Main body of code runs in a while loop until user exits the program'''
while True:
    
    #Give option to close program or run again
    run = input("Type 'close' to exit the program, or any other key to continue: ")
    if run == 'close':
        break

    #Get binary file and output directory from user
    binary_path, output_dir = GetUserInput()
    
    #Create output directory
    os.mkdir(output_dir)
    
    #Create path for hash file
    hash_file_name = output_dir + 'hashes.txt'
    
    #Open the binary file
    with open(binary_path, 'rb') as binary_file:
        #Read the binary data into memory
        binary_data = binary_file.read()
        #Convert the binary to hex
        hex_dump = binary_data.hex()

        #Call the LocateFiles function 3 times, one for each type
        print('\n******PNG files******') #Print new line to make output look better
        png_count = LocateFiles('png', PNG_SOF_string, PNG_EOF_string, hex_dump, output_dir, hash_file_name)
        print('\n******JPEG files******')
        jpg_count = LocateFiles('jpg', JPG_SOF_string, JPG_EOF_string, hex_dump, output_dir, hash_file_name)
        print('\n******PDF files******')
        pdf_count = LocateFiles('pdf', PDF_SOF_string, PDF_EOF_string, hex_dump, output_dir, hash_file_name)

    #Display summary of results
    #Print number of each file type
    print(f'\nFinal results:\n{png_count} PNG files found\n{jpg_count} JPEG files found\n'
          f'{pdf_count} PDF files found\n')

'''End of code'''
