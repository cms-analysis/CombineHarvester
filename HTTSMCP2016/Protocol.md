
# creating datacards
    
    `MorphingSMCP2016 --output_folder="cp261217" --postfix="-2D" --control_region=1 --mm_fit=false --ttbar_fit=true`

# Building the workspaces:
   `combineTool.py -M T2W -P CombineHarvester.CombinePdfs.CPMixture:CPMixture -i output/cp261217/{cmb,em,et,mt,tt}/* -o ws.root --parallel 8`

# Run maximum liklihood scan

    `combineTool.py -m 125 -M MultiDimFit --setPhysicsModelParameters muF=1,muV=1,alpha=0 --setPhysicsModelParameterRanges alpha=0,1 --points 20 --redefineSignalPOIs alpha  -d output/cp261217/cmb/125/ws.root --algo grid -t -1`

the params set by the option `--setPhysicsModelParameters` determin the parameters of the azimov dataset i.e SM params

# Plot scan

    `python scripts/plot1DScan.py --main=higgsCombine.Test.MultiDimFit.mH125.root --POI=alpha --output=test`





