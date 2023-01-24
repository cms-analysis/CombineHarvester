from __future__ import absolute_import
import CombineHarvester.CombineTools.ch as ch

cb = ch.CombineHarvester()
cb.SetVerbosity(3)

cats = [(0, 'A'), (1, 'B'), (2, 'C'), (3, 'D')]

obs_rates = {
    'A': 10,
    'B': 50,
    'C': 100,
    'D': 500
}

cb.AddObservations( ['*'], [''], ['13TeV'], [''],          cats)
cb.AddProcesses(    ['*'], [''], ['13TeV'], [''], ['bkg'], cats, False)

cb.ForEachObs(lambda x: x.set_rate(obs_rates[x.bin()]))
cb.ForEachProc(lambda x: x.set_rate(1))

cb.cp().bin(['D']).AddSyst(cb, 'DummySys', 'lnN', ch.SystMap()(1.0001))

cb.cp().bin(['B', 'C', 'D']).AddSyst(cb, 'scale_$BIN', 'rateParam', ch.SystMap('bin')
        (['B'], float(obs_rates['B']))
        (['C'], float(obs_rates['C']))
        (['D'], float(obs_rates['D']))
    )

cb.cp().bin(['A']).AddSyst(cb, 'scale_$BIN', 'rateParam', ch.SystMap()
        (('(@0*@1/@2)', ','.join(['scale_'+x for x in ['B', 'C', 'D']])))
    )

cb.PrintAll()
cb.WriteDatacard('example3.txt')

