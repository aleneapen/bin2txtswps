from igor import binarywave

def get_header_dict(filename):
    return binarywave.load(filename)["wave"]["wave_header"]
