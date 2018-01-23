import os
import stat
from functools import partial
from multiprocessing import Pool

DRY_RUN = False

JOB_PREFIX = """#!/bin/sh
ulimit -s unlimited
set -e
cd %(CMSSW_BASE)s/src
export SCRAM_ARCH=%(SCRAM_ARCH)s
eval `scramv1 runtime -sh`
cd %(PWD)s
""" % ({
    'CMSSW_BASE': os.environ['CMSSW_BASE'],
    'SCRAM_ARCH': os.environ['SCRAM_ARCH'],
    'PWD': os.environ['PWD']
})

CONDOR_TEMPLATE = """executable = %(EXE)s
arguments = $(ProcId)
output                = %(TASK)s.$(ClusterId).$(ProcId).out
error                 = %(TASK)s.$(ClusterId).$(ProcId).err
log                   = %(TASK)s.$(ClusterId).log

# Send the job to Held state on failure.
on_exit_hold = (ExitBySignal == True) || (ExitCode != 0)

# Periodically retry the jobs every 10 minutes, up to a maximum of 5 retries.
periodic_release =  (NumJobStarts < 3) && ((CurrentTime - EnteredCurrentStatus) > 600)

%(EXTRA)s
queue %(NUMBER)s

"""

CRAB_PREFIX = """
set -x
set -e
ulimit -s unlimited
ulimit -c 0

function error_exit
{
  if [ $1 -ne 0 ]; then
    echo "Error with exit code ${1}"
    if [ -e FrameworkJobReport.xml ]
    then
      cat << EOF > FrameworkJobReport.xml.tmp
      <FrameworkJobReport>
      <FrameworkError ExitStatus="${1}" Type="" >
      Error with exit code ${1}
      </FrameworkError>
EOF
      tail -n+2 FrameworkJobReport.xml >> FrameworkJobReport.xml.tmp
      mv FrameworkJobReport.xml.tmp FrameworkJobReport.xml
    else
      cat << EOF > FrameworkJobReport.xml
      <FrameworkJobReport>
      <FrameworkError ExitStatus="${1}" Type="" >
      Error with exit code ${1}
      </FrameworkError>
      </FrameworkJobReport>
EOF
    fi
    exit 0
  fi
}

trap 'error_exit $?' ERR
"""

CRAB_POSTFIX = """
tar -cf combine_output.tar higgsCombine*.root
rm higgsCombine*.root
"""


def run_command(dry_run, command):
    if not dry_run:
        print '>> ' + command
        return os.system(command)
    else:
        print '[DRY-RUN]: ' + command


class CombineToolBase:
    description = 'Base class that passes through all arguments to combine and handles job creation and submission'
    requires_root = False

    def __init__(self):
        self.job_queue = []
        self.args = None
        self.passthru = []
        self.job_mode = 'interactive'
        self.prefix_file = ''
        self.parallel = 1
        self.merge = 1
        self.task_name = 'combine_task'
        self.dry_run = False
        self.bopts = ''  # batch submission options
        self.custom_crab = None
        self.custom_crab_post = None
        self.add_stat_only = False
        self.add_no_thunc = False

    def attach_job_args(self, group):
        group.add_argument('--job-mode', default=self.job_mode, choices=[
                           'interactive', 'script', 'lxbatch', 'SGE', 'condor', 'crab3'], help='Task execution mode')
        group.add_argument('--prefix-file', default=self.prefix_file,
                           help='Path to file containing job prefix')
        group.add_argument('--task-name', default=self.task_name,
                           help='Task name, used for job script and log filenames for batch system tasks')
        group.add_argument('--parallel', type=int, default=self.parallel,
                           help='Number of jobs to run in parallel [only affects interactive job-mode]')
        group.add_argument('--merge', type=int, default=self.merge,
                           help='Number of jobs to run in a single script [only affects batch submission]')
        group.add_argument('--dry-run', action='store_true',
                           help='Print commands to the screen but do not run them')
        group.add_argument('--sub-opts', default=self.bopts,
                           help='Options for batch/crab submission')
        group.add_argument('--memory', type=int,
                           help='Request memory for job [MB]')
        group.add_argument('--crab-area',
                           help='crab working area')
        group.add_argument('--custom-crab', default=self.custom_crab,
                           help='python file containing a function with name signature "custom_crab(config)" that can be used to modify the default crab configuration')
        group.add_argument('--custom-crab-post', default=self.custom_crab_post,
                           help='txt file containing command lines that can be used in the crab job script instead of the defaults.')
        group.add_argument('--add-stat-only', action='store_true',
                           help="for every combine call, also call the same command adding --freezeParameters 'rgx{^.*$}'")
        group.add_argument('--add-no-thunc', action='store_true',
                           help="for every combine call, also call the same command freezing signal theory uncs (hard coded here)")

    def attach_intercept_args(self, group):
        pass

    def attach_args(self, group):
        pass

    def set_args(self, known, unknown):
        self.args = known
        self.job_mode = self.args.job_mode
        self.prefix_file = self.args.prefix_file
        self.task_name = self.args.task_name
        self.parallel = self.args.parallel
        self.merge = self.args.merge
        self.dry_run = self.args.dry_run
        self.passthru.extend(unknown)
        self.bopts = self.args.sub_opts
        self.custom_crab = self.args.custom_crab
        self.memory = self.args.memory
        self.crab_area = self.args.crab_area
        self.custom_crab_post = self.args.custom_crab_post
        self.add_stat_only = self.args.add_stat_only
        self.add_no_thunc = self.args.add_no_thunc

    def put_back_arg(self, arg_name, target_name):
        if hasattr(self.args, arg_name):
            self.passthru.extend([target_name, getattr(self.args, arg_name)])
            delattr(self.args, arg_name)

    def extract_arg(self, arg, args_str):
        args_str = args_str.replace(arg+'=', arg+' ')
        args = args_str.split()
        if arg in args:
            idx = args.index(arg)
            assert idx != -1 and idx < len(args)
            val = args[idx+1]
            del args[idx:idx+2]
            return val, (' '.join(args))
        else:
            return None, args_str

    def create_job_script(self, commands, script_filename, do_log = False):
        fname = script_filename
        logname = script_filename.replace('.sh', '.log')
        with open(fname, "w") as text_file:
            text_file.write(JOB_PREFIX)
            for i, command in enumerate(commands):
                tee = 'tee' if i == 0 else 'tee -a'
                log_part = '\n'
                if do_log: log_part = ' 2>&1 | %s ' % tee + logname + log_part
                if command.startswith('combine') or command.startswith('pushd'):
                    text_file.write(
                        'eval ' + command + log_part)
                else:
                    text_file.write(command)
        st = os.stat(fname)
        os.chmod(fname, st.st_mode | stat.S_IEXEC)
        # print JOB_PREFIX + command
        print 'Created job script: %s' % script_filename

    def run_method(self):
        print vars(self.args)
        # Put the method back in because we always take it out
        self.put_back_arg('method', '-M')
        print self.passthru
        command = 'combine ' + ' '.join(self.passthru)
        self.job_queue.append(command)
        self.flush_queue()

    def extract_workspace_arg(self, cmd_list=[]):
        for arg in ['-d', '--datacard']:
            if arg in cmd_list:
                idx = cmd_list.index(arg)
                assert idx != -1 and idx < len(cmd_list)
                return cmd_list[idx + 1]
        raise RuntimeError('The workspace argument must be specified explicity with -d or --datacard')
    def flush_queue(self):
        if self.job_mode == 'interactive':
            pool = Pool(processes=self.parallel)
            result = pool.map(
                partial(run_command, self.dry_run), self.job_queue)
        script_list = []
        if self.job_mode in ['script', 'lxbatch', 'SGE']:
            if self.prefix_file != '':
                if self.prefix_file.endswith('.txt'):
                  job_prefix_file = open(self.prefix_file,'r')
                else :
                  job_prefix_file = open(os.environ['CMSSW_BASE']+"/src/CombineHarvester/CombineTools/input/job_prefixes/job_prefix_"+self.prefix_file+".txt",'r')
                global JOB_PREFIX
                JOB_PREFIX=job_prefix_file.read() %({
                  'CMSSW_BASE': os.environ['CMSSW_BASE'],
                  'SCRAM_ARCH': os.environ['SCRAM_ARCH'],
                  'PWD': os.environ['PWD']
                })
                job_prefix_file.close()
            for i, j in enumerate(range(0, len(self.job_queue), self.merge)):
                script_name = 'job_%s_%i.sh' % (self.task_name, i)
                # each job is given a slice from the list of combine commands of length 'merge'
                # we also keep track of the files that were created in case submission to a
                # batch system was also requested
                self.create_job_script(
                    self.job_queue[j:j + self.merge], script_name, self.job_mode == 'script')
                script_list.append(script_name)
        if self.job_mode == 'lxbatch':
            for script in script_list:
                full_script = os.path.abspath(script)
                logname = full_script.replace('.sh', '_%J.log')
                run_command(self.dry_run, 'bsub -o %s %s %s' % (logname, self.bopts, full_script))
        if self.job_mode == 'SGE':
            for script in script_list:
                full_script = os.path.abspath(script)
                logname = full_script.replace('.sh', '_%J.log')
                run_command(self.dry_run, 'qsub -o %s %s %s' % (logname, self.bopts, full_script))
        if self.job_mode == 'condor':
            outscriptname = 'condor_%s.sh' % self.task_name
            subfilename = 'condor_%s.sub' % self.task_name
            print '>> condor job script will be %s' % outscriptname
            outscript = open(outscriptname, "w")
            outscript.write(JOB_PREFIX)
            jobs = 0
            wsp_files = set()
            for i, j in enumerate(range(0, len(self.job_queue), self.merge)):
                outscript.write('\nif [ $1 -eq %i ]; then\n' % jobs)
                jobs += 1
                for line in self.job_queue[j:j + self.merge]:
                    newline = line
                    outscript.write('  ' + newline + '\n')
                outscript.write('fi')
            outscript.close()
            subfile = open(subfilename, "w")
            condor_settings = CONDOR_TEMPLATE % {
              'EXE': outscriptname,
              'TASK': self.task_name,
              'EXTRA': self.bopts,
              'NUMBER': jobs
            }
            subfile.write(condor_settings)
            subfile.close()
            run_command(self.dry_run, 'condor_submit %s' % (subfilename))
 
        if self.job_mode == 'crab3':
            #import the stuff we need
            from CRABAPI.RawCommand import crabCommand
            from httplib import HTTPException
            print '>> crab3 requestName will be %s' % self.task_name
            outscriptname = 'crab_%s.sh' % self.task_name
            print '>> crab3 script will be %s' % outscriptname
            outscript = open(outscriptname, "w")
            outscript.write(CRAB_PREFIX)
            jobs = 0
            wsp_files = set()
            for i, j in enumerate(range(0, len(self.job_queue), self.merge)):
                jobs += 1
                outscript.write('\nif [ $1 -eq %i ]; then\n' % jobs)
                for line in self.job_queue[j:j + self.merge]:
                    newline = line
                    if line.startswith('combine'): newline = line.replace('combine', './combine', 1)
                    wsp = str(self.extract_workspace_arg(newline.split()))

                    newline = newline.replace(wsp, os.path.basename(wsp))
                    if wsp.startswith('root://'):
                        newline = ('./copyRemoteWorkspace.sh %s ./%s; ' % (wsp, os.path.basename(wsp))) + newline
                    else:
                        wsp_files.add(wsp)
                    outscript.write('  ' + newline + '\n')

                    if (self.add_stat_only):
                        nameOut = newline.split("-n ")[1].split(" ")[0].rstrip(".POINTS")
                        if ("freezeParameters" in newline):
                            statline = newline.replace(wsp, os.path.basename(wsp)).replace("freezeParameters ","freezeParameters 'rgx{^.*$}',") + '\n'
                            statline = statline.replace(nameOut,nameOut+".StatOnly")
                            outscript.write('  ' + statline)
                        else:
                            statline = newline.replace(wsp, os.path.basename(wsp))+ " --freezeParameters 'rgx{^.*$}'" + '\n'
                            statline = statline.replace(nameOut,nameOut+".StatOnly")
                            outscript.write('  ' + statline)
                    if (self.add_no_thunc):
                        nameOut = newline.split("-n ")[1].split(" ")[0].rstrip(".POINTS")
                        if ("freezeParameters" in newline):
                            nothline = newline.replace(wsp, os.path.basename(wsp)).replace("freezeParameters ","freezeParameters 'rgx{.*THU.*}',QCDscale_qqH,QCDscale_VH,QCDscale_ggZH,QCDscale_ttH,pdf_Higgs_gg,pdf_Higgs_qqbar,pdf_Higgs_qg,CMS_vhbb_boost_EWK_13TeV,CMS_vhbb_boost_QCD_13TeV,QCDscale_VH_ggZHacceptance_highPt,param_alphaS,param_mB,param_mC,param_mt,HiggsDecayWidthTHU_hqq,HiggsDecayWidthTHU_hvv,HiggsDecayWidthTHU_hll,HiggsDecayWidthTHU_hgg,HiggsDecayWidthTHU_hzg,HiggsDecayWidthTHU_hgluglu,") + '\n'
                            nothline = nothline.replace(nameOut,nameOut+".NoThUnc")
                            outscript.write('  ' + nothline)
                        else:
                            nothline = newline.replace(wsp, os.path.basename(wsp))+ " --freezeParameters 'rgx{.*THU.*}',QCDscale_qqH,QCDscale_VH,QCDscale_ggZH,QCDscale_ttH,pdf_Higgs_gg,pdf_Higgs_qqbar,pdf_Higgs_qg,CMS_vhbb_boost_EWK_13TeV,CMS_vhbb_boost_QCD_13TeV,QCDscale_VH_ggZHacceptance_highPt,param_alphaS,param_mB,param_mC,param_mt,HiggsDecayWidthTHU_hqq,HiggsDecayWidthTHU_hvv,HiggsDecayWidthTHU_hll,HiggsDecayWidthTHU_hgg,HiggsDecayWidthTHU_hzg,HiggsDecayWidthTHU_hgluglu" + '\n'
                            nothline = nothline.replace(nameOut,nameOut+".NoThUnc")
                            outscript.write('  ' + nothline)
                outscript.write('fi')
            if self.custom_crab_post is not None:
                with open(self.custom_crab_post, 'r') as postfile:
                    outscript.write(postfile.read())
            else:
                outscript.write(CRAB_POSTFIX)
            outscript.close()
            from CombineHarvester.CombineTools.combine.crab import config
            config.General.requestName = self.task_name
            config.JobType.scriptExe = outscriptname
            config.JobType.inputFiles.extend(wsp_files)
            config.Data.totalUnits = jobs
            config.Data.outputDatasetTag = config.General.requestName
            if self.memory is not None:
                config.JobType.maxMemoryMB = self.memory
            if self.crab_area is not None:
                config.General.workArea = self.crab_area
            if self.custom_crab is not None:
                d = {}
                execfile(self.custom_crab, d)
                d['custom_crab'](config)
            print config
            if not self.dry_run:
                try:
                    crabCommand('submit', config = config)
                except HTTPException, hte:
                    print hte.headers
        del self.job_queue[:]
