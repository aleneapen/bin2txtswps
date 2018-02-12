ATF_VER="1.0"
OPT_HEADERS=["SweepStartTimesMS","NumSamplesPerSweep","ScaleFactor_mVperUnit"]



class SweepObject:
    def __init__(self, data, file_format, header = {}):
        self.sweep_data = data
        self.file_format = file_format
        self.header = header

    def build_sweep_header(self):
        
