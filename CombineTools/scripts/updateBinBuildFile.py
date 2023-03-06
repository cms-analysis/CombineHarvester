#!/usr/bin/env python

# Example usage: updateBinBuildFile.py bin/BuildFile.xml bin/*.cpp
from __future__ import absolute_import
from __future__ import print_function
import os
import sys

args = sys.argv[1:]

assert(len(args) > 1)

buildfile = args[0]
bins = args[1:]

print('>> Will update binaries in %s' % buildfile)
print('>> New binaries will be:')
print(bins)

with open(buildfile) as f:
    content = f.readlines()

filtered = [x for x in content if '<bin' not in x]

fout = open(buildfile, 'w')
for line in bins:
    basename = os.path.basename(line)
    noext = os.path.splitext(basename)[0]
    result = '<bin file="%s" name="%s"></bin>\n' % (basename, noext)
    fout.write(result)
for line in filtered:
    fout.write(line)
fout.close()

print('>> Operation completed successfully, the new BuildFile.xml looks like:')
with open(buildfile, 'r') as fin:
    print(fin.read())
