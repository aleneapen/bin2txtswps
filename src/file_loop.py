from os import path, makedirs, listdir
import time
from neo_IO_function import neo_IO_function

# Functions to loop over all files in a folder

def bin_files(folderName,bin_format):
    bin_file_list = []
    for file in listdir(folderName):
        if file.lower().endswith("."+bin_format):
            bin_file_list.append(file)
    if not bin_file_list:
        print "No "+bin_format+" files found."
        raw_input()
        exit()
    return bin_file_list


def folder_converter(folderName,bin_format,out_format = ".atf",out_folder="bin2txtswps"):
    start_time = time.time()				
    
    elapsed_time = time.time() - start_time
    bin_file_list = bin_files(folderName,bin_format)
    writeFolder = path.join(folderName,out_folder)

    if not (path.exists(writeFolder)):
        makedirs(writeFolder)

    file_i = 0
    for file in bin_file_list:
        fullPath_read = path.join(folderName,file)
        

        # Call IO function here
        file_i += neo_IO_function(fullPath_read,out_format,out_folder)


    elapsed_time = time.time() - start_time
    # Summary info:
    print "Created " + str(file_i) + " new txt files."
    print "Time elapsed: " + str('{:.3f}'.format(elapsed_time)) + " seconds"
    raw_input()
