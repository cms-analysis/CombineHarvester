
export SCRAM_ARCH=slc6_amd64_gcc481  
scram project CMSSW CMSSW_7_4_7  
cd CMSSW_7_4_7/src  
cmsenv  

#git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit  
#git clone ssh://git@github.com:7999/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit  
git clone git@github.com:cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit  
cd HiggsAnalysis/CombinedLimit  
git fetch origin  
#git tag #check which tag is most recent  
git checkout v6.3.2  #v6.3.2 as of May 2018
cd ../..  

#git clone https://github.com/mflechl/CombineHarvester.git CombineHarvester  
#git clone ssh://git@github.com:7999/mflechl/CombineHarvester.git CombineHarvester  
git clone git@github.com:mflechl/CombineHarvester.git CombineHarvester  
#cd CombineHarvester/          #not needed anymore, merged to master  
#git remote add cms git@github.com:cms-analysis/CombineHarvester.git  #not needed atm  
#git checkout MSSMFull2016-dev #not needed anymore, merged to master  
#cd ..                         #not needed anymore, merged to master  
scram b -j 8  

cd CombineHarvester/MSSMFull2016  
git clone https://gitlab.cern.ch/cms-htt/MSSM-Full-2016.git shapes  
git pull --rebase  
