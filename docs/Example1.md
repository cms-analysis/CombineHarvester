Examples Part I {#intro1}
=========================

[TOC]


**File**: CombineTools/bin/Example1.cpp

In this example we use CombineHarvester to parse an existing datacard and then extract information from it. Open the file above and take a look at the source code. To run the example, first make sure the code has been compiled with `scram`:

    cd $CMSSW_BASE/src
    scram b -j4
    Example1

Parsing a single card {#ex1-p1}
===============================
In the first part we locate and open a single text datacard file:

\snippet CombineTools/bin/Example1.cpp part1

When parsing a datacard, CombineHarvester breaks down the information it contains into sets of objects, each represented by a C++ class. A ch::Observation object stores the information about the observed data in a single category, and likewise ch::Process stores the information for one expected signal or background process in a category. A ch::Systematic object records the uncertainty value assigned to a particular process from a particular source.

\note Internally a CombineHarvester contains three vectors, one for each kind of object. It's the job of the [ParseDatacard](\ref ch::CombineHarvester::ParseDatacard) method to build a new set of these objects, extract the mapped histograms, and append them to these vectors. The histogram extraction is done automatically using the mapping rules given in the datacard (the lines starting with `shape`). Once the mapped ROOT file has been located and opened, the relevant histograms are copied into their corresponding CombineHarvester objects.

Each object class stores a standard set of metadata, designed to aid in the filtering and selection of particular objects within a CombineHarvester, and which in the example above is specified explicitly. The possible metadata is listed in the following table.

 | name         | type       | example value |
 | :----------: | :--------: | :----------:  |
 | bin          | string     | *automatic*   |
 | process      | string     | *automatic*   |
 | analysis     | string     | "htt"         |
 | era          | string     | "8TeV"        |
 | channel      | string     | "mt"          |
 | bin_id       | int        | 6             |
 | mass         | string     | "125"         |

 Of these only `bin`, `process` and `mass` are tracked and used by combine, the others are optional and can be left empty if unneeded. The `bin` property is used to uniquely label an event category. Along with the process names, this is written directly into the datacard and is extracted automatically. The `mass` property is an exception: although we typically create a datacard for a particular signal mass hypothesis this information is not recorded in the datacard, but rather is passed to combine as a command line option, e.g. `combine -M Asymptotic -m 125 my_datacard.txt`.

 \warning If `mass` is not specified, [ParseDatacard](\ref ch::CombineHarvester::ParseDatacard) is likely to fail as this property is often needed to map signal processes to histograms in the input ROOT file. You can tell if this property is needed by looking for the term `$MASS` in the `shapes` rules at the top of the text datacard.

An important concept is that the objects created from a datacard are not explicitly linked - each is completely independent. When it's necessary to determine which objects are related, e.g. if we ask for the total uncertainty on a particular  process, CombineHarvester will determine this on-the-fly by matching up ch::Process and ch::Systematic objects that have identical metadata.

The last line of the code will print the information stored about the Observation, Process and Systematic entries that we've created. Like many CombineHarvester methods, these Print functions return a reference to the calling object, meaning they can be chained together to keep the code concise. The output will look like:

\verbinclude CombineTools/input/examples/example1_1.txt

Parsing multiple cards {#ex1-p2}
================================
Next we create another CombineHarvester instance and parse several datacards, this time using a method in which the object metadata is inferred from the datacard filenames:

\snippet CombineTools/bin/Example1.cpp part2

In this ParseDatacard method only two arguments are required: the path to the text datacard and a string containing place-holders for the metadata. Note that there's no obligation to include all five place-holders in this string. Additionally, the place-holders are not restricted to appearing in the filename but may also be included in the preceding directory path, e.g. `$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt` is also valid.

Filtering {#ex1-p3}
===================
Now let's pretend we are no longer interested in the first four categories we parsed. To remove objects we use a filter method. There are four generic filter methods: FilterAll, FilterObs, FilterProcs and FilterSysts that each accept a function, or function-type object that must have a single ch::Object, ch::Observation, ch::Process or ch::Systematic pointer argument and return a bool. A `true` return value indicates that the object should be dropped. The FilterAll method will act on all three object collections whereas the others operate only on their respective collections. It's often convenient to write a small lambda function in-place:

\snippet CombineTools/bin/Example1.cpp part3a

Alternatively,there are a number of fixed-property filters, in which you need only supply a vector of the object properties you want to keep:

\snippet CombineTools/bin/Example1.cpp part3b

An optional boolean can be supplied as a second argument. When set to false this reverses the logic -  objects with a property in the list will be dropped. In the second line we use this to remove all information about the QCD process. The full list of filter methods is found [here](\ref CH-Filters)

Yields, copying and sets {#ex1-p4}
==================================
In the final part of this example we take a look at the rate evaluation methods. These calculate the total event yields for either the observed data or the expected processes:

\snippet CombineTools/bin/Example1.cpp part4

Note that these functions are greedy - they will sum the contribution from every available Observation or Process entry. This means in the first line we get the total number of observed events in the three remaining categories. To get the yield for a single category we can prefix the function with a filter method. But here we must be careful, because we don't want to actually remove the information on the other categories permanently, which is what would happen if we just do:

    cmb2.bin({"muTau_vbf_loose"}).GetObservedRate();
    // cmb2 only contains objects for the "muTau_vbf_loose" category now!

To get around this we first call the [cp](\ref ch::CombineHarvester::cp) method on our CombineHarvester instance. This makes a shallow copy of the instance - in this it is only pointers to the contained objects, not the objects themselves, which are copied into a new instance. Such a copy is computationally fast to make, and we are free to filter objects from it without affecting the original instance at all.

\note Although filtering the objects in a shallow copy has no effect on the object lists in the original instance, both instances do still point to the same objects, so modifying the actual contents via the shallow copy will affect both instances. To create a full CombineHarvester copy, in which the underlying objects are also duplicated, use the [deep](\ref ch::CombineHarvester::deep) copy method instead.

The last part of the example code uses the CombineHarvester set-generating methods to conveniently loop through all defined (bin, process) combinations and print out the expected yield. The full list of available set-generating methods can be found [here](\ref CH-Set-Producers).
