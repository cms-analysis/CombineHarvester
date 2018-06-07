#!/usr/bin/python
import os, subprocess, sys
from collections import OrderedDict

label="2017Dec05-VHbb"
source="/home/acaan/ttHAnalysis/2016/"+label+"/datacards/"
channels = ["1l_2tau"]
fileTags=["_Old","_OldVar","_OldVarHTT","_HTTWithKinFit_MVAonly","_HTTWithKinFit","_HTTLepID"]
nbins=[50,25,10,5,1]
#
print "Doing dictionaries"
shapeVariables=OrderedDict()
datacardFiles=OrderedDict()
WriteDatacard_executables=OrderedDict()
makePostFitPlots_macros=OrderedDict()
for nbin in nbins :
    for channel in channels:
        for fileTag in fileTags :
            name=channel+fileTag+"_nbin_"+str(nbin)
            shapeVariables[name] = "mvaOutput_1l_2tau_ttbar"+fileTag
            datacardFiles[name] = source+channel+"/prepareDatacards_"+channel+"_mvaOutput_"+channel+"_ttbar"+fileTag+"_"+str(nbin)+"bins.root"
            WriteDatacard_executables[name] = 'WriteDatacards_'+channel
            makePostFitPlots_macros[name] = 'makePostFitPlots_'+channel+'.C'


def run_cmd(command):
  print "executing command = '%s'" % command
  p = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
  stdout, stderr = p.communicate()
  print stderr
  return stdout

workingDir = os.getcwd()
datacardDir = "/home/acaan/VHbbNtuples_8_0_x/CMSSW_8_1_0/src/HiggsAnalysis/CombineHarvester/ttH_htt/"

#for channel in channels:
folder="limits_"+label
run_cmd('mkdir %s ' % (folder))
file = open("execute_plots.sh","w")
file.write("#!/bin/bash\n")
for shapeVariable in list(shapeVariables.keys()):
    print shapeVariable
    channel_base = None
    for search_string in [ "1l_2tau", "2lss_1tau", "3l_1tau" ]:
      if shapeVariable.find(search_string) != -1:
        channel_base = search_string
    ##datacardFile_input = os.path.join(datacardDir, channel_base, datacardFiles[channel] % shapeVariable)
    datacardFile_input = os.path.join(workingDir, datacardFiles[shapeVariable])
    datacardFile_output = os.path.join(workingDir, folder, "ttH_%s.root" % shapeVariable)
    #run_cmd('rm ttH_%s.txt' % shapeVariable)
    #run_cmd('rm %s' % datacardFile_output)
    #run_cmd('cp %s %s' % (datacardFile_input,datacardDir))
    run_cmd('%s --input_file=%s --output_file=%s --add_shape_sys=false' % (WriteDatacard_executables[shapeVariable], datacardFile_input, datacardFile_output))
    txtFile = datacardFile_output.replace(".root", ".txt")
    run_cmd('cp %s %s' % (datacardFile_output, datacardFile_output.replace(folder+"/", "/")))
    ##run_cmd('combine -M MaxLikelihoodFit -t -1 -m 125 %s' % txtFile)
    ##run_cmd('combine -M MaxLikelihoodFit -m 125 %s' % txtFile)
    logFile = os.path.join(workingDir, folder, "ttH_%s_2016.log" % (shapeVariable))
    ##run_cmd('rm %s' % logFile)
    ##run_cmd('combine -M Asymptotic -t -1 -m 125 %s &> %s' % (txtFile, logFile))
    run_cmd('combine -M Asymptotic -m %s -t -1 %s &> %s' % (str(125),txtFile, logFile)) # shapeVariable
    rootFile = os.path.join(workingDir, folder, "ttH_%s_shapes.root" % (shapeVariable))
    run_cmd('rm %s' % rootFile)
    run_cmd('PostFitShapes -d %s -o %s -m 125 ' % (txtFile, rootFile)) # -f mlfit.root:fit_s --postfit --sampling --print ## doing asimov now
    makeplots='root -l -b -n -q '+workingDir+'/macros/'+makePostFitPlots_macros[shapeVariable]+'++(\\"'+shapeVariable+'\\",\\"'+folder+'\\")'
    file.write(makeplots+ "\n")

file.close()
os.chmod("execute.sh", 0o755)
#subprocess.call(". ./execute.sh", shell=True)
