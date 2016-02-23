import sys
import os
import re
import pickle
import math
import json
import copy
import string
import operator

pMap = {}
nMap = {}
tMap = {}
dMap = {}
mapTrainer = {}
pTotal = 0
nTotal = 0
dTotal = 0
tTotal = 0
probPos = {}
probNeg = {}
probDec = {}
probTru = {}

STOPWORDS = ['i', 'me', 'my', 'myself', 'we', 'us', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself',
        'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they',
        'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am',
        'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
        'will', 'mightnt', 'neednt', 'would', 'shall', 'should', 'can', 'could', 'may', 'might', 'must', 'ought', 'im',
        'youre', 'hes', 'shes', 'its', 'were', 'theyre', 'ive', 'youve', 'weve', 'theyve', 'id', 'youd', 'hed', 'shed',
        'wed', 'theyd', 'ill', 'youll', 'hell', 'shell', 'well', 'theyll', 'isnt', 'arent', 'wasnt', 'werent', 'hasnt',
        'havent', 'hadnt', 'doesnt', 'dont', 'didnt', 'wont', 'wouldnt', 'shant', 'shouldnt', 'cant', 'cannot',
        'couldnt', 'mustnt', 'lets', 'thats', 'whos', 'whats', 'heres', 'theres', 'whens', 'wheres', 'whys', 'hows',
        'darent', 'oughtnt', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at',
        'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above',
        'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then',
        'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most',
        'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very']

def SplitWords(review):
    review = review.read()
    line = review.translate(string.maketrans("", ""), string.punctuation)
    line = line.lower().strip()
    tokens = line.split(' ')
    return filter(None, tokens)

def Tokenize(pStr, iden):
    if pStr.endswith('.txt'):
        input = open(pStr, 'r')
        samp = SplitWords(input)
        #lowInput = str(input).lower()
        #exclude = set(string.punctuation)
        #samp = ''.join(ch for ch in lowInput if ch not in exclude)
        #m = re.compile('\w+')
        #samp = m.findall(samp)
        for data in samp:
            if data not in STOPWORDS:
                if 1 == iden:
                    if data not in pMap:
                        pMap[data] = 1
                    else:
                        pMap[data] += 1
                elif 2 == iden:
                    if data not in nMap:
                        nMap[data] = 1
                    else:
                        nMap[data] += 1
                elif 3 == iden:
                    if data not in tMap:
                        tMap[data] = 1
                    else:
                        tMap[data] += 1
                else:
                    if data not in dMap:
                        dMap[data] = 1
                    else:
                        dMap[data] += 1

inFileStr = sys.argv[1]
pCount = 0
nCount = 0
tCount = 0
dCount = 0

for root, directories, filenames in os.walk(inFileStr):
    for filename in filenames:
        if -1 != os.path.join(root,filename).find("positive_polarity"):
            pCount += 1
            Tokenize(os.path.join(root,filename), 1)
        elif -1 != os.path.join(root,filename).find("negative_polarity"):
            nCount += 1 
            Tokenize(os.path.join(root,filename), 2)

        if -1 != os.path.join(root,filename).find("truthful_"):
            tCount += 1
            Tokenize(os.path.join(root,filename), 3)
        elif -1 != os.path.join(root,filename).find("deceptive_"):
            dCount += 1
            Tokenize(os.path.join(root,filename), 4)

tempPN = copy.deepcopy(pMap)
tempPN.update(nMap)
tempTD = copy.deepcopy(tMap)
tempTD.update(dMap)

lenUniquePN = len(tempPN)
lenUniqueTD = len(tempTD)

for key, value in pMap.iteritems():
    pTotal += value
for key, value in nMap.iteritems():
    nTotal += value
for key, value in tMap.iteritems():
    tTotal += value
for key, value in dMap.iteritems():
    dTotal += value

for x in tempPN.keys():
    if x in pMap:
        probPos[x] = math.log10((pMap[x] + 1) / float(pTotal + lenUniquePN))
    else:
        probPos[x] = math.log10((1) / float(pTotal + lenUniquePN))

for x in tempPN.keys():
    if x in nMap:
        probNeg[x] = math.log10((nMap[x] + 1) / float(nTotal + lenUniquePN))
    else:
        probNeg[x] = math.log10((1) / float(pTotal + lenUniquePN))

for x in tempPN.keys():
    if x in tMap:
        probTru[x] = math.log10((tMap[x] + 1) / float(tTotal + lenUniquePN))
    else:
        probTru[x] = math.log10((1) / float(tTotal + lenUniquePN))

for x in tempPN.keys():
    if x in dMap:
        probDec[x] = math.log10((dMap[x] + 1) / float(dTotal + lenUniquePN))
    else:
        probDec[x] = math.log10((1) / float(dTotal + lenUniquePN))

mapTrainer["positive"] = probPos
mapTrainer["negative"] = probNeg
mapTrainer["truthful"] = probTru
mapTrainer["deceptive"] = probDec

mapTrainer["posCount"] = math.log10(pCount / float(pCount + nCount))
mapTrainer["negCount"] = math.log10(nCount / float(pCount + nCount))
mapTrainer["truCount"] = math.log10(tCount / float(tCount + dCount))
mapTrainer["decCount"] = math.log10(dCount / float(tCount + dCount))

with open('nbmodel.txt', 'w') as handle:
    json.dump(mapTrainer, handle, indent = True)