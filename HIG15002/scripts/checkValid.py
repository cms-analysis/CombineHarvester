#!/usr/bin/env python
import sys
import json
import os

check = ['ValidErrorHi', 'ValidErrorLo']

open_list = []
prefix = '/Users/Andrew/Dropbox/Apps/PlotDrop/plots/22.08.2015'

for arg in sys.argv[1:]:
    print '> %s' % arg
    exp = arg.replace('.json', '')
    with open(arg) as jsonfile:
        js = json.load(jsonfile)
        for m, p in js.iteritems():
            for par, vals in p.iteritems():
                print '%-15s %-10.2f %-+10.2f %-+10.2f %i %i' % (par, vals['Val'], vals['ErrorHi'], vals['ErrorLo'], vals['ValidErrorHi'], vals['ValidErrorLo']) 
                for ch in check:
                    if ch in vals and not vals[ch]:
                        #print '%-15s %-20s %-20s False' % (m, par, ch)
                        open_list.append('scan_obs_exp_%s_%s_%s.pdf' % (exp, m, par))

#os.system('open ' + ' '.join(open_list))
print 'open ' + ' '.join(open_list)
