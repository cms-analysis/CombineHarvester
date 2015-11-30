from HiggsAnalysis.CombinedLimit.PhysicsModel import *
import os
import ROOT
import math
import itertools
import pprint
import sys

class MSSMHiggsModel(PhysicsModel):
    def __init__(self):
        PhysicsModel.__init__(self)
        self.filePrefix = ''
        self.modelFiles = {}
        self.h_dict = {}
        self.h_dict[0] = {
            'mH'  : 'h_mH',
            'mh'  : 'h_mh',
            'mHp' : 'h_mHp',
            'br_tHpb'       : 'h_brHpb_t',
            'br_Hptaunu'    : 'h_brtaunu_Hp',
            'br_Hhh'        : 'h_brh0h0_H',
            'br_AZh'        : 'h_brZh0_A'
        }
        self.h_dict[1] = {
            'mH'  : 'm_H',
            'mh'  : 'm_h',
            'mHp' : 'm_Hp',
            'br_tHpb'       : 'br_t_Hpb',
            'br_Hptaunu'    : 'br_Hp_taunu',
            'br_Hhh'        : 'br_H_hh',
            'br_AZh'        : 'br_A_Zh'
        }
        for X in ['h', 'H', 'A']:
            self.h_dict[0].update({
                'xs_gg%s'%X     : 'h_ggF_xsec_%s'%X,
                'xs_bb4f%s'%X   : 'h_bbH4f_xsec_%s'%X,
                'xs_bb5f%s'%X   : 'h_bbH_xsec_%s'%X,
                'br_%stautau'%X : 'h_brtautau_%s'%X,
                'br_%sbb'%X     : 'h_brbb_%s'%X,
                })
            self.h_dict[1].update({
                'xs_gg%s'%X     : 'xs_gg_%s'%X,
                'xs_bb4f%s'%X   : 'xs_bb4F_%s'%X,
                'xs_bb5f%s'%X   : 'xs_bb5F_%s'%X,
                'br_%stautau'%X : 'br_%s_tautau'%X,
                'br_%sbb'%X     : 'br_%s_bb'%X
                })
        # Define the known production and decay processes
        # These are strings we will look for in the process names to
        # determine the correct normalisation scaling
        self.ERAS = ['7TeV', '8TeV', '13TeV', '14TeV']
        self.PROC_SETS = []
        self.SMSignal  = "SM125" #SM signal

    def setPhysicsOptions(self,physOptions):
        for po in physOptions:
            if po.startswith('filePrefix='):
                self.filePrefix = po.replace('filePrefix=', '')
                print 'Set file prefix to: %s' % self.filePrefix
            if po.startswith('modelFiles='):
                cfgList = po.replace('modelFiles=', '').split(':')
                for cfg in cfgList:
                    cfgSplit = cfg.split(',')
                    if len(cfgSplit) != 3:
                        raise RuntimeError, 'Model file argument %s should be in the format ERA,FILE,VERSION' % cfg
                    self.modelFiles[cfgSplit[0]] = (cfgSplit[1], int(cfgSplit[2]))
                pprint.pprint(self.modelFiles)

    def setModelBuilder(self, modelBuilder):
        """We're not supposed to overload this method, but we have to because 
        this is our only chance to import things into the workspace while it
        is completely empty. This is primary so we can define some of our MSSM
        Higgs boson masses as functions instead of the free variables that would
        be imported later as dependents of the normalisation terms."""
        # First call the parent class implementation
        PhysicsModel.setModelBuilder(self, modelBuilder)
        self.buildModel()

    def doHistFunc(self, name, hist, varlist, interpolate=0):
        "method to conveniently create a RooHistFunc from a TH1/TH2 input"
        print 'Doing histFunc %s...' % name
        dh = ROOT.RooDataHist('dh_%s'%name, 'dh_%s'%name, ROOT.RooArgList(*varlist), ROOT.RooFit.Import(hist))
        hfunc = ROOT.RooHistFunc(name, name, ROOT.RooArgSet(*varlist), dh)
        hfunc.setInterpolationOrder(interpolate)
        self.modelBuilder.out._import(hfunc, ROOT.RooFit.RecycleConflictNodes())
        return self.modelBuilder.out.function(name)

    def doAsymPow(self, name, h_kappa_lo, h_kappa_hi, param, varlist):
        "create AsymPow rate scaler given two TH2 inputs corresponding to kappa_hi and kappa_lo"
        param_var = self.modelBuilder.out.var(param)
        if not param_var:
            self.modelBuilder.doVar('%s[0,-7,7]'%param)
            param_var = self.modelBuilder.out.var(param)
        print param_var
        hi = self.doHistFunc('%s_hi'%name, h_kappa_hi, varlist)
        lo = self.doHistFunc('%s_lo'%name, h_kappa_lo, varlist)
        asym = ROOT.AsymPow('systeff_%s'%name, '', lo, hi, param_var)
        self.modelBuilder.out._import(asym)
        return self.modelBuilder.out.function('systeff_%s'%name)

    def santanderMatching(self, h4f, h5f, mass = None):
        res = h4f.Clone()
        for x in xrange(1, h4f.GetNbinsX() + 1):
            for y in xrange(1, h4f.GetNbinsY() +1):
               mh = h4f.GetXaxis().GetBinCenter(x) if mass is None else mass.GetBinContent(x, y)
               if mh <= 0:
                    print 'santanderMatching: Have mh = %f at (%f,%f), using h4f value' % (mh,  h4f.GetXaxis().GetBinCenter(x),  h4f.GetYaxis().GetBinCenter(y))
                    res.SetBinContent(x, y, h4f.GetBinContent(x, y))
               else:
                    t = math.log(mh / 4.92) - 2.
                    fourflav = h4f.GetBinContent(x, y)
                    fiveflav = h5f.GetBinContent(x, y)
                    sigma = (1. / (1. + t)) * (fourflav + t * fiveflav)
                    res.SetBinContent(x, y, sigma)
        return res

    def safeTH2DivideForKappa(self, h1, h2):
        """Divides two TH2s taking care of exceptions like divide by zero
        and potentially doing more checks in the future"""
        res = h1.Clone()
        for x in xrange(1, h1.GetNbinsX() + 1):
            for y in xrange(1, h2.GetNbinsY() +1):
                val_h1 = h1.GetBinContent(x, y)
                val_h2 = h2.GetBinContent(x, y)
                if val_h1 == 0. or val_h2 == 0.:
                    print ('Warning: dividing histograms %s and %s at bin (%i,%i)=(%g, %g) '
                           'with values: %g/%g, will set the kappa to 1.0 here' % (
                                h1.GetName(), h2.GetName(), x, y, h1.GetXaxis().GetBinCenter(x),
                                h1.GetYaxis().GetBinCenter(y), val_h1, val_h2
                            ))
                    new_val = 1.
                else:
                    new_val = val_h1 / val_h2
                res.SetBinContent(x, y, new_val)
        return res
        
    def buildModel(self):
        # It's best not to set ranges for the model parameters here.
        # RooFit will create them automatically from the x- and y-axis
        # ranges of the input histograms
        mA = ROOT.RooRealVar('mA', 'mA', 120.)
        tanb = ROOT.RooRealVar('tanb', 'tanb', 20.)
        pars = [mA, tanb]
        #  ggF_xsec_h_scale_hi_str = "xs_gg_h_scaleUp"
        #  ggF_xsec_h_scale_lo_str = "xs_gg_h_scaleDown"
        #  ggF_xsec_h_scale_hi_str = "h_ggF_xsec05_h"
        #  ggF_xsec_h_scale_lo_str = "h_ggF_xsec20_h"
        doneMasses = False

        for era, (file, version) in self.modelFiles.iteritems():
            hd = self.h_dict[version]
            f = ROOT.TFile(self.filePrefix + file)

            # We take the masses from the 1st model file, under the
            # assumption that they are the same in all model files
            if not doneMasses:
                self.doHistFunc('mH', f.Get(hd['mH']), pars)
                self.doHistFunc('mh', f.Get(hd['mh']), pars)
                self.doHistFunc('mHp', f.Get(hd['mHp']), pars)
                doneMasses = True

            # Do the xsecs and BRs for the three neutral Higgs bosons
            for X in ['h', 'H', 'A']:
                self.doHistFunc('xs_gg%s_%s' % (X, era), f.Get(hd['xs_gg%s'%X]), pars)
                # Build the Santander-matched bbX cross section. The matching depends
                # on the mass of the Higgs boson in question, so for the h and H we
                # pass the mh or mH TH2 as an additional argument
                self.doHistFunc('xs_bb%s_%s' % (X, era), self.santanderMatching(
                    f.Get(hd['xs_bb4f%s'%X]),
                    f.Get(hd['xs_bb5f%s'%X]),
                    None if X=='A' else f.Get(hd['m%s'%X])), pars)
                self.doHistFunc('br_%stautau_%s' % (X, era), f.Get(hd['br_%stautau'%X]), pars)
                self.doHistFunc('br_%sbb_%s' % (X, era), f.Get(hd['br_%sbb'%X]), pars)
                # Make a note of what we've built, will be used to create scaling expressions later
                self.PROC_SETS.append(([ 'gg%s'%X, 'bb%s'%X ], [ '%stautau'%X, '%sbb'%X], [era])
            )
            # Do the BRs for the charged Higgs
            self.doHistFunc('br_tHpb_%s'%era, f.Get(hd['br_tHpb']), pars)
            self.doHistFunc('br_Hptaunu_%s'%era, f.Get(hd['br_Hptaunu']), pars)
            self.PROC_SETS.append((['tt'], ['HptaunubHptaunub', 'HptaunubWb', 'WbWb'], [era]))
            # And the extra term we need for H->hh
            self.doHistFunc('br_Hhh_%s'%era, f.Get(hd['br_Hhh']), pars)
            self.PROC_SETS.append((['ggH'], ['Hhhbbtautau'], [era]))
            # And the extra term we need for A->Zh
            self.doHistFunc('br_AZh_%s'%era, f.Get(hd['br_AZh']), pars)
            self.PROC_SETS.append((['ggA'], ['AZhLLtautau'], [era]))
            # And the SM terms
            for X in ['ggH', 'qqH', 'VH']:
                self.PROC_SETS.append((['%s'%X], ['SM125'], [era]))

        # h_ggF_xsec_h_scale_hi = self.safeTH2DivideForKappa(f.Get(ggF_xsec_h_scale_hi_str), f.Get(ggF_xsec_h_str))
        # h_ggF_xsec_h_scale_lo = self.safeTH2DivideForKappa(f.Get(ggF_xsec_h_scale_lo_str), f.Get(ggF_xsec_h_str))
        # ggF_xsec_h_scale = self.doAsymPow('systeff_ggF_xsec_h_scale_8TeV', h_ggF_xsec_h_scale_lo, h_ggF_xsec_h_scale_hi, 'ggF_xsec_h_scale_8TeV', [mA, tanb])
        # ftest = ROOT.TFile('model_debug.root', 'RECREATE')
        # ftest.WriteTObject(h_ggF_xsec_h_scale_hi, 'h_ggF_xsec_h_scale_hi')
        # ftest.WriteTObject(h_ggF_xsec_h_scale_lo, 'h_ggF_xsec_h_scale_lo')
        # ftest.Close()

    # def preProcessNuisances(self,nuisances):
    #     nuisances.append(("ggF_xsec_h_scale_8TeV",False, "param", [ "0", "1"], [] ) )

    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""
        self.modelBuilder.doVar("r[1,0,20]")

        #MSSMvsMS
        self.modelBuilder.doVar("x[1,0,1]")
        self.modelBuilder.factory_("expr::not_x(\"(1-@0)\", x)")
        self.sigNorms = { True:'x', False:'not_x' }

        self.modelBuilder.doSet('POI', 'x,r')
        # We don't intend on actually floating these in any fits...
        self.modelBuilder.out.var('mA').setConstant(True)
        self.modelBuilder.out.var('tanb').setConstant(True)

        # Build the intermediate terms for charged Higgs scaling
        for E in self.modelFiles:
            self.modelBuilder.doVar('xs_tt_%s[1.0]' % E)
            self.modelBuilder.factory_('expr::br_HptaunubHptaunub_%s("@0*@0*@1*@1", br_tHpb_%s,br_Hptaunu_%s)' % (E,E,E))
            self.modelBuilder.factory_('expr::br_HptaunubWb_%s("2 * (1-@0)*@0*@1", br_tHpb_%s,br_Hptaunu_%s)' % (E,E,E))
            self.modelBuilder.factory_('expr::br_WbWb_%s("(1-@0)*(1-@0)", br_tHpb_%s)' % (E,E))

        # Build the intermediate terms for H->hh->bbtautau and A->Zh->LLtautau scaling
        for E in self.modelFiles:
            self.modelBuilder.factory_('expr::br_Hhhbbtautau_%s("2*@0*@1*@2", br_Hhh_%s,br_htautau_%s,br_hbb_%s)' % (E,E,E,E))
            self.modelBuilder.factory_('expr::br_AZhLLtautau_%s("0.10099*@0*@1", br_AZh_%s,br_htautau_%s)' % (E,E,E))

        for proc_set in self.PROC_SETS:
            for (P, D, E) in itertools.product(*proc_set):
                # print (P, D, E)
                if ((self.SMSignal not in D) and ("ww125" not in P) and ("tt125" not in P)): #altenative hypothesis if SMSignal not in process name
                    terms = ['xs_%s_%s' % (P, E), 'br_%s_%s'% (D, E)]
                    terms += ['r']
                    terms += [self.sigNorms[1]]
                else:
                    terms = [self.sigNorms[0]]
                self.modelBuilder.factory_('prod::scaling_%s_%s_%s(%s)' % (P,D,E,','.join(terms)))
                self.modelBuilder.out.function('scaling_%s_%s_%s' % (P,D,E)).Print('')


    def getHiggsProdDecMode(self, bin, process):
        """Return a triple of (production, decay, energy)"""
        P = ''
        D = ''
        if "_" in process: 
            (P, D) = process.split("_")
        else:
            raise RuntimeError, 'Expected signal process %s to be of the form PROD_DECAY' % process
        E = None
        for era in self.ERAS:
            if era in bin:
                if E: raise RuntimeError, "Validation Error: bin string %s contains multiple known energies" % bin
                E = era
        if not E:
                raise RuntimeError, 'Did not find a valid energy in bin string %s' % bin
        return (P, D, E)
        
    def getYieldScale(self,bin,process):
        if self.DC.isSignal[process]:
            (P, D, E) = self.getHiggsProdDecMode(bin, process)
            scaling = 'scaling_%s_%s_%s' % (P, D, E)
            print 'Scaling %s/%s as %s' % (bin, process, scaling)
            return scaling
        else:
            return 1


MSSM = MSSMHiggsModel()

