import CombineHarvester.CombineTools.ch as ch
# import CombineHarvester.CombineTools.pdgRounding as pdgRounding
import ROOT

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

ROOT.gSystem.Load('libHiggsAnalysisCombinedLimit')

fin = ROOT.TFile('output/test_zerout/cmb/ws.root')
wsp = fin.Get('w')

cmb = ch.CombineHarvester()
cmb.SetFlag("workspaces-use-clone", True)
ch.ParseCombineWorkspace(cmb, wsp, 'ModelConfig', 'data_obs', False)


mlf = ROOT.TFile('fitDiagnostics.Test.root')
rfr = mlf.Get('fit_s')


def PrintTables(cmb, uargs):
    c_znn = cmb.cp().bin(['Znn_13TeV_Signal'])
    c_wmn = cmb.cp().bin(['WmnHighPt'])
    c_wen = cmb.cp().bin(['WenHighPt'])
    c_zeelow = cmb.cp().bin(['ZeeLowPt_13TeV'])
    c_zmmlow = cmb.cp().bin(['ZuuLowPt_13TeV'])
    c_zeehi = cmb.cp().bin(['ZeeHighPt_13TeV'])
    c_zmmhi = cmb.cp().bin(['ZuuHighPt_13TeV'])

    print r"""
\begin{tabular}{|l|r@{$ \,\,\pm\,\, $}lr@{$ \,\,\pm\,\, $}l|}
\hline
Process & \multicolumn{2}{c}{1-lepton(e)} & \multicolumn{2}{c|}{1-lepton($\mu$)} \\
\hline
\hline"""
    print r'Wbb                                        & $%.2f$ & $%.2f$ & $%.2f$ & $%.2f$ \\' % (
        c_wen.cp().process(['Wj2b']).GetRate(), c_wen.cp().process(['Wj2b']).GetUncertainty(*uargs),
        c_wmn.cp().process(['Wj2b']).GetRate(), c_wmn.cp().process(['Wj2b']).GetUncertainty(*uargs))
    print r'Wb                                        & $%.2f$ & $%.2f$ & $%.2f$ & $%.2f$ \\' % (
        c_wen.cp().process(['Wj1b']).GetRate(), c_wen.cp().process(['Wj1b']).GetUncertainty(*uargs),
        c_wmn.cp().process(['Wj1b']).GetRate(), c_wmn.cp().process(['Wj1b']).GetUncertainty(*uargs))
    print r'W+udscg                                       & $%.2f$ & $%.2f$ & $%.2f$ & $%.2f$ \\' % (
        c_wen.cp().process(['Wj0b']).GetRate(), c_wen.cp().process(['Wj0b']).GetUncertainty(*uargs),
        c_wmn.cp().process(['Wj0b']).GetRate(), c_wmn.cp().process(['Wj0b']).GetUncertainty(*uargs))
    #ETC...
    print r'\hline'
    print r'Total expected background                        & $%.2f$ & $%.2f$ & $%.2f$ & $%.2f$ \\ ' % (
        c_wen.cp().backgrounds().GetRate(), c_wen.cp().backgrounds().GetUncertainty(*uargs),
        c_wmn.cp().backgrounds().GetRate(), c_wmn.cp().backgrounds().GetUncertainty(*uargs))
    print r'\hline'
    print r'Observed data                                    & \multicolumn{2}{c}{$%g$} & \multicolumn{2}{c|}{$%g$} \\' % (
        c_wen.cp().GetObservedRate(), c_wmn.cp().GetObservedRate())
    print r"""\hline
\end{tabular}"""


print 'Pre-fit tables:'
PrintTables(cmb, tuple())

cmb.UpdateParameters(rfr)

print 'Post-fit tables:\n\n'
PrintTables(cmb, (rfr, 500))
