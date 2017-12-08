def get_header_list(file_name_wcp,HB_size=1024):
with open(file_name_wcp,mode='rb') as wcp_file:
    wcp_header_data = wcp_file.read()[:HB_size]
    return wcp_header_data.decode("ASCII").split("\n")

file_name = "/home/theemaram/repos/bin2txtswps/experimental/test_files/ibw/AvAllo.ibw"
HB_size=1024