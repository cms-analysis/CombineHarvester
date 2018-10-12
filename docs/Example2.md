Examples Part II {#intro2}
==========================

[TOC]


**File**: CombineTools/bin/Example2.cpp

In this example we will set up a simplified version of the Higgs to tau tau datacards, while exploring the main features of datacard creation with the CombineHarvester tool. To run the example, first make sure the code has been compiled:

    cd $CMSSW_BASE/src
    scram b -j4
    Example2

Defining categories and processes {#ex2-p1}
===========================================

We start by defining two analysis categories (or 'bins'). It's a good idea for each bin to have a unique name: this is required by combine, and while not required by CombineHarvester explicitly, a number of functions rely on this being true. CombineHarvester also allows for each object to be assigned an integer value, called a "bin_id", that does not need to be unique. This can be useful to label a "type-of-category" that might appear more than once. For example, VBF event categories for both the 7TeV and 8TeV datasets might have a common bin_id, but different names: "vbf_7TeV" and "vbf_8TeV".

\snippet CombineTools/bin/Example2.cpp part1

Now we define the signal mass points we will build datacards for, but note these are specified as strings, not floats. The function `ch::MassesFromRange` is used to quickly generate mass values from 120 to 135 GeV in 5 GeV steps.

\snippet CombineTools/bin/Example2.cpp part2

The next step is to add some new objects to the CombineHarvester instance. First we will specifiy the observations (i.e. the actual data). The [AddObservations](\ref ch::CombineHarvester::AddObservations) method takes a series of vectors as arguments. Each vector specifies some property, such as the analysis name, the dataset era or the bin information. Every possible combination of elements from these vectors will be used to add a new Observation entry.

The arguments are:
    AddObservations(masses, analyses, eras, channels, categories)

Below we specify one mass entry ("*"), which implies we only need one entry that will cover all signal mass hypotheses. Then we specify the higgs-tau-tau analysis ("htt"), the 8TeV dataset ("8TeV"), the mu+tau analysis channel ("mt") and the categories we defined above. If the analysis, era and channel properties aren't relevant for your analysis, you can always leave them as a single emtpy string.

\snippet CombineTools/bin/Example2.cpp part3

Next we add the signal and background processes. The arguments are similar to the AddObservations method. An extra argument is added after the channels for the list of processes, and a final boolean option specifies whether these are signal or background processes. Note that each process name here should correspond to the histogram name in your input file. In the signal case we pass the list of Higgs mass hypotheses generated above instead of the generic "*".

\snippet CombineTools/bin/Example2.cpp part4

Creating systematics {#ex2-p2}
==============================
The next step is to add details of the systematic uncertainties. The details of an uncertainty on a single process in a single bin is called a ch::Systematic. With CombineHarvester we create the ch::Systematic entries for each uncertainty source in turn. In doing so we must specify: the name of the nuisance parameter we want to use, the type (i.e. normalisation or shape), which processes it should be applied to and the magnitude of the uncertainty on each process. All this information can be expressed in a single line of code (though for clarity we will usually split it over multiple lines), for example the luminosity uncertainty:

\snippet CombineTools/bin/Example2.cpp part5

We can break this line down into several parts. cb.cp() returns a shallow copy of the CombineHarvester instance - i.e. the Observation and Process entries are shared with the original object (see the documentation of [Example 1](\ref ex1-p4)). However, removing entries from this shallow copy leaves the entries in the original instance intact. The next method, [signals()](\ref ch::CombineHarvester::signals), acts on this copy. This is one of several filter methods. It removes any non-signal process from the internal entries. We do this because we only want to create Systematic entries for the signal processes. Like all filter methods this returns a reference to itself. Then we can apply the actual [AddSyst](\ref ch::CombineHarvester::AddSyst) method. The first argument is a reference to the CombineHarvester instance where the new Systematic entries should be created. In this case we just give it our original instance (remember we are calling the AddSyst method on a copy of this instance). The next argument is the Systematic name. Before the Systematic entry for each Process is created a number of string substitutions will be made, based on the properties of the process in question. These are:

    $BIN       --> proc.bin()
    $PROCESS   --> proc.process()  (the process name)
    $MASS      --> proc.mass()
    $ERA       --> proc.era()
    $CHANNEL   --> proc.channel()
    $ANALYSIS  --> proc.analysis()

So in this example we will expect names like "lumi_8TeV". This substitution provides a quick way of renaming systematics to be correlated/uncorrelated between different channels/analyses/bins etc. Next we specifiy the nuisance type, which must be either "lnN" or "shape". The final argument is special map (SystMap) that contains the set of values that should be added. The [SystMap](\ref ch::syst::SystMap) is a templated class, which can take an arbitrary number of template parameters. Each parameter specifies a Process property that will be used as part of the key to map to the values. In this case we will just use the process era as a key. We initialse a new map with `init`, then provide a series of entries. Each entry should consist of a series of vectors, one for each key value, and end in the lnN value that should be assigned. Processes matching any combination of key properties in this map will be assigned the given value. In this map, we assign any Process with era "7TeV" a value of 1.022, and any "8TeV" Process a value of 1.026. More examples are given below:

\snippet CombineTools/bin/Example2.cpp part6

Creation of asymmetric "lnN" uncertainties is supported through the [SystMapAsymm](\ref ch::syst::SystMapAsymm) class, whose interface is very similar to [SystMap](\ref ch::syst::SystMap). Instead of a single uncertainty value, simply provide the "down" and "up" relative uncertainties as two separate arguments.

Extracting shape inputs {#ex2-p3}
=================================
Next we populate these Observation, Process and Systematic entries with the actual histograms (and also yields). The last two arguments are the patterns which will be used to determine the paths of the nominal and systematic shape templates in the given file. Here we must do this separately for signal and background shapes which use a different naming convention. NOTE: In this method only the following substitutions are supported:

    $BIN        --> proc.bin()
    $PROCESS    --> proc.process()
    $MASS       --> proc.mass()
    $SYSTEMATIC --> syst.name()

Also note that data histogram must be named data_obs to be extracted by this command.

\snippet CombineTools/bin/Example2.cpp part7

Adding bin-by-bin uncertainties {#ex2-p4}
=========================================
The next step is optional. This will generate additional shape uncertainties to account for limited template statistics, so-called "bin-by-bin" uncertainties.

\snippet CombineTools/bin/Example2.cpp part8

We first create a ch::BinByBinFactory instance, and specify the bin error threshold over which an uncertainty should be created, expressed as a percentage of the bin content. We also set the flag "FixedNorm", which controls the normalisation of the Up and Down shapes that are created. If set to true, the normalisation is fixed to nominal rate. If false, the normalisation is allowed to vary. We then call the AddBinByBin method specifying that only the background processes should be considered.

Writing datacards {#ex2-p5}
===========================
Now we will iterate through the set of bins and mass points and write a text datacard file for each:

\snippet CombineTools/bin/Example2.cpp part9

While we are required to write a separate datacard for each mass point, there is no obligation to generate one for each bin. For example,

         cb.cp().mass({"125", "*"}).WriteDatacard("combined_125.txt", output);

will produce a datacard containing all categories.





