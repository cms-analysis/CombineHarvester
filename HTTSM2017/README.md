
The following is obsolete (old instructions for CMSSW_7_4_7). Please refer to Protocol_SM_Htt_2017.md.

# Setting up the environment
```
export SCRAM_ARCH=slc6_amd64_gcc481 #bash, for tcsh: setenv SCRAM_ARCH slc6_amd64_gcc481
scram project CMSSW CMSSW_7_4_7
cd CMSSW_7_4_7/src
cmsenv
git clone git@github.com:/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v6.3.2
cd ../..
git clone git@github.com:/cms-analysis/CombineHarvester.git CombineHarvester -b SMHTT2017-dev
scram b -j 8
```

---

# Input shape files
Will be stored in a gitlab repository. For now, to use your datacards:
```
cd $CMSSW_BASE/src/CombineHarvester/HTTSM2017
mkdir -p shapes/Vienna #substitute Vienna suitably
cp -p <datacard location> shapes/Vienna/
```
When running Morphing2017, add flags like "--input_folder_mt=Vienna/" as required.

