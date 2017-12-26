
# creating datacards
    
    `MorphingSMCP2016 --output_folder="cp261217" --postfix="-2D" --control_region=1 --mm_fit=false --ttbar_fit=true`

# Building the workspaces:
   `combineTool.py -M T2W -P CombineHarvester.CombinePdfs.CPMixture:CPMixture -i output/cp261217/{cmb,em,et,mt,tt}/* -o ws.root --parallel 8`

# Generate toys assuming SM Higgs
    generate toys assuming SM Higgs couplings and CP = even:
    `combineTool.py -m 125 -M GenerateOnly --setPhysicsModelParameters muF=1,muV=1,alpha=0 -d output/cp261217/cmb/125/ws.root -t -1 --saveToys -n ".Toys"`







