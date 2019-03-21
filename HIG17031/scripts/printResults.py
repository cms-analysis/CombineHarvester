#!/usr/bin/env python
import sys
import json
import os

"""
Usage: printResults.py [json files] [model]

e.g. printResults.py lhc.json A1_5PD

"""

args = sys.argv[1:]

file = args[0]
model = args[1]
if len(args) >= 3:
    split = args[2].split(',')
else:
    split = []

with open(file) as jsonfile:
    js = json.load(jsonfile)
    if model not in js:
        print 'Model %s not in json file, available models:' % model
        print [str(x) for x in js.keys()]
        sys.exit(0)
    js = js[model]
    headerstr = '%-30s %7s %11s %11s %7s' % ('POI', 'Val', '+1sig', '-1sig', '1sig')
    for x in split:
        headerstr += ' %7s' % x
    print headerstr
    for POI, res in sorted(js.iteritems()):
        if 'ErrorHi' in res and 'ErrorLo' in res:
            errSym = (res['ErrorHi'] - res['ErrorLo']) / 2.
            line = '%-30s %+7.3f %+7.3f (%i) %+7.3f (%i) %+7.3f' % (POI, res['Val'], res['ErrorHi'], res['ValidErrorHi'], res['ErrorLo'], res['ValidErrorLo'], errSym)
            for x in split:
                xSym = (res['%sHi' % x] - res['%sLo' % x]) / 2.
                line += ' %+7.3f' % xSym
            print line
        else:
            print '%-30s %+7.3f' % (POI, res['Val'])