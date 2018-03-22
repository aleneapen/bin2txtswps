from numpy import savetxt, subtract, array, concatenate
import quantities as pq 
from sweepsio import SweepObject

def write_ATF(analogSignals,write_path,file_header,file_type='abf',file_name=""):
    sweep_object = SweepObject(analogSignals,file_type,file_header,file_name)
    time_format_spec = '%s\t'
    full_format_spec = time_format_spec + '\t'.join(['%s' for channel in analogSignals])



    # print(sweep_object.build_sweep_array())
    savetxt(write_path,\
            sweep_object.build_sweep_array(),\
            fmt=(full_format_spec),\
            newline='\n',\
            header = sweep_object.build_atf_header(),
            comments=''
    )