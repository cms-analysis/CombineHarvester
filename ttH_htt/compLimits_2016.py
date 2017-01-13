import os, subprocess, sys

channels = [
  "1l_2tau_3jets",
  "1l_2tau_4jets",
  #"2lss_1tau_3L",
  #"2lss_1tau_2lepton",
  #"2lss_1tau_3L_3jets",
  #"2lss_1tau_3L_4jets",
  #"3l_1tau"
]

shapeVariables = {
  "1l_2tau_3jets"   : [ "EventCounter", "numJets", "mvaOutput_1l_2tau_ttbar_TMVA", "mvaOutput_1l_2tau_ttbar_sklearn", "mTauTauVis" ],
  "1l_2tau_4jets"   : [ "EventCounter", "numJets", "mvaOutput_1l_2tau_ttbar_TMVA", "mvaOutput_1l_2tau_ttbar_sklearn", "mTauTauVis" ],
  "2lss_1tau_3L" : [ "EventCounter", "numJets", "mvaDiscr_2lss", "mvaOutput_2lss_1tau_ttbar_TMVA", "mvaOutput_2lss_1tau_ttbar_sklearn", "mTauTauVis", "memOutput_LR" ],
  "2lss_1tau_2lepton" : [ "EventCounter", "numJets", "mvaDiscr_2lss", "mvaOutput_2lss_1tau_ttbar_TMVA", "mvaOutput_2lss_1tau_ttbar_sklearn", "mTauTauVis" ],
  "2lss_1tau_3L_3jets" : [ "EventCounter", "numJets", "mvaDiscr_2lss", "mvaOutput_2lss_1tau_ttbar_TMVA", "mvaOutput_2lss_1tau_ttbar_sklearn", "mTauTauVis", "memOutput_LR" ],
  "2lss_1tau_3L_4jets" : [ "EventCounter", "numJets", "mvaDiscr_2lss", "mvaOutput_2lss_1tau_ttbar_TMVA", "mvaOutput_2lss_1tau_ttbar_sklearn", "mTauTauVis", "memOutput_LR" ],
  "3l_1tau"   : [ "EventCounter", "numJets", "mvaDiscr_3l", "mTauTauVis" ]
}

datacardFiles = {
  "1l_2tau_3jets" : "ttH_1l_2tau_2016Nov09_3jets_dR03mvaTight_%s.input.root",
  "1l_2tau_4jets" : "ttH_1l_2tau_2016Nov09_4jets_dR03mvaTight_%s.input.root",
  "2lss_1tau_3L" : "ttH_2lss_1tau_2016Nov03_dR03mvaMedium_%s.input.root",
  "2lss_1tau_2lepton" : "ttH_2lss_1tau_2016Oct19_2lepton_dR03mvaMedium_%s.input.root",
  "2lss_1tau_3L_3jets" : "ttH_2lss_1tau_2016Nov09_3jets_dR03mvaMedium_%s.input.root",
  "2lss_1tau_3L_4jets" : "ttH_2lss_1tau_2016Nov09_4jets_dR03mvaMedium_%s.input.root",
  "3l_1tau" : "ttH_3l_1tau_2016Oct19_dR03mvaMedium_%s.input.root"
}

WriteDatacard_executables = {
  "1l_2tau_3jets"   : 'WriteDatacards_1l_2tau',
  "1l_2tau_4jets"   : 'WriteDatacards_1l_2tau',
  "2lss_1tau_3L_3jets" : 'WriteDatacards_2lss_1tau',
  "2lss_1tau_3L_4jets" : 'WriteDatacards_2lss_1tau',
  "2lss_1tau_2lepton" : 'WriteDatacards_2lss_1tau',
  "3l_1tau"   : 'WriteDatacards_3l_1tau'
}

makePostFitPlots_macros = {
  "1l_2tau"   : 'makePostFitPlots_1l_2tau.C',
  "2lss_1tau_3L" : 'makePostFitPlots_2lss_1tau.C',
  "2lss_1tau_2lepton" : 'makePostFitPlots_2lss_1tau.C',
  "3l_1tau"   : 'makePostFitPlots_3l_1tau.C'
}    

def run_cmd(command):
  print "executing command = '%s'" % command
  p = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
  stdout, stderr = p.communicate()
  return stdout

workingDir = os.getcwd()
datacardDir = "/home/veelken/public/HIG16022_datacards/Tallinn/cut_optimization/"

for channel in channels:
  for shapeVariable in shapeVariables[channel]:
    channel_base = None
    for search_string in [ "1l_2tau", "2lss_1tau", "3l_1tau" ]:
      if channel.find(search_string) != -1:
        channel_base = search_string
    datacardFile_input = os.path.join(datacardDir, channel_base, datacardFiles[channel] % shapeVariable)
    datacardFile_output = "ttH_%s.root" % channel
    run_cmd('%s --input_file=%s --output_file=%s --add_shape_sys=false' % (WriteDatacard_executables[channel], datacardFile_input, datacardFile_output))
    txtFile = os.path.join(workingDir, "cut_optimization", "ttH_%s_%s_2016.txt" % (channel_base, shapeVariable))
    run_cmd('mv ttH_%s.txt %s' % (channel, txtFile))
    run_cmd('combine -M MaxLikelihoodFit -t -1 -m 125 %s' % txtFile)
    logFile = os.path.join(workingDir, "cut_optimization", "ttH_%s_%s_2016.log" % (channel, shapeVariable))
    run_cmd('rm %s' % logFile)
    run_cmd('combine -M Asymptotic -t -1 -m 125 %s &> %s' % (txtFile, logFile))
    rootFile = os.path.join(workingDir, "cut_optimization", "ttH_%s_%s_2016_shapes.root" % (channel_base, shapeVariable))
    run_cmd('PostFitShapes -d %s -o %s -m 125 -f mlfit.root:fit_s --postfit --sampling --print' % (txtFile, rootFile))
    ##run_cmd('root -b -n -q -l %s++' % os.path.join(workingDir, "macros", makePostFitPlots_macros[channel]))

