ATF_VER="1.0"
OPT_HEADER="3"

class SweepObject:
    def __init__(self,sweep_data,file_format,header={}):
        self.sweep_data = sweep_data
        self.file_format = file_format
        self.header = header

    def build_atf_header(self):
        if self.file_format = "abf":
            data_cols = len(analogSignal_list)+1
            data_col_format = '\t"{0} ({1})"'
            data_col_header = ""

            channel_units_array = file_header.get("sADCUnits")
            channel_names_array = file_header.get("sADCChannelName")

            for channel_i in range(len(analogSignal_list)):
                print(channel_units_array)
                rec_units = str(pq.Quantity(1,channel_units_array[channel_i].strip(' \t\r\n\0')).units)
                channel_name = channel_names_array[channel_i]
                data_col_header += data_col_format.format(
                    channel_name.strip(' \t\r\n\0'), \
                    rec_units if rec_units.lower() != "dimensionless" else ""
                    )
            time_header = "\"Time (ms)\""

            header_string = "\n".join(["ATF\t" + ATF_VER,
                            OPT_HEADER + "\t" + str(data_cols),
                            "\"SweepStartTimesMS = " + str(analogSignal_list[0].t_start.rescale('ms'))[:-2].strip(" \n\t") + "\"",
                            "\"NumSamplesPerSweep = " + str(find_NumSamplesPerSweep(file_header)) + "\"",
                            "\"ScaleFactor_mVperUnit = " + ", ".join([str(num) for num in find_ScaleFactor_mVperUnit(file_header,file_type)]) + "\"",
                            time_header + data_col_header])
                            
            return header_string

    def find_NumSamplesPerSweep(self,):
        """
        Function to find number of samples in each sweep from file header (if available)
        """

            

        # just return length of analogSignal
        return len(self.sweep_data[0]) if len(self.sweep_data > 0) else 0


    def find_ScaleFactor_mVperUnit(self):
        """
        Function to find the total gain in mVperunit

        """



        ret_list = []

        # Process WCP header
        if self.file_format == 'wcp':
            for channel in range(int(self.header['NC'])):
                mVperUnit = float(self.header.get("YG{}".format(channel)))
                ret_list.append(mVperUnit)
            return ret_list


        if self.file_format == 'ibw':
            if "botFullScale" in self.header and "topFullScale" in self.header:
                return [1000 / ((self.header["topFullScale"] - self.header["botFullScale"])/20)]
            return [0]

        # Process ABF header

        if self.file_format == 'abf':

            # Look in header first
            abf_version = int(file_header.get("fFileVersionNumber",0))
            if abf_version == 2:
                # channel_headers = ['fInstrumentScaleFactor', 'fADCProgrammableGain',('nTelegraphEnable','fTelegraphAdditGain')]
                if 'listADCInfo' not in self.header:
                    return [0 for i in range(len(analogSignal_list))] # Return 0 for ScaleFactor_mVperUnit scale information is not in ABF header 

                
                
                for channel_dict in self.header['listADCInfo']:
                    total_scalefactor_V = 1
                    if 'fSignalGain' in channel_dicheadert:
                        if 'nSignalType' in self.header and self.header['nSignalType']!=0:
                            total_scalefactor_V *= channel_dict['fSignalGain']
                    if 'fInstrumentScaleFactor' in channel_dict:
                        total_scalefactor_V *= channel_dict['fInstrumentScaleFactor']
                    if 'fADCProgrammableGain' in channel_dict:
                        total_scalefactor_V *= channel_dict['fADCProgrammableGain']
                    if 'nTelegraphEnable' in channel_dict and channel_dict['nTelegraphEnable'] != 0:
                        total_scalefactor_V *= channel_dict['fTelegraphAdditGain']
                    
                    ret_list.append(total_scalefactor_V*1000)
                return ret_list
            
            if abf_version == 1:
                num_channels = int(self.header.get('nADCNumChannels',0))
                signalGain = [float(x) for x,channel in zip(self.header.get('fSignalGain',[1]),range(0,num_channels))]
                InstrumentScaleFactor = [float(x) for x,channel in zip(self.header.get('fInstrumentScaleFactor',[1]),range(0,num_channels))]
                ADCProgrammableGain = [float(x) for x,channel in zip(self.header.get('fADCProgrammableGain',[1]),range(0,num_channels))]
                TelegraphEnable = [float(x) for x,channel in zip(self.header.get('nTelegraphEnable',[1]),range(0,num_channels))]
                TelegraphAdditGain = [float(x) for x,teleEnable in zip(self.header.get('fTelegraphAdditGain',[1]),TelegraphEnable) if teleEnable == 1 else 1]

                return [ a*b*c*d*1000 for a,b,c,d in zip(signalGain,InstrumentScaleFactor,ADCProgrammableGain,TelegraphAdditGain) ]
                
        return ret_list