file_name = "C:\\Users\\Alen\\Documents\\repos\\bin2txtswps\\experimental\\test\\mine\\77280483.abf"
file_name_wcp = "C:\\Users\\Alen\\Documents\\repos\\bin2txtswps\\experimental\\test\\160323_002.wcp"
import neo 

r = neo.io.AxonIO(filename=file_name)
# r = neo.io.WinWcpIO(filename=file_name_wcp)
info_dict = r.read_header()
# with open('output_'+file_name.split("\\")[-1].split(".")[0],mode='w+') as output_file:
#     for key in info_dict:
#         output_file.write(str(info_dict[key]))
#         output_file.write("\n\n\n")
