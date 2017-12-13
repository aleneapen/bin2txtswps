from numpy import savetxt, subtract, array, concatenate


# Function to write ATF file
def build_full_header(analogSignal_list,ATF_VER="1.0",OPT_HEADER="3", file_header = {},file_type='abf'):
    

    def find_NumSamplesPerSweep(file_header):
        """
        Function to find number of samples in each sweep from file header (if available)
        """



        # Look in header first
        if 'listADCInfo' in file_header and 'lNumSamplesPerEpisode' in file_header:
            if len(file_header['listADCInfo']>0):
                return int(file_header['lNumSamplesPerEpisode']/len(file_header['listADCInfo']))
            else:
                return file_header['lNumSamplesPerEpisode']

        # if not just return length of analogSignal
        return len(analogSignal_list[0])

    
    def find_ScaleFactor_mVperUnit(file_header, file_type):
        """
        Function to find the total gain in mVperunit

        """

        ret_list = []

        # Process WCP header
        if file_type == 'wcp':
            for channel in range(int(file_header['NC'])):
                mVperUnit = float(file_header.get("YG{}".format(channel)))
                ret_list.append(mVperUnit)
            return ret_list


        if file_type == 'ibw':
            if "botFullScale" in file_header and "topFullScale" in file_header:
                return [1000 / ((file_header["topFullScale"] - file_header["botFullScale"])/20)]
            return [0]

        # Process ABF header

        channel_headers = ['fInstrumentScaleFactor', 'fADCProgrammableGain',('nTelegraphEnable','fTelegraphAdditGain')]

        if 'listADCInfo' not in file_header:
            return [0 for i in range(len(analogSignal_list))] # Return 0 for ScaleFactor_mVperUnit scale information is not in ABF header 

        
        for channel_dict in  file_header['listADCInfo']:
            total_scalefactor_V = 1
            if 'fSignalGain' in channel_dict:
                if 'nSignalType' in file_header and file_header['nSignalType']!=0:
                    total_scalefactor_V *= channel_dict['fSignalGain']
            if 'fInstrumentScaleFactor' in channel_dict:
                total_scalefactor_V *= channel_dict['fInstrumentScaleFactor']
            if 'fADCProgrammableGain' in channel_dict:
                total_scalefactor_V *= channel_dict['fADCProgrammableGain']
            if 'nTelegraphEnable' in channel_dict and channel_dict['nTelegraphEnable'] != 0:
                total_scalefactor_V *= channel_dict['fTelegraphAdditGain']
            
            ret_list.append(total_scalefactor_V*1000)
        return ret_list





    data_cols = len(analogSignal_list)+1

    data_col_format = '\t"{0} ({1})"'
    data_col_header = ""

    for channel in analogSignal_list:
        rec_units = str(channel.units.dimensionality)
        
        if rec_units.endswith("A"):
            rec_units = "pA"
        elif rec_units.endswith("V"):
            rec_units ="mV"

        data_col_header += data_col_format.format(
            str(channel.name).strip(' \t\r\n\0'), \
            rec_units if rec_units.lower() != "dimensionless" else ""
            )
    time_header = "\"Time (ms)\""

    header_string = "\n".join(["ATF\t" + ATF_VER,
                    OPT_HEADER + "\t" + str(data_cols),
                    "\"SweepStartTimesMS = " + str(channel.times[0].rescale('ms'))[:-2].strip(" \n\t") + "\"",
                    "\"NumSamplesPerSweep = " + str(find_NumSamplesPerSweep(file_header)) + "\"",
                    "\"ScaleFactor_mVperUnit = " + ", ".join([str(num) for num in find_ScaleFactor_mVperUnit(file_header,file_type)]) + "\"",
                    time_header + data_col_header])
                    
    return header_string
    
def write_ATF(analogSignals,write_path,file_header,file_type='abf'):

    ret_array = array(subtract(analogSignals[0].times, analogSignals[0].times[0]).rescale("ms")).reshape(len(analogSignals[0].times),1)


    for signal in analogSignals:
        if signal.units.dimensionality.string.endswith("A"):
            signal = signal.rescale("pA")
        elif signal.units.dimensionality.string.endswith("V"):
            signal = signal.rescale("mV")
        ret_array = concatenate((ret_array,array(signal)),axis=1)

    savetxt(write_path,\
            ret_array,\
            fmt=('%f' + '\t%0.4f'*len(analogSignals)),\
            newline='\n',\
            header=build_full_header(analogSignals,file_header=file_header,file_type=file_type),
            comments=''
    )