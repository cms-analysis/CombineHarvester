import os, subprocess, sys

channels = [
  "2lss_1tau",
]

datacardFiles = {
  ##"2lss_1tau" : "ttH_2lss_1tau_2016Oct05_dR03mvaMedium_mvaDiscr_2lss.input.root",
  "2lss_1tau" : "ttH_2lss_1tau_2016Aug29_dR03mvaMedium_mvaDiscr_2lss.input.root"
}

WriteDatacard_executables = {
  "0l_2tau"   : 'WriteDatacards_0l_2tau',
  "1l_1tau"   : 'WriteDatacards_1l_1tau',
  "0l_3tau"   : 'WriteDatacards_0l_3tau',
  "1l_2tau"   : 'WriteDatacards_1l_2tau',
  "2lss_1tau" : 'WriteDatacards_2lss_1tau',
  "2los_1tau" : 'WriteDatacards_2los_1tau',
  "2l_2tau"   : 'WriteDatacards_2l_2tau',
  "3l_1tau"   : 'WriteDatacards_3l_1tau'
}

makePostFitPlots_macros = {
  "0l_2tau"   : 'makePostFitPlots_0l_2tau.C',
  "1l_1tau"   : 'makePostFitPlots_1l_1tau.C',
  "0l_3tau"   : 'makePostFitPlots_0l_3tau.C',
  "1l_2tau"   : 'makePostFitPlots_1l_2tau.C',
  "2lss_1tau" : 'makePostFitPlots_2lss_1tau.C',
  "2los_1tau" : 'makePostFitPlots_2los_1tau.C',
  "2l_2tau"   : 'makePostFitPlots_2l_2tau.C',
  "3l_1tau"   : 'makePostFitPlots_3l_1tau.C'
}    

def run_cmd(command):
  print "executing command = '%s'" % command
  p = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
  stdout, stderr = p.communicate()
  return stdout

workingDir = os.getcwd()
datacardDir = "/home/veelken/public/HIG15008_datacards/Tallinn/cut_optimization/"

for channel in channels:
  datacardFile = os.path.join(datacardDir, channel, datacardFiles[channel])
  run_cmd('%s --input_file=%s --add_shape_sys=false' % (WriteDatacard_executables[channel], datacardFile))
  txtFile = os.path.join(workingDir, "cut_optimization", "ttH_%s_2015.txt" % channel)
  run_cmd('mv ttH_%s.txt %s' % (channel, txtFile))
  run_cmd('combine -M MaxLikelihoodFit -t -1 -m 125 %s' % txtFile)
  logFile = os.path.join(workingDir, "cut_optimization", "ttH_%s_2015.log" % channel)
  run_cmd('rm %s' % logFile)
  run_cmd('combine -M Asymptotic -t -1 -m 125 %s &> %s' % (txtFile, logFile))
  rootFile = os.path.join(workingDir, "cut_optimization", "ttH_%s_2015_shapes.root" % channel)
  run_cmd('PostFitShapes -d %s -o %s -m 125 -f mlfit.root:fit_s --postfit --sampling --print' % (txtFile, rootFile))
  run_cmd('root -b -n -q -l %s++' % os.path.join(workingDir, "macros", makePostFitPlots_macros[channel]))

