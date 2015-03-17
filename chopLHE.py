#!/usr/bin/env python

import sys
import os
import optparse

parser = optparse.OptionParser(usage = 'usage: chopLHE.py [OPTION]... INPUT...')

parser.add_option('-s', '--start', dest = 'start', help = 'Event number to start. Default 1 (first event).', type = 'int', metavar = 'EVENT', default = 1)
parser.add_option('-n', '--num-events', dest = 'numEvents', help = 'Number of events in each output file. Default 1. When -1, all events up to the end of input are written.', type = 'int', metavar = 'NUM', default = 1)
parser.add_option('-N', '--num-output', dest = 'numOutput', help = 'Number of output files. When not 1, -o option must be present. When -1, maximum possible number of output files are created. Default 1.', type = 'int', metavar = 'NUM', default = 1)
parser.add_option('-o', '--output-name', dest = 'outputName', help = 'Name of the output file. Name must end with ".lhe".', metavar = 'NAME', default = '')

options, inputNames = parser.parse_args()

if (options.numOutput != 1 and not options.outputName) or \
options.outputName[-4:] != '.lhe' or \
not len(inputNames):
    parser.print_usage()
    sys.exit(1)

iEvt = 1
nOut = 0
inputFile = open(inputNames.pop(0))
line = inputFile.readline()
header = ''
while '<event>' not in line:
    header += line
    line = inputFile.readline()

while nOut != options.numOutput:
    while iEvt != options.start:
        line = inputFile.readline()
        if '<event>' in line: iEvt += 1
        elif line == '':
            inputFile.close()
            try:
                inputFile = open(inputNames.pop(0))
                continue
            except IndexError:
                print 'Input events less than ', options.start
                sys.exit(0)

    # line is expected to be '<event>' at the beginning of the loop
    while '<event>' not in line:
        line = inputFile.readline()
        if line == '':
            try:
                inputFile = open(inputNames.pop(0))
            except IndexError:
                break

    if line == '': break

    outputName = options.outputName
    if options.numOutput != 1:
        outputNameBase = outputName[:len(outputName) - 4]
        outputName = outputNameBase + '_' + str(nOut) + '.lhe'

    if outputName:
        if os.path.exists(outputName):
            inputFile.close()
            raise RuntimeError(outputName + ' already exists')
        outputFile = open(outputName, 'w')
    else:
        outputFile = sys.stdout

    outputFile.write(header)
    outputFile.write(line)

    nEvt = 0
    while nEvt != options.numEvents:
        line = inputFile.readline()

        if '</event>' in line: nEvt += 1
        elif line == '':
            inputFile.close()
            try:
                inputFile = open(inputNames.pop(0))
                while '<event>' not in line:
                    line = inputFile.readline()
                    if line == '': break

            except IndexError:
                nOut = options.numOutput - 1
                break

        outputFile.write(line)

    outputFile.write('</LesHouchesEvents>\n')

    if outputName:
        outputFile.close()

    nOut += 1
