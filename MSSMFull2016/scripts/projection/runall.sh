#!/bin/bash

lumis=( 36.9 300 3000 )

#no syst
for l in "${lumis[@]}"; do
    echo "###############################"
    run.py --lumi $l --nosyst
    echo "###############################"
    run.py --lumi $l
    echo "###############################"
    run.py --lumi $l --scale all
    echo "###############################"
    run.py --lumi $l --scale bbb
done
