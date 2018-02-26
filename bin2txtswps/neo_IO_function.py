from neo.io import (WinWcpIO, IgorIO)
from Modified_AxonIO import AxonIO
from os import path
from ATF_functions import write_ATF
from math import (ceil, log10)
import process_winwcp_header 
import process_igor_header

# The IO function based on neo
def neo_IO_function(fullPath_read,out_format,out_folder,file_i=0):

    input_format = ''
    file_header = {}


    # Open and Read the file, add more here if needed
    if fullPath_read.lower().endswith("abf"):
        r = AxonIO(filename=fullPath_read)
        input_format = "abf"
        try:
            file_header = r.read_header()
        except AttributeError:
            pass
    elif fullPath_read.lower().endswith("wcp"):
        r = WinWcpIO(filename=fullPath_read)
        input_format = "wcp"
        file_header = process_winwcp_header.read_bin_header(fullPath_read)
    elif fullPath_read.lower().endswith("ibw"):
        r = IgorIO(filename=fullPath_read)
        input_format = "ibw"
        file_header = process_igor_header.get_header_dict(fullPath_read)

    
    bl = r.read_block(lazy=False, cascade=True,)
    
    if len(bl.segments) > 1:
        zfill_max_int = int(ceil(log10(len(bl.segments)))+1)

    # Iterate through each segment and analogsignal list
    for i in range(0,len(bl.segments)):
        folderName,tail_name = path.split(fullPath_read)
        fileName = path.splitext(path.basename(fullPath_read))[0]

        if len(bl.segments) <= 1:
            txtFileName = fileName + out_format
        else:
            txtFileName = fileName + "_" + str(i+1).zfill(zfill_max_int) + out_format            

        fullPathtxt = path.join(folderName,out_folder,txtFileName)
        analogSignals =  bl.segments[i].analogsignals            
        
        write_ATF(analogSignals,fullPathtxt,file_header,input_format)

        print("Wrote {} to {}".format(tail_name,txtFileName))
        file_i += 1
        yield file_i
