file_name_wcp = ""
import struct
with open(file_name_wcp,mode='rb') as wcp_file:
    wcp_header_data = wcp_file.read()[:1024]
    header_list = wcp_header_data.decode("ASCII").split("\n")
    header_dict = {}
    
    for header_info in header_list:
        try:
            key,value = header_info.strip("\r").split("=")
            if key == "NC" and value != 1:
                HB_size = ((int(value-1)/8) + 1) x 1024

                
            header_dict.update({key:value})
        except ValueError:
            pass
    