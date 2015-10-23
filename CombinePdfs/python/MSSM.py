from HiggsAnalysis.CombinedLimit.PhysicsModel import *
import os
import ROOT
import math
import itertools

class MSSMHiggsModel(PhysicsModel):
    def __init__(self, modelname):
        PhysicsModel.__init__(self)
        # Define the known production and decay processes
        # These are strings we will look for in the process names to
        # determine the correct normalisation scaling
        self.ERAS = ['7TeV', '8TeV', '13TeV', '14TeV']
        # We can't add anything here that we're not actually going to have
        # loaded from the model files. Should integrate this into the options
        # somehow.
        eras = ['8TeV']
        self.modelname = modelname
        self.PROC_SETS = []
        self.PROC_SETS.append(
            ([ 'ggh', 'bbh' ], [ 'htautau' ], eras)
            )
        self.PROC_SETS.append(
            ([ 'ggH', 'bbH' ], [ 'Htautau' ], eras)
            )
        self.PROC_SETS.append(
            ([ 'ggA', 'bbA' ], [ 'Atautau' ], eras)
            )
    #    self.model = 'out.mhmax-mu+200-8TeV-tanbHigh-nnlo.root'
    #    self.era = '8TeV'
        
        
    #def setPhysicsOptions(self, physOptions):
    #    """
    #    Options are: model.  
    #    """
    #    for po in physOptions:
    #        if po.startswith("model="): self.model = po.replace("model=", "")
    #        if po.startswith("era=") : self.era = po.replace("era=", "")
            
    def setModelBuilder(self, modelBuilder):
        """We're not supposed to overload this method, but we have to because 
        this is our only chance to import things into the workspace while it
        is completely empty. This is primary so we can define some of our MSSM
        Higgs boson masses as functions instead of the free variables that would
        be imported later as dependents of the normalisation terms."""
        # First call the parent class implementation
        PhysicsModel.setModelBuilder(self, modelBuilder)
        if self.modelname == "mhmax_7TeV" : filename = 'out.mhmax-mu+200-7TeV-tanbHigh-nnlo.root'
        if self.modelname == "mhmax_8TeV" : filename = 'out.mhmax-mu+200-8TeV-tanbHigh-nnlo.root'
        if self.modelname == "mhmax_13TeV" : filename = 'newmhmax_mu200_13TeV.root'
        if self.modelname == "mhmax_14TeV" : filename = 'newmhmax_mu200_14TeV.root'
        if self.modelname == "mhmodp_7TeV" : filename = 'out.mhmodp-7TeV-tanbHigh-nnlo.root'
        if self.modelname == "mhmodp_8TeV" : filename = 'out.mhmodp-8TeV-tanbHigh-nnlo.root'
        if self.modelname == "mhmodp_13TeV" : filename = 'mhmodp_mu200_13TeV.root'
        if self.modelname == "mhmodp_14TeV" : filename = 'mhmodp_mu200_14TeV.root'
        if self.modelname == "mhmodm_7TeV" : filename = 'out.mhmodm-7TeV-tanbHigh-nnlo.root'
        if self.modelname == "mhmodm_8TeV" : filename = 'out.mhmodm-8TeV-tanbHigh-nnlo.root'
        if self.modelname == "mhmodm_13TeV" : filename = 'mhmodm_13TeV.root'
        if self.modelname == "mhmodm_14TeV" : filename = 'mhmodm_14TeV.root'
        if self.modelname == "lightstau_7TeV" : filename = 'out.lightstau1-7TeV-tanbHigh-nnlo.root'
        if self.modelname == "lightstau_8TeV" : filename = 'out.lightstau1-8TeV-tanbHigh-nnlo.root'
        if self.modelname == "lightstau_13TeV" : filename = 'lightstau1_13TeV.root'
        if self.modelname == "lightstau_14TeV" : filename = 'lightstau1_14TeV.root'
        if self.modelname == "lightstopmod_7TeV" : filename = 'out.lightstopmod-7TeV-tanbHigh-nnlo.root'
        if self.modelname == "lightstopmod_8TeV" : filename = 'out.lightstopmod-8TeV-tanbHigh-nnlo.root'
        if self.modelname == "lightstopmod_13TeV" : filename = 'lightstopmpd_13TeV.root'
        if self.modelname == "lightstopmod_14TeV" : filename = 'lightstopmod_14TeV.root'
        if self.modelname == "tauphobic_7TeV" : filename = 'out.tauphobic-7TeV-tanbAll-nnlo.root'
        if self.modelname == "tauphobic_8TeV" : filename = 'out.tauphobic-8TeV-tanbAll-nnlo.root'
        if self.modelname == "tauphobic_13TeV" : filename = 'tauphobic_13TeV.root'
        if self.modelname == "tauphobic_14TeV" : filename = 'tauphobic_14TeV.root'
        if self.modelname == "hMSSM_8TeV" : filename = 'hMSSM_8TeV.root'
        if self.modelname == "hMSSM_13TeV" : filename = 'hMSSM_13TeV.root'
        if self.modelname == "low-tb-high_8TeV" : filename = 'low-tb-high_8TeV.root'
        if self.modelname == "low-tb-high_13TeV" : filename = 'low-tb-high_13TeV.root'
        self.buildModel(os.environ['CMSSW_BASE']+'/src/auxiliaries/models/'+filename)
        #self.buildModel(os.environ['CMSSW_BASE']+'/src/auxiliaries/models/'+self.model)

    def doHistFunc(self, name, hist, varlist, interpolate=1):
        "method to conveniently create a RooHistFunc from a TH1/TH2 input"
        dh = ROOT.RooDataHist('dh_%s'%name, 'dh_%s'%name, ROOT.RooArgList(*varlist), ROOT.RooFit.Import(hist))
        hfunc = ROOT.RooHistFunc(name, name, ROOT.RooArgSet(*varlist), dh)
        hfunc.setInterpolationOrder(interpolate)
        self.modelBuilder.out._import(hfunc, ROOT.RooFit.RecycleConflictNodes())
        return self.modelBuilder.out.function(name)

    def santanderMatching(self, h4f, h5f, mass = None):
        res = h4f.Clone()
        for x in xrange(1, h4f.GetNbinsX() + 1):
            for y in xrange(1, h4f.GetNbinsY() +1):
               mh = h4f.GetXaxis().GetBinCenter(x) if mass is None else mass.GetBinContent(x, y)
               t = math.log(mh / 4.92) - 2.
               fourflav = h4f.GetBinContent(x, y)
               fiveflav = h5f.GetBinContent(x, y)
               sigma = (1. / (1. + t)) * (fourflav + t * fiveflav)
               res.SetBinContent(x, y, sigma)
        return res  

    def buildModel(self, filename):
        mA = ROOT.RooRealVar('mA', 'mA', 344., 90., 1000.)
        tanb = ROOT.RooRealVar('tanb', 'tanb', 9., 1., 60.)
        f = ROOT.TFile(filename)
        #Take care of different histogram names: (May can be reduced if ultimately changed to 13TeV/14TeV)
        if 'hMSSM' in self.modelname or 'low-tb-high' in self.modelname or '13TeV' in self.modelname or '14TeV' in self.modelname:
            mH_str = "m_H"
            mh_str = "m_h"
            ggF_xsec_h_str = "xs_gg_h"
            ggF_xsec_H_str = "xs_gg_H"
            ggF_xsec_A_str = "xs_gg_A"
            bbH_4f_xsec_h_str = "xs_bb4F_h"
            bbH_4f_xsec_H_str = "xs_bb4F_H"
            bbH_4f_xsec_A_str = "xs_bb4F_A"
            bbH_xsec_h_str = "xs_bb5F_h"
            bbH_xsec_H_str = "xs_bb5F_H"
            bbH_xsec_A_str = "xs_bb5F_A"
            brtautau_h_str = "br_h_tautau"
            brtautau_H_str = "br_H_tautau"
            brtautau_A_str = "br_A_tautau"
        else :
            mH_str = "h_mH"
            mh_str = "h_mh"
            ggF_xsec_h_str = "h_ggF_xsec_h"
            ggF_xsec_H_str = "h_ggF_xsec_H"
            ggF_xsec_A_str = "h_ggF_xsec_A"
            bbH_4f_xsec_h_str = "h_bbH4f_xsec_h"
            bbH_4f_xsec_H_str = "h_bbH4f_xsec_H"
            bbH_4f_xsec_A_str = "h_bbH4f_xsec_A"
            bbH_xsec_h_str = "h_bbH_xsec_h"
            bbH_xsec_H_str = "h_bbH_xsec_H"
            bbH_xsec_A_str = "h_bbH_xsec_A"
            brtautau_h_str = "h_brtautau_h"
            brtautau_H_str = "h_brtautau_H"
            brtautau_A_str = "h_brtautau_A"
        mH = self.doHistFunc('mH', f.Get(mH_str), [mA, tanb])
        mh = self.doHistFunc('mh', f.Get(mh_str), [mA, tanb])
        ggF_xsec_h = self.doHistFunc('xsec_ggh_8TeV', f.Get(ggF_xsec_h_str), [mA, tanb])
        ggF_xsec_H = self.doHistFunc('xsec_ggH_8TeV', f.Get(ggF_xsec_H_str), [mA, tanb])
        ggF_xsec_A = self.doHistFunc('xsec_ggA_8TeV', f.Get(ggF_xsec_A_str), [mA, tanb])
        bbH_xsec_h = self.doHistFunc('xsec_bbh_8TeV', self.santanderMatching(f.Get(bbH_4f_xsec_h_str), f.Get(bbH_xsec_h_str), f.Get(mh_str)), [mA, tanb])
        bbH_xsec_H = self.doHistFunc('xsec_bbH_8TeV', self.santanderMatching(f.Get(bbH_4f_xsec_H_str), f.Get(bbH_xsec_H_str), f.Get(mH_str)), [mA, tanb])
        bbH_xsec_A = self.doHistFunc('xsec_bbA_8TeV', self.santanderMatching(f.Get(bbH_4f_xsec_A_str), f.Get(bbH_xsec_A_str)), [mA, tanb])
        brtautau_h = self.doHistFunc('br_htautau', f.Get(brtautau_h_str), [mA, tanb])
        brtautau_H = self.doHistFunc('br_Htautau', f.Get(brtautau_H_str), [mA, tanb])
        brtautau:A = self.doHistFunc('br_Atautau', f.Get(brtautau_A_str), [mA, tanb])
        #print f.Get(brtautau_h_str).GetBinContent(f.Get(brtautau_h_str).GetXaxis().FindBin(mA.getVal()),f.Get(brtautau_h_str).GetYaxis().FindBin(tanb.getVal())), brtautau_h.getVal()
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
                # print (P, D, E)
                terms = ['xsec_%s_%s' % (P, E), 'br_%s'%D]
                terms += ['r']
                self.modelBuilder.factory_('prod::scaling_%s_%s_%s(%s)' % (P,D,E,','.join(terms)))
                self.modelBuilder.out.function('scaling_%s_%s_%s' % (P,D,E)).Print('')

        # self.modelBuilder.out.Print()
        self.modelBuilder.doSet('POI', 'r')

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



#7TeV
mhmax_7TeV = MSSMHiggsModel("mhmax_7TeV")
mhmodp_7TeV = MSSMHiggsModel("mhmodp_7TeV")
mhmodm_7TeV = MSSMHiggsModel("mhmodm_7TeV")
lightstau_7TeV = MSSMHiggsModel("lightstau_7TeV")
lightstopmod_7TeV = MSSMHiggsModel("lightstopmod_7TeV")
tauphobic_7TeV = MSSMHiggsModel("tauphobic_7TeV")

#8TeV
mhmax_8TeV = MSSMHiggsModel("mhmax_8TeV")
mhmodp_8TeV = MSSMHiggsModel("mhmodp_8TeV")
mhmodm_8TeV = MSSMHiggsModel("mhmodm_8TeV")
lightstau_8TeV = MSSMHiggsModel("lightstau_8TeV")
lightstopmod_8TeV = MSSMHiggsModel("lightstopmod_8TeV")
tauphobic_8TeV = MSSMHiggsModel("tauphobic_8TeV")
hMSSM_8TeV = MSSMHiggsModel("hMSSM_8TeV")
lowtbhigh_8TeV = MSSMHiggsModel("low-tb-high_8TeV")

#13TeV
mhmax_13TeV = MSSMHiggsModel("mhmax_13TeV")
mhmodp_13TeV = MSSMHiggsModel("mhmodp_13TeV")
mhmodm_13TeV = MSSMHiggsModel("mhmodm_13TeV")
lightstau_13TeV = MSSMHiggsModel("lightstau_13TeV")
lightstopmod_13TeV = MSSMHiggsModel("lightstopmod_13TeV")
tauphobic_13TeV = MSSMHiggsModel("tauphobic_13TeV")
hMSSM_13TeV = MSSMHiggsModel("hMSSM_13TeV")
lowtbhigh_13TeV = MSSMHiggsModel("low-tb-high_13TeV")

#14TeV
mhmax_14TeV = MSSMHiggsModel("mhmax_14TeV")
mhmodp_14TeV = MSSMHiggsModel("mhmodp_14TeV")
mhmodm_14TeV = MSSMHiggsModel("mhmodm_14TeV")
lightstau_14TeV = MSSMHiggsModel("lightstau_14TeV")
lightstopmod_14TeV = MSSMHiggsModel("lightstopmod_14TeV")
tauphobic_14TeV = MSSMHiggsModel("tauphobic_14TeV")

#BR Charged Higgs
brChargedHiggs = BRChargedHiggs()

