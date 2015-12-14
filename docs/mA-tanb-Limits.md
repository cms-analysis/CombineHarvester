Model dependent Limits using MorphingMSSMUpdate {#MSSMUpdateModelDep}
=================================================================

These instruction shall elaborate how to produce MSSM model dependent limits using the 8TeV part of the MSSM (CMS-PAS-HIG-14-029) analysis.


Creating datacards {#p1}
========================

First we create the datacards.

    cd CombineHarvester/Run1BSMComb/
    MorphingMSSMUpdate

The created datacards contain six signals: Three for each considered production process, ggH and bbH and each of them separated in the three neutral MSSM Higgs bosons h, H and A. The particular interesting feature of the "-NoModel" creation of the datacards is that all considered signal masses are stored in the workspace instead of having a single datacard for each mass. This has the advantage that high-level morphing tools of combine could be directly used instead of having to perform manual morphing using fixed mass datacards.


Scaling the workspace accordingly {#p2}
=======================================

The combined datacard "htt_mssm.txt" is now transfered to a MSSM model dependent workspace.

    text2workspace.py -b output/mssm_nomodel/htt_mssm.txt -o output/mssm_nomodel/htt_cmb_mhmodp.root -P CombineHarvester.CombinePdfs.MSSMv2:MSSM --PO filePrefix=$CMSSW_BASE/src/auxiliaries/models/ --PO modelFiles=8TeV,out.mhmodp-8TeV-tanbHigh-nnlo.root,0

Therefore, a physic model "MSSMv2.py" is used. It will try to read model files from the directory auxiliaries/models/, so we need to add this path as well as the model files themselves as additional parameters. The syntax for setting the path to the models is as above. The general syntax for the model files themselves is "--PO modelFiles=ERA,FILE,VERSION". In this example, we choose the mhmod+ model for high values of tanb at 8TeV. For a list of all available options for text2workspace, run text2workspace.py -h. For upcoming 13/14TeV runs VERSION=1 should be set.
After the creation the workspace "htt_cmb_mhmodp.root" contains the model information like BR/xs/masses for all considered mA/tanb which are set as parameters of interest. The six signal processes dependent on the parameters of interest.


Calculating values {#p3}
========================

In the next step we calculate the limits in the considered MSSM model phase space.

    python ../CombineTools/scripts/combineTool.py -M AsymptoticGrid scripts/mssm_asymptotic_grid.json -d output/mssm_nomodel/htt_cmb_mssm.root --job-mode 'lxbatch' --task-name 'mssm_mhodp' --sub-opts '-q 1nh' --merge=8

The scanned grid (=considered mA/tanb points) in the MSSM model is defined in the json file "mssm_asymptotic_grid.json". As example:

   "opts" : "--singlePoint 1.0",
   "POIs" : ["mA", "tanb"],
   "grids" : [
     ["130:150|10", "1:3|1", "0"],
     ["130:150|10", "4:60|20", ""]
   ],
   "hist_binning" : [87, 130, 1000, 60, 1, 60]

The "opts", "POIS" are mandatory. The "hist_binning" has no influence yet. The list of grids can be set like above. The first row, ["130:150|10", "1:3|1", "0"], defines a grid of mA=130, 140 and 150 GeV scanning tanb=1,2 and 3. The third command, here "0", sets the CLs limit to the given value instead of calculating it. This could be used to exclude some regions of the phase space which for example are known to be excluded by other theoretical constraints. If the third option is empty "" the CLs limit for the given region will be computed. Like in the second row, ["130:150|10", "4:60|20", ""], where a grid of mA=130, 140 and 150 GeV and tanb=4, 24 and 44 is scanned.
Here, the lxbatch computing system is used. Eight grid points are merged in one job.


Collecting the results in a single file {#p4}
=============================================

After all jobs have finished, the results can be collected by simple rerunning the calculating command.

    python ../CombineTools/scripts/combineTool.py -M AsymptoticGrid scripts/mssm_asymptotic_grid.json -d output/mssm_nomodel/htt_cmb_mhmodp.root --task-name 'mssm_mhodp'

The limits for the median expected, expected error bands and observed are stored in TGraph2D. The resulting file "asymptotic_grid.root" is needed for the plotting.


Plotting the limits {#p5}
=========================

The plotting is done be the "MSSMtanbPlot.py" script.

    python ../CombineTools/scripts/MSSMtanbPlot.py --file=asymptotic_grid.root --scenario="mhmodp"

Again, the filename after "--file" has to be the root file which was created in the previous step. MSSMtanbPlot.py also requires a name for the scenario, which will be written in the plot. MSSMtanbPlot.py will only produce the plots as a png- and pdf file. The plotting is still work in progress.
