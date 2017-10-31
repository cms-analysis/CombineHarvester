import ROOT
from array import array
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', help='input file')
parser.add_argument('-l', help='output label')
parser.add_argument('--POI', help='POI to scan')
parser.add_argument('--range', type=float, help='scan range')
parser.add_argument(
    '--saveInactivePOI', action='store_true',
    help='save other param values in tree')
parser.add_argument('-p', type=int, help='scan points')
parser.add_argument('-t', help='type', default=None)
args = parser.parse_args()

ROOT.gSystem.Load('libHiggsAnalysisCombinedLimit')

fin = ROOT.TFile(args.i)
POI = args.POI
type = args.t
if type is None:
    type = 'Default'

w = fin.Get('w')
# w.Print()

pdf = w.function('nll')
#data = w.data('global_obs')

wfinal = w


def doKappa_g(wsp,
              k_t='kappa_t',
              k_b='kappa_b'):
    kappa_g = '1.06*@0*@0 + 0.01*@1*@1 - 0.07*@0*@1'
    wsp.factory('expr::kappa_g("sqrt(%s)",%s)' % (kappa_g, ','.join([k_t, k_b])))


def doKappa_gam(wsp,
                k_W='kappa_W',
                k_t='kappa_t'):
    kappa_gam = '1.59*@0*@0 + 0.07*@1*@1 - 0.66*@0*@1'
    wsp.factory('expr::kappa_gam("sqrt(%s)",%s)' %
                (kappa_gam, ','.join([k_W, k_t])))


def doKappaH(wsp,
             k_b='kappa_b',
             k_W='kappa_W',
             k_tau='kappa_tau',
             k_Z='kappa_Z',
             k_t='kappa_t',
             k_g='kappa_g',
             k_gam='kappa_gam'):
    kappaHscale = ('0.57*@0*@0 + 0.22*@1*@1 + 0.06*@2*@2 + 0.03*@3*@3 + '
                   '0.03*@4*@4 + 0.0016 + 0.0001*@5*@5 + 0.00022*@6*@6 + '
                   '0.09*@7*@7 + 0.0023*@8*@8')
    wsp.factory('expr::kappa_H("sqrt(%s)",%s)' % (
        kappaHscale,
        ','.join([k_b, k_W, k_tau, k_Z, k_t, k_b, k_tau, k_g, k_gam])))


# K1 --> K3
if type == 'K1toK3':
    kV = 'kappa_V'
    kF = 'kappa_F'
    wnew = ROOT.RooWorkspace()
    wnew.factory('%s[1,0.0,2.0]' % kV)
    wnew.factory('%s[1,0.0,2.0]' % kF)
    wnew.factory('expr::kappa_t("@0",kappa_F)')
    wnew.factory('expr::kappa_W("@0",kappa_V)')
    wnew.factory('expr::kappa_Z("@0",kappa_V)')
    wnew.factory('expr::kappa_b("@0",kappa_F)')
    wnew.factory('expr::kappa_tau("@0",kappa_F)')
    getattr(wnew, 'import')(pdf, ROOT.RooFit.RecycleConflictNodes())
    pdf = wnew.pdf('pdf')
    pdf.Print('tree')
    wfinal = wnew

# K2 --> K3
if type == 'K2toK3':
    kV = 'kappa_V'
    kF = 'kappa_F'
    wnew = ROOT.RooWorkspace()
    wnew.factory('%s[1,0.0,2.0]' % kV)
    wnew.factory('%s[1,0.0,2.0]' % kF)
    wnew.factory('expr::kappa_t("@0",kappa_F)')
    wnew.factory('expr::kappa_W("@0",kappa_V)')
    wnew.factory('expr::kappa_Z("@0",kappa_V)')
    wnew.factory('expr::kappa_b("@0",kappa_F)')
    wnew.factory('expr::kappa_tau("@0",kappa_F)')
    doKappa_g(wnew, k_t=kF, k_b=kF)
    doKappa_gam(wnew, k_W=kV, k_t=kF)
    getattr(wnew, 'import')(pdf, ROOT.RooFit.RecycleConflictNodes())
    pdf = wnew.pdf('pdf')
    pdf.Print('tree')
    wfinal = wnew

# L1 --> K1
if type == 'L1toK1':
    k_t = 'kappa_t'
    k_b = 'kappa_b'
    k_W = 'kappa_W'
    k_Z = 'kappa_Z'
    k_tau = 'kappa_tau'
    kappas = [k_t, k_b, k_W, k_Z, k_tau]
    wnew = ROOT.RooWorkspace()
    for k in kappas:
        wnew.factory('%s[1,0.0,2.0]' % k)
    doKappa_g(wnew)
    doKappa_gam(wnew)
    doKappaH(wnew)
    wnew.function('kappa_H').Print()
    wnew.factory('expr::kappa_gZ("@0*@1/@2",kappa_g, kappa_Z, kappa_H)')
    wnew.factory('expr::lambda_WZ("@0/@1",kappa_W, kappa_Z)')
    wnew.factory('expr::lambda_Zg("@0/@1",kappa_Z, kappa_g)')
    wnew.factory('expr::lambda_bZ("@0/@1",kappa_b, kappa_Z)')
    wnew.factory('expr::lambda_gamZ("@0/@1",kappa_gam, kappa_Z)')
    wnew.factory('expr::lambda_tauZ("@0/@1",kappa_tau, kappa_Z)')
    wnew.factory('expr::lambda_tg("@0/@1",kappa_t, kappa_g)')
    getattr(wnew, 'import')(pdf, ROOT.RooFit.RecycleConflictNodes())
    pdf = wnew.pdf('pdf')
    pdf.Print('tree')
    wfinal = wnew

# L1 --> K2
if type == 'L1toK2':
    k_t = 'kappa_t'
    k_b = 'kappa_b'
    k_W = 'kappa_W'
    k_Z = 'kappa_Z'
    k_tau = 'kappa_tau'
    k_g = 'kappa_g'
    k_gam = 'kappa_gam'
    kappas = [k_t, k_b, k_W, k_Z, k_tau, k_g, k_gam]
    wnew = ROOT.RooWorkspace()
    for k in kappas:
        wnew.factory('%s[1,0.0,3.0]' % k)
    doKappaH(wnew)
    wnew.function('kappa_H').Print()
    wnew.factory('expr::kappa_gZ("@0*@1/@2",kappa_g, kappa_Z, kappa_H)')
    wnew.factory('expr::lambda_WZ("@0/@1",kappa_W, kappa_Z)')
    wnew.factory('expr::lambda_Zg("@0/@1",kappa_Z, kappa_g)')
    wnew.factory('expr::lambda_bZ("@0/@1",kappa_b, kappa_Z)')
    wnew.factory('expr::lambda_gamZ("@0/@1",kappa_gam, kappa_Z)')
    wnew.factory('expr::lambda_tauZ("@0/@1",kappa_tau, kappa_Z)')
    wnew.factory('expr::lambda_tg("@0/@1",kappa_t, kappa_g)')
    getattr(wnew, 'import')(pdf, ROOT.RooFit.RecycleConflictNodes())
    pdf = wnew.pdf('pdf')
    pdf.Print('tree')
    wfinal = wnew

# L1 --> K3
if type == 'L1toK3':
    kV = 'kappa_V'
    kF = 'kappa_F'
    wnew = ROOT.RooWorkspace()
    wnew.factory('%s[1,0.0,2.0]' % kV)
    wnew.factory('%s[1,0.0,2.0]' % kF)
    doKappa_g(wnew, k_t=kF, k_b=kF)
    doKappa_gam(wnew, k_W=kV, k_t=kF)
    doKappaH(wnew, k_b=kF, k_W=kV, k_tau=kF, k_Z=kV, k_t=kF)
    wnew.function('kappa_H').Print()
    wnew.factory('expr::kappa_gZ("@0*@1/@2",kappa_g, kappa_V, kappa_H)')
    wnew.factory('expr::lambda_WZ("@0/@1",kappa_V, kappa_V)')
    wnew.factory('expr::lambda_Zg("@0/@1",kappa_V, kappa_g)')
    wnew.factory('expr::lambda_bZ("@0/@1",kappa_F, kappa_V)')
    wnew.factory('expr::lambda_gamZ("@0/@1",kappa_gam, kappa_V)')
    wnew.factory('expr::lambda_tauZ("@0/@1",kappa_F, kappa_V)')
    wnew.factory('expr::lambda_tg("@0/@1",kappa_F, kappa_g)')
    getattr(wnew, 'import')(pdf, ROOT.RooFit.RecycleConflictNodes())
    pdf = wnew.pdf('pdf')
    pdf.Print('tree')
    wfinal = wnew

# B1ZZ_TH --> A1_mu
if type == 'B1ZZ_THtoA1_mu':
    wnew = ROOT.RooWorkspace()
    wnew.factory('mu[1,0.0,2.0]')
    wnew.factory('expr::mu_XS_ggF_x_BR_ZZ("@0", mu)')
    wnew.factory('mu_XS_VBF_r_XS_ggF[1]')
    wnew.factory('mu_XS_WH_r_XS_ggF[1]')
    wnew.factory('mu_XS_ZH_r_XS_ggF[1]')
    wnew.factory('mu_XS_ttH_r_XS_ggF[1]')
    wnew.factory('mu_BR_WW_r_BR_ZZ[1]')
    wnew.factory('mu_BR_bb_r_BR_ZZ[1]')
    wnew.factory('mu_BR_gamgam_r_BR_ZZ[1]')
    wnew.factory('mu_BR_tautau_r_BR_ZZ[1]')
    getattr(wnew, 'import')(pdf, ROOT.RooFit.RecycleConflictNodes())
    pdf = wnew.function('nll')
    pdf.Print('tree')
    wfinal = wnew

# B1ZZ_TH --> A1_5D
if type == 'B1ZZ_THtoA1_5D':
    wnew = ROOT.RooWorkspace()
    for P in ['mu_BR_WW', 'mu_BR_ZZ', 'mu_BR_bb', 'mu_BR_gamgam', 'mu_BR_tautau']:
        wnew.factory('%s[1,-10.0,10.0]' % P)
    wnew.factory('expr::mu_XS_ggF_x_BR_ZZ("@0", mu_BR_ZZ)')
    wnew.factory('mu_XS_VBF_r_XS_ggF[1]')
    wnew.factory('mu_XS_WH_r_XS_ggF[1]')
    wnew.factory('mu_XS_ZH_r_XS_ggF[1]')
    wnew.factory('mu_XS_ttH_r_XS_ggF[1]')
    wnew.factory('expr::mu_BR_WW_r_BR_ZZ("@0/@1", mu_BR_WW, mu_BR_ZZ)')
    wnew.factory('expr::mu_BR_bb_r_BR_ZZ("@0/@1", mu_BR_bb, mu_BR_ZZ)')
    wnew.factory('expr::mu_BR_gamgam_r_BR_ZZ("@0/@1", mu_BR_gamgam, mu_BR_ZZ)')
    wnew.factory('expr::mu_BR_tautau_r_BR_ZZ("@0/@1", mu_BR_tautau, mu_BR_ZZ)')
    getattr(wnew, 'import')(pdf, ROOT.RooFit.RecycleConflictNodes())
    pdf = wnew.pdf('pdf')
    pdf.Print('tree')
    wfinal = wnew

# B1ZZ_TH --> A1_5P
if type == 'B1ZZ_THtoA1_5P':
    wnew = ROOT.RooWorkspace()
    for P in ['mu_XS_ggFbbH', 'mu_XS_VBF', 'mu_XS_WH', 'mu_XS_ZH', 'mu_XS_ttHtH']:
        wnew.factory('%s[1,-10.0,10.0]' % P)
    wnew.factory('expr::mu_XS_ggF_x_BR_ZZ("@0", mu_XS_ggFbbH)')
    wnew.factory('expr::mu_XS_VBF_r_XS_ggF("@0/@1", mu_XS_VBF, mu_XS_ggFbbH)')
    wnew.factory('expr::mu_XS_WH_r_XS_ggF("@0/@1", mu_XS_WH, mu_XS_ggFbbH)')
    wnew.factory('expr::mu_XS_ZH_r_XS_ggF("@0/@1", mu_XS_ZH, mu_XS_ggFbbH)')
    wnew.factory('expr::mu_XS_ttH_r_XS_ggF("@0/@1", mu_XS_ttHtH, mu_XS_ggFbbH)')
    wnew.factory('mu_BR_WW_r_BR_ZZ[1]')
    wnew.factory('mu_BR_bb_r_BR_ZZ[1]')
    wnew.factory('mu_BR_gamgam_r_BR_ZZ[1]')
    wnew.factory('mu_BR_tautau_r_BR_ZZ[1]')
    getattr(wnew, 'import')(pdf, ROOT.RooFit.RecycleConflictNodes())
    pdf = wnew.pdf('pdf')
    pdf.Print('tree')
    wfinal = wnew

# B1ZZ_TH --> B1WW_TH
if type == 'B1ZZ_THtoB1WW_TH':
    wnew = ROOT.RooWorkspace()
    for P in ['mu_XS_ggF_x_BR_WW', 'mu_XS_VBF_r_XS_ggF', 'mu_XS_ttH_r_XS_ggF', 'mu_XS_WH_r_XS_ggF', 'mu_XS_ZH_r_XS_ggF', 'mu_BR_tautau_r_BR_WW', 'mu_BR_bb_r_BR_WW', 'mu_BR_gamgam_r_BR_WW', 'mu_BR_ZZ_r_BR_WW']:
        wnew.factory('%s[1,-10.0,10.0]' % P)
    wnew.factory(
        'expr::mu_XS_ggF_x_BR_ZZ("@0*@1", mu_XS_ggF_x_BR_WW, mu_BR_ZZ_r_BR_WW)')
    wnew.factory('expr::mu_BR_WW_r_BR_ZZ("1/@0", mu_BR_ZZ_r_BR_WW)')
    wnew.factory(
        'expr::mu_BR_bb_r_BR_ZZ("@0/@1", mu_BR_bb_r_BR_WW, mu_BR_ZZ_r_BR_WW)')
    wnew.factory(
        'expr::mu_BR_gamgam_r_BR_ZZ("@0/@1", mu_BR_gamgam_r_BR_WW, mu_BR_ZZ_r_BR_WW)')
    wnew.factory(
        'expr::mu_BR_tautau_r_BR_ZZ("@0/@1", mu_BR_tautau_r_BR_WW, mu_BR_ZZ_r_BR_WW)')
    getattr(wnew, 'import')(pdf, ROOT.RooFit.RecycleConflictNodes())
    pdf = wnew.pdf('pdf')
    pdf.Print('tree')
    wfinal = wnew

# A1_5PD --> A1_mu
if type == 'A1_5PDtoA1_mu':
    wnew = ROOT.RooWorkspace()
    wnew.factory('mu[1,0.0,2.0]')
    for P in ['ggFbbH', 'VBF', 'WH', 'ZH', 'ttHtH']:
        for D in ['WW', 'ZZ', 'gamgam', 'tautau', 'bb']:
            wnew.factory('expr::mu_XS_%s_BR_%s("@0", mu)' % (P, D))
    getattr(wnew, 'import')(pdf, ROOT.RooFit.RecycleConflictNodes())
    pdf = wnew.pdf('pdf')
    pdf.Print('tree')
    wfinal = wnew

# A1_5PD --> A1_5P
if type == 'A1_5PDtoA1_5P':
    wnew = ROOT.RooWorkspace()
    for P in ['mu_XS_ggFbbH', 'mu_XS_VBF', 'mu_XS_WH', 'mu_XS_ZH', 'mu_XS_ttHtH']:
        wnew.factory('%s[1,-10.0,10.0]' % P)
    for P in ['ggFbbH', 'VBF', 'WH', 'ZH', 'ttHtH']:
        for D in ['WW', 'ZZ', 'gamgam', 'tautau', 'bb']:
            wnew.factory('expr::mu_XS_%s_BR_%s("@0", mu_XS_%s)' % (P, D, P))
    getattr(wnew, 'import')(pdf, ROOT.RooFit.RecycleConflictNodes())
    pdf = wnew.pdf('pdf')
    pdf.Print('tree')
    wfinal = wnew

if type == 'A1_5PDtoA1_4P':
    wnew = ROOT.RooWorkspace()
    for P in ['mu_XS_ggFbbH', 'mu_XS_VBF', 'mu_XS_VH', 'mu_XS_ttHtH']:
        wnew.factory('%s[1,-10.0,10.0]' % P)
    for P in ['ggFbbH', 'VBF', 'WH', 'ZH', 'ttHtH']:
        for D in ['WW', 'ZZ', 'gamgam', 'tautau', 'bb']:
            PX = P
            if P in ['WH', 'ZH']:
                PX = 'VH'
            wnew.factory('expr::mu_XS_%s_BR_%s("@0", mu_XS_%s)' % (P, D, PX))
    getattr(wnew, 'import')(pdf, ROOT.RooFit.RecycleConflictNodes())
    pdf = wnew.pdf('pdf')
    pdf.Print('tree')
    wfinal = wnew

# A1_5PD --> A1_5D
if type == 'A1_5PDtoA1_5D':
    wnew = ROOT.RooWorkspace()
    # for D in ['mu_BR_WW']:
    for D in ['mu_BR_WW', 'mu_BR_ZZ', 'mu_BR_bb', 'mu_BR_gamgam', 'mu_BR_tautau']:
        wnew.factory('%s[1,-10.0,10.0]' % D)
    for P in ['ggFbbH', 'VBF', 'WH', 'ZH', 'ttHtH']:
        # for D in ['WW']:
        for D in ['WW', 'tautau', 'ZZ', 'bb', 'gamgam']:
            wnew.factory('expr::mu_XS_%s_BR_%s("@0", mu_BR_%s)' % (P, D, D))
    getattr(wnew, 'import')(pdf, ROOT.RooFit.RecycleConflictNodes())
    pdf = wnew.pdf('pdf')
    # pdf.Print('tree')
    wfinal = wnew

#nll = pdf.createNLL(data)
nll = pdf

minim = ROOT.RooMinimizer(nll)
minim.setVerbose(False)
minim.minimize('Minuit2', 'migrad')
minim.setPrintLevel(-1)
wfinal.allFunctions().Print('v')
wfinal.allVars().Print('v')

nll0 = nll.getVal()

param = wfinal.var(POI)
param.setConstant()

# Figure out the other floating parameters
params = pdf.getParameters(ROOT.RooArgSet())
param_it = params.createIterator()
var = param_it.Next()
float_params = set()
snapshot = {}
while var:
    if not var.isConstant():
        float_params.add(var.GetName())
        snapshot[var.GetName()] = var.getVal()
    var = param_it.Next()

fit_range = args.range
points = args.p

r_min = max(param.getVal() - fit_range, param.getMin())
r_max = min(param.getVal() + fit_range, param.getMax())
width = (r_max - r_min) / points

r = r_min + 0.5 * width

fout = ROOT.TFile('scan_covariance_%s_%s_%s.root' %
                  (args.l, type, POI), 'RECREATE')
tout = ROOT.TTree('limit', 'limit')

a_r = array('f', [param.getVal()])
a_deltaNLL = array('f', [0])
a_quantileExpected = array('f', [1])

float_arrs = []
for var in float_params:
    float_arrs.append(array('f', [0.]))
    tout.Branch(var, float_arrs[-1], '%s/f' % var)

tout.Branch(POI, a_r, '%s/f' % POI)
tout.Branch('deltaNLL', a_deltaNLL, 'deltaNLL/f')
tout.Branch('quantileExpected', a_quantileExpected, 'quantileExpected/f')

for i, var in enumerate(float_params):
    float_arrs[i][0] = wfinal.var(var).getVal()
tout.Fill()

for p in xrange(points):
    for key,val in snapshot.iteritems():
      wfinal.var(key).setVal(val)
    param.setVal(r)
    a_r[0] = r
    minim.minimize('Minuit2', 'migrad')
    #wfinal.allVars().Print('v')
    for i, var in enumerate(float_params):
        float_arrs[i][0] = wfinal.var(var).getVal()
    nllf = nll.getVal()
    print '%s = %f; nll0 = %f; nll = %f, deltaNLL = %f' % (POI, r, nll0, nllf,  nllf - nll0)
    a_deltaNLL[0] = nllf - nll0
    if a_deltaNLL[0] > 0.: tout.Fill()
    r += width

tout.Write()
fout.Close()
