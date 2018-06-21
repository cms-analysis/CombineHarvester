import os,sys,ROOT
import datetime,time

##############################################
def stamp():
    ts = time.time()
    print '\n\n'
    print datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S');sys.stdout.flush()

def execute(command):
    print(command)
    os.system(command)

##############################################

output_folder = "testJun20_"
year = "2017"

print 'change dir to submission';sys.stdout.flush()
os.chdir('/afs/cern.ch/work/p/perrozzi/private/git/Hbb/combination/CMSSW_8_1_0/src/CombineHarvester/VH2017/')

stamp()
print 'create datacards';sys.stdout.flush()
command = 'python scripts/VHbb2017.py --output_folder '+output_folder+' --year '+year+''
execute(command)

# os.system('combineTool.py -M T2W -o "ws.root" -i output/'+output_folder+''+year+'/*')

stamp()
print 'create masked workspaces';sys.stdout.flush()
command = 'combineTool.py -M T2W -o "ws_masked.root" -i output/'+output_folder+''+year+'/* --channel-masks'
execute(command)

stamp()
print 'start channel loop';sys.stdout.flush()
for channel in ['Zll','Wln','Znn','cmb']:
# for channel in ['Zll']:
    print '\n\n'
    print datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S');sys.stdout.flush()
    print 'channel',channel;sys.stdout.flush()
    print 'build asimov dataset';sys.stdout.flush()
    command = 'combineTool.py -M GenerateOnly --setParameters '\
                                      'mask_vhbb_Zmm_1_13TeV'+year+'=1,mask_vhbb_Zmm_2_13TeV'+year+'=1,'\
                                      'mask_vhbb_Zee_1_13TeV'+year+'=1,mask_vhbb_Zee_2_13TeV'+year+'=1,'\
                                      'mask_vhbb_Wen_1_13TeV'+year+'=1,mask_vhbb_Wmn_1_13TeV'+year+'=1,'\
                                      'mask_vhbb_Znn_1_13TeV'+year+'=1 '\
                                      '-t -1 --toysFrequentist --expectSignal 1 --saveToys --there -d output/'+output_folder+''+year+'/'+channel+'/ws_masked.root'
    execute(command)

    stamp()
    print 'Pre-fit significance (run the maximum likelihood fit)';sys.stdout.flush()
    command = 'combineTool.py -M Significance --significance -d output/'+output_folder+''+year+'/'+channel+'/ws_masked.root --there -t -1 --expectSignal 1'
    execute(command)

    stamp()
    print 'Post-fit CR-only significance (run the maximum likelihood fit)';sys.stdout.flush()
    command = 'combineTool.py -M Significance --significance -d output/'+output_folder+''+year+'/'+channel+'/ws_masked.root '\
                                                  '--there --toysFrequentist -t -1 --toysFile higgsCombine.Test.GenerateOnly.mH120.123456.root'
    execute(command)

    stamp()
    print 'Post-fit CR-only diagnostic';sys.stdout.flush()
    command = 'combineTool.py -M FitDiagnostics -m 125 -d output/'+output_folder+''+year+'/'+channel+'/ws_masked.root --there --cminDefaultMinimizerStrategy 0'
    execute(command)
    f = ROOT.TFile('output/'+output_folder+''+year+'/'+channel+'/fitDiagnostics.Test.root')
    fit_b = f.Get('fit_b')
    fit_b.Print()


    stamp()
    print 'Dump over-constrained nuisances';sys.stdout.flush()
    command = 'python diffNuisances.py -f html output/'+output_folder+''+year+'/'+channel+'/fitDiagnostics.Test.root > '\
                                              'output/'+output_folder+''+year+'/'+channel+'/'+channel+'_diffNuisances.htm'
    execute(command)

