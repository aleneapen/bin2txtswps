from neo import io

file_name = "experimental/Avcontrol.ibw"

r = io.IgorIO(filename=file_name)
bl = r.read_block()
for seg in bl.segments:
    print(seg.analogsignals)