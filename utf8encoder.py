import sys

inFileStr = sys.argv[1]
inFilePtr = open(inFileStr, 'rb')
inList = []

inData = inFilePtr.read(2)
while inData:
    inList.append(int("".join(map(lambda x: '%02x' % ord(x), inData)),16)) #conversion to hex and to int
    inData = inFilePtr.read(2)

outFilePtr = open('utf8encoder_out.txt','w')

for intVal in inList:
    bVal = '{0:08b}'.format(intVal)
    bComp = str(bVal)

    if intVal < 128:
        res = '0' + bComp
        outFilePtr.write(chr(int(res,2)))

    elif intVal < 2048:
        res = '1100000010000000'
        length = len(bComp)
        bCompList = list(bComp)
        resList = list(res)

        for i in range(15, 9, -1):
            if(length > 0):
                resList[i] = bCompList[length-1]
                length -= 1
        for j in range(7,2, -1):
            if(length > 0):
                resList[j] = bCompList[length-1]
                length -= 1
        res = ''.join(resList)
        outFilePtr.write(chr(int(res[:8],2)) + chr(int(res[8:],2)))
    else:
        res = '111000001000000010000000'
        length = len(bComp)
        bCompList = list(bComp)
        resList = list(res)

        for i in range(23,17,-1):
            if(length > 0):
                resList[i] = bCompList[length-1]
                length -= 1
        for j in range(15,9,-1):
            if(length > 0):
                resList[j] = bCompList[length-1]
                length -= 1
        for l in range(7,3,-1):
            if(length > 0):
                resList[l] = bCompList[length-1]
                length -= 1
        res = ''.join(resList)
        outFilePtr.write(chr(int(res[:8],2)) + chr(int(res[8:16],2)) + chr(int(res[16:],2)))

outFilePtr.close()
inFilePtr.close()