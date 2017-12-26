
# creating datacards
    
    `MorphingSMCP2016 --output_folder="cp261217" --postfix="-2D" --control_region=1 --mm_fit=false --ttbar_fit=true`

# Building the workspaces:
   `combineTool.py -M T2W -P CombineHarvester.CombinePdfs.CPMixture:CPMixture -i output/cp261217/{cmb,em,et,mt,tt}/* -o ws.root --parallel 8`

# Generate toys assuming SM Higgs
    generate toys assuming SM Higgs couplings and CP = even:
    `combineTool.py -m 125 -M GenerateOnly --setPhysicsModelParameters muF=1,muV=1,alpha=0 --freezeNuisances alpha,muF,muV --redefineSignalPOI alpha -t -1 --toysFrequentist -d output/cp261217/cmb/125/ws.root --there -n ".InitalFit" --saveWorkspace`

    `combineTool.py -m 125 -M GenerateOnly --setPhysicsModelParameters muF=1,muV=1,alpha=0 --snapshot clean --freezeNuisances alpha,muF,muV  -d output/cp261217/cmb/125/higgsCombine.InitalFit.GenerateOnly.mH125.root --there -n ".Toys" --saveToys`

# Run maximum liklihood scan

    `combineTool.py -m 125 -M MultiDimFit --setPhysicsModelParameters muF=1,muV=1,alpha=0 --setPhysicsModelParameterRanges alpha=0,1 --points 20 --redefineSignalPOIs alpha  -d output/cp261217/cmb/125/ws.root --algo grid -t -1 --toysFile output/cp261217/cmb/125/higgsCombine.Toys.GenerateOnly.mH125.123456.root` 

# Plot scan

    `python scripts/plot1DScan.py --main=higgsCombine.Test.MultiDimFit.mH125.root --POI=alpha --output=test`





