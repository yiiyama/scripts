#!/usr/bin/env python

import re
import sys
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-r", "--range", dest="range", help="run range", metavar="BEGIN-END")
parser.add_option("-i", "--intersection", action="store_true", dest="intersection", help="show intersections")
parser.add_option("-u", "--union", action="store_true", dest="union", help="show union")

(options, args) = parser.parse_args()

begin = 0
end = 1000000
if options.range:
    m = re.match('([0-9]+)-([0-9]+)', options.range)
    begin = int(m.group(1))
    end = int(m.group(2))
    if begin >= end:
        raise

new = file(args[0]).read()
old = file(args[1]).read()

runPat = re.compile(r'"([0-9]+)": \[\s*((?:\[[0-9]+,\s*[0-9]+\],?\s*)+)\]')
lumiPat = re.compile(r'\[([0-9]+),\s*([0-9]+)\]')

oldList = dict()
newList = dict()

for sourceDest in ((old, oldList), (new, newList)):
    source = sourceDest[0]
    dest = sourceDest[1]
    
    runBlocks = runPat.findall(source)
    for runBlock in runBlocks:
        run = int(runBlock[0])
        if run < begin or run > end:
            continue
    
        lumiBlocks = lumiPat.findall(runBlock[1])
        boundPairs = []
        if run in dest:
            boundPairs = dest[run]
            
        for lumiBlock in lumiBlocks:
            boundPairs.append((int(lumiBlock[0]), int(lumiBlock[1])))

        dest[run] = boundPairs

jsonTxt = '{'

runs = set(newList.keys())
if options.union:
    runs |= set(oldList.keys())

runsList = list(runs)
runsList.sort()

for run in runsList:
    allOldLumis = set()
    allNewLumis = set()

    if run in oldList:
        for boundPair in oldList[run]:
            allOldLumis |= set(range(boundPair[0], boundPair[1] + 1))

    if run in newList:
        for boundPair in newList[run]:
            allNewLumis |= set(range(boundPair[0], boundPair[1] + 1))

    if options.union:
        allLumis = allNewLumis.union(allOldLumis)
    elif options.intersection:
        allLumis = allNewLumis.intersection(allOldLumis)
    else:
        allLumis = allNewLumis.difference(allOldLumis)

    if len(allLumis) == 0:
        continue

    lumiList = list(allLumis)
    lumiList.sort()

    jsonTxt += '"' + str(run) + '": ['

    beginOfBlock = lumiList[0]
    currentLumi = lumiList[0]
    for i in range(1, len(lumiList)):
        if lumiList[i] != currentLumi + 1:
            jsonTxt += '[' + str(beginOfBlock) + ', ' + str(currentLumi) + '], '
            beginOfBlock = lumiList[i]

        currentLumi = lumiList[i]

    jsonTxt += '[' + str(beginOfBlock) + ', ' + str(currentLumi) + ']], '

jsonTxt = jsonTxt.rstrip(', ')
jsonTxt += '}'

print jsonTxt
