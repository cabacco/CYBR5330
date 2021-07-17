import hashlib #Library for computing hash values
import re #Library for using regular expressions
import os #Library to enable creation of directories

'''Define magic numbers using regex notation'''
PNG_SOF_string = '89504e470d0a1a0a'
PNG_EOF_string = '49454e44ae426082'
JPG_SOF_string = 'ffd8ffe[018d]'
JPG_EOF_string = '(?:ffda\w+?)(ffd9)'
PDF_SOF_string = '25504446'
PDF_EOF_string = '[0ad]{2,4}2525454f46[0ad]{0,4}(?=00)'

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
def WriteHash(new_file_name):

    #Open the carved file and read the data
    with open(output_dir + new_file_name, "rb") as f:
     data = f.read()

     #Calculate the hash of the data
     md5hash = hashlib.md5(data).hexdigest()

     #Open the hash file and append the new hash
     with open(hash_file_name, 'a') as m:
        m.write(new_file_name + ' :' + md5hash + '\n')

    return

'''Function to display file type, location, and size (size is calculated using offsets)'''
def DisplayFileInfo(file_type, SOF, EOF, new_file_name):

    #Print memory offsets for SOF and EOF
    print(f"\nCarved '{new_file_name}'")
    print("File SOF :" ,SOF)
    print("File EOF :" ,EOF)

    #Print file size (calculate using EOF-SOF)
    file_size= (int(EOF, 16) - int(SOF, 16))
    print("File Size :" ,file_size ,"bytes")

    return

'''Function to carve a file from the given binary data. This function will copy the data between
the SOF and EOF and write that data to a new file.'''
def CarveFile(file_type, SOF, EOF, type_counter):
    
    #Copy data from binary_data between SOF and EOF
    file_data = binary_data[int(SOF, 16):int(EOF, 16)]

    #Open new file for writing with name <type>-<type counter> (ex. “png-1”)
    new_file_name = file_type + '-' + str(type_counter) + '.' + file_type
    new_file_path = output_dir + new_file_name
    file_newfile = open(new_file_path, 'wb')

    #Write data to file
    file_newfile.write(file_data)
    file_newfile.close()

    #Display file info
    DisplayFileInfo(file_type, SOF, EOF, new_file_name)

    #Compute and save the hash of the file
    WriteHash(new_file_name)

    return

'''Function to search hex dump for carveable JPEGs. If a JPEG is found, the function will
call a function to carve the JPEG.'''
def LocateJPEGs(file_type, SOF_string, EOF_string):

    print('\nsearching for JPEGs...')
    #Compile regex for the SOF string
    SOF_regex = re.compile(SOF_string)

    #Create a list of all SOF matches in the hex dump
    SOF_matches = SOF_regex.finditer(hex_dump)

    #Loop through SOF matches to remove any invalid byte positions (i.e. starts on odd number)
    SOF_locations = []
    for match in SOF_matches:
        if match.start()%2 == 0:
            SOF_locations.append(match.start())

    '''This giant complicated section searches from each SOF position to find the nearest
        valid EOF position. It also creates the list of offsets in hexadecimal format.'''
    #Create dynamic lists to hold values as they are found
    SOF_offsets = []
    EOF_offsets = []
    EOF_locations = []
    #Initialize boolean so that operation is different 
    first_match = True
    #This will loop through each recorded SOF marker location
    for match in SOF_locations:
        #Calculate the memory offset and add to offset list
        SOF_offsets.append(hex(match // 2))
        #Compile the default JPEG EOF regex
        EOF_regex = re.compile(EOF_string)
        #Search for the first EOF marker from the current SOF location
        EOF = EOF_regex.search(hex_dump, match+8)
        z = 0 #Counter to track number of invalid EOFs (i.e. odd-numbered starting locations)
        #Loop that runs until a valid, non-duplicate EOF is found
        while True:
            #Check that the string is matching on the byte boundary (even-numbered index)
            if EOF.end(1)%2 == 0:
                #If a valid byte position, then search for duplicates
                #If statement to prevent searching for duplicates after the first match
                if not first_match:
                    #Loop through the previous EOF locations in reverse order (most recent first)
                    duplicate = False
                    for loc in reversed(EOF_locations):
                        #Check the current EOF location against the stored EOF location
                        if EOF.end(1) == loc:
                            #If they match, execute new search and stop looping thru list
                            EOF = EOF_regex.search(hex_dump, EOF_locations[-1])
                            #Set duplicate flag to true
                            duplicate = True
                            break
                    #If duplicate was found, go back to while loop to check newly found EOF
                    if duplicate:
                        continue

                #End of loop will execute once EOF has passed validity and duplicate checks
                #Add the new EOF location to the list
                EOF_locations.append(EOF.end(1))
                #Add the new EOF offset to the list
                EOF_offsets.append(hex((EOF.end(1)-1) // 2))
                #Set first_match to False so every future match will be checked for duplicates
                first_match = False
                break
            
            #If not a valid byte position, adjust regex and search again
            else:
                z += 1 #Increment counter for number of invalid EOF markers
                #Add a non-capture group 'ffd9' to the regex for each invalid marker
                new_EOF_string = '(?:ffda\w+?)(?:ffd9\w+?){' + str(z) + '}(ffd9)'
                #Compile new regex
                EOF_regex = re.compile(new_EOF_string)
                #Search for next match from the original SOF
                EOF = EOF_regex.search(hex_dump, match+8)
                
    #Call JPEGSorter function and get back count of JPEGs
    count = JPEGSorter(SOF_locations, EOF_locations, SOF_offsets, EOF_offsets)

    return(count)
'''Function that takes all valid SOF and EOF markers and sorts through them to eliminate
markers for embedded JPEGs that do not need to be carved. Once the desired markers are found,
the function calls CarveFiles() to carve the JPEG.'''
def JPEGSorter(SOF_locations, EOF_locations, SOF_offsets, EOF_offsets):
    #Append extra entries to lists to allow for code to work
    append_value = EOF_locations[-1]
    for i in range(2):
        SOF_locations.append(EOF_locations[-1]+1)
    EOF_locations.append(EOF_locations[-1])
    
    #Define variables necessary to control the loop
    true_SOF = 0
    SOF_index = 1
    false_SOF_count = 0
    EOF_index = 0
    count = 0
    
    #Loop through the SOF and EOF lists to eliminate JPEGs embedded inside other JPEGs
    while SOF_index < len(EOF_locations):
        #Check if the next SOF offset is after the next EOF offset
        if SOF_locations[SOF_index] > EOF_locations[EOF_index]:
            #If next SOF comes after the next EOF, then carve from the previous SOF to next EOF
            count += 1
            CarveFile('jpg', SOF_offsets[true_SOF], EOF_offsets[EOF_index], count)
            #Increment and reset counters as necessary
            true_SOF += false_SOF_count + 1
            EOF_index += 1
            SOF_index = true_SOF + 1
            false_SOF_count = 0
        #Check if the next next SOF is after the EOF
        elif SOF_locations[SOF_index + 1] > EOF_locations[EOF_index]:
            #Increment counters and return the while loop
            SOF_index += 1
            EOF_index += 1
            false_SOF_count += 1
        #Skip current SOF in case there are more than 2 SOFs in a row
        else:
            true_SOF += 1
            SOF_index += 1
            
    return(count)

'''Function to search hex dump for carveable PDFs and PNGs. If a file is found, the function will
call a function to carve the file.'''
def LocatePFiles(file_type, SOF_string, EOF_string):

    #Print status message
    if file_type == 'png':
        print('\nsearching for PNGs...')
    if file_type == 'pdf':
        print('\nsearching for PDFs...')
    
    #Initialize counter for number of files found
    count = 0

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
        EOF_offset = hex((file.end()-1) // 2)
        #Carve the file
        CarveFile(file_type, SOF_offset, EOF_offset, count)

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

    #Call the Locate functions 3 times, one for each type
    print('\n******PNG files******') #Print new line to make output look better
    png_count = LocatePFiles('png', PNG_SOF_string, PNG_EOF_string)
    print('\n******PDF files******')
    pdf_count = LocatePFiles('pdf', PDF_SOF_string, PDF_EOF_string)
    print('\n******JPEG files******')
    jpg_count = LocateJPEGs('jpg', JPG_SOF_string, JPG_EOF_string)

    #Display summary of results
    #Print number of each file type
    print(f'\nFinal results:\n{png_count} PNG files found\n{jpg_count} JPEG files found\n'
          f'{pdf_count} PDF files found\n')

'''End of code'''
