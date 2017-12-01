from neo import io
from os import path
from ATF_functions import build_full_header,write_ATF
from math import ceil


# The IO function based on neo
def neo_IO_function(fullPath_read,out_format,out_folder,file_i=0):

    # Open and Read the file, add more here if needed
    if fullPath_read.lower().endswith("abf"):
        r = io.AxonIO(filename=fullPath_read)
    elif fullPath_read.lower().endswith("wcp"):
        r = io.WinWcpIO(filename=fullPath_read)
    elif fullPath_read.lower().endswith("ibw"):
        r = io.IgorIO(filename=fullPath_read)

    
    bl = r.read_block(lazy=False, cascade=True,)

    # Try to get the header info (for supported formats)
    file_header = {}
    try:
        file_header = r.read_header()
    except AttributeError:
        pass
            
    # Iterate through each segment and analogsignal list
    for i in range(0,len(bl.segments)):
        folderName,tail_name = path.split(fullPath_read)
        fileName = path.splitext(path.basename(fullPath_read))[0]

        if len(bl.segments) == 1:
            txtFileName = fileName + out_format
        else:
            
            txtFileName = fileName + "_" + str(i+1).zfill(int(ceil(len(bl.segments)/10)+1)) + out_format
                
        fullPathtxt = path.join(folderName,out_folder,txtFileName)
        analogSignals =  bl.segments[i].analogsignals               

        write_ATF(analogSignals,fullPathtxt,file_header)

        print("Wrote " + tail_name +  " to " + txtFileName)
        file_i += 1
    return file_i
