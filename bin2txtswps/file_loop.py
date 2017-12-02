from os import path, makedirs, listdir
import time
from neo_IO_function import neo_IO_function

# Functions to loop over all files in a folder
BIN_FORMATS = ("abf","wcp","ibw")
def bin_files(folderName):
    bin_file_list = []
    for file in listdir(folderName):
        if file.lower().endswith(BIN_FORMATS):
            bin_file_list.append(file)
    
    return bin_file_list


def folder_converter(folderName="",out_format = ".atf",out_folder="bin2txtswps"):
    bin_file_list = bin_files(folderName)
    writeFolder = path.join(folderName,out_folder)

    if len(bin_file_list) == 0:
        print("No {} files found.".format("/".join(BIN_FORMATS)))
        return

    if not (path.exists(writeFolder)):
        makedirs(writeFolder)

    for each_file in bin_file_list:
        fullPath_read = path.join(folderName,each_file)
        # Call IO function here
        yield neo_IO_function(fullPath_read,out_format,out_folder)