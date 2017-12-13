

def get_header_list(file_name_wcp,HB_size=1024):
    with open(file_name_wcp,mode='rb') as wcp_file:
        wcp_header_data = wcp_file.read()[:HB_size]
        return wcp_header_data.decode("ASCII").split("\n")



def process_header(header_list):
    header_dict = {}
    for header_info in header_list:
        try:
            key,value = header_info.strip("\r").split("=")
            header_dict.update({key:value})
        except ValueError as e:
            pass
    return header_dict

def read_bin_header(file_name_wcp,HB_size = 1024):
    # First read 1024 bytes and process header:
    header_dict = process_header(get_header_list(file_name_wcp))

    return header_dict

    

    



