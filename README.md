# CombineHarvester

Full documentation: http://cms-analysis.github.io/CombineHarvester

## Quick start

This package requires HiggsAnalysis/CombinedLimit to be in your local CMSSW area. We follow the release recommendations of the combine developers which can be found [here](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/#setting-up-the-environment-and-installation). The CombineHarvester framework is compatible with the CMSSW 10_2_X and 11_3_X series releases. The default branch, `main`, is for developments in the 11_3_X releases, and the current recommended tag is `v2.0.0`. The `102x` branch should be used in CMSSW_10_2_X, and is expected to receive only minor updates.

If you just need the core CombineHarvester/CombineTools subpackage, then the following scripts can be used to clone the repository with a sparse checkout for this one only:

    git clone via ssh:
    bash <(curl -s https://raw.githubusercontent.com/cms-analysis/CombineHarvester/main/CombineTools/scripts/sparse-checkout-ssh.sh)
    git clone via https:
    bash <(curl -s https://raw.githubusercontent.com/cms-analysis/CombineHarvester/main/CombineTools/scripts/sparse-checkout-https.sh)

A new full release area can be set up and compiled in the following steps:

    export SCRAM_ARCH=slc7_amd64_gcc900
    scram project CMSSW CMSSW_11_3_4
    cd CMSSW_11_3_4/src
    cmsenv
    git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
    # IMPORTANT: Checkout the recommended tag on the link above
    git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
    git checkout v2.0.0
    scram b

Previously this package contained some analysis-specific subpackages. These packages can now be found [here](https://gitlab.cern.ch/cms-hcg/ch-areas). If you would like a repository for your analysis package to be created in that group, please create an issue in the CombineHarvester repository stating the desired package name and your NICE username. Note: you are not obliged to store your analysis package in this central group.
