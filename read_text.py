from os import path
import subprocess 


inputVal = "4x4spatial_test.txt"
outputStart = "4x4spatial_test_"
mapLoci = {}
lociList = []
flagged = set()
jitter = 0.00001
Deme_dimension = 4**2 ##
if Deme_dimension < 20:
    Augmentation_factor = 10
elif Deme_dimension < 50:
    Augmentation_factor = 3
else:
    Augmentation_factor = 1
print(f"Augmentation_factor:{Augmentation_factor}")
sample_size = Augmentation_factor*Deme_dimension

def writeOutput(position, mutationCount, outputFileName, nbase):
    if path.exists(outputFileName) == False:
        output = open(outputFileName, "w")
        output.write("position\t" + "x\t" + "n\t" + "folded\n")
        output.close()
    output = open(outputFileName, "a")
    output.write(str(position) + "\t" + str(mutationCount) + "\t" + str(nbase) + "\t" + "0\n")
    output.close()

#Make sure the input in the right format
subprocess.run(f"dos2unix {inputVal}", shell=True)
#Compiles allele frequency data from input file.
x = 0
with open(inputVal, "r") as file:
    listLocation = 0
    #line_no = 0
    for line in file:
        #line_no += 1
        #print(line_no)
        #Identify all the segregating sites
        if line[0:10] == "positions:":
            splitLine = line[12:]
            currentNum = ""
            for character in splitLine:
                if character != " " and character != "\n" and character != "":
                    currentNum += character
                else:
                    if currentNum == "":
                        break
                    cast = float(currentNum)
                    currentNum = ""
                    lociList.append(cast)
        #Identify the counts at the i-th segsite
        elif line[0] == "1" or line[0] == "0":
            for character in line:
                if character == "\n":
                    listLocation = 0
                    flagged = set()
                elif character == "1":
                    position = lociList[listLocation]
                    while position in flagged:
                        position += jitter
                    count = mapLoci.get(position)
                    if count is not None:
                        mapLoci[position] = mapLoci[position] + 1
                    else:
                        mapLoci[position] = 1
                    listLocation += 1
                    flagged.add(position)
                else:
                    listLocation += 1
        #Write output and clear data structures for next trial
        elif line[0] == "/":
            if x == 0:
                x += 1
                continue
            output = outputStart + str(x) + ".txt"
            for location in mapLoci:
                writeOutput(location, mapLoci[location], output, sample_size)
                
            lociList = []
            mapLoci = {}
            flagged = set()
            subprocess.run(f"dos2unix {output}", shell=True)
            x += 1
        else:
            continue
        
#If there is any trial data left, process it.
if len(mapLoci) > 0:
    output = outputStart + str(x) + ".txt"
    for location in mapLoci:
        writeOutput(location, mapLoci[location], output, sample_size)
    subprocess.run(f"dos2unix {output}", shell=True)


#Make sure the output in the right format
