import stfio
from os import path, makedirs, listdir
from numpy import array,savetxt


# The IO function based on stimfit
def stf_IO_function(folderName,bin_format, file_i=0):
    txtFolder = path.join(folderName,"bin2txtswps")
    for file in listdir(folderName):
        
        
        if file[-3:].lower() == bin_format:
            if not path.exists(txtFolder):
                makedirs(txtFolder)
            fullPath = path.join(folderName,file)
            print fullPath
            # Open the file using stimfitio
            rec = stfio.read(str(fullPath))
            

            for i in range(0,len(rec[0])):
                if (len(rec[0]) == 1):
                    txtFileName = file[0:-4] + '.txt'
                else:
                    txtFileName = file[0:-4]+ "_" + str(i+1).zfill(4) + '.txt'
                
                fullPathtxt = path.join(txtFolder,txtFileName)
                
                # Create NumPy array to write
                write_array = array([rec[j][i].asarray() for j in range(0,len(rec))]).transpose()
                
                # Header string with sampling frequency
                header_string = "\t".join([str(1000/rec.dt)+"Hz" for j in range(0,write_array.shape[1])])
                
                # Save to txt file
                savetxt(fullPathtxt,write_array, fmt=('%0.4f'), delimiter='\t', newline='\n',header = header_string)
                
                print "Wrote " + file +  " to " + txtFileName
                file_i += 1
    return file_i