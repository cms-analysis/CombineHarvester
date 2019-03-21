#!/usr/bin/env python
import ROOT
# import math
import json
import argparse

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.TH1.AddDirectory(0)

parser = argparse.ArgumentParser()
parser.add_argument('--input', '-i', help='input json file')
parser.add_argument('--model', '-m', default='A1_mu', help='model')
parser.add_argument('--output', '-o', help='name of the output file to create')
args = parser.parse_args()


with open(args.input) as jsonfile:
    full = json.load(jsonfile)


model = full[args.model]

output = {}

for POI in model.keys():
    info = model[POI]
    output[POI] = {}
    if info['ValidErrorHi'] and info['ValidErrorLo']:
        mean_error = (abs(info['ErrorHi']) + abs(info['ErrorLo'])) / 2.
        output[POI] = {
            'BestFit': info['Val'],
            'StencilSize': mean_error,
            'Validity': mean_error * 10.,
            'OutputRange': [info['Val'] - mean_error * 10, info['Val'] + mean_error * 10]
        }
    elif info['ValidErrorHi'] and not info['ValidErrorLo']:
        output[POI] = {
            'BestFit': info['Val'],
            'StencilRange': [info['Val'], info['Val'] + abs(info['ErrorHi'])],
            'Validity': mean_error * 10.,
            'OutputRange': [info['Val'] - mean_error * 10, info['Val'] + mean_error * 10]
        }
    elif not info['ValidErrorHi'] and info['ValidErrorLo']:
        output[POI] = {
            'BestFit': info['Val'],
            'StencilRange': [info['Val'] - abs(info['ErrorLo']), info['Val']],
            'Validity': mean_error * 10.,
            'OutputRange': [info['Val'] - mean_error * 10, info['Val'] + mean_error * 10]
        }
    else:
        print 'Problem with POI %s!' % POI


jsondata = json.dumps(
    output, sort_keys=True, indent=2, separators=(',', ': '))
# print jsondata
if args.output is not None:
    with open(args.output, 'w') as out_file:
        out_file.write(jsondata)
