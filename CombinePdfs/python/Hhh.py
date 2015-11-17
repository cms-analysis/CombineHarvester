from HiggsAnalysis.CombinedLimit.PhysicsModel import *
import os
import ROOT
import math
import itertools

class MSSMHhhHiggsModel(PhysicsModel):
    def __init__(self, modelname):
        PhysicsModel.__init__(self)
        # Define the known production and decay processes
        # These are strings we will look for in the process names to
        # determine the correct normalisation scaling
        self.ERAS = ['7TeV', '8TeV', '13TeV']
        # We can't add anything here that we're not actually going to have
        # loaded from the model files. Should integrate this into the options
        # somehow.
        eras = ['8TeV']
        self.modelname = modelname
        self.PROC_SETS = []
        self.PROC_SETS.append(
            ([ 'ggH' ], [ 'Hhhbbtautau' ], eras)
            )

    def setModelBuilder(self, modelBuilder):
        """We're not supposed to overload this method, but we have to because 
        this is our only chance to import things into the workspace while it
        is completely empty. This is primary so we can define some of our MSSM
        Higgs boson masses as functions instead of the free variables that would
        be imported later as dependents of the normalisation terms."""
        # First call the parent class implementation
        PhysicsModel.setModelBuilder(self, modelBuilder)
        if self.modelname == "low-tb-high_8TeV" : filename = 'out.low-tb-high-8TeV-tanbAll-nnlo.root'
        if self.modelname == "low-tb-high_13TeV" : filename = 'low-tb-high_13TeV.root'
        if self.modelname == "hMSSM_8TeV" : filename = 'hMSSM_8TeV.root'
        if self.modelname == "hMSSM_13TeV" : filename = 'hMSSM_13TeV.root'
        self.buildModel(os.environ['CMSSW_BASE']+'/src/auxiliaries/models/'+filename)

    def doHistFunc(self, name, hist, varlist, interpolate=1):
        "method to conveniently create a RooHistFunc from a TH1/TH2 input"
        dh = ROOT.RooDataHist('dh_%s'%name, 'dh_%s'%name, ROOT.RooArgList(*varlist), ROOT.RooFit.Import(hist))
        hfunc = ROOT.RooHistFunc(name, name, ROOT.RooArgSet(*varlist), dh)
        hfunc.setInterpolationOrder(interpolate)
        self.modelBuilder.out._import(hfunc, ROOT.RooFit.RecycleConflictNodes())
        return self.modelBuilder.out.function(name)

    def buildModel(self, filename):
        mA = ROOT.RooRealVar('mA', 'mA', 300.)
        tanb = ROOT.RooRealVar('tanb', 'tanb', 1.)
        f = ROOT.TFile(filename)
        #Take care of different histogram names for hMSSM:
        if 'hMSSM' in self.modelname or '13TeV' in self.modelname or '14TeV' in self.modelname:
            mH_str = "m_H"
            mh_str = "m_h"
            ggF_xsec_H_str = "xs_gg_H"
            brtautau_h_str = "br_h_tautau"
            brbb_h_str = "br_h_bb"
            brh0h0_H_str="br_H_hh"
        else :
            mH_str = "h_mH"
            mh_str = "h_mh"
            ggF_xsec_H_str = "h_ggF_xsec_H"
            brtautau_h_str = "h_brtautau_h"
            brbb_h_str = "h_brbb_h"
            brh0h0_H_str="h_brh0h0_H"
        
        mH = self.doHistFunc('mH', f.Get(mH_str), [mA, tanb])
        mh = self.doHistFunc('mh', f.Get(mh_str), [mA, tanb])
        ggF_xsec_H = self.doHistFunc('xsec_ggH_8TeV', f.Get(ggF_xsec_H_str), [mA, tanb])
        total_br_hist = ROOT.TH2F()
        total_br_hist = (f.Get(brtautau_h_str)) * (f.Get(brbb_h_str)) * (f.Get(brh0h0_H_str))
        total_br_hist *= 2
        brHhhbbtautau = self.doHistFunc('br_Hhhbbtautau', total_br_hist, [mA, tanb])

        # Next step: creating theory uncertainties
        #  1) for each syst source build kappaHi and kappaLo TH1s by doing a *careful* divide
        #     between nominal and shifted TH2s => "kappa_hi_xsec_ggh_8TeV_scale"
        #  2) create nuisance parameter (QCD_scale_ggH?) and constraint. Like:
        #         def preProcessNuisances(self,nuisances):
        #           if self.add_bbH and not any(row for row in nuisances if row[0] == "QCDscale_bbH"):
        #               nuisances.append(("QCDscale_bbH",False, "param", [ "0", "1"], [] ) )
        #     --> probably have to create the param ourself first, preProcessNuisances doesn't
        #     happen until later (after doParametersOfInterest)
        #  3) create AsymPow and add to the norm product

    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""
        # print '>> In doParametersOfInterest, workspace contents:'
        self.modelBuilder.doVar("r[1,0,20]")
        self.modelBuilder.out.var('mA').setConstant(True)
        self.modelBuilder.out.var('tanb').setConstant(True)
        for proc_set in self.PROC_SETS:
            for (P, D, E) in itertools.product(*proc_set):
                print (P, D, E)
                terms = ['xsec_%s_%s' % (P, E), 'br_%s'%D]
                terms += ['r']
                self.modelBuilder.factory_('prod::scaling_%s_%s_%s(%s)' % (P,D,E,','.join(terms)))
                self.modelBuilder.out.function('scaling_%s_%s_%s' % (P,D,E)).Print('')

        # self.modelBuilder.out.Print()
        self.modelBuilder.doSet('POI', 'r')

    def getHiggsProdDecMode(self, bin, process):
        """Return a triple of (production, decay, energy)"""
        print process
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
            print "is signal"
            # something going wrong here 
            (P, D, E) = self.getHiggsProdDecMode(bin, process)
            scaling = 'scaling_%s_%s_%s' % (P, D, E)
            print 'Scaling %s/%s as %s' % (bin, process, scaling)
            return scaling
        else:
            return 1

class BRChargedHiggs(PhysicsModel):
    def __init__(self):
        PhysicsModel.__init__(self)

    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""
        self.modelBuilder.doVar('BR[0,0,1]');

        self.modelBuilder.doSet('POI','BR')

        self.modelBuilder.factory_('expr::Scaling_HH("@0*@0", BR)')
        self.modelBuilder.factory_('expr::Scaling_WH("2 * (1-@0)*@0", BR)')
        #self.modelBuilder.factory_('expr::Scaling_tt("(1-@0)*(1-@0)", BR)')
        self.modelBuilder.factory_('expr::Scaling_tt("1 - (@0+@1)", Scaling_HH, Scaling_WH)')

        self.processScaling = { 'tt_ttHchHch':'HH', 'tt_ttHchW':'WH', 'tt':'tt' }

        # self.modelBuilder.out.Print()
        
    def getYieldScale(self,bin,process):
        for prefix, model in self.processScaling.iteritems():
            if process == prefix:
                print 'Scaling %s/%s as %s' % (bin, process, 'Scaling_'+model)
                return 'Scaling_'+model
        return 1




#8TeV
hMSSM_8TeV = MSSMHhhHiggsModel("hMSSM_8TeV")
lowtbhigh_8TeV = MSSMHhhHiggsModel("low-tb-high_8TeV")

#13TeV
hMSSM_13TeV = MSSMHhhHiggsModel("hMSSM_13TeV")
lowtbhigh_13TeV = MSSMHhhHiggsModel("low-tb-high_13TeV")

brChargedHiggs = BRChargedHiggs()

