# This program converts various neuroscience files to ASCII text files.
__author__ = "Alen Eapen"

# Usage: bin2txtswps.exe "FOLDER" "INPUT FORMAT" "OUTPUT FORMAT" "OUTPUT FOLDER"

# import stfio

from os import path
import file_loop

# Supported format list
bin_format_l = ["abf","wcp"]
out_format_l = ["atf","txt"]

if __name__ == "__main__":
    import sys
    folderName = ""
    if len(sys.argv) > 1 and path.exists(path.normpath(sys.argv[1])):
        folderName = path.normpath(sys.argv[1])
        print(folderName)

    while not (path.exists(folderName)):
        folderName = input("The path does not exist, re-enter: ")
        folderName = path.normpath(folderName)
          
    
    bin_format = ""
    if len(sys.argv) > 2 and str(sys.argv[2]).lower().strip() in bin_format_l:
        bin_format = str(sys.argv[2]).lower().strip()
        print("Chosen format:",bin_format)

    while not (bin_format in bin_format_l):
        bin_format = input("Enter the format to convert: ").lower().strip()
    
    if len(sys.argv)>3 and str(sys.argv[3]).lower().strip() in out_format_l:
        out_format = "." + str(sys.argv[3]).lower().strip()
    else:
        out_format = ".atf"

    if len(sys.argv)>4:
        out_folder = str(sys.argv[4]).lower().strip()
    else:
        out_folder = "bin2txtswps"

    file_loop.folder_converter(folderName,bin_format,out_format,out_folder)


    

