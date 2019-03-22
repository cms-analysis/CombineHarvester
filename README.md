# CombineHarvester

Full documentation: http://cms-analysis.github.io/CombineHarvester

## Quick start

This pacakge requires HiggsAnalysis/CombinedLimit to be in your local CMSSW area. We follow the release recommendations of the combine developers which can be found [here](https://cms-hcomb.gitbooks.io/combine/content/part1/#for-end-users-that-dont-need-to-commit-or-do-any-development). The CombineHarvester framework is  compatible with the CMSSW 7_4_X and 8_1_X series releases.

If you just need the core CombineHarvester/CombineTools subpackge, then the following scripts can be used to clone the repository with a sparse checkout for this one only:

    git clone via ssh:
    bash <(curl -s https://raw.githubusercontent.com/cms-analysis/CombineHarvester/master/CombineTools/scripts/sparse-checkout-ssh.sh)
    git clone via https:
    bash <(curl -s https://raw.githubusercontent.com/cms-analysis/CombineHarvester/master/CombineTools/scripts/sparse-checkout-https.sh)

A new full release area can be set up and compiled in the following steps:

    export SCRAM_ARCH=slc6_amd64_gcc530
    scram project CMSSW CMSSW_8_1_0
    cd CMSSW_8_1_0/src
    cmsenv
    git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
    # IMPORTANT: Checkout the recommended tag on the link above
    git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
    scram b

Previously this package contained some analysis-specific subpackages. These packages can now be found [here](https://gitlab.cern.ch/cms-hcg/ch-areas). If you would like a repository for your analysis package to be created in that group, please create an issue in the CombineHarvester repository stating the desired package name and your NICE username. Note: you are not obliged to store your analysis package in this central group.
