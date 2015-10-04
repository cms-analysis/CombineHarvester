Introduction {#mainpage}
========================

[TOC]

This page documents the CombineHarvester framework for the production and analysis of datacards for use with the CMS [combine](https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit) tool. The central part of this framework is the [CombineHarvester](\ref ch::CombineHarvester) class, which provides a representation of the text-format datacards and the associated shape input.

The production of new datacards typically requires several steps, for example:

  * Defining analysis categories, signal and background processes
  * Adding systematic uncertainties
  * Extracting the related shape inputs from ROOT files
  * Modifying this information in-place, e.g. scaling signal processes to different cross sections, switching processes from background to signal and *vice versa*
  * Applying bin error merging and creating bin-by-bin uncertainties
  * Pruning the set of bin-by-bin nuisance parameters
  * Exporting to the text datacard format and creating the associated ROOT shape files

All of these operations are performed either directly by methods of the CombineHarvester class, or by using higher-level helper functions (see \ref high-level-tools below). By design all of the input required for these steps can be specified directly in the code. This makes it possible to quickly build a datacard from scratch in a single, self-contained file, without the use of any external scripts or configuration files.

Other functions include extracting information about the fit model:

  * Evaluating the expected rates of signal and background processes, both pre- and post-fit, and for the latter taking into account the nuisance parameter correlations
  * Similar evaluation of the background shapes, including the ability to scale, modify and re-bin the shapes in-place

As well as histogram-based templates, the production of datacards with arbitrary RooFit PDFs and datasets is also supported.

Getting started {#getting-started}
==================================
The CombineHarvester code (https://github.com/cms-analysis/CombineHarvester) is contained within a "top-level" CMSSW package: `$CMSSW_BASE/src/CombineHarvester` with subpackages for the core framework (`CombineHarvester/CombineTools`) and custom PDF extensions  (`CombineHarvester/CombinePdfs`). Further analysis-specific sub-packages will be added in future.

You should checkout the HiggsAnalysis/HiggsToTauTau CMSSW package alongside the HiggsAnalysis/CombinedLimit package, using the release recommended by the combine developers [here](https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideHiggsAnalysisCombinedLimit#SLC6_release). Note that the CombineHarvester framework is only compatible with the CMSSW 7_X_Y series releases. A new release area can be set up and compiled in the following steps:

    export SCRAM_ARCH=slc6_amd64_gcc481
    scram project CMSSW CMSSW_7_1_5
    cd CMSSW_7_1_5/src
    cmsenv
    git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
    git clone https://github.com/cms-analysis/HiggsAnalysis-HiggsToTauTau.git HiggsAnalysis/HiggsToTauTau
    scram build
    cd HiggsAnalysis/HiggsToTauTau/CombineHarvester
    make all
    # optional, sets variable CHPATH to the CombineHarvester directory and allows python lib loading
    eval `make env`

If you are using this framework for the first time we recommend taking a look through some of the examples below which demonstrate the main features:

  * [Examples Part 1](\ref intro1): How CombineHarvester builds a datacard representation, parsing existing datacards, evaluating contents
  * [Examples Part 2](\ref intro2): Creating a new datacard, defining processes and systematics, writing text datacards
  * Examples Part 3: Creating post-fit yield-tables - *coming soon*
  * Examples Part 4: Creating post-fit plots - *coming soon*

\warning To run many of these examples you must first ensure the [auxiliaries](https://github.com/roger-wolf/HiggsAnalysis-HiggsToTauTau-auxiliaries) repository is located at `$CMSSW_BASE/src/auxiliaries` and up-to-date:
\verbatim
git clone https://github.com/roger-wolf/HiggsAnalysis-HiggsToTauTau-auxiliaries.git auxiliaries \endverbatim
The input root files will be sourced from here.

More realistic, though less well documented, examples can be found in the following files:
  * `CombineTools/bin/PostFitShapes` ([source code](\ref CombineTools/bin/PostFitShapes.cpp)) - see separate page [here](\ref post-fit-shapes)
  * `CombineTools/bin/SMLegacyExample` ([source code](\ref CombineTools/bin/SMLegacyExample.cpp)) - produces a complete set of htt datacards for the legacy Run I SM analysis (HIG-13-004). The same workflow is also possible in python, see `CombineTools/scripts/SMLegacyExample.py`
  * `CombineTools/bin/MSSMYieldTable` ([source code](\ref CombineTools/bin/MSSMYieldTable.cpp)) - produces the latex yield tables for the MSSM htt analysis (HIG-13-021). Run via the script `CombineTools/scripts/yield_tables_mssm_example.sh`. You will first need to copy the input datacards: `cd CombineTools; cp -r /afs/cern.ch/work/a/agilbert/public/CombineTools/data/mssm-paper-cmb ./input/`

High-level tools {#high-level-tools}
====================================
A number of high-level tools have been developed to provide a more convenient interface for some common CombineHarvester tasks:

  * ch::CardWriter: In a nutshell, calls `CombineHarvester::WriteDatacard` so you don't have to. It can be used to write a set of datacards into the familiar **LIMITS** directory structure, or any other structure based on simple pattern strings.
  * ch::BinByBinFactory: Does the merging of bin uncertainties within a category and creates bin-by-bin shape systematics
  * CopyTools.h: Provides functions like ch::CloneProcsAndSysts and ch::SplitSyst for duplicating existing processes and systematics
  * ch::ParseCombineWorkspace: A function that can populate a CombineHarvester instance directly from a `combine` workspace. May be useful for extracting post-fit yields and shapes for more complex physics models. Should be considered experimental at the moment.

Other comments {#note}
======================
**Creating a new package**: It is planned that each new analysis will create their own package within the `CombineHarvester` directory, where all the datacard creation, plotting and other tools specific to the analysis will be stored. This keeps the analysis-specific code self-contained, and ensures different analyses do not disrupt each other's workflow during the development phase. From within your own analysis package it is easy to mark other packages as dependencies, and thus use any common tools that have already been developed. Indeed we expect that tools or functions developed for specific analyses will be of more general use, in which case they will be promoted to the main `CombineTools` package. **Please raise an issue [here](https://github.com/cms-analysis/HiggsAnalysis-HiggsToTauTau/issues/new) if you would like a new package to be created for your analysis.**

**Code developments**: Please bear in mind this framework is still relatively new, with most parts written from the ground-up. The core code is well tested and stable, but it is likely over time the interface may change to accommodate new features and options -  especially after some real-world usage. If it's decided to remove or change a function or method it will first be marked as deprecated - a list of deprecated methods can be found via the menu on the left. At the same time, new features and developments are always welcome - either contact the developers directly or make a pull request.

**Python interface**: A python interface is also available - see the documentation page [here](\ref python-interface) for usage instructions. This is ultimately just a wrapper around the C++ code and most functions can be called in python in exactly the same way as their C++ counterparts. There are some functions however, especially those using template arguments, which have been adapted for python usage and may not provide exactly the same interface. Furthermore, as each C++ function has to be wrapped by hand, the python interface is liable to lag behind the C++ one.

**Error handling**: Note that it is quite possible to do things in a CombineHarvester instance that don't make sense, or at least don't allow for the production of a valid datacard - for example objects with missing shape information, negative process yields and categories without either observed data or background processes. The framework has been designed to detect many of these issues at the point in which they become a problem for a given function to proceed as intended. However there is no guarantee that all such issues will be detected. If a problem is encountered, a runtime exception will be thrown indicated the nature of the problem, for example, trying to extract a histogram missing from the input root file will produce this message:

    terminate called after throwing an instance of 'std::runtime_error'
      what():
    *******************************************************************************
    Context: Function ch::GetClonedTH1 at
      CombineHarvester/CombineTools/src/TFileIO.cc:21
    Problem: TH1 eleTau_0jet_medium/ggH not found in CMSSW_7_0_7/src/auxiliaries/shapes/htt_et.inputs-sm-7TeV-hcg.root
    *******************************************************************************

If the cause of such an error message is unclear, or if you believe the error message should not have been produced, please raise an issue here with full details on reproducing the problem: https://github.com/cms-analysis/CombineHarvester/issues/new

Please also raise an issue if you encounter any bugs, unintended behaviour, abrupt errors or segmentation faults - these will be addressed promptly by the developers.

