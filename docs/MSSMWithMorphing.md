MSSM Limits with RooMorphingPdf {#MSSMWithMorphing}
===================================================
**This example demonstrates the use of the RooMorphingPdf and other RooFit objects to build a complete MSSM signal model within a single datacard.** From this datacard we will build a workspace in which \f$m_{A}\f$ and \f$\tan\beta\f$ are free model parameters which can be scanned or fixed as needed, in exactly the same way as for other physics models, e.g. the \f$\kappa_{f}\f$ vs \f$\kappa_{v}\f$ model in the SM analysis. However, unlike the \f$\kappa_{f}\f$, \f$\kappa_{v}\f$ model where the parameters simply scale the signal processes with simple formulae, the \f$m_{A}\f$,\f$\tan\beta\f$ model must fix the masses, cross sections and branching ratios for each of the \f$h\f$, \f$H\f$ and \f$A\f$ bosons using the 2D scans provided by the LHC Higgs XS working group.

Getting Started
===============
Ensure you are setting up in a recommended CMSSW release on an SLC6 machine (see [here](https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideHiggsAnalysisCombinedLimit#SLC6_release)). Make sure your local copy of the [HiggsToTauTau](https://github.com/cms-analysis/HiggsAnalysis-HiggsToTauTau) repository is up-to-date. The [auxiliaries](https://github.com/roger-wolf/HiggsAnalysis-HiggsToTauTau-auxiliaries) repository is also required, and must be located at `$CMSSW_BASE/src/auxiliaries`. The RooMorphingPdf is currently provided in a private branch of the [CombinedLimit](https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit) package. You can get this as follows:

    cd HiggsAnalysis/CombinedLimit
    git remote add htt-dev https://github.com/ajgilbert/HiggsAnalysis-CombinedLimit.git
    git fetch htt-dev
    git checkout -b slc6-dev htt-dev/slc6-dev
    scramv1 b -j4
    cd -

Once this branch is checked-out it will be possible to compile the `CombinePdfs` package that is part of the `CombineHarvester` tool:

    cd HiggsAnalysis/HiggsToTauTau/CombineHarvester/CombinePdfs
    make

We will build the datacard using the program `bin/MorphingMSSM`. Take a look through the source code in `test/MorphingMSSM.cpp`.

