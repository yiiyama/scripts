#!/usr/bin/env python

import sys
import re
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-r", "--read", action="store_true", dest="readMode")

(options, args) = parser.parse_args()

inputName = args[0]
tree = args[1]

try:
    input = file(inputName, "r")
except:
    sys.exit(1)

prog = re.compile('[ ]*([a-zA-Z_ ]+)[ ]+([a-zA-Z_][a-zA-Z0-9_]*)(|\[[a-zA-Z0-9:_]+\]|\(.*\));')

output = ""

parse = False
for line in input:
    if 'mkbranch' in line:
        parse = True

    if not parse:
        continue
    
    result = prog.match(line)
    if not result:
        continue

    typeName = result.group(1).strip()
    varName = result.group(2)
    isArray = len(result.group(3)) != 0

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

    if options.readMode:
        output += tree + '->SetBranchAddress("' + varName + '", '
        if not isArray:
            output += '&'

        output += varName + ');\n'
    else:    
        output += tree + '->Branch("' + varName + '", '
        if not isArray:
            output += '&'

        output += varName + ', "' + varName
        if isArray:
            output += '[SIZEVAR]'
            
        output += '/' + typeId + '");\n'

print output
