#!/usr/bin/env python
# import argparse
import ROOT
from array import array
# import CombineHarvester.CombineTools.ch as ch


def PrintTopCorrs(fitres, parname):
    arglist = fitres.correlation(parname)
    vals = []
    for i in xrange(arglist.getSize()):
        vals.append((arglist.at(i).GetName(), arglist.at(i).getVal()))
    vals.sort(key=lambda x: abs(x[1]), reverse=True)
    vals = vals[:10]
    print vals
    # arglist.Print('v')



for m in ['mva_m_dm0_pt30',
          'mva_m_dm1_pt30',
          'mva_m_dm10_pt30']:
    print m
    f_in = ROOT.TFile('mlfit.%s.root' % m)
    rfr = f_in.Get('fit_s')
    pars = rfr.floatParsFinal()
    effsf = pars.find('effsf')
    effsf.Print()
    val, err = (effsf.getVal(), (effsf.getErrorHi() - effsf.getErrorLo()) / 2.)
    print val, err
    PrintTopCorrs(rfr, 'effsf')
    # h = ROOT.TH2F(m, m, 1, 40, 200, 1, -2.1, 2.1)
    # h.SetBinContent(1, 1, val)
    # h.SetBinError(1, 1, err)
    # f.cd()
    # h.Write()


# f = ROOT.TFile('tau_id_sfs_2016.root', 'RECREATE')

# for m in [('mva_m_dm0_pt20_30', 'mva_m_dm0_pt30'),
#           ('mva_m_dm1_pt20_30', 'mva_m_dm1_pt30'),
#           ('mva_m_dm10_pt20_30', 'mva_m_dm10_pt30')]:
#     print m
#     h = ROOT.TH2F(m[1], m[1], 2, array('d', [20., 30., 200.]), 1, -2.3, 2.3)
#     for i in xrange(2):
#         f_in = ROOT.TFile('mlfit.%s.root' % m[i])
#         rfr = f_in.Get('fit_s')
#         pars = rfr.floatParsFinal()
#         effsf = pars.find('effsf')
#         effsf.Print()
#         val, err = (effsf.getVal(), (effsf.getErrorHi() - effsf.getErrorLo()) / 2.)
#         h.SetBinContent(1 + i, 1, val)
#         h.SetBinError(1 + i, 1, err)
#     f.cd()
#     h.Write()


# for m in ['mva_t_dm0_pt40_eta2p1',
#           'mva_t_dm1_pt40_eta2p1',
#           'mva_t_dm10_pt40_eta2p1']:
#     print m
#     f_in = ROOT.TFile('mlfit.%s.root' % m)
#     rfr = f_in.Get('fit_s')
#     pars = rfr.floatParsFinal()
#     effsf = pars.find('effsf')
#     effsf.Print()
#     val, err = (effsf.getVal(), (effsf.getErrorHi() - effsf.getErrorLo()) / 2.)
#     h = ROOT.TH2F(m, m, 1, 40, 200, 1, -2.1, 2.1)
#     h.SetBinContent(1, 1, val)
#     h.SetBinError(1, 1, err)
#     f.cd()
#     h.Write()

# f.Close()
