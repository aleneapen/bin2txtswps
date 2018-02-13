from numpy import savetxt, subtract, array, concatenate
import quantities as pq 
from sweepsio import SweepObject

def write_ATF(analogSignals,write_path,file_header,file_type='abf'):
    sweep_object = SweepObject(analogSignals,file_type,file_header)

    savetxt(write_path,\
            sweep_object.build_sweep_array(),\
            fmt=('%f' + '\t%e'*len(analogSignals)),\
            newline='\n',\
            header = sweep_object.build_atf_header(),
            comments=''
    )