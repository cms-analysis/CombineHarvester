import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--file', '-f',help='files to merge')
parser.add_argument('--outname', '-o',help='output name')

args = parser.parse_args()
files = args.file.split(',')

result = {}
js = {}
for f in files:
  with open(f, 'rb') as infile:
    result.update(json.load(infile))


with open(args.outname,"wb") as outfile:
  json.dump(result,outfile,indent=4)
