#!/usr/bin/env python 
import sys

RANGES = {
    'D1_general': {
        'mu_WW'         : [0,5],
        'mu_ZZ'         : [0,5],
        'mu_gamgam'     : [0,5],
        'mu_tautau'     : [0,5],
        'l_VBF_gamgam'  : [0,5],
        'l_VBF_WW'      : [0,5],
        'l_VBF_ZZ'      : [0,10],
        'l_VBF_tautau'  : [0,5],
        'l_WH_gamgam'   : [0,30],
        'l_WH_WW'       : [0,10],
        'l_WH_ZZ'       : [0,30],
        'l_WH_tautau'   : [0,10],
        'l_WH_bb'       : [0,10],
        'l_ZH_gamgam'   : [0,10],
        'l_ZH_WW'       : [0,20],
        'l_ZH_ZZ'       : [0,50],
        'l_ZH_tautau'   : [0,20],
        'l_ZH_bb'       : [0,5],
        'l_ttH_gamgam'  : [0,20],
        'l_ttH_WW'      : [0,10],
        'l_ttH_ZZ'      : [0,50],
        'l_ttH_tautau'  : [0,30],
        'l_ttH_bb'      : [0,10]
    },
    'D1_rank1' : {
        'mu_WW'     : [0,5],
        'mu_ZZ'     : [0,5],
        'mu_gamgam' : [0,5],
        'mu_tautau' : [0,5],
        'mu_bb'     : [0,5],
        'l_VBF'     : [0,5],
        'l_WH'      : [0,5],
        'l_ZH'      : [0,5],
        'l_ttH'     : [0,10]
    }
}




args = sys.argv[1:]
assert(len(args) >= 2)
expr = '--setPhysicsModelParameterRanges='
expr_list = []

for p, vals in RANGES[args[0]].iteritems():
  if p == args[1]:
    vmin = vals[1]*-1
    vmax = vals[1]
  else:
    vmin = vals[0]
    vmax = vals[1]
  expr_list.append('%s=%g,%g' % (p, vmin, vmax))


sys.stdout.write(expr + ':'.join(expr_list))

