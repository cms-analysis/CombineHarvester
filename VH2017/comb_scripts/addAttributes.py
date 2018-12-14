import ROOT
import json
import argparse
import re
import pprint

parser = argparse.ArgumentParser()
parser.add_argument( '-i', '--input', help='Input workspace')
parser.add_argument( '--json', help='json file containing attribute maps')
parser.add_argument( '--fixRanges', action='store_true', help='remove ranges where possible')
parser.add_argument( '-o', '--output', help='output workspace')
parser.add_argument( '--freezeGroups', help='comma separated list of groups to freeze')

args = parser.parse_args()

ROOT.gSystem.Load('libHiggsAnalysisCombinedLimit')

freeze_groups = set()
if args.freezeGroups is not None:
    for arg in args.freezeGroups.split(','):
        freeze_groups.add(arg)

groups = {}
with open(args.json) as jsonfile:
    groups = json.load(jsonfile)

print groups
fin = ROOT.TFile(args.input)
w = fin.Get('w')

mc = w.genobj("ModelConfig")

# allvars = w.allVars()
allvars = mc.GetNuisanceParameters()
it = allvars.createIterator()
var = it.Next()

result = {}

while var:
    # print var.GetName()
    if not var.isConstant():
        result[var.GetName()] = list()
        for grp in groups:
            for pattern in groups[grp]:
                if re.match(pattern+'$', var.GetName()):
                    result[var.GetName()].append(str(grp))
                    print 'Adding attribute "%s" to parameter "%s" matching pattern "%s"' % (grp, var.GetName(), pattern)
                    var.setAttribute(grp)
                    if grp in freeze_groups:
                        var.setConstant(True)
                        print 'Setting parameter %s constant' % (var.GetName())
                    break
    var = it.Next()

pprint.pprint(result, indent=4)


if args.fixRanges:
    newErrors = {
        'CMS_hww_DYttnorm0j': 0.06,
        'CMS_hww_DYttnorm1j': 0.05,
        'CMS_hww_DYttnorm2j': 0.1,
        'CMS_hww_DYttnormvbf': 0.17,
        'CMS_hww_DYttnormvh2j': 0.13,
        'CMS_hww_Topnorm0j': 0.05,
        'CMS_hww_Topnorm0jsf': 0.05,
        'CMS_hww_Topnorm1j': 0.1,
        'CMS_hww_Topnorm1jsf': 0.03,
        'CMS_hww_Topnorm2j': 0.1,
        'CMS_hww_Topnormvbf': 0.05,
        'CMS_hww_Topnormvh2j': 0.03,
        'CMS_hww_WWnorm0j': 0.1,
        'CMS_hww_WWnorm0jsf': 0.10,
        'CMS_hww_WWnorm1j': 0.1,
        'CMS_hww_WWnorm1jsf': 0.2,
        'CMS_hww_WWnorm2j': 0.1,
        'CMS_hww_WWnormvbf': 0.5,
        'CMS_hww_WWnormvh2j': 0.5,
        'CMS_hww_WZ3lnorm': 0.5,
        'CMS_hww_ZZ4lnorm': 0.07,
        'CMS_hww_Zg3lnorm': 0.15,
        'SF_TT_norm_high_Zll': 0.04,
        'SF_TT_norm_low_Zll': 0.05,
        'SF_Zj0b_norm_high_Zll': 0.05,
        'SF_Zj0b_norm_low_Zll': 0.06,
        'SF_Zj1b_norm_high_Zll': 0.1,
        'SF_Zj1b_norm_low_Zll': 0.06,
        'SF_Zj2b_norm_high_Zll': 0.07,
        'SF_Zj2b_norm_low_Zll': 0.06,
        'bgnorm_ddQCD_fh_j7_t3': 0.02,
        'bgnorm_ddQCD_fh_j7_t4': 0.02,
        'bgnorm_ddQCD_fh_j8_t3': 0.02,
        'bgnorm_ddQCD_fh_j8_t4': 0.02,
        'bgnorm_ddQCD_fh_j9_t3': 0.02,
        'bgnorm_ddQCD_fh_j9_t4': 0.02,
        'model_mu_cat_vbf_qcd_zjets_bin_0': 57.0164,
        'model_mu_cat_vbf_qcd_zjets_bin_1': 43.2539,
        'model_mu_cat_vbf_qcd_zjets_bin_2': 35.0569,
        'model_mu_cat_vbf_qcd_zjets_bin_3': 21.6465,
        'model_mu_cat_vbf_qcd_zjets_bin_4': 13.4286,
        'model_mu_cat_vbf_qcd_zjets_bin_5': 10.5568,
        'model_mu_cat_vbf_qcd_zjets_bin_6': 6.33966,
        'model_mu_cat_vbf_qcd_zjets_bin_7': 1.93791,
        'model_mu_cat_vbf_qcd_zjets_bin_8': 1.04446
    }

    allvars = mc.GetPdf().getParameters(mc.GetObservables())

    problemVars = []

    it = allvars.createIterator()
    var = it.Next()
    while var:
        if (not var.isConstant()) and var.InheritsFrom("RooRealVar"):
            if var.getAttribute("optimizeBounds"):
                var.Print()
                var.removeRange()
                var.setError(1.0)
                var.setAttribute("optimizeBounds", False)
                var.Print()
            elif not (var.hasMin() and var.hasMax()) and var.getError() == 0.:
                print 'Var %s has no range and no error' % var.GetName()
                var.Print()
                if var.GetName() in newErrors:
                    var.setError(newErrors[var.GetName()])
                    print 'Will set error to %f' % var.getError()
                    var.Print()
                else:
                    problemVars.append(var.GetName())
            else:
                print 'Something else:'
                var.Print()

        var = it.Next()

    pprint.pprint(problemVars, indent=4)

w.writeToFile(args.output)
