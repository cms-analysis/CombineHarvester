import os,sys,ROOT,time
import datetime,time
from pyteetime import tee
channels="--channel Zll,Wmn,Znn,cmb"
lxbatch_jobs_submitted = []

##############################################
def stamp():
    ts = time.time()
    print '\n\n';sys.stdout.flush()
    print datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S');sys.stdout.flush()

def execute(command,usebatch,bash_script_name,queue,lxbatch_jobs_submitted,fitdiagnostic=''):
    print(command);sys.stdout.flush()
    if not usebatch:
        os.system(command)
    else:
        file = open(bash_script_name,'w')        
        file.write('#!/bin/bash\n') 
        file.write('cd '+os.getcwd()+'\n') 
        file.write('eval `scramv1 runtime -sh`\n') 
        file.write('ulimit -s unlimited\n') 
        file.write('echo "'+bash_script_name+'"\n')          
        file.write(command+' 2>&1 | tee '+os.getcwd()+'/logs/'+bash_script_name.replace('.sh','.log')+' \n')          
        file.write('echo ""\n')          
        file.write('echo "command was:"\n')          
        file.write('echo "'+command.replace('"','\"')+'" >> '+os.getcwd()+'/logs/'+bash_script_name.replace('.sh','.log')+'\n')          
        file.close()
        submitted = os.popen('chmod +x '+bash_script_name+'; bsub -u pippo123 -C 0 -q '+queue+' '+bash_script_name).read();
        os.system('sleep 1')
        if '<' in submitted:
            lxbatch_jobs_submitted.append(submitted.split('>')[0].split('<')[1])
            # print 'submitted',lxbatch_jobs_submitted

def check_running(lxbatch_jobs_submitted):
    still_running = True
    while still_running:
        os.system("bjobs -w")
        bjobs_running = os.popen("bjobs -w | grep $USER | grep RUN | awk '{print $1}'").read();
        bjobs_running = bjobs_running.split('\n')
        bjobs_running = filter(None, bjobs_running)
        bjobs_all = os.popen("bjobs -w | grep $USER | awk '{print $1}'").read();
        bjobs_all = bjobs_all.split('\n')
        bjobs_all = filter(None, bjobs_all)
        list_common = list(set(bjobs_all).intersection(lxbatch_jobs_submitted))
        if len(list_common)>0:
            still_running = True
            print len(lxbatch_jobs_submitted),'jobs submitted, ',list_common,',',len(list_common),'to go,',len(bjobs_running),'running. Waiting 30 sec and checking again\r'
            os.system('rm -rf LSFJOB_* 2>&1 > /dev/null')
            time.sleep(30)
        else:
            still_running = False
  
##############################################
###### START OF STEERABLE PARAMETERS #########
##############################################

usebatch = True
queue = '1nh'
# usebatch = False

# FOLDERS 
output_folder = "test_Jun29_rebinCR_v2" # specify output folder prefix
# year = "2016" # select 2016 or 2017
# extra_folder = "--extra_folder 2016_June19_forUnblinding_DNNTransformed" # specify sub-folder for AT shapes
year = "2017" # select 2016 or 2017
extra_folder = "--extra_folder 2017_June19_forUnblinding_DNNPirminTransform" # specify sub-folder for AT shapes

rebinning_scheme = 'v3' # '' no rebinning , 'v1', 'v2','v3'

# CHANNELS
channels = "--channel Znn,Wln,Zll,cmb" # separate channels by comma without space, comment line for all channels
# channels = "--channel Znn" # separate channels by comma without space, comment line for all channels
# channels = "--channel Zll,Wln,Znn"

# DATACARDS, WS, TOYS
# create_datacards = True
# create_masked_ws = True
# create_unmasked_ws = True
# build_asimov_dataset = True

# FITS
significance_without_systematics = True
significance_prefit = True
# significance_postfit_cr = True

# DIAGNOSTIC
# diagnostic_postfit_cr = True
# diagnostic_postfit_cr_sr_blind = True
# dump_diagnostic_overconstraints_cr = True
# dump_diagnostic_overconstraints_cr_sr = True

# NOT USED / TO BE TESTED
# diagnostic_postfit_cr_ws = True

###############################################
######### END OF STEERABLE PARAMETERS #########
###############################################

# LOGFILE = tee.stdout_start('log_from_'+extra_folder.replace('--extra_folder ','')+'_to_'+output_folder+'_'+year+'_'+channels.replace("--channel ",'').replace(',','_')+'_STDOUT.log',append=False) # STDOUT
# tee.stderr_start('log_from_'+extra_folder.replace('--extra_folder ','')+'_to_'+output_folder+'_'+year+'_'+channels.replace("--channel ",'').replace(',','_')+'_STDERR.log',append=False) # STDERR

bash_script_name = 'CHANNEL_submit_from_'+extra_folder.replace('--extra_folder ','')+'_to_'+output_folder+'_rebin_'+rebinning_scheme+'_'+year+'.sh'
# print 'This text will appear on screen and also in the logfile'

channels_loop = channels.replace("--channel ",'');
if channels_loop == '': channels_loop = '*'

print 'change dir to submission';sys.stdout.flush()
os.chdir('/afs/cern.ch/work/p/perrozzi/private/git/Hbb/combination/CMSSW_8_1_0/src/CombineHarvester/VH2017/')
print 'creating output dir if needed';sys.stdout.flush()
if not os.path.exists('output/'+output_folder+''+year):
    os.makedirs('output/'+output_folder+''+year)

if 'create_datacards' in globals() and create_datacards:
    stamp()
    for channel in channels_loop.split(','):
        if channel == 'cmb': continue
        print 'create datacards','channel',channel;sys.stdout.flush()
        command = 'python scripts/VHbb2017.py --rebinning_scheme '+rebinning_scheme+' --output_folder '+output_folder+' --year '+year+' '+extra_folder+' --channel '+channel
        execute(command,usebatch,'create_datacards_'+bash_script_name.replace('CHANNEL',channel),queue,lxbatch_jobs_submitted)

if usebatch: check_running(lxbatch_jobs_submitted)
lxbatch_jobs_submitted = []

if 'create_unmasked_ws' in globals() and create_unmasked_ws:
    stamp()
    for channel in channels_loop.split(','):
        print 'create unmasked workspaces','channel',channel;sys.stdout.flush()
        command = 'combineTool.py -M T2W -o "ws.root" -i output/'+output_folder+''+year+'/'+channel
        execute(command,usebatch,'create_unmasked_workspaces_'+bash_script_name.replace('CHANNEL',channel),queue,lxbatch_jobs_submitted)

if usebatch: check_running(lxbatch_jobs_submitted)
lxbatch_jobs_submitted = []

if 'create_masked_ws' in globals() and  create_masked_ws:
    stamp()
    for channel in channels_loop.split(','):
        print 'create masked workspaces','channel',channel;sys.stdout.flush()
        command = 'combineTool.py -M T2W -o "ws_masked.root" -i output/'+output_folder+''+year+'/'+channel+' --channel-masks'
        execute(command,usebatch,'create_masked_workspaces_'+bash_script_name.replace('CHANNEL',channel),queue,lxbatch_jobs_submitted)

if usebatch: check_running(lxbatch_jobs_submitted)
lxbatch_jobs_submitted = []

if channels_loop == '*': channels_loop = 'Zll,Wln,Znn,cmb'

# stamp()
# print 'start channel loop';sys.stdout.flush()
# for channel in ['Zll','Wln','Znn','cmb']:
      
if 'build_asimov_dataset' in globals() and  build_asimov_dataset:
    # print '\n\n';sys.stdout.flush()
    stamp()
    for channel in channels_loop.split(','):
        print 'build asimov dataset','channel',channel;sys.stdout.flush()
        command = 'combineTool.py -M GenerateOnly --setParameters '\
                                          'mask_vhbb_Zmm_1_13TeV'+year+'=1,mask_vhbb_Zmm_2_13TeV'+year+'=1,'\
                                          'mask_vhbb_Zee_1_13TeV'+year+'=1,mask_vhbb_Zee_2_13TeV'+year+'=1,'\
                                          'mask_vhbb_Wen_1_13TeV'+year+'=1,mask_vhbb_Wmn_1_13TeV'+year+'=1,'\
                                          'mask_vhbb_Znn_1_13TeV'+year+'=1 '\
                                          '-t -1 --toysFrequentist --expectSignal 1 --saveToys --there -d output/'+output_folder+''+year+'/'+channel+'/ws_masked.root'
        execute(command,usebatch,'build_asimov_dataset_'+bash_script_name.replace('CHANNEL',channel),queue,lxbatch_jobs_submitted)

if usebatch: check_running(lxbatch_jobs_submitted)
lxbatch_jobs_submitted = []

if 'significance_without_systematics' in globals() and  significance_without_systematics:
    stamp()
    for channel in channels_loop.split(','):
        print 'Fit significance without systematics (run the maximum likelihood fit)','channel',channel;sys.stdout.flush()
        command = 'combineTool.py -M Significance --cminDefaultMinimizerStrategy 0 --freezeParameters all --cminPreFit=1 --significance -d output/'+output_folder+''+year+'/'+channel+'/ws_masked.root --there -t -1 --expectSignal 1'
        execute(command,usebatch,'significance_nosyst_'+bash_script_name.replace('CHANNEL',channel),queue,lxbatch_jobs_submitted)

if 'significance_prefit' in globals() and  significance_prefit:
    stamp()
    for channel in channels_loop.split(','):
        print 'Pre-fit significance (run the maximum likelihood fit)','channel',channel;sys.stdout.flush()
        command = 'combineTool.py -M Significance --cminDefaultMinimizerStrategy 0 --cminPreFit=1 --significance -d output/'+output_folder+''+year+'/'+channel+'/ws_masked.root --there -t -1 --expectSignal 1'
        execute(command,usebatch,'significance_prefit_'+bash_script_name.replace('CHANNEL',channel),queue,lxbatch_jobs_submitted)

if 'significance_postfit_cr' in globals() and  significance_postfit_cr:
    stamp()
    for channel in channels_loop.split(','):
        print 'Post-fit CR-only significance (run the maximum likelihood fit)','channel',channel;sys.stdout.flush()
        command = 'combineTool.py -M Significance --cminDefaultMinimizerStrategy 1 --cminPreFit=1 --significance -d output/'+output_folder+''+year+'/'+channel+'/ws_masked.root '\
                                                      '--there --toysFrequentist -t -1 --toysFile higgsCombine.Test.GenerateOnly.mH120.123456.root'
        execute(command,usebatch,'significance_postfit_cr_'+bash_script_name.replace('CHANNEL',channel),'8nh',lxbatch_jobs_submitted)

if 'diagnostic_postfit_cr_ws' in globals() and  diagnostic_postfit_cr_ws:
    stamp()
    for channel in channels_loop.split(','):
        print 'Post-fit CR-only significance (run the maximum likelihood fit)','channel',channel;sys.stdout.flush()
        command = 'combineTool.py -M FitDiagnostics -m 125 -d output/'+output_folder+''+year+'/'+channel+'/ws_masked.root --there '\
              '--cminDefaultMinimizerStrategy 0 --setParameters mask_vhbb_Zmm_1_13TeV2017=1,mask_vhbb_Zmm_2_13TeV2017=1,mask_vhbb_Zee_1_13TeV2017=1,mask_vhbb_Zee_2_13TeV2017=1,mask_vhbb_Wen_1_13TeV2017=1,mask_vhbb_Wmn_1_13TeV2017=1,mask_vhbb_Znn_1_13TeV2017=1,r=0 -n .SRMasked --redefineSignalPOIs SF_TT_Wln_2017 --freezeParameters r,CMS_res_j_13TeV'
        execute(command,usebatch,'diagnostic_postfit_cr_ws_'+bash_script_name.replace('CHANNEL',channel),'8nh',lxbatch_jobs_submitted)

if 'diagnostic_postfit_cr' in globals() and  diagnostic_postfit_cr:
    stamp()
    for channel in channels_loop.split(','):
        print 'Post-fit CR-only diagnostic','channel',channel;sys.stdout.flush()
        command = 'combineTool.py -M FitDiagnostics -m 125 --cminDefaultMinimizerStrategy 0 --cminPreFit=1 -d output/'+output_folder+''+year+'/'+channel+'/ws_masked.root --there'
        execute(command,usebatch,'diagnostic_postfit_cr_'+bash_script_name.replace('CHANNEL',channel),'8nh',lxbatch_jobs_submitted)

if 'diagnostic_postfit_cr_sr_blind' in globals() and  diagnostic_postfit_cr_sr_blind:
    stamp()
    for channel in channels_loop.split(','):
        print 'Post-fit CR+SR (blind) significance (run the maximum likelihood fit)','channel',channel;sys.stdout.flush()
        POI = channel if (not 'cmb' in channel) else 'Wln'
        if channel == 'Zll': POI = POI.replace('Zll','high_Zll')
        command = 'combineTool.py -M FitDiagnostics -m 125 -d output/'+output_folder+''+year+'/'+channel+'/ws.root --there --cminDefaultMinimizerStrategy 0 --redefineSignalPOIs SF_TT_'+POI+'_'+year+' --freezeParameters r --setParameters r=1'
        execute(command,usebatch,'significance_postfit_crsr_'+bash_script_name.replace('CHANNEL',channel),'8nh',lxbatch_jobs_submitted)

if 'dump_diagnostic_overconstraints_cr' in globals() and  dump_diagnostic_overconstraints_cr:
    stamp()
    for channel in channels_loop.split(','):
        print 'Dump over-constrained nuisances','channel',channel;sys.stdout.flush()
        f = ROOT.TFile('output/'+output_folder+''+year+'/'+channel+'/fitDiagnostics.Test.root')
        fit_b = f.Get('fit_b')
        fit_b.Print()
        command = 'python diffNuisances.py -f html output/'+output_folder+''+year+'/'+channel+'/fitDiagnostics.Test.root > '\
                                                  'output/'+output_folder+''+year+'/'+channel+'/'+channel+'_diffNuisances.htm'
        execute(command,False,'dump_diagnostic_postfit_cr_'+bash_script_name.replace('CHANNEL',channel),queue,lxbatch_jobs_submitted)

if 'dump_diagnostic_overconstraints_cr_sr' in globals() and  dump_diagnostic_overconstraints_cr_sr:
    stamp()
    for channel in channels_loop.split(','):
        print 'Dump over-constrained nuisances','channel',channel;sys.stdout.flush()
        f = ROOT.TFile('output/'+output_folder+''+year+'/'+channel+'/fitDiagnostics.Test.root')
        fit_b = f.Get('fit_b')
        # temp = sys.stdout
        # sys.stdout = sys.stderr
        # sys.stderr = temp

        'significance_postfit_crsr_'+bash_script_name.replace('CHANNEL',channel),
        fit_b.Print() 
        command = 'python diffNuisances.py -f html output/'+output_folder+''+year+'/'+channel+'/fitDiagnostics.Test.root > '\
                                                  'output/'+output_folder+''+year+'/'+channel+'/'+channel+'_diffNuisances.htm'
        execute(command,False,'dump_diagnostic_postfit_crsr_'+bash_script_name.replace('CHANNEL',channel),queue,lxbatch_jobs_submitted)
        
if usebatch: check_running(lxbatch_jobs_submitted)
