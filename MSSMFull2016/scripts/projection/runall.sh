#!/bin/bash

lumis=( 36.9 300 3000 )
odir="jun07"

#no syst
for l in "${lumis[@]}"; do
    echo "###############################"
    run.py --lumi $l --outdir $odir  --nosyst
    echo "###############################"
    run.py --lumi $l --outdir $odir
    echo "###############################"
    run.py --lumi $l --outdir $odir --scale all
    echo "###############################"
    run.py --lumi $l --outdir $odir --scale bbb
done
