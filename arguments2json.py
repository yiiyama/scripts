#!/usr/bin/env python

from optparse import OptionParser
from xml.dom.minidom import parseString

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", help="list of job numbers", metavar="FILE")

(options, args) = parser.parse_args()

jobNumbers = []

if options.filename:
    filelist = file(options.filename, "r")
    for f in filelist:
        jobNumbers.append(f.strip())

    filelist.close()

    source = file(args[0])
else:
    jobNumbers = args[0].split(',')
    source = file(args[1])

xmlStr = source.read()

source.close()

lumilist = dict()

dom = parseString(xmlStr)

jobTags = dom.getElementsByTagName('Job')

for tag in jobTags:
    process = False
    for i in range(tag.attributes.length):
        attr = tag.attributes.item(i)
        if attr.name == 'JobID' and attr.value in jobNumbers:
            process = True
            jobNumbers.remove(attr.value)
        elif attr.name == 'Lumis':
            xmlLumis = attr.value

    if not process:
        continue

    runLumiBlocks = xmlLumis.split(',')
        
    for block in runLumiBlocks:
        if '-' in block:
            ends = block.split('-')
            run = ends[0].split(':')[0]
            begin = int(ends[0].split(':')[1])
            end = int(ends[1].split(':')[1]) + 1
        else:
            run = block.split(':')[0]
            begin = int(block.split(':')[1])
            end = begin + 1

        if run not in lumilist:
            lumilist[run] = list()

        for l in range(begin, end):
            lumilist[run].append(l)

jsonTxt = "{"

runs = lumilist.keys()
runs.sort()

for run in runs:
    lumis = lumilist[run]
    if len(lumis) == 0:
        continue
    
    lumis.sort()

    jsonTxt += '"' + str(run) + '": [[' + str(lumis[0]) + ', '

    l = lumis[0] - 1
    for lumi in lumis:
        if lumi != l + 1:
            jsonTxt += str(l) + '], [' + str(lumi) + ', '

        l = lumi

    jsonTxt += str(lumis[len(lumis) - 1]) + ']], '

jsonTxt = jsonTxt.rstrip(', ')
jsonTxt += "}"

print jsonTxt

