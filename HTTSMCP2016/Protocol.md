
# creating datacards
    
    `MorphingSMCP2016 --output_folder="cp261217" --postfix="-2D" --control_region=1 --mm_fit=false --ttbar_fit=true`

# Building the workspaces:
   `combineTool.py -M T2W -P CombineHarvester.CombinePdfs.CPMixture:CPMixture -i output/cp261217/{cmb,em,et,mt,tt}/* -o ws.root --parallel 8`

# Run maximum liklihood scan

    `combineTool.py -m 125 -M MultiDimFit --setPhysicsModelParameters muF=1,muV=1,alpha=0 --setPhysicsModelParameterRanges alpha=0,1 --points 20 --redefineSignalPOIs alpha  -d output/cp261217/cmb/125/ws.root --algo grid -t -1`

the params set by the option `--setPhysicsModelParameters` determin the parameters of the azimov dataset i.e SM params

# Plot scan

    `python scripts/plot1DScan.py --main=higgsCombine.Test.MultiDimFit.mH125.root --POI=alpha --output=test --no-numbers --no-box --x_title="#alpha (#frac{#pi}{2})"`

# Running with contrain on cross-section

At the moment this uses an approximation for the scaling of the cross-section with alpha. The PS cross-section is assumed to be 2.25x the SM cross-section based on Table 6 in https://arxiv.org/pdf/1407.5089.pdf. The cross-section is assumed to scale as XS_sm*cos(alpha)^2 + XS_ps*sin(alpha)^2.

Build the workspace using:

    `combineTool.py -M T2W -P CombineHarvester.CombinePdfs.CPMixture:CPMixture -i output/cp090118/{cmb,em,et,mt,tt}/* -o ws.root --PO constrain_ggHYield`

Then run the maximum liklihood scan using:
    
    `combineTool.py -m 125 -M MultiDimFit --setPhysicsModelParameters muV=1,alpha=0 --setPhysicsModelParameterRanges alpha=0,1 --points 20 --redefineSignalPOIs alpha  -d output/cp090118/cmb/125/ws.root --algo grid -t -1 --parallel=8`

# Run 2D fit

    `combineTool.py -m 125 -M MultiDimFit --setPhysicsModelParameters muF=1,muV=1,alpha=0 --setPhysicsModelParameterRanges alpha=0,1 --redefineSignalPOIs alpha,muF -d output/cp090118_aachen/cmb/125/ws.root --there -n ".2DScan" --points 500 --algo grid -t -1 --parallel=8`

