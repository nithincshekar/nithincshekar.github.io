import sys
import re
import json
import os
pRes = 0.0
nRes = 0.0
tRes = 0.0
dRes = 0.0
outPtr = open('nboutput.txt', 'w')
def Classify(pStr):
    global pRes
    global nRes
    global tRes
    global dRes

    if pStr.endswith('.txt'):
        input = open(pStr, 'r').read()
        lowInput = str(input).lower()
        m = re.compile('\w+')
        samp = m.findall(lowInput)

        with open("nbmodel.txt") as data_file:    
            data = json.load(data_file)
        pRes = data["posCount"]
        nRes = data["negCount"]
        tRes = data["truCount"]
        dRes = data["decCount"]

        for dat in samp:
            if dat in data["positive"]:
                pRes += data["positive"][dat]
            if dat in data["negative"]:
                nRes += data["negative"][dat]
            if dat in data["truthful"]:
                tRes += data["truthful"][dat]
            if dat in data["deceptive"]:
                dRes += data["deceptive"][dat]
        
        if tRes >= dRes:
            outPtr.write("truthful ")
        else:
            outPtr.write("deceptive ")
        if pRes >= nRes:
            outPtr.write("positive " + pStr + "\n")
        else:
            outPtr.write("negative " + pStr + "\n")

inFileStr = sys.argv[1]
for root, directories, filenames in os.walk(inFileStr):
    for filename in filenames:
        if -1 != os.path.join(root,filename):
            Classify(os.path.join(root,filename))
