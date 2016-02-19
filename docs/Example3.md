Examples Part III {#intro3}
==========================

[TOC]


**File**: CombineTools/bin/Example3.cpp

This examples demonstrates how to create a simple four-bin counting experiment datacard. It is based on the example given on the combine twiki [here](https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsWG/SWGuideNonStandardCombineUses#Rate_Parameters). Special `rateParam` directives are added to the datacard to allow the normalisations in three of these four bins to float freely and the fourth will be expressed as a function of the these three parameters. Here we follow the C++ interface example, a similar python version can be found in `CombineTools/scripts/Example3.py`. Make sure all the code is compiled and run the example:

    cd $CMSSW_BASE/src
    scram b -j4
    Example3

We start by defining four categories: A, B, C and D in the normal way. Contrary to the previous shape-based examples, with a counting experiment we have to specify all of the observed and expected yields directly. To start with we'll define a map containing the observed yields in each category.

\snippet CombineTools/bin/Example3.cpp part1

Next we create the CombineHarvester instance and populate it with Observation and Process entries. Then using the `ForEachProc` and `ForEachObs` methods we supply small lambda functions that set the observed and expected yields, for the former using our map defined above. For the latter we will set each yield to one and then create some `rateParam` entries that will allow these yields to float.

\snippet CombineTools/bin/Example3.cpp part2

First we add a regular `lnN` systematic uncertainty with the `AddSyst` method. Then, using the same technique, we add a `rateParam` systematic to each of the bins B, C and D. The name we give will be turned into a floating parameter which will be multiplied by the process yield that we set above to determine the overall process normalisation in the model. The name we specify here supports pattern substitution like any other systematic. In this case we have created a unique parameter per bin. In the SystMap we set the initial value of each parameter to the observed yield in the respective bin.

Then we create the second type of `rateParam` term, one which is a function of the other parameters we have specified. This sets the expected yield in bin A as a function of the three free parameters we just created, like in a standard ABCD method to set a background normalisation via control regions. As for the floating parameters this expression will be multiplied by the nominal process yield. To define the expression we use different mapping object, a `SystMapFunc`, which accepts two string arguments instead of a float. The first is a RooFit formula in terms of generic parameters, e.g. `@0`, and the second is a comma-separated list of the corresponding parameter names.

\snippet CombineTools/bin/Example3.cpp part3

\warning When calling `AddSyst` a check is made to see if the named parameter already exists. If so, and if it is a floating parameter, its initial value will be updated. If it is a formula, then the existing formula will be used to create the Systematic and the new value will be ignored, i.e. once a formula has been entered into the CombineHarvester instance it cannot be modified.

Finally we print the CombineHarvester contents. Note that the while the Systematic entries for the `rateParam` terms are shown in the list the "value" column currently always shows zero. For floating terms the actual values are given in the final list of parameters. We end by writing the text datacard, where the initial parameter values and formulae will be written at the end.

\snippet CombineTools/bin/Example3.cpp part4

\warning None of the CombineHarvester methods that evaluate process rates or shapes currently evaluate the effect of the `rateParam` terms. This will be implemented in a later release.





