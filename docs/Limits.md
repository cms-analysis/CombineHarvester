Limits {#limits}
================

[TOC]

# Limits Documentation

In these examples we will work through several different limit calculations using datacards from the Run 1 HTT analyses.

## Limits in models with one POI

First we will compute limits vs MH in the legacy SM Higgs analysis. Go to the `CombineTools` directory and create the datacards using the `SMLegacyExample.py` script:

    cd $CMSSW_BASE/src/CombineHarvester/CombineTools
    python scripts/SMLegacyEsxample.py

This will create a familiar structure of datacards in output/sm_cards, with a subdirectory containing the datacards for all channels and categories (cmb) and subdirectories containing just the cards for specific channels (e.g. tt). Within each of these directories the cards are organised into further subdirectories corresponding to the mass of the signal. 

We will focus on computing the limits for each channel separately, but before we get to this we need to turn the datacards into binary RooFit workspaces. This means combining the cards from each category into a single text datacard with combineCards.py, then running text2workspace.py. The combineTool.py script has a mode called T2W that passes options through to `text2workspace.py` and supports multiple datacard or directory options. With a directory argument, all the cards within that directory are combined first. If the enclosing directory is a number then this will automatically be used as the `-m [mass]` option in `text2workspace.py`, so there is no need to specify this explicitly. We can also take advantage of the `--parallel` option to build multiple workspaces simultaneously.

    cd output/sm_cards
    combineTool.py -M T2W [emt][emt]/* -o workspace.root --parallel 4



 combine -M Asymptotic -d workspace.root -m 110:145:5
 
## Limit as a function of some other variable (multiple workspaces)

 combineTool.py -M Asymptotic -d pt.20.root pt.30.root pt.40.root -n .'${WSP_PREFIX}' -m 125
 
 or
 
 combineTool.py -M Asymptotic -d pt.20/wsp.root pt.30/wsp.root pt.40/wsp.root -n .'${DIR}'
 for X in */wsp.root
 
 should generate:
 combine -M Asymptotic -d pt.20.root -n .pt.20 -m 125

## Limits in models with more than one POI

### Expected limits: pre-fit vs post-fit (fit-to-asimov vs fit-to-data)

With the *Asymptotic* method of combine it is only possible to determine a limit for a single POI at a time. This POI will be chosen as the first one in the list of POIs embedded within the workspace. Therefore it is best to always specify the POI list explicitly, putting the one you want the limit for first in the list, e.g.

    combine -M Asymptotic -d workspace.root -m 125 --redefineSignalPOIs r_ggH,r_qqH
    
to set a limit on `r_ggH`. You should also decide how to treat the other POIs in the fits for the limit extraction. By default combine will allow all other POIs to float freely, so in this example `r_qqH` will be profiled. If instead you wish to fix it to a particular value then it should not be included in the list of POIs, e.g.

    combine -M Asymptotic -d workspace.root -m 125 --redefineSignalPOIs r_ggH --setPhysicsModelParameters r_qqH=0.0 --freezeNuisances r_qqH

There is a further issue to consider when computing expected limits without a fit to the data (combine option `--run blind` or when generating toy datasets with `-t`). For the profiled case combine must generate a background-only pre-fit asimov dataset for use in the asymptotic calculation. In doing this only the first POI in the list will be fixed to zero. So if the other POI values are non-zero then the asimov dataset will contain a (probably) unwanted signal contribution. To avoid this it is safest to explicitly set the values of the other POIs to zero, e.g.

    combine -M Asymptotic -d workspace.root -m 125 --redefineSignalPOIs r_ggH,r_qqH --setPhysicsModelParameters r_qqH=0.0


### Signal injected limits

Here we outline a procedure for generating toy datasets at a chosen mass hypothesis and determining the expected limit at other mass hypotheses. This example assumes you have a single workspace in which `MH` is a free parameter.

Postfit:

combine -M MultiDimFit -t -1 --toysFrequentist --redefineSignalPOIs r -m 125 --setPhysicsModelParameters r=1 --expectSignal 1 -v 3 -d htt_mt.root --cminDefaultMinimizerType Minuit2 --saveWorkspace -n .postfit

Dealing with multiple POIs:

Injected SM125 into MSSM:
 - generate with x=1

combine -M GenerateOnly --saveToys -t 10 -d higgsCombine.postfit.MultiDimFit.mH125.root -m 125 -n .postfit.toys --expectSignal 1 --snapshotName MultiDimFit


    combineTool.py -M Asymptotic -t 10 --toysFile higgsCombine.postfit.toys.GenerateOnly.mH125.'%(SEED)s'.root -s 1,2,3 -m 110:145:5 -d higgsCombine.postfit.MultiDimFit.mH125.root --expectSignal 1 --snapshotName MultiDimFit --setPhysicsModelParameters MH='%(MASS)s' --run observed --dry-run




