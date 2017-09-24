from numpy import savetxt, subtract, array, stack

# Function to write ATF version 1 file
def build_full_header(analogSignal_list,ATF_VER="ATF\t1.0",OPT_HEADER="0"):
    rec_units = str(analogSignal_list[0].units.dimensionality)
    data_cols = len(analogSignal_list)+1

    data_col_format = '\t"{0} ({1})"'
    data_col_header = ""

    for channel in analogSignal_list:
        
        
        data_col_header += data_col_format.format(
            str(channel.name).strip(' \t\r\n\0'), \
            rec_units if rec_units.lower() != "dimensionless" else ""
            )
    time_header = "\"Time (ms)\""
    header_string = ATF_VER+"\n"+OPT_HEADER+"\t"+str(data_cols)+"\n"\
        + time_header+data_col_header


    return header_string
    
def write_ATF(analogSignals,write_path):

    ret_array = array(subtract(analogSignals[0].times, analogSignals[0].times[0]).rescale("ms")).reshape(len(analogSignals[0].times),1)

    
    for signal in analogSignals:
        ret_array = stack((ret_array,array(signal)),axis=1)

    savetxt(write_path,\
            ret_array,\
            fmt=('%f' + '\t%0.4f'*len(analogSignals)),\
            newline='\n',\
            header=build_full_header(analogSignals)
    )
