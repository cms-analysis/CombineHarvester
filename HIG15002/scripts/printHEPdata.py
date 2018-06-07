#!/usr/bin/env python
# import sys
# import json
# import os
# import argparse
import ROOT


# parser = argparse.ArgumentParser()
# parser.add_argument('-i', '--input', help='inputs')
# parser.add_argument('--location', default='Figure X')
# parser.add_argument('--dscomment', default='A caption for this figure')
# parser.add_argument('--reackey', default='p p --> H X')
# parser.add_argument('--qual', nargs='+', default=['SQRT(S) IN GEV : 8000.0'])
# parser.add_argument('--xheader', default='XVAR')
# parser.add_argument('--yheader', default='YVAR')
# args = parser.parse_args()


def GraphXYTable(input, location, dscomment, reackey, qual, yheader, xheader):
    filename, objname = input.split(':')
    f = ROOT.TFile(filename)
    graph = f.Get(objname)
    print '*dataset:'
    print '*location: %s' % location
    print '*dscomment: %s' % dscomment
    print '*reackey: %s' % reackey
    for qual_item in qual:
        print '*qual: %s' % qual_item
    print '*yheader: %s' % yheader
    print '*xheader: %s' % xheader
    print '*data: x : y'
    for i in xrange(graph.GetN()):
        print ' %.3f; %.3f;' % (graph.GetX()[i], graph.GetY()[i])
    print '*dataend:\n'


GraphXYTable('paper/scan2d_kappa_V_kappa_F_exp.root:comb_best',
             location='Figure 26 (top)',
             dscomment="""ATLAS+CMS combined best-fit in the ($\kappa_{F}$,$\kappa_{V}$) plane""",
             reackey='p p --> H X',
             qual=['SQRT(S) IN GEV : 7000.0', 'SQRT(S) IN GEV : 8000.0'],
             yheader="""$\kappa_{F}$""",
             xheader="""$\kappa_{V}$""")

GraphXYTable('paper/scan2d_kappa_V_kappa_F_exp.root:graph68_comb_0',
             location='Figure 26 (top)',
             dscomment="""ATLAS+CMS combined 68% CL negative log-likelihood contour in the ($\kappa_{F}$,$\kappa_{V}$) plane""",
             reackey='p p --> H X',
             qual=['SQRT(S) IN GEV : 7000.0', 'SQRT(S) IN GEV : 8000.0'],
             yheader="""$\kappa_{F}$""",
             xheader="""$\kappa_{V}$""")

GraphXYTable('paper/scan2d_kappa_V_kappa_F_exp.root:graph95_comb_0',
             location='Figure 26 (top)',
             dscomment="""ATLAS+CMS combined 95% CL negative log-likelihood contour in the ($\kappa_{F}$,$\kappa_{V}$) plane""",
             reackey='p p --> H X',
             qual=['SQRT(S) IN GEV : 7000.0', 'SQRT(S) IN GEV : 8000.0'],
             yheader="""$\kappa_{F}$""",
             xheader="""$\kappa_{V}$""")


GraphXYTable('paper/scan2d_kappa_V_kappa_F_exp.root:atlas_best',
             location='Figure 26 (top)',
             dscomment="""ATLAS best-fit in the ($\kappa_{F}$,$\kappa_{V}$) plane""",
             reackey='p p --> H X',
             qual=['SQRT(S) IN GEV : 7000.0', 'SQRT(S) IN GEV : 8000.0'],
             yheader="""$\kappa_{F}$""",
             xheader="""$\kappa_{V}$""")

GraphXYTable('paper/scan2d_kappa_V_kappa_F_exp.root:graph68_atlas_0',
             location='Figure 26 (top)',
             dscomment="""ATLAS 68% CL negative log-likelihood contour in the ($\kappa_{F}$,$\kappa_{V}$) plane""",
             reackey='p p --> H X',
             qual=['SQRT(S) IN GEV : 7000.0', 'SQRT(S) IN GEV : 8000.0'],
             yheader="""$\kappa_{F}$""",
             xheader="""$\kappa_{V}$""")

GraphXYTable('paper/scan2d_kappa_V_kappa_F_exp.root:graph95_atlas_0',
             location='Figure 26 (top)',
             dscomment="""ATLAS+CMS combined 95% CL negative log-likelihood contour in the ($\kappa_{F}$,$\kappa_{V}$) plane""",
             reackey='p p --> H X',
             qual=['SQRT(S) IN GEV : 7000.0', 'SQRT(S) IN GEV : 8000.0'],
             yheader="""$\kappa_{F}$""",
             xheader="""$\kappa_{V}$""")


GraphXYTable('paper/scan2d_kappa_V_kappa_F_exp.root:cms_best',
             location='Figure 26 (top)',
             dscomment="""CMS best-fit in the ($\kappa_{F}$,$\kappa_{V}$) plane""",
             reackey='p p --> H X',
             qual=['SQRT(S) IN GEV : 7000.0', 'SQRT(S) IN GEV : 8000.0'],
             yheader="""$\kappa_{F}$""",
             xheader="""$\kappa_{V}$""")

GraphXYTable('paper/scan2d_kappa_V_kappa_F_exp.root:graph68_cms_0',
             location='Figure 26 (top)',
             dscomment="""CMS 68% CL negative log-likelihood contour in the ($\kappa_{F}$,$\kappa_{V}$) plane""",
             reackey='p p --> H X',
             qual=['SQRT(S) IN GEV : 7000.0', 'SQRT(S) IN GEV : 8000.0'],
             yheader="""$\kappa_{F}$""",
             xheader="""$\kappa_{V}$""")

GraphXYTable('paper/scan2d_kappa_V_kappa_F_exp.root:graph95_cms_0',
             location='Figure 26 (top)',
             dscomment="""CMS 95% CL negative log-likelihood contour in the ($\kappa_{F}$,$\kappa_{V}$) plane""",
             reackey='p p --> H X',
             qual=['SQRT(S) IN GEV : 7000.0', 'SQRT(S) IN GEV : 8000.0'],
             yheader="""$\kappa_{F}$""",
             xheader="""$\kappa_{V}$""")


# with open(file) as jsonfile:
#     js = json.load(jsonfile)
#     if model not in js:
#         print 'Model %s not in json file, available models:' % model
#         print [str(x) for x in js.keys()]
#         sys.exit(0)
#     js = js[model]
#     print '%-30s %7s %11s %11s' % ('POI', 'Val', '+1sig', '-1sig')
#     for POI, res in sorted(js.iteritems()):
#         if 'ErrorHi' in res and 'ErrorLo' in res:
#             print '%-30s %+7.3f %+7.3f (%i) %+7.3f (%i)' % (POI, res['Val'], res['ErrorHi'], res['ValidErrorHi'], res['ErrorLo'], res['ValidErrorLo'])
#         else:
#             print '%-30s %+7.3f' % (POI, res['Val'])
