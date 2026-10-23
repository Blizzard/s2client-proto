#!/usr/bin/python3
import glob,os

# this will create a folder "s2clientprotocol_proto3" with the converted proto3 definition files
# just for current .proto files, it is not a generic proto2 to proto3 converter!
def convert_proto3():
    files = glob.glob("s2clientprotocol/*.proto")

    out_dir = "s2clientprotocol_proto3"

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for fle in files:   
        with open(fle) as f:
            outf = open(out_dir +"/" + fle[17:], "w");
            text = f.readlines()
            prevline = ""

            for line in text:   
                    
                if ( line.strip().find("optional ") == 0):  # remove optional 
                    outf.write(line.replace("optional ","",1))
                elif (line.find("syntax =") == 0):          # change version declaration
                    outf.write('syntax = "proto3";\n')
                else:                                       # add dummy element to enum with starting value 0
                    enumpos = prevline.find("enum ")        # for correct indentation
                    if (prevline.strip().find("enum ") == 0 and 
                        line[line.find("=")+1:line.find(";")].strip() == "1"):
                        outf.write((" "*enumpos) +"  "+ prevline.strip().split()[1]+"_UNSET = 0;\n" )
                        outf.write(line)
                    else:
                        outf.write(line)
                prevline = line
            outf.close()



convert_proto3()