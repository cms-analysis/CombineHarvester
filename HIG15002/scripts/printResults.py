#!/usr/bin/env python
import sys
import json
import os

args = sys.argv[1:]

file = args[0]
model = args[1]


with open(file) as jsonfile:
    js = json.load(jsonfile)[model]
    for POI, res in js.iteritems():
        print '%-30s %.3f +/- %.3f' % (POI, res['Val'], (res['ErrorHi'] - res['ErrorLo'] )/ 2.)
    print '%-30s %7s %11s %11s' % ('POI', 'Val', '+1sig', '-1sig')
    for POI, res in sorted(js.iteritems()):
        print '%-30s %+7.3f %+7.3f (%i) %+7.3f (%i)' % (POI, res['Val'], res['ErrorHi'], res['ValidErrorHi'], res['ErrorLo'], res['ValidErrorLo'])
    #     for par, vals in p.iteritems():
    #         print '%-15s %-10.2f %-+10.2f %-+10.2f %i %i' % (par, vals['Val'], vals['ErrorHi'], vals['ErrorLo'], vals['ValidErrorHi'], vals['ValidErrorLo']) 
    #         for ch in check:
    #             if ch in vals and not vals[ch]:
    #                 #print '%-15s %-20s %-20s False' % (m, par, ch)
    #                 open_list.append('scan_obs_exp_%s_%s_%s.pdf' % (exp, m, par))

