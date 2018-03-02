ATF_VER="1.0"
OPT_HEADER="3"
from numpy import savetxt, subtract, array, concatenate
import quantities as pq 


class SweepObject:
    def __init__(self,sweep_data,file_format,header={}):
        self.sweep_data = sweep_data
        self.file_format = file_format
        self.header = header
        if self.file_format == "abf":
            self.abf_version = int(self.header.get("fFileVersionNumber",0))

    def build_sweep_array(self):
        ret_array = array(subtract(self.sweep_data[0].times, self.sweep_data[0].times[0]).rescale("ms")).reshape(len(self.sweep_data[0].times),1)
        for signal in self.sweep_data:
            ret_array = concatenate((ret_array,array(signal)),axis=1)
        return ret_array

    def build_atf_header(self):
        data_cols = len(self.sweep_data)+1
        data_col_format = '\t"{0} ({1})"'
        data_col_header = ""

        # ABF formats should build from the header
        if self.file_format == "abf":
            channel_units_array = []
            channel_names_array = []

            if self.abf_version == 1:
                channel_units_array = self.header.get("sADCUnits")
                channel_names_array = self.header.get("sADCChannelName")

            if self.abf_version == 2:
                channel_list = self.header.get("listADCInfo")
                
                if channel_list:
                    for channel_dict in channel_list:
                        channel_units_array.append(channel_dict.get("ADCChUnits"))
                        channel_names_array.append(channel_dict.get("ADCChNames"))


            for channel_i in range(len(self.sweep_data)):
                try:
                    rec_units = str(pq.Quantity(1,channel_units_array[channel_i].strip(b' \t\r\n\0')).dimensionality)
                except:
                    rec_units = str(self.sweep_data[channel_i].units.dimensionality)
                                
                channel_name = channel_names_array[channel_i].strip(b' \t\r\n\0')
                if channel_name == "":
                    channel_name = self.sweep_data[channel_i].name.strip(' \t\r\n\0')

                
                data_col_header += data_col_format.format(
                    channel_name, \
                    rec_units if rec_units.lower() != "dimensionless" else str(channel_units_array[channel_i].strip(b' \t\r\n\0'))
                    )


        # Other formats can use neo
        else:
            for channel in self.sweep_data:
                rec_units = str(channel.units.dimensionality)
                data_col_header += data_col_format.format(
                    str(channel.name).strip(' \t\r\n\0'), \
                    rec_units if rec_units.lower() != "dimensionless" else ""
                    )
            
        time_header = "\"Time (ms)\""

        header_string = "\n".join(["ATF\t" + ATF_VER,
                        "{} \t {}".format(OPT_HEADER,str(data_cols)),
                        "\"SweepStartTimesMS = {}\"".format(float(self.sweep_data[0].t_start.rescale('ms'))),
                        "\"NumSamplesPerSweep = {}\"".format(str(self.find_NumSamplesPerSweep())),
                        "\"ScaleFactor_mVperUnit = {}\"".format(", ".join([str(num) for num in self.find_ScaleFactor_mVperUnit()])),
                        "{}{}".format(time_header,data_col_header)])
                            
        return header_string

    def find_NumSamplesPerSweep(self,):
        """
        Function to find number of samples in each sweep from file header (if available)
        """

            

        # just return length of analogSignal
        return len(self.sweep_data[0]) if len(self.sweep_data) > 0 else 0


    def find_ScaleFactor_mVperUnit(self):
        """
        Function to find the total gain in mVperunit

        """


        ret_list = []

        # Process WCP header
        if self.file_format == 'wcp':
            for channel in range(int(self.header['NC'])):
                mVperUnit = float(self.header.get("YG{}".format(channel),))
                ret_list.append(mVperUnit)
            return ret_list

        # Igor binary wave file
        if self.file_format == 'ibw':
            if "botFullScale" in self.header and "topFullScale" in self.header:
                print(self.header["botFullScale"])
                print(self.header["topFullScale"])  
                return [1000 / ((self.header["topFullScale"] - self.header["botFullScale"])/20)]
            return [0]

        # Process ABF header
        if self.file_format == 'abf':

            # Look in header first
            
            if self.abf_version == 2:
                # channel_headers = ['fInstrumentScaleFactor', 'fADCProgrammableGain',('nTelegraphEnable','fTelegraphAdditGain')]
                if 'listADCInfo' not in self.header:
                    return [0 for i in range(len(self.sweep_data))] # Return 0 for ScaleFactor_mVperUnit scale information is not in ABF header 

                
                
                for channel_dict in self.header['listADCInfo']:
                    total_scalefactor_V = 1
                    if 'fSignalGain' in channel_dict:
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
            
            if self.abf_version == 1:
                num_channels = int(self.header.get('nADCNumChannels',0))
                signalGain = [float(x) for x,channel in zip(self.header.get('fSignalGain',[1]),range(0,num_channels))]
                InstrumentScaleFactor = [float(x) for x,channel in zip(self.header.get('fInstrumentScaleFactor',[1]),range(0,num_channels))]
                ADCProgrammableGain = [float(x) for x,channel in zip(self.header.get('fADCProgrammableGain',[1]),range(0,num_channels))]
                TelegraphEnable = [float(x) for x,channel in zip(self.header.get('nTelegraphEnable',[1]),range(0,num_channels))]
                TelegraphAdditGain = [float(x) if teleEnable == 1 else 1 for x,teleEnable in zip(self.header.get('fTelegraphAdditGain',[1]),TelegraphEnable) ]

                return [ a*b*c*d*1000 for a,b,c,d in zip(signalGain,InstrumentScaleFactor,ADCProgrammableGain,TelegraphAdditGain) ]
                
        return ret_list