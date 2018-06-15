#!/usr/bin/python

import argparse
import os
import sys
from time import localtime, strftime

CMSSW_BASE=os.environ['CMSSW_BASE']
rundir=CMSSW_BASE+'/src/CombineHarvester/MSSMFull2016/'
mdir=strftime("%Y-%m-%d_%Hh%Mm%S", localtime())
physdir=rundir+'output/'+mdir+'/'
symdir='latest/'
basedir=rundir+'output/'+symdir
logfile=basedir+'log.txt'

baselumi=36.9
dryrun=False

def main(argv):

  global mdir,physdir
  global loglevel
  global symdir,basedir,logfile

  parser = argparse.ArgumentParser(description='Steer the projection')
  parser.add_argument('mode', nargs='*',                         default=['all'],  choices=['all','datacard','ws','limit','mlfit','np'],     help='Mode of operation')
  parser.add_argument('--lumi',     dest='lumi',     type=float, default=baselumi,                                    help='Luminosity in fb-1')
  parser.add_argument('--nosyst',   dest='syst', nargs='?',      default=True, const=False,                           help='Flag to disable ystematics')
  parser.add_argument('--scale',    dest='scale',                default='none',   choices=['all','bbb','none'],      help='Scaling of uncertainties. Options: all, bbb, none')
  parser.add_argument('--model',    dest='model',                default='none',   choices=['mhmod','hmssm','none'],  help='Model-(in)dependent limits. Options: none, mhmod, hmssm')
  parser.add_argument('--loglevel', dest='loglevel', type=int,   default=1,                                           help='Verbosity, 0-essential, 1-most commands, 2-all commands')
  parser.add_argument('--outdir',   dest='outdir',               default=mdir,                                        help='root of output dir name (default: date/time)')
  parser.add_argument('--symdir',   dest='symdir',               default='latest/',                                   help='Symlink of output dir (change when running parallel!)')

  args = parser.parse_args()

  lumiscale=round(args.lumi/baselumi,2)
  syst=args.syst
  scale=args.scale
  loglevel=args.loglevel
  model=args.model
#  mdir+='_lumi-'+str(args.lumi)
  mdir=args.outdir+'_lumi-'+str(args.lumi)
  if not syst: mdir+='_nosyst'
  if not scale=='none': mdir+='_scale-'+scale
  physdir=rundir+'output/'+mdir+'/'

  symdir=args.symdir
  if not symdir.endswith('/'): symdir+='/'
  basedir=rundir+'output/'+symdir
  logfile=basedir+'log.txt'

  if 'all' in args.mode:
    args.mode.remove('all')
    args.mode.append('datacard')
    args.mode.append('ws')
    args.mode.append('limit')
    args.mode.append('mlfit')
    args.mode.append('np')

  if 'datacard' in args.mode:
    create_output_dir()

  make_print ( ' '.join(sys.argv)+' #COMMAND' , 0)
  make_print ( 'Mode: '+str(args.mode) )
  make_print ( 'Projecting to lumi='+str(args.lumi)+' using a lumi scale of '+str(lumiscale)+' to scale the base lumi of '+str(baselumi) )
  make_print ( 'Applying systematics: '+str(syst) )
  make_print ( 'Scaling uncertainties: '+scale )
  make_print ( 'Model: '+model )
  make_print ( 'Writing to '+physdir )

  os.chdir(rundir)
  ############################################## DATACARD
  if 'datacard' in args.mode:
    pcall_base='MorphingMSSMFull2016 --output_folder='+symdir+' --manual_rebin=true --real_data=false'
    if model=='none':
      pcall=pcall_base+' -m MH'
    else:
      pcall=pcall_base+' --remove_h=true'
    pcall=pcall+' &>'+basedir+'/log_datacard.txt'
    make_pcall(pcall,'Producing data cards for model '+model,0)
  ############################################## DATACARD

  ############################################## WORKSPACE
  if 'ws' in args.mode:
    scale_bbb='--X-nuisance-function \'CMS_htt_.*bin_[0-9]+\' \'"expr::lumisyst(\\"1/sqrt(@0)\\",lumi[1])"\''
    scale_all='--X-nuisance-function \'CMS_+\' \'"expr::lumisyst(\\"1/sqrt(@0)\\",lumi[1])"\''  +  ' --X-nuisance-function \'lumi_+\' \'"expr::lumisyst(\\"1/sqrt(@0)\\",lumi[1])"\''

    scaleterm=''
    if scale=='all':
      scaleterm=scale_all
    if scale=='bbb':
      scaleterm=scale_bbb

#    pcall='combineTool.py -M T2W -o ws.root --parallel 8 -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO \'"map=^.*/ggH.?$:r_ggH[0,0,200]"\' --PO \'"map=^.*/bbH$:r_bbH[0,0,200]"\' '+scaleterm+' -i output/'+symdir+'* &> '+basedir+'/log_ws.txt'
    pcall_base='combineTool.py -M T2W -o ws.root --parallel 8 '+scaleterm+' -i output/'+symdir+'*'

    if model=='none':
      pcall=pcall_base+' -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO \'"map=^.*/ggH.?$:r_ggH[0,0,200]"\' --PO \'"map=^.*/bbH$:r_bbH[0,0,200]"\''
    elif model=='mhmod':
      pcall=pcall_base+' -P CombineHarvester.CombinePdfs.MSSM:MSSM --PO filePrefix=$PWD/shapes/Models/ --PO modelFiles=13TeV,mhmodp_mu200_13TeV.root,1 --PO MSSM-NLO-Workspace=$PWD/shapes/Models/higgs_pt_v3_mssm_mode.root'
    elif model=='hmssm':
      pcall=pcall_base+' -P CombineHarvester.CombinePdfs.MSSM:MSSM --PO filePrefix=$PWD/shapes/Models/ --PO modelFiles=13TeV,hMSSM_13TeV.root,1 --PO MSSM-NLO-Workspace=$PWD/shapes/Models/higgs_pt_v3_mssm_mode.root'

    pcall+=' &> '+basedir+'/log_ws.txt'
    make_pcall(pcall,'Producing workspace',0)
  ############################################## WORKSPACE

  ############################################## LIMIT
  if 'limit' in args.mode:
    nfreeze='lumi'
    if not syst: nfreeze='all'

    if model=='none':
      proc=[ 'ggH' , 'bbH' ]
      make_pcall('echo Processes: '+str(proc)+' > '+basedir+'/log_lim.txt','',2)
      for p in proc:
        pcall1='combineTool.py -m "90,100,110,120,130,140,160,180,200,250,350,400,450,500,600,700,800,900,1000,1200,1400,1600,1800,2000,2300,2600,2900,3200" -M Asymptotic -t -1 --parallel 7 --rAbsAcc 0 --rRelAcc 0.0005 --boundlist input/mssm_boundaries-100.json --setPhysicsModelParameters r_ggH=0,r_bbH=0,lumi='+str(lumiscale)+' --freezeNuisances '+nfreeze+' --redefineSignalPOIs r_'+p+' -d output/'+symdir+'cmb/ws.root --there -n ".'+p+'" &>> '+basedir+'/log_lim.txt'
        pcall2='combineTool.py -M CollectLimits output/'+symdir+'cmb/higgsCombine.'+p+'*.root --use-dirs -o "output/'+symdir+p+'.json" &>> '+basedir+'/log_lim.txt'
        pcall3='python scripts/plotMSSMLimits.py --logy --logx --show exp output/'+symdir+p+'_cmb.json --cms-sub="Preliminary" -o output/'+symdir+p+'_cmb --process=\''+p[0:2]+'#phi\' --title-right="'+str(args.lumi)+' fb^{-1} (13 TeV)" --use-hig-17-020-style >> '+basedir+'/log_lim.txt'
        make_pcall(pcall1,'Producing  limit for '+p,0)
        make_pcall(pcall2,'Collecting limit for '+p,0)
        make_pcall(pcall3,'Plotting   limit for '+p,0)
    else:
      os.chdir(basedir)
      dp='../../'
      if model=='mhmod': js=dp+'./scripts/mssm_asymptotic_grid_mhmodp.json'
      if model=='hmssm': js=dp+'./scripts/mssm_asymptotic_grid_hMSSM.json'
      it=0
      while True:
        it+=1
        pcall='combineTool.py -M AsymptoticGrid '+js+' -d cmb/ws.root --setPhysicsModelParameters lumi='+str(lumiscale)+' --freezeNuisances '+nfreeze+' -t -1 --parallel 8 &>> '+basedir+'/log_lim.txt'
        make_pcall(pcall,'Producing  limit for '+model,0)
        ret=os.popen('tail -1 '+basedir+'/log_lim.txt').read().rstrip()
        if 'Replacing existing TGraph2D' in ret: 
          break
        if it>10: 
          make_print( 'Stopping after restarting AsymptoticGrid for ten times. There is probably some problem, rather give up than ending up in an infinite loop' )
          break
        
      make_print( 'python ../CombineTools/scripts/plotLimitGrid.py asymptotic_grid.root --scenario-label="m_{h}^{mod+} scenario" --output="mssm_mhmodp_cmb" --title-right="36.9 fb^{-1} (13 TeV)" --cms-sub="Preliminary" --contours="exp-2,exp-1,exp0,exp+1,exp+2,obs" --model_file=$PWD/shapes/Models/mhmodp_mu200_13TeV.root' )
      make_print( '#Run the above on lxplus: /afs/cern.ch/work/m/mflechl/mssm_projection_tmp/CMSSW_7_4_7/src/CombineHarvester/MSSMFull2016' )
  ############################################## LIMIT

  ############################################## NP
  smass=700
  nfreeze='r_bbH,lumi'
  if not syst: nfreeze='all'
  os.chdir(basedir)

  if 'mlfit' in args.mode:

    mllog=basedir+'log_mlfit.txt'
    pcall2='combineTool.py -M MaxLikelihoodFit --parallel 8 --setPhysicsModelParameters r_ggH=0.0,r_bbH=0.0,lumi='+str(lumiscale)+' --freezeNuisances '+nfreeze+' --setPhysicsModelParameterRanges r_ggH=-0.000001,0.000001 --setPhysicsModelParameterRanges r_bbH=-0.000001,0.000001 -d cmb/ws.root --redefineSignalPOIs r_ggH --there -m '+str(smass)+' --boundlist '+rundir+'/input/mssm_boundaries.json --minimizerTolerance 0.1 --minimizerStrategy 0 --name ".res" '+' &>'+mllog
    make_pcall(pcall2, 'Running ML fit')
    make_pcall('mv cmb/mlfit.res.root cmb/mlfit.root','Renaming mlfit output files',2)

    make_print( '########################################################################################' )
    ret=os.popen('root -l cmb/mlfit.root <<<"fit_b->Print();" | grep "covariance matrix quality"').read().rstrip()
    make_print( ret , 0 )
    print_file(ret,mllog,'a')
    make_print( '########################################################################################' )

  if 'np' in args.mode:
#    pcall='python '+CMSSW_BASE+'/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py cmb/mlfit.root -A -a --stol 0.99 --stol 0.99 --vtol 99. --vtol2 99. -f text --poi r_ggH --histogram nuisance_tests.root &> '+basedir+'/log_np.txt'
    pcall='python '+CMSSW_BASE+'/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py cmb/mlfit.root -a --stol 0.99 --stol 0.99 --vtol 99. --vtol2 99. -f text --poi r_ggH --histogram nuisance_tests.root &> '+basedir+'/log_np.txt'
    make_pcall(pcall,'Make NP texts... in dir: '+basedir)

    exvar=' --exclude `cat ../combined.txt.cmb | awk {\'print $1\'} | grep _bin_ | head -c -1 | tr \'\\n\' \',\' `'
    idir=basedir+'/cmb/impacts'
    make_dir(idir)
    os.chdir(idir)
    make_print( '### Make NP plots... in dir: '+idir)
    pcall4=[ 
      'combineTool.py -t -1 -M Impacts -d ../ws.root -m '+str(smass)+' --setPhysicsModelParameters r_bbH=0,r_ggH=0,lumi='+str(lumiscale)+' --setPhysicsModelParameterRanges r_ggH=-1.0,1.0 --doInitialFit --robustFit 1 --minimizerAlgoForMinos Minuit2,Migrad --redefineSignalPOIs r_ggH --freezeNuisances '+nfreeze+exvar+' &>log1.txt',
      'combineTool.py -t -1 -M Impacts -d ../ws.root -m '+str(smass)+' --setPhysicsModelParameters r_bbH=0,r_ggH=0,lumi='+str(lumiscale)+' --setPhysicsModelParameterRanges r_ggH=-1.0,1.0 --robustFit 1 --doFits --minimizerAlgoForMinos Minuit2,Migrad  --redefineSignalPOIs r_ggH --freezeNuisances '+nfreeze+ ' --allPars --parallel 8'+exvar+' &>log2.txt',
      'combineTool.py -M Impacts -d ../ws.root --allPars --redefineSignalPOIs r_ggH --setPhysicsModelParameters r_bbH=0,r_ggH=0,lumi='+str(lumiscale)+' --exclude r_bbH,lumi -m '+str(smass)+' -o impacts.json'+exvar+' &>log3.txt',
      'plotImpacts.py -i impacts.json -o impacts --transparent &>log4.txt',
      'cp -p impacts.pdf ../',
      ]
    ll=[1,1,1,1,2]
    for j,p4 in enumerate(pcall4):
      make_pcall(p4,'',ll[j])

    os.chdir(rundir)

  ############################################## NP


#def create_output_dir(webdir):
def create_output_dir():
    if not dryrun: 
        os.system('mkdir -p '+physdir)
        if os.path.islink(basedir.rstrip('/')): os.remove(basedir.rstrip('/'))
        os.symlink(mdir,basedir.rstrip('/')) #symdir
        make_print( '### output dir '+physdir+' and symlink created.' , 0)

        print 'XXXX',physdir,mdir,basedir.rstrip('/')

#        make_dir(webdir.replace(symdir.rstrip('/'),mdir))
#        if os.path.islink(webdir): 
#            os.remove(webdir)
#        os.symlink(mdir,webdir)

def make_dir(d,msg=''):
    if not msg=='':
        make_print( '### '+msg )

    if not os.path.exists(d):
        make_print( ' >> mkdir -p '+d )
        os.makedirs(d)

def make_print(msg,level=1):
    global logf
    if not 'logf' in globals():
        logf = open(logfile, 'a')

    if level <= loglevel:
        print msg

    logf.write(msg+'\n')

def print_file(text,fname,mode='w'):
    f = open(fname, mode)
    f.write(text)
    f.close()

def make_pcall(pcall,msg='',level=1,rep=0):
    if rep==0 and not msg=='': 
        make_print( '### '+msg )
    make_print( ' >> '+pcall.replace(basedir,'') , level )

    if not dryrun: os.system(pcall)

if __name__ == '__main__':
  main(sys.argv[1:])




#combineTool.py -M T2W -o "ws.root" -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO '"map=^.*/ggH.?$:r_ggH[0,0,200]"' --PO '"map=^.*/bbH$:r_bbH[0,0,200]"' -i output/mssm_201017_scale-bbb/* --X-nuisance-function 'CMS_htt_.*bin_[0-9]+' '"expr::lumisyst(\"1/sqrt(@0)\",lumiscale[1])"' &> output/mssm_201017_scale-bbb/log_ws.txt
#combineTool.py -M T2W -o "ws.root" -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO '"map=^.*/ggH.?$:r_ggH[0,0,200]"' --PO '"map=^.*/bbH$:r_bbH[0,0,200]"' -i output/mssm_201017_scale-all/* --X-nuisance-function 'CMS_+' '"expr::lumisyst(\"1/sqrt(@0)\",lumiscale[1])"' --X-nuisance-function 'lumi_+' '"expr::lumisyst(\"1/sqrt(@0)\",lumiscale[1])"' &> output/mssm_201017_scale-all/log_ws.txt
