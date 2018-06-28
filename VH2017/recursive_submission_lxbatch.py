import os,sys,ROOT
import datetime,time
from pyteetime import tee
channels=""

##############################################
def stamp():
    ts = time.time()
    print '\n\n';sys.stdout.flush()
    print datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S');sys.stdout.flush()

def execute(command):
    print(command);sys.stdout.flush()
    os.system(command)

##############################################

output_folder = "test_symmetry_"
year = "2016"
extra_folder = "--extra_folder 2016forUnblinding_retry_June25"
channels = "--channel Zll"
# channels = "--channel Wmn"

# DATACARDS, WS, TOYS
create_datacards = True
create_masked_ws = True
build_asimov_dataset = True
# FITS
significance_without_systematics = True
significance_prefit = True
significance_postfit_cr = True
# DIAGNOSTIC
diagnostic_postfit_cr = True
dump_diagnostic_overconstraints = True

create_unmasked_ws = False

# LOGFILE = tee.stdout_start('log_from_'+extra_folder.replace('--extra_folder ','')+'_to_'+output_folder+'_'+year+'_'+channels.replace("--channel ",'').replace(',','_')+'_STDOUT.log',append=False) # STDOUT
# tee.stderr_start('log_from_'+extra_folder.replace('--extra_folder ','')+'_to_'+output_folder+'_'+year+'_'+channels.replace("--channel ",'').replace(',','_')+'_STDERR.log',append=False) # STDERR

# print 'This text will appear on screen and also in the logfile'

print 'change dir to submission';sys.stdout.flush()
os.chdir('/afs/cern.ch/work/p/perrozzi/private/git/Hbb/combination/CMSSW_8_1_0/src/CombineHarvester/VH2017/')
print 'creating output dir if needed';sys.stdout.flush()
if not os.path.exists('output/'+output_folder+''+year):
    os.makedirs('output/'+output_folder+''+year)

if create_datacards:
    stamp()
    print 'create datacards';sys.stdout.flush()
    command = 'python scripts/VHbb2017.py --output_folder '+output_folder+' --year '+year+' '+extra_folder+' '+channels
    execute(command)

if create_unmasked_ws:
    os.system('combineTool.py -M T2W -o "ws.root" -i output/'+output_folder+''+year+'/*')

# DO NOT COMMENT OUT!
channels = channels.replace("--channel ",'');
if channels == '': channels = '*'

if create_masked_ws:
    stamp()
    print 'create masked workspaces';sys.stdout.flush()
    for channel in channels.split(','):
        command = 'combineTool.py -M T2W -o "ws_masked.root" -i output/'+output_folder+''+year+'/'+channel+' --channel-masks'
        execute(command)

stamp()
print 'start channel loop';sys.stdout.flush()
# for channel in ['Zll','Wln','Znn','cmb']:
for channel in channels.split(','):
      
    if build_asimov_dataset:
        print '\n\n';sys.stdout.flush()
        stamp()
        print 'channel',channel;sys.stdout.flush()
        print 'build asimov dataset';sys.stdout.flush()
        command = 'combineTool.py -M GenerateOnly --setParameters --cminDefaultMinimizerStrategy 0'\
                                          'mask_vhbb_Zmm_1_13TeV'+year+'=1,mask_vhbb_Zmm_2_13TeV'+year+'=1,'\
                                          'mask_vhbb_Zee_1_13TeV'+year+'=1,mask_vhbb_Zee_2_13TeV'+year+'=1,'\
                                          'mask_vhbb_Wen_1_13TeV'+year+'=1,mask_vhbb_Wmn_1_13TeV'+year+'=1,'\
                                          'mask_vhbb_Znn_1_13TeV'+year+'=1 '\
                                          '-t -1 --toysFrequentist --expectSignal 1 --saveToys --there -d output/'+output_folder+''+year+'/'+channel+'/ws_masked.root'
        execute(command)

    if significance_without_systematics:
        stamp()
        print 'Fit significance without systematics (run the maximum likelihood fit)';sys.stdout.flush()
        command = 'combineTool.py -M Significance --cminDefaultMinimizerStrategy 0 --freezeParameters all --cminPreFit=1 --significance -d output/'+output_folder+''+year+'/'+channel+'/ws_masked.root --there -t -1 --expectSignal 1'
        execute(command)

    if significance_prefit:
        stamp()
        print 'Pre-fit significance (run the maximum likelihood fit)';sys.stdout.flush()
        command = 'combineTool.py -M Significance --cminDefaultMinimizerStrategy 0 --cminPreFit=1 --significance -d output/'+output_folder+''+year+'/'+channel+'/ws_masked.root --there -t -1 --expectSignal 1'
        execute(command)

    if significance_postfit_cr:
        stamp()
        print 'Post-fit CR-only significance (run the maximum likelihood fit)';sys.stdout.flush()
        command = 'combineTool.py -M Significance --cminDefaultMinimizerStrategy 0 --cminPreFit=1 --significance -d output/'+output_folder+''+year+'/'+channel+'/ws_masked.root '\
                                                      '--there --toysFrequentist -t -1 --toysFile higgsCombine.Test.GenerateOnly.mH120.123456.root'
        execute(command)

    if diagnostic_postfit_cr:
        stamp()
        print 'Post-fit CR-only diagnostic';sys.stdout.flush()
        command = 'combineTool.py -M FitDiagnostics -m 125 --cminDefaultMinimizerStrategy 0 --cminPreFit=1 -d output/'+output_folder+''+year+'/'+channel+'/ws_masked.root --there'
        execute(command)
        f = ROOT.TFile('output/'+output_folder+''+year+'/'+channel+'/fitDiagnostics.Test.root')
        fit_b = f.Get('fit_b')
        fit_b.Print()


    if dump_diagnostic_overconstraints:
        stamp()
        print 'Dump over-constrained nuisances';sys.stdout.flush()
        command = 'python diffNuisances.py -f html output/'+output_folder+''+year+'/'+channel+'/fitDiagnostics.Test.root > '\
                                                  'output/'+output_folder+''+year+'/'+channel+'/'+channel+'_diffNuisances.htm'
        execute(command)

