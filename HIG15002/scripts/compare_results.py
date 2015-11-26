#!/usr/bin/env python
import sys
import json
import os

args = sys.argv[1:]

old = args[0]
new = args[1]


with open(old) as jsonfile:
    js_old = json.load(jsonfile)
with open(new) as jsonfile:
    js_new = json.load(jsonfile)

for M in sorted(js_old.keys()):
    print '\n%-40s | %-15s | %-15s | %-7s | %-10s | %-10s' % (M, 'PAS', 'New', 'New-PAS', '(New-PAS)/Err', 'NewErr/PASErr')
    print '%s | %s | %s | %s | %s | %s | %s' % ('-'*40, '-'*15, '-'*5, '-'*7, '-'*7, '-'*13, '-'*13)
    if M in js_new.keys():
      for POI in sorted(js_old[M].keys()):
        val_old = js_old[M][POI]["Val"]
        val_new = js_new[M][POI]["Val"]
        err_old = (js_old[M][POI]["ErrorHi"] - js_old[M][POI]["ErrorLo"]) / 2.
        err_new = (js_new[M][POI]["ErrorHi"] - js_new[M][POI]["ErrorLo"]) / 2.
        frac_shift = (val_new - val_old) / err_old
        print '%-40s | %.3f +/- %.3f | %.3f +/- %.3f |  %+.3f | %+12.0f%% | %.3f' % (POI, val_old, err_old, val_new, err_new, val_new - val_old, frac_shift*100., err_new/err_old)

