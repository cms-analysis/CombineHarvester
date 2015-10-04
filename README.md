# CombineHarvester

Full documentation: http://cms-analysis.github.io/CombineHarvester

## Quick start

This pacakge requires HiggsAnalysis/CombinedLimit to be in your local CMSSW area. We follow the release recommendations of the combine developers which can be found [here](https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideHiggsAnalysisCombinedLimit#ROOT5_SLC6_release_CMSSW_7_1_X). Note that the CombineHarvester framework is only compatible with the CMSSW 7_X_Y series releases.  A new release area can be set up and compiled in the following steps:

    export SCRAM_ARCH=slc6_amd64_gcc481
    scram project CMSSW CMSSW_7_1_5
    cd CMSSW_7_1_5/src
    cmsenv
    git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
    git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
    scram b

**Important:** The CombineHarvester package currently requires the head of the default HiggsAnalysis/CombinedLimit branch (`slc6-root5.34.17`) and will not compile successfully with the tag listed on the combine twiki page. A new tag will be provided soon.

