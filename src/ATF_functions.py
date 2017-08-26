from numpy import savetxt, vstack

# Function to write ATF version 1 file
def build_full_header(analogSignal_list,ATF_VER="ATF\t1.0",OPT_HEADER="0"):
    data_cols = len(analogSignal_list)+1
    data_col_header = "".join(["\t\""+ str(analogSignal_list[x].name).strip() \
        +" (" + str(analogSignal_list[x].units.dimensionality)+")\"" for x in range(0,len(analogSignal_list))])
    time_header = "\"Time (ms)\""
    header_string = ATF_VER+"\n"+OPT_HEADER+"\t"+str(data_cols)+"\n"\
        + time_header+data_col_header
    return header_string
    
def write_ATF(analogSignals,write_path):
    savetxt(write_path,vstack((analogSignals[0].times.rescale("ms"),analogSignals[0].transpose())).transpose(), fmt=('%f' + '\t%0.4f'*len(analogSignals)),\
    newline='\n', header=build_full_header(analogSignals), comments="")
