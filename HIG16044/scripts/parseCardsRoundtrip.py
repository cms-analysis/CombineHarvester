#!/usr/bin/env python
import ROOT
import CombineHarvester.CombineTools.ch as ch
import os

ROOT.TH1.AddDirectory(False)

shapes = os.environ['CMSSW_BASE'] + '/src/CombineHarvester/HIG16044/HIG16044cards/'
output = os.environ['CMSSW_BASE'] + '/src/CombineHarvester/HIG16044/output/vhbb_original/'

cb = ch.CombineHarvester()

cb.ParseDatacard(shapes+"vhbb_2016_13TeV.txt","vhbb","13TeV","")

writer=ch.CardWriter(output+"vhbb_2016_original.txt",
                      output+ "vhbb_input.root")
writer.SetWildcardMasses([])
writer.SetVerbosity(1);


writer.WriteCards("cmb",cb);







