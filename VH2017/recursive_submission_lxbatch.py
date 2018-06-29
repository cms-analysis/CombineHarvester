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

def execute(command,usebatch,bash_script_name,queue,lxbatch_jobs_submitted):
    print(command);sys.stdout.flush()
    if not usebatch:
        os.system(command)
    else:
        file = open(bash_script_name,'w')        
        file.write('#!/bin/bash\n') 
        file.write('cd '+os.getcwd()+'\n') 
        file.write('eval `scramv1 runtime -sh`\n') 
        file.write('ulimit -s unlimited\n') 
        file.write(command+'\n')          
        file.close()
        submitted = os.popen('chmod +x '+bash_script_name+'; bsub -u pippo123 -C 0 -q '+queue+' '+bash_script_name).read();
        os.system('sleep 1')
        if '<' in submitted:
            lxbatch_jobs_submitted.append(submitted.split('>')[0].split('<')[1])
            # print 'submitted',lxbatch_jobs_submitted

##############################################
###### START OF STEERABLE PARAMETERS #########
##############################################

usebatch = True
queue = '1nh'
# usebatch = False

# FOLDERS / CHANNELS
output_folder = "test_Jun29_rebinCR_onlyZll" # specify output folder prefix
# year = "2016" # select 2016 or 2017
# extra_folder = "--extra_folder 2016_June19_forUnblinding_DNNTransformed" # specify sub-folder for AT shapes
year = "2017" # select 2016 or 2017
extra_folder = "--extra_folder 2017_June19_forUnblinding_DNNPirminTransform" # specify sub-folder for AT shapes
channels = "--channel Znn,Wln,Zll,cmb" # separate channels by comma without space, comment line for all channels
# channels = "--channel Znn" # separate channels by comma without space, comment line for all channels
# channels = "--channel Zll,Wln,Znn"

# DATACARDS, WS, TOYS
create_datacards = True
# create_datacards = False
# create_masked_ws = True
create_masked_ws = False
# build_asimov_dataset = True
build_asimov_dataset = False

# FITS
# significance_without_systematics = True
significance_without_systematics = False
# significance_prefit = True
significance_prefit = False
# significance_postfit_cr = True
significance_postfit_cr = False
# significance_postfit_cr_sr_blind = True
significance_postfit_cr_sr_blind = False

# DIAGNOSTIC
# diagnostic_postfit_cr = True
diagnostic_postfit_cr = False
# dump_diagnostic_overconstraints = True
dump_diagnostic_overconstraints = False

# NOT USED / TO BE TESTED
create_unmasked_ws = False
diagnostic_postfit_cr_ws = False

###############################################
######### END OF STEERABLE PARAMETERS #########
###############################################

# LOGFILE = tee.stdout_start('log_from_'+extra_folder.replace('--extra_folder ','')+'_to_'+output_folder+'_'+year+'_'+channels.replace("--channel ",'').replace(',','_')+'_STDOUT.log',append=False) # STDOUT
# tee.stderr_start('log_from_'+extra_folder.replace('--extra_folder ','')+'_to_'+output_folder+'_'+year+'_'+channels.replace("--channel ",'').replace(',','_')+'_STDERR.log',append=False) # STDERR

bash_script_name = 'submit_from_'+extra_folder.replace('--extra_folder ','')+'_to_'+output_folder+'_'+year+'_'+channels.replace("--channel ",'').replace(',','_')+'.sh'
# print 'This text will appear on screen and also in the logfile'

# DO NOT COMMENT OUT!
channels_loop = channels.replace("--channel ",'');
if channels_loop == '': channels_loop = '*'

print 'change dir to submission';sys.stdout.flush()
os.chdir('/afs/cern.ch/work/p/perrozzi/private/git/Hbb/combination/CMSSW_8_1_0/src/CombineHarvester/VH2017/')
print 'creating output dir if needed';sys.stdout.flush()
if not os.path.exists('output/'+output_folder+''+year):
    os.makedirs('output/'+output_folder+''+year)

if create_datacards:
    stamp()
    print 'create datacards';sys.stdout.flush()
    for channel in channels_loop.split(','):
        print 'channel',channel;sys.stdout.flush()
        command = 'python scripts/VHbb2017.py --output_folder '+output_folder+' --year '+year+' '+extra_folder+' '+channel
        execute(command,usebatch,'create_datacards_'+bash_script_name,queue,lxbatch_jobs_submitted)

if create_unmasked_ws:
    for channel in channels_loop.split(','):
        print 'channel',channel;sys.stdout.flush()
        os.system('combineTool.py -M T2W -o "ws.root" -i output/'+output_folder+''+year+'/*')

if create_masked_ws:
    stamp()
    print 'create masked workspaces';sys.stdout.flush()
    for channel in channels_loop.split(','):
        print 'channel',channel;sys.stdout.flush()
        command = 'combineTool.py -M T2W -o "ws_masked.root" -i output/'+output_folder+''+year+'/'+channel+' --channel-masks'
        execute(command,usebatch,'create_masked_workspaces_'+bash_script_name,queue,lxbatch_jobs_submitted)

if channels_loop == '*': channels_loop = 'Zll,Wln,Znn,cmb'

stamp()
# print 'start channel loop';sys.stdout.flush()
# for channel in ['Zll','Wln','Znn','cmb']:
      
if build_asimov_dataset:
    print '\n\n';sys.stdout.flush()
    print 'build asimov dataset';sys.stdout.flush()
    stamp()
    for channel in channels_loop.split(','):
        print 'channel',channel;sys.stdout.flush()
        command = 'combineTool.py -M GenerateOnly --setParameters '\
                                          'mask_vhbb_Zmm_1_13TeV'+year+'=1,mask_vhbb_Zmm_2_13TeV'+year+'=1,'\
                                          'mask_vhbb_Zee_1_13TeV'+year+'=1,mask_vhbb_Zee_2_13TeV'+year+'=1,'\
                                          'mask_vhbb_Wen_1_13TeV'+year+'=1,mask_vhbb_Wmn_1_13TeV'+year+'=1,'\
                                          'mask_vhbb_Znn_1_13TeV'+year+'=1 '\
                                          '-t -1 --toysFrequentist --expectSignal 1 --saveToys --there -d output/'+output_folder+''+year+'/'+channel+'/ws_masked.root'
        execute(command,usebatch,'build_asimov_dataset_'+bash_script_name,queue,lxbatch_jobs_submitted)

if significance_without_systematics:
    stamp()
    print 'Fit significance without systematics (run the maximum likelihood fit)';sys.stdout.flush()
    for channel in channels_loop.split(','):
        print 'channel',channel;sys.stdout.flush()
        command = 'combineTool.py -M Significance --cminDefaultMinimizerStrategy 0 --freezeParameters all --cminPreFit=1 --significance -d output/'+output_folder+''+year+'/'+channel+'/ws_masked.root --there -t -1 --expectSignal 1'
        execute(command,usebatch,'significance_nosyst_'+bash_script_name,queue,lxbatch_jobs_submitted)

if significance_prefit:
    stamp()
    print 'Pre-fit significance (run the maximum likelihood fit)';sys.stdout.flush()
    for channel in channels_loop.split(','):
        print 'channel',channel;sys.stdout.flush()
        command = 'combineTool.py -M Significance --cminDefaultMinimizerStrategy 0 --cminPreFit=1 --significance -d output/'+output_folder+''+year+'/'+channel+'/ws_masked.root --there -t -1 --expectSignal 1'
        execute(command,usebatch,'significance_prefit_'+bash_script_name,queue,lxbatch_jobs_submitted)

if significance_postfit_cr:
    stamp()
    print 'Post-fit CR-only significance (run the maximum likelihood fit)';sys.stdout.flush()
    for channel in channels_loop.split(','):
        print 'channel',channel;sys.stdout.flush()
        command = 'combineTool.py -M Significance --cminDefaultMinimizerStrategy 1 --cminPreFit=1 --significance -d output/'+output_folder+''+year+'/'+channel+'/ws_masked.root '\
                                                      '--there --toysFrequentist -t -1 --toysFile higgsCombine.Test.GenerateOnly.mH120.123456.root'
        execute(command,usebatch,'significance_postfit_cr_'+bash_script_name,queue,lxbatch_jobs_submitted)

if diagnostic_postfit_cr_ws:
    stamp()
    print 'Post-fit CR-only significance (run the maximum likelihood fit)';sys.stdout.flush()
    for channel in channels_loop.split(','):
        print 'channel',channel;sys.stdout.flush()
        command = 'combineTool.py -M FitDiagnostics -m 125 -d output/'+output_folder+''+year+'/'+channel+'/ws_masked.root --there '\
              '--cminDefaultMinimizerStrategy 0 --setParameters mask_vhbb_Zmm_1_13TeV2017=1,mask_vhbb_Zmm_2_13TeV2017=1,mask_vhbb_Zee_1_13TeV2017=1,mask_vhbb_Zee_2_13TeV2017=1,mask_vhbb_Wen_1_13TeV2017=1,mask_vhbb_Wmn_1_13TeV2017=1,mask_vhbb_Znn_1_13TeV2017=1,r=0 -n .SRMasked --redefineSignalPOIs SF_TT_Wln_2017 --freezeParameters r,CMS_res_j_13TeV'
        execute(command,usebatch,'diagnostic_postfit_cr_ws_'+bash_script_name,queue,lxbatch_jobs_submitted)

if diagnostic_postfit_cr:
    stamp()
    print 'Post-fit CR-only diagnostic';sys.stdout.flush()
    for channel in channels_loop.split(','):
        print 'channel',channel;sys.stdout.flush()
        command = 'combineTool.py -M FitDiagnostics -m 125 --cminDefaultMinimizerStrategy 0 --cminPreFit=1 -d output/'+output_folder+''+year+'/'+channel+'/ws_masked.root --there'
        execute(command,usebatch,'diagnostic_postfit_cr_'+bash_script_name,queue,lxbatch_jobs_submitted)
        f = ROOT.TFile('output/'+output_folder+''+year+'/'+channel+'/fitDiagnostics.Test.root')
        fit_b = f.Get('fit_b')
        fit_b.Print()


if dump_diagnostic_overconstraints:
    stamp()
    print 'Dump over-constrained nuisances';sys.stdout.flush()
    for channel in channels_loop.split(','):
        print 'channel',channel;sys.stdout.flush()
        command = 'python diffNuisances.py -f html output/'+output_folder+''+year+'/'+channel+'/fitDiagnostics.Test.root > '\
                                                  'output/'+output_folder+''+year+'/'+channel+'/'+channel+'_diffNuisances.htm'
        execute(command,False,'dump_diagnostic_postfit_cr_'+bash_script_name,queue,lxbatch_jobs_submitted)


if significance_postfit_cr_sr_blind:
    stamp()
    print 'Post-fit CR+SR (blind) significance (run the maximum likelihood fit)';sys.stdout.flush()
    for channel in channels_loop.split(','):
        print 'channel',channel;sys.stdout.flush()
        command = 'combineTool.py -M FitDiagnostics -m 125 -d output/'+output_folder+''+year+'/'+channel+'/ws.root --there --cminDefaultMinimizerStrategy 0 --redefineSignalPOIs SF_TT_Wln_2017 --freezeParameters r --setParameters r=1'
        execute(command,usebatch,'significance_postfit_crsr_'+bash_script_name,queue,lxbatch_jobs_submitted)

        
if usebatch:
    still_running = True
    while still_running:
        running = os.popen("bjobs | awk '{print $1}'").read();
        running = running.split('\n')
        # print 'running',running
        # print 'lxbatch_jobs_submitted',lxbatch_jobs_submitted
        list_common = list(set(running).intersection(lxbatch_jobs_submitted))
        if len(list_common)>0:
            still_running = True
            print 'jobs',list_common,'still running, waiting 30 sec and check again\r'
            time.sleep(30)
        else:
            still_running = False

        