#!/bin/sh

# Usage:
#
# channel:      must be one of [et, mt, em, tt, mm]
# header:       Latex-format text for the header of the table
# columns:      A list of categories to include, each entry of the form "<label>:<category number>",
#               where the <label> can be in latex and will be the column heading, and the <category number>
#               is the integer in the datacard name
# eras:         A list of datasets to include, of the form "XTeV:<Lumi>", where lumi is in pb-1. This is needed
#               for the eff * acc calculation
# d:            the model-specific datacard, will be named something like tmp_<tanb>.txt
# s:            the standard separate datacards, with a single resonance normalised using a xsec of 1 pb
# f:            the fit result from the mlfit.root file, of the form mlfit.root:fit_s or mlfit.root:fit_b depending
#               on whether you want the signal+bakground or background-only fit applied. Note this mlfit.root should
#               come from fitting the model-specific datacard.
# signal_mass:  which mass point to use
# tanb:         which value of tan(beta)
# postfit:      true/false


tanb=30
mass=350
input=data/bbb-SMHbkg-mlfit/cmb/
postfit="true"

./bin/MSSMtauptYieldTable --channel=mt --header="$\\Pgm\\Pgt_{h}$ channel" \
  --columns "No B-Tag:8" "B-Tag:9" --eras "7TeV:4935" \
  -d $input/$mass/tmp_30.00.txt -s $input/$mass/htt_mt_*.txt \
  -f $input/$mass/out/mlfit.root:fit_s \
  --signal_mass=$mass --tanb=$tanb --postfit=$postfit &> mt_yields_7TeV.tex

./bin/MSSMtauptYieldTable --channel=mt --header="$\\Pgm\\Pgt_{h}$ channel" \
  --columns "No B-Tag low:10" "No B-Tag medium:11" "No B-Tag high:12" "B-Tag low:13" "B-Tag high:14" --eras "8TeV:19712" \
  -d $input/$mass/tmp_30.00.txt -s $input/$mass/htt_mt_*.txt \
  -f $input/$mass/out/mlfit.root:fit_s \
  --signal_mass=$mass --tanb=$tanb --postfit=$postfit &> mt_yields_8TeV.tex

./bin/MSSMtauptYieldTable --channel=et --header="$\\Pe\\Pgt_{h}$ channel" \
  --columns "No B-Tag:8" "B-Tag:9" --eras "7TeV:4935" \
  -d $input/$mass/tmp_30.00.txt -s $input/$mass/htt_et_*.txt \
  -f $input/$mass/out/mlfit.root:fit_s \
  --signal_mass=$mass --tanb=$tanb --postfit=$postfit &> et_yields_7TeV.tex

./bin/MSSMtauptYieldTable --channel=et --header="$\\Pe\\Pgt_{h}$ channel" \
  --columns "No B-Tag low:10" "No B-Tag medium:11" "No B-Tag high:12" "B-Tag low:13" "B-Tag high:14" --eras "8TeV:19712" \
  -d $input/$mass/tmp_30.00.txt -s $input/$mass/htt_et_*.txt \
  -f $input/$mass/out/mlfit.root:fit_s \
  --signal_mass=$mass --tanb=$tanb --postfit=$postfit &> et_yields_8TeV.tex

./bin/MSSMtauptYieldTable --channel=em --header="$\\Pe\\Pgm$ channel" \
  --columns "No B-Tag:8" "B-Tag:9" --eras "7TeV:4980" "8TeV:19712" \
  -d $input/$mass/tmp_30.00.txt -s $input/$mass/htt_em_*.txt \
  -f $input/$mass/out/mlfit.root:fit_s \
  --signal_mass=$mass --tanb=$tanb --postfit=$postfit &> em_yields.tex

./bin/MSSMtauptYieldTable --channel=mm --header="$\\Pgm\\Pgm$ channel" \
  --columns "No B-Tag:8" "B-Tag:9" --eras "7TeV:4980" "8TeV:19712" \
  -d $input/$mass/tmp_30.00.txt -s $input/$mass/htt_mm_*.txt \
  -f $input/$mass/out/mlfit.root:fit_s \
  --signal_mass=$mass --tanb=$tanb --postfit=$postfit &> mm_yields.tex

./bin/MSSMtauptYieldTable --channel=tt --header="$\\Pgt_{h}\\Pgt_{h}$ channel" \
  --columns "No B-Tag low:10" "No B-Tag medium:11" "No B-Tag high:12" "B-Tag low:13" "B-Tag high:14"  --eras "8TeV:18400" \
  -d $input/$mass/tmp_30.00.txt -s $input/$mass/htt_tt_*.txt \
  -f $input/$mass/out/mlfit.root:fit_s \
  --signal_mass=$mass --tanb=$tanb --postfit=$postfit &> tt_yields.tex
