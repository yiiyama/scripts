#!/usr/bin/env python

import sys
import re
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-r", "--read", action="store_true", dest="readMode")
parser.add_option("-s", "--set-status", action="store_true", dest="setStatus")
parser.add_option("-u", "--keep-underscore", action='store_true', dest='keepUnderscore')

(options, args) = parser.parse_args()

inputName = args[0]
tree = args[1]

if tree[len(tree) - 1] != '.':
    tree += '->'

try:
    input = file(inputName, "r")
except:
    sys.exit(1)

prog = re.compile('[ ]*([a-zA-Z_ ]+)[ ]+([a-zA-Z_][a-zA-Z0-9_]*)(|\[[a-zA-Z0-9:_]+\])(?:|\(.*\));')

output = ""

if options.readMode and options.setStatus:
    output += tree + 'SetBranchStatus("*", 0);\n'

parse = False
for line in input:
    if 'mkbranch' in line:
        parse = not parse

    if not parse:
        continue
    
    result = prog.match(line)
    if not result:
        continue

    varName = result.group(2)
    if options.keepUnderscore:
        bName = varName
    else:
        bName = varName.strip('_')
    isArray = len(result.group(3)) != 0

    if options.readMode:
        if options.setStatus:
            output += tree + 'SetBranchStatus("' + bName + '", 1);\n'

        output += tree + 'SetBranchAddress("' + bName + '", '
        if not isArray:
            output += '&'

        output += varName + ');\n'

        continue

    typeName = result.group(1).strip()

    unsigned = False
    if "unsigned" in typeName:
        unsigned = True
        typeName = typeName[len("unsigned"):].strip()
        if len(typeName) == 0:
            typeName = "int"

    if typeName == "char":
        typeId = "B"
    elif typeName == "short":
        typeId = "S"
    elif typeName == "int":
        typeId = "I"
    elif typeName == "long":
        typeId = "L"
    elif typeName == "float":
        typeId = "F"
    elif typeName == "double":
        typeId = "D"
    elif typeName == "bool":
        typeId = "O"
    else:
        raise RuntimeError("Unknown type " + typeName)

    if unsigned:
        typeId = typeId.lower()

    output += tree + 'Branch("' + bName + '", '
    if not isArray:
        output += '&'

    output += varName + ', "' + bName
    if isArray:
        output += '[SIZEVAR]'
        
    output += '/' + typeId + '");\n'

print output
