Reproducing Run 1 H->tautau results {#introrun1HTT}
=========================

Using all of the techniques described previously, both in terms of datacard production and usage of the RooMorphingPdf object for signal processes, code to reproduce many of the Run 1 H->tautau results is included in the package. For some analyses, development was first performed for the datacard production without morphing applied, and fully validated, before moving to using morphing for the signal process. Note that in the non-morphing version many of the analyses have an equivalent python version. Once the usage of RooMorphingPdf for signal was validated in several use cases some additional analyses were added making use of this method only. This section describes how to find the code for each of the legacy analyses and details any specifics beyond the previous examples. More detail on the validation which was made can be found in the analysis note AN-15-235. Note that to run all of the examples below, the shape files exist in /auxiliaries and are linked to the script correctly. For more information on running the statistical results with the produced datacards, see later sections.


Systematics for legacy H->tautau results {#run1HTTsystematics}
=========================

**Files** CombineTools/interface/HttSystematics.h, CombineTools/python/systematics

For analyses with a large number of systematic uncertainties, it is neater to detail these in a separate file from the main datacard production code. Files for the different analyses can be found at the paths above, either in c++ or python. 

Legacy SM H->tautau results {#run1HTTSM}
=========================

**Files** : CombineTools/bin/SMLegacyExample.cpp, CombineTools/scripts/SMLegacyExample.py

**Files** : CombinePdfs/bin/SMLegacyMorphing.cpp

The datacards for the legacy SM H->tautau results can be produced using the files listed above, available in both c++ and python. The code currently includes all the main tautau channels: ee, mm, mt, et, em and tt, and not the VH channels. The datacards are up to date with those used in the most recent CMS-ATLAS combination.

The code itself makes use of similar functions as to those already described for Example1 and Example2. A few new features are used as well:

1) Scaling signals by a cross-section times branching ratio factor

Generally for the SM analysis, limits are set on best fit signal strength mu with reference to the SM prediction for cross section times branching ratio. Thus it makes sense to scale the signal according to this value when filling the datacard. This can be done via code like:

\snippet CombineTools/bin/SMLegacyExample.cpp part1

This reads the values for cross section times branching ratio from a text file and then uses them to scale each of the signal processes by the appropriate value.  

2) Merging bin by bin uncertainties

The addition of bin by bin uncertainties was illustrated in Example2. The SM H->tautau code uses an additional option in the BinByBinFactory which allows the user to merge uncertainties from different background processes in a given bin. This can be useful when an analysis has a large number of bins and/or processes contributing, such that adding a separate nuisance for each case would be costly in computing time for the limit calculations. The code starts in the same way as in Example2, by setting up the BinByBinFactory as follows:

\snippet CombineTools/bin/SMLegacyExample.cpp part2

In this example the merge threshold is set to 0.5. This controls the proportion of the total error that is allowed to be merged. The add threshold controls the value below which the stat uncertainty should be for the bin by bin uncertainty to be added. The uncertainties for different processes can then be added and merged simultaneously using calls like:

\snippet CombineTools/bin/SMLegacyExample.cpp part3

The filters for eta, bin id and channel can be used in this way to add the specific requirements for each channel and category, of which there were many for the legacy SM analysis.

3) Pruning uncertainties

Alongside merging of bin by bin uncertainties, another trick is employed in the SM analysis to help reduce the computing time for the limits. The method is to first run a maximum likelihood fit in each of the channels separately, using the full uncertainty model, and then use the information on the impacts of the uncertainties to judge which ones have a negligible effect on the fit result. These are then removed from the uncertainty model for the full combined fit. The procedure is to read in a text file which includes the list of uncertainties to be dropped (this was created at the time using the old statistical framework, but could easily be created again if required). The systematics added to the CH instance are then filtered using this list, with code as follows: 

\snippet CombineTools/bin/SMLegacyExample.cpp part4

The validation of the produced SM cards as compared to the official cards can be found in the Analysis Note.


Run 1 H->hh->bbtautau and A->Zh->lltautau results {#run1HTTHhhAZh}
=========================

**Files** Run1BSMComb/bin/AZh.cpp, Run1BSMComb/bin/Hhh.cpp, CombineTools/scripts/HhhExample.py

**Files** Run1BSMComb/bin/MorphingAZh.cpp, Run1BSMComb/bin/MorphingHhh.cpp

The above scripts illustrate the datacard production for the H->hh and A->Zh analyses of HIG-14-034. The cards are very similar to those shown previously. The H->hh analysis makes use of the bin by bin merging functions exactly as described for the SM analysis. The A->Zh analysis makes use of one feature described for the SM cards- the ability to multiply signal by a constant factor. In this case the factor is 1000 to put the signal into femptobarns instead of picobarns.  

The validation of the produced cards as compared to the official cards can be found in the Analysis note.


MSSM update H->tautau results {#run1HTTMSSM}
=========================

**File** Run1BSMComb/bin/MorphingMSSMUpdate.cpp

The fit model for the MSSM update analysis is similarly complicated to the SM legacy analysis. There are a couple of unique features which are illustrated below:

1) Possibility to setup 3 Higgs bosons

In the MSSM there are three neutral Higgs bosons, and to set a limit on a particular MSSM model the signal model contains all three for the correct mass and ratios of cross section times branching ratios. For the model dependent limits therefore we need to have 6 separate signal processes in the datacards, one for each of the three neutral Higgs bosons, multiplied by two for the two different signal production mechanisms. This is done by mapping what exists in the shape files (two signal production processes generically named ggH and bbH, which can stand for any one of the three Higgs bosons) to the signal processes we want, using the following:

\snippet Run1BSMComb/bin/MorphingMSSMUpdate.cpp part1

When declaring the processes to be added to the CH instance, the full set of signal processes is included:

\snippet Run1BSMComb/bin/MorphingMSSMUpdate.cpp part2

Whereas when reading in the information from the shape file the usual names are used the individual ggH and bbH templates are used to fill the processes for all 3 Higgs bosons:

\snippet Run1BSMComb/bin/MorphingMSSMUpdate.cpp part3

When running model dependent limits, the 6 signal processes are used and manipulated in the required way to build a signal template for a given mA-tanb point. When running model independent limits, the datacards are simply setup with only one neutral Higgs boson, as appropriate for a single resonance search.

2) Tail fit uncertainties

During Run 1 for the MSSM analysis an analytic fit was performed to the high mass tail of the mass distribution for some of the backgrounds and associated systematics were included, in order to reduce problems with low statistics in the tails. For the initial implementation of the Run 1 cards, these tail fits are added 'by hand', i.e. directly included in the input shape file rather than the fits rerun. The systematics are then lifted from the shape file directly as shape uncertainties in the format:

\snippet CombineTools/src/HttSystematics_MSSMUpdate.cc part1

The validation of the MSSM update analysis has been performed in terms of the model independent and model dependent limits and is detailed in the Analysis note.
