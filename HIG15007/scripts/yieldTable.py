import CombineHarvester.CombineTools.ch as ch
# import CombineHarvester.CombineTools.pdgRounding as pdgRounding
import ROOT

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

ROOT.gSystem.Load('libHiggsAnalysisCombinedLimit')

fin = ROOT.TFile('output/LIMITS-svfit/cmb/wsp.root')
wsp = fin.Get('w')

cmb = ch.CombineHarvester()
cmb.SetFlag("workspaces-use-clone", True)
ch.ParseCombineWorkspace(cmb, wsp, 'ModelConfig', 'data_obs', False)


mlf = ROOT.TFile('output/LIMITS-svfit/cmb/mlfit.Test.root')
rfr = mlf.Get('fit_s')


def PrintTables(cmb, uargs):
    c_et = cmb.cp().bin(['et_inclusive'])
    c_mt = cmb.cp().bin(['mt_inclusive'])
    c_em = cmb.cp().bin(['em_inclusive'])
    c_tt = cmb.cp().bin(['tt_inclusive'])

    print r"""
\begin{tabular}{|l|r@{$ \,\,\pm\,\, $}lr@{$ \,\,\pm\,\, $}l|}
\hline
Process & \multicolumn{2}{c}{$\taue\tauh$} & \multicolumn{2}{c|}{$\taum\tauh$} \\
\hline
\hline"""
    print r'QCD multijet                                     & $%.2f$ & $%.2f$ & $%.2f$ & $%.2f$ \\' % (
        c_et.cp().process(['QCD']).GetRate(), c_et.cp().process(['QCD']).GetUncertainty(*uargs),
        c_mt.cp().process(['QCD']).GetRate(), c_mt.cp().process(['QCD']).GetUncertainty(*uargs))
    print r'$\PW$+jets                                       & $%.2f$ & $%.2f$ & $%.2f$ & $%.2f$ \\' % (
        c_et.cp().process(['W']).GetRate(), c_et.cp().process(['W']).GetUncertainty(*uargs),
        c_mt.cp().process(['W']).GetRate(), c_mt.cp().process(['W']).GetUncertainty(*uargs))
    print r'$\cPZ$+jets (jet faking $\Pgt$)                  & $%.2f$ & $%.2f$ & $%.2f$ & $%.2f$ \\' % (
        c_et.cp().process(['ZJ']).GetRate(), c_et.cp().process(['ZJ']).GetUncertainty(*uargs),
        c_mt.cp().process(['ZJ']).GetRate(), c_mt.cp().process(['ZJ']).GetUncertainty(*uargs))
    print r'$\cPqt\cPaqt$ (jet faking $\Pgt$)                & $%.2f$ & $%.2f$ & $%.2f$ & $%.2f$ \\' % (
        c_et.cp().process(['TT']).GetRate(), c_et.cp().process(['TT']).GetUncertainty(*uargs),
        c_mt.cp().process(['TT']).GetRate(), c_mt.cp().process(['TT']).GetUncertainty(*uargs))
    print r'\hline'
    print r'$\cPZ$+jets ($\Pe$ or $\Pgm$ faking $\Pgt$)      & $%.2f$ & $%.2f$ & $%.2f$ & $%.2f$ \\' % (
        c_et.cp().process(['ZL']).GetRate(), c_et.cp().process(['ZL']).GetUncertainty(*uargs),
        c_mt.cp().process(['ZL']).GetRate(), c_mt.cp().process(['ZL']).GetUncertainty(*uargs))
    print r'$\cPqt\cPaqt$ (excl. jet faking $\Pgt$)          & $%.2f$ & $%.2f$ & $%.2f$ & $%.2f$ \\' % (
        c_et.cp().process(['TT']).GetRate(), c_et.cp().process(['TT']).GetUncertainty(*uargs),
        c_mt.cp().process(['TT']).GetRate(), c_mt.cp().process(['TT']).GetUncertainty(*uargs))
    print r'Diboson + single top                             & $%.2f$ & $%.2f$ & $%.2f$ & $%.2f$ \\' % (
        c_et.cp().process(['VV']).GetRate(), c_et.cp().process(['VV']).GetUncertainty(*uargs),
        c_mt.cp().process(['VV']).GetRate(), c_mt.cp().process(['VV']).GetUncertainty(*uargs))
    ## Not in all datacard inputs + no agreed naming convention. Leave empty for now.
    print r'SM Higgs                                         & $%.2f$ & $%.2f$ & $%.2f$ & $%.2f$ \\' % (
        c_et.cp().process(['']).GetRate(), c_et.cp().process(['']).GetUncertainty(*uargs),
        c_mt.cp().process(['']).GetRate(), c_mt.cp().process(['']).GetUncertainty(*uargs))
    print r'\hline'
    print r'Total expected background                        & $%.2f$ & $%.2f$ & $%.2f$ & $%.2f$ \\ ' % (
        c_et.cp().backgrounds().GetRate(), c_et.cp().backgrounds().GetUncertainty(*uargs),
        c_mt.cp().backgrounds().GetRate(), c_mt.cp().backgrounds().GetUncertainty(*uargs))
    print r'\hline'
    print r'Observed data                                    & \multicolumn{2}{c}{$%g$} & \multicolumn{2}{c|}{$%g$} \\' % (
        c_et.cp().GetObservedRate(), c_mt.cp().GetObservedRate())
    print r"""\hline
\end{tabular}"""


    print r"""
\begin{tabular}{|l|r@{$ \,\,\pm\,\, $}lr@{$ \,\,\pm\,\, $}l|}
\hline
Process & \multicolumn{2}{c}{$\tauh\tauh$} & \multicolumn{2}{c|}{$\taue\taum$} \\
\hline
\hline"""
    print r'QCD multijet                                     & $%.2f$ & $%.2f$ & $%.2f$ & $%.2f$ \\' % (
        c_tt.cp().process(['QCD']).GetRate(), c_tt.cp().process(['QCD']).GetUncertainty(*uargs),
        c_em.cp().process(['QCD']).GetRate(), c_em.cp().process(['QCD']).GetUncertainty(*uargs))
    print r'$\PW$+jets                                       & $%.2f$ & $%.2f$ & $%.2f$ & $%.2f$ \\' % (
        c_tt.cp().process(['W']).GetRate(), c_tt.cp().process(['W']).GetUncertainty(*uargs),
        c_em.cp().process(['W']).GetRate(), c_em.cp().process(['W']).GetUncertainty(*uargs))
    print r'$\cPZ$+jets (jet faking $\Pgt$)                  & $%.2f$ & $%.2f$ & $%.2f$ & $%.2f$ \\' % (
        c_tt.cp().process(['ZJ', 'ZLL']).GetRate(), c_tt.cp().process(['ZJ', 'ZLL']).GetUncertainty(*uargs),
        c_em.cp().process(['ZJ', 'ZLL']).GetRate(), c_em.cp().process(['ZJ', 'ZLL']).GetUncertainty(*uargs))
    print r'$\cPqt\cPaqt$ (jet faking $\Pgt$)                & $%.2f$ & $%.2f$ & $%.2f$ & $%.2f$ \\' % (
        c_tt.cp().process(['TT']).GetRate(), c_tt.cp().process(['TT']).GetUncertainty(*uargs),
        c_em.cp().process(['TT']).GetRate(), c_em.cp().process(['TT']).GetUncertainty(*uargs))
    print r'\hline'
    print r'$\cPZ$+jets ($\Pe$ or $\Pgm$ faking $\Pgt$)      & $%.2f$ & $%.2f$ & $%.2f$ & $%.2f$ \\' % (
        c_tt.cp().process(['ZL']).GetRate(), c_tt.cp().process(['ZL']).GetUncertainty(*uargs),
        c_em.cp().process(['ZL']).GetRate(), c_em.cp().process(['ZL']).GetUncertainty(*uargs))
    print r'$\cPqt\cPaqt$ (excl. jet faking $\Pgt$)          & $%.2f$ & $%.2f$ & $%.2f$ & $%.2f$ \\' % (
        c_tt.cp().process(['TT']).GetRate(), c_tt.cp().process(['TT']).GetUncertainty(*uargs),
        c_em.cp().process(['TT']).GetRate(), c_em.cp().process(['TT']).GetUncertainty(*uargs))
    print r'Diboson + single top                             & $%.2f$ & $%.2f$ & $%.2f$ & $%.2f$ \\' % (
        c_tt.cp().process(['VV']).GetRate(), c_tt.cp().process(['VV']).GetUncertainty(*uargs),
        c_em.cp().process(['VV']).GetRate(), c_em.cp().process(['VV']).GetUncertainty(*uargs))
    ## Not in all datacard inputs + no agreed naming convention. Leave empty for now.
    print r'SM Higgs                                         & $%.2f$ & $%.2f$ & $%.2f$ & $%.2f$ \\' % (
        c_tt.cp().process(['']).GetRate(), c_tt.cp().process(['']).GetUncertainty(*uargs),
        c_em.cp().process(['']).GetRate(), c_em.cp().process(['']).GetUncertainty(*uargs))
    print r'\hline'
    print r'Total expected background                        & $%.2f$ & $%.2f$ & $%.2f$ & $%.2f$ \\ ' % (
        c_tt.cp().backgrounds().GetRate(), c_tt.cp().backgrounds().GetUncertainty(*uargs),
        c_em.cp().backgrounds().GetRate(), c_em.cp().backgrounds().GetUncertainty(*uargs))
    print r'\hline'
    print r'Observed data                                    & \multicolumn{2}{c}{$%g$} & \multicolumn{2}{c|}{$%g$} \\' % (
        c_tt.cp().GetObservedRate(), c_em.cp().GetObservedRate())
    print r"""\hline
\end{tabular}"""


print 'Pre-fit tables:'
PrintTables(cmb, tuple())

cmb.UpdateParameters(rfr)

print 'Post-fit tables:\n\n'
PrintTables(cmb, (rfr, 500))


# cmb.GetParameter('r').set_frozen(True)
# cmb.PrintAll()




# for b in cmb.bin_set():
#     print b
#     for p in cmb.cp().bin([b]).cp().process_set():
#         cmb_proc = cmb.cp().bin([b]).cp().process([p])
#         # val, err = pdgRounding.pdgRound(cmb_proc.GetRate(), cmb_proc.GetUncertainty(*uargs))
#         val, err = ('%g' % cmb_proc.GetRate(), '%g' % cmb_proc.GetUncertainty(*uargs))
#         print '%-20s %s +/- %s' % (p, val, err)

