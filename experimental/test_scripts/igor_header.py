from igor import binarywave

def get_header_dict(filename):
    return binarywave.load(filename)

def get_ScaleFactor_mVperUnit_igor(header_dict):
    if "botFullScale" in header_dict and "topFullScale" in header_dict:
        return 1000 / ((header_dict["topFullScale"] - header_dict["botFullScale"])/20)
    return 0



filename = r"C:\Users\Alen\Documents\repos\bin2txtswps\experimental\test_files\igor_test\Avcontrol.ibw"

my_dict["wave"]["wave_header"]["botFullScale"]