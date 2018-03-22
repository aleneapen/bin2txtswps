ATF_VER="1.0"
OPT_HEADER="3"
WARNING_NO_GAIN = """
******* WARNING for file: {} *******
ScaleFactors (mV/Unit, ie Gains) in the header are 0 or couldn't be found.
Reasonable ScaleFactors have been substituted.
Manually adjust if necessary during reanalysis.
***********************
"""
WARNING_NEGATIVE_GAIN = """
******* Warning for file: {} *******
ScaleFactors (mV/Unit, ie Gains) in the header are negative.
Reasonable ScaleFactors have been substituted.
Manually adjust if necessary during reanalysis.
***********************"""

from numpy import savetxt, subtract, array, concatenate
import quantities as pq 


class SweepObject:
    def __init__(self,sweep_data,file_format,header={},file_name=""):
        self.sweep_data = sweep_data
        self.file_format = file_format
        self.header = header
        self.file_name = file_name
        if self.file_format == "abf":
            self.abf_version = int(self.header.get("fFileVersionNumber",0))

    def build_sweep_array(self):
        if len(self.sweep_data[0].times) == 0:
            print("File ({}) doesn't appear to have data?".format(self.file_name))
            return array([[0,0]])
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


    def correct_igor_gains(self):
        
        ret_list = []
        for channel in self.sweep_data:
            if str(channel.units.dimensionality) == 'A' or str(channel.units.dimensionality) == 'mA' or str(channel.units.dimensionality) == 'uA':
                ret_list.append(1)
            if str(channel.units.dimensionality) == 'V':
                ret_list.append(1)
            if str(channel.units.dimensionality) == 'mV':
                ret_list.append(100)
            if str(channel.units.dimensionality) == 'pA':
                ret_list.append(10)
            if str(channel.units.dimensionality) == 'nA':
                ret_list.append(1000)
        return ret_list

    def find_ScaleFactor_mVperUnit(self):
        """
        Function to find the total gain in mVperunit

        """


        ret_list = []

        # Process WCP header
        if self.file_format == 'wcp':
            for channel in range(int(self.header['NC'])):
                mVperUnit = float(self.header.get("YG{}".format(channel))) * 1000
                ret_list.append(mVperUnit)
            return ret_list

        # Igor binary wave file
        if self.file_format == 'ibw':
            scale_factor = []
            if "botFullScale" in self.header and "topFullScale" in self.header:
                try:
                    scale_factor_header = 1000 / ((self.header["topFullScale"] - self.header["botFullScale"])/20)
                    if scale_factor_header < 0:
                        print(WARNING_NEGATIVE_GAIN.format(self.file_name))
                        scale_factor = self.correct_igor_gains()
                    else:
                        return [scale_factor_header]

                    return scale_factor
                except ZeroDivisionError:
                    pass
            print(WARNING_NO_GAIN.format(self.file_name))
            scale_factor = self.correct_igor_gains()
            
            
            return scale_factor

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

    def get_data_type(self):
        for channel in self.sweep_data:
           
            if channel.dtype.char != 'f':
                return "string"
        return "float"