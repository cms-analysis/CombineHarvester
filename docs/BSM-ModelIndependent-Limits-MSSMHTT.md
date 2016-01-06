BSM Model independent Limits using MorphingMSSMUpdate {#MSSMUpdateNoModel}
=================================================================

These instruction shall elaborate how to produce model independent limits using the 8TeV part of the MSSM (CMS-HIG-14-039) analysis. Below there will be given instruction how to set limits on one signal process (ggH) while another is left floating (bbH).

Creating datacards {#MSSMUpdate-p1}
========================

The first step is to create the datacards, which will be used to produce the limit later on. To do this, go into the Folder CombineHarvester/Run1BSMComb/ and then execute MorphingMSSMUpdate. All of the programs in the following steps also need to be executed from this folder. Also make sure that all the files have been computed beforehand:

    cd CombineHarvester/Run1BSMComb/
    MorphingMSSMUpdate -m MH

MorphingMSSMUpdate.cpp is set up similarly like Example2.cpp. More information about the datacard steps could be found in the respective example. Adding the option "-m MH" when executing MorphingMSSMUpdate is necessary to ensure that the signal types are set to only assume one single narrow resonance produced via ggH and bbH instead of distinguishing between the three neutral MSSM bosons h, A and H.
It should be mentioned that CombineHarvester needs to use specific shape-rootfiles, which have been edited to reproduce the original result, since tail-fitting is not yet included in Combine Harvester.
The output will be a set of datacards. The special point is that not for each mass a datacard is created. In contrast a workspace is given for the signals which contain all centrally produced mass hypothesis. In the calculating process the signal will be morphed to the chosen mass. If, for example, MC signal templates exist for m=100GeV and 200GeV one could still calculate limits for m=150GeV ("combine -m 150 ..."). The created root file, named "htt_mssm_demo.root", will be in the CombinePdfs folder. It contains the centrally available MC signals for each channel, category and mass. Per default a combined datacard "htt_mssm.txt" is created, which contains all the information of the other datacards together.

Scaling the workspace accordingly {#MSSMUpdate-p2}
=======================================

Now that the datacards have been created, we can add which model we would like to study. We need to have a workspace, where the signals for each process are scaled correctly according to whatever model is selected.

    text2workspace.py -b output/mssm_nomodel/htt_mssm.txt -o output/mssm_nomodel/htt_ggPhi_mssm.root -P CombineHarvester.CombinePdfs.ModelIndependent:floatingMSSMXSHiggs --PO 'modes=ggH' --PO 'ggHRange=0:20'

This creates a workspace "output/mssm_nomodel/htt_ggPhi_mssm.root" based on the combined datacard. The physic model "floatingMSSMXSHiggs" is built to split the signal into the processes ggH and bbH. A signal scaling parameter is assigned to one process while the other is left floating and therefore will be treated as an nuisance parameter in the fit later on. In this example we like to set a limit on the xs*BR of the ggH (to tau tau) process. The fit range of 0 to 20 is set for this parameter (be sure that the fitting range contains the minimum and has sensible ranges). Here the bbH process is left floating. By changing "ggH" to "bbH" in the text2workspace.py step it is easily possible to switch this.
More advanced users might extend the physic model to be able to scale different processes (like ttH ...).


Calculating values {#MSSMUpdate-p3}
========================

Now that we have created the workspace htt_ggPhi_mssm.root, which can again be found in the output-folder, we now run combineTool.py, which will lead to the calculation all the values, which will later be used to create a plot.

    python ../CombineTools/scripts/combineTool.py -m 100:200:20,90,100,250:500:50,600:1000:100 -M Asymptotic --boundlist $CMSSW_BASE/src/CombineHarvester/CombinePdfs/scripts/mssm_ggh_boundaries.json output/mssm_nomodel/htt_ggPhi_mssm.root --freezeNuisances MH --setPhysicsModelParameters r_ggH=0

This program by itself only creates lists of jobs for the program "combine". These jobs can be run interactively on your own computer, or they can be sent somewhere else by using the option "--job-mode" (for example --job-mode 'lxbatch' when using CERN's computing power). To avoid sending too many jobs, we may use "--merge" to include a certain number of combine calls into one job (for example --merge=8 will include up to 8 combine calls into one single job).
Other than that, we need to specify which method to use, as well as the workspace. The specification of what method to use is done with the option "-M". In this example, the asymptotic limits are being calculated. The mass-range can be include with the option "-m". In this example, 19 different combine calls will be produced for the Higgs masses as seen at the bottom of this example. Since sensible boundaries on the parameter of interest (here ggH) can be mass dependent an important option can be to add a list of boundaries of the POI for each mass via a extern json fil, here "scripts/mssm_ggh_boundaries.json". This will set the range of relevant physics model parameters, depending on the production process and the mass.
The option "--freezeNuisances MH" is important to fix the hypothetical Higgs mass of the considered process to the one selected via the option "-m" instead of letting it freely floating in the fitting process.


Collecting the results in a single file {#MSSMUpdate-p4}
=============================================

Once all the jobs sent in the previous step and done, we will then collect all relevant data from the created root files into a single file. To do this, we will run combineTool.py again, but time with the method "CollectLimits", as well as different options.

    python ../CombineTools/scripts/combineTool.py -M CollectLimits -i higgsCo* -o mssm.json

The option "-i" is used to include all root files which have been previously created. These filenames usually all begin with "higgsCombine*". The filename specified after "-o" is the name of the json file which will be created. This json file contains all necessary, computated values from the root files, which will be needed to plot the limit. These include the values for the observation, expectation and the -2, -1, +1, +2 sigma uncertainties.


Plotting the limits {#MSSMUpdate-p5}
=========================

Finally we can produce the plot. To do this, we use the program "plotBSMxsBRLimit.py".

    python ../CombineTools/scripts/plotBSMxsBRLimit.py --file=mssm.json

The filename specified as "--file" is the json file produced in the previous step. We may also add more options regarding the aesthetics of the plot, such as changing the range of the x- and y-axis, or enabling logarithmic scaling. Executing this program along with the additional parameters will create the desired plot as a png- and pdf file. It will also create a textfile "mssm_limit_table.txt", which contains a list of the exact values for all mass points.
The limits of the described example should agree with the following numbers: 

|  mass  |   minus2sigma    |   minus1sigma    |     expected     |    plus1sigma    |    plus2sigma   |      observed     |
|--------|------------------|------------------|------------------|------------------|-----------------|-------------------|
|   90.0 |    7.44689941406 |    10.4886741638 |          15.3125 |    22.3316726685 |   31.1344871521 |     21.4247200433 |
|  100.0 |     6.0858001709 |     8.5330581665 |       12.4140625 |    18.1046066284 |   25.0876998901 |     17.6605401733 |
|  120.0 |    1.18392789364 |    1.57787442207 |    2.17265629768 |    3.03002619743 |   4.02200269699 |     2.97035384799 |
|  130.0 |   0.639678955078 |   0.856723308563 |        1.1953125 |    1.68129837513 |    2.2536046505 |     1.59457176432 |
|  140.0 |   0.438079833984 |   0.584083616734 |   0.815625011921 |    1.14398777485 |   1.52501606941 |     0.94770346896 |
|  160.0 |   0.253028869629 |   0.337358653545 |    0.47109374404 |   0.660751521587 |  0.886857688427 |    0.460536925886 |
|  180.0 |   0.180056750774 |   0.240920364857 |   0.332812488079 |   0.466799587011 |  0.626536250114 |    0.302229212372 |
|  200.0 |   0.143707275391 |    0.19228386879 |         0.265625 |   0.370445460081 |   0.49172270298 |    0.227834272278 |
|  250.0 |  0.0768411234021 |   0.102051369846 |   0.142031252384 |   0.198079377413 |  0.264753729105 |    0.117494322717 |
|  300.0 |  0.0484149158001 |  0.0645136460662 |   0.090468749404 |   0.126169368625 |  0.168638512492 |     0.06854323815 |
|  350.0 |  0.0495315566659 |  0.0657380968332 |  0.0886718779802 |   0.118715122342 |  0.152319088578 |   0.0842439601436 |
|  400.0 |  0.0397595204413 |   0.052680041641 |  0.0721874982119 |  0.0972210913897 |   0.12731602788 |   0.0725939537161 |
|  450.0 |  0.0276245102286 |   0.035754583776 |  0.0484374985099 |    0.06581415236 |  0.086501725018 |   0.0503201500801 |
|  500.0 |  0.0173510741442 |  0.0233783721924 |  0.0321874991059 |  0.0452741757035 | 0.0613017454743 |   0.0379442905513 |
|  600.0 |  0.0101513667032 |  0.0140254208818 |   0.019687499851 |    0.02816282399 | 0.0385656952858 |   0.0255840519774 |
|  700.0 | 0.00771972676739 | 0.00984832737595 |  0.0145312501118 |  0.0205551572144 | 0.0290479976684 |   0.0209467474855 |
|  800.0 |  0.0062255859375 | 0.00794219970703 |       0.01171875 |  0.0165767390281 | 0.0222346615046 |   0.0163398869015 |
|  900.0 |    0.00439453125 | 0.00567626953125 |        0.0078125 |  0.0113002872095 | 0.0163606926799 |   0.0107711296097 |
| 1000.0 | 0.00259765610099 | 0.00385009753518 | 0.00593749992549 | 0.00858821813017 | 0.0124341268092 | 0.008082145785341 |
