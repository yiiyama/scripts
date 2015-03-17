#!/usr/bin/env python

import sys
from optparse import OptionParser
#from xml.dom.minidom import parseString
import re

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", help="list of jfr files", metavar="FILE")

(options, args) = parser.parse_args()

filenames = []

if options.filename:
    filelist = file(options.filename, "r")
    for f in filelist:
        filenames.append(f.strip())

    filelist.close()
else:
    filenames = args

lumilist = dict()

## hack to make multiple file processing possible
#lines = '<Files>'
#
#for f in filenames:
#    try:
#        lines += file(f, "r").read()
#    except IOError:
#        sys.stderr.write("Cannot open " + f + "\n")
#
#lines += '</Files>'
#
#dom = parseString(lines)
#
#runBlocks = dom.getElementsByTagName('Run')
#
#for runTag in runBlocks:
#    run = 0
#    for i in range(runTag.attributes.length):
#        attr = runTag.attributes.item(i)
#        if attr.name == "ID":
#            run = attr.value
#
#    if run == 0:
#        raise RuntimeError("No runnumber")
#
#    if run not in lumilist:
#        lumilist[run] = list()
#
#    children = runTag.childNodes
#
#    for child in children:
#        if child.localName == "LumiSection":
#            for i in range(child.attributes.length):
#                attr = child.attributes.item(i)
#                if attr.name == "ID":
#                    lumilist[run].append(int(attr.value))

for filename in filenames:
    fjrfile = file(filename, 'r')
    reading = False
    for line in fjrfile:
        line = line.strip()
        if '<Runs>' in line: reading = True
        if '</Runs>' in line: reading = False
        if reading:
            matches = re.match('[ ]*({[^\}]*})', line)
            if not matches: continue
            ll = eval(matches.group(1))
            for run, lumis in ll.items():
                try:
                    lumilist[run] += lumis
                except KeyError:
                    lumilist[run] = lumis

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
