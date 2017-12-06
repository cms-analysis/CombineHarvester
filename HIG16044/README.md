Setting up a new release area:

    export SCRAM_ARCH=slc6_amd64_gcc530
    scram project CMSSW CMSSW_8_1_0
    cd CMSSW_8_1_0
    cmsenv
    git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
    git checkout v7.0.4
    git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
    git checkout -b HIG16044-dev origin/HIG16044-dev
    scram b

The input shape files are stored in an external repository. On a machine with a kerberos token for CERN access (e.g. lxplus) the repository can be checked out as:

`git clone https://:@gitlab.cern.ch:8443/cms-vhbb/HIG16044.git shapes`

This doesn't require a password. Otherwise with normal https access (which does require a username and password) the repository can be checked out as:

`git clone https://gitlab.cern.ch/cms-vhbb/HIG16044.git shapes`
