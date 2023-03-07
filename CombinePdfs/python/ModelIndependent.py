from __future__ import absolute_import
from __future__ import print_function
from HiggsAnalysis.CombinedLimit.PhysicsModel import *
import os
import ROOT
import math
import itertools
import six

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
        for prefix, model in six.iteritems(self.processScaling):
            if process == prefix:
                print('Scaling %s/%s as %s' % (bin, process, 'Scaling_'+model))
                return 'Scaling_'+model
        return 1

class MSSMLikeHiggsModel(PhysicsModel):
    """
    Base class for all further derivatives. At the moment this allows for ggH and bbA for production and hbb, htt, hmm for
    decay. Supported run periods are 7Tev and 8TeV. The decay channels and run period has to be part of the datacards name.
    The production channel is taken from the samples name following the CMSHCG convention for production channels.
    """
    #def getHiggsSignalYieldScale(self, production, decay, energy):
    #        raise RuntimeError, "Not implemented"
    def getYieldScale(self,bin,process):
        """
        Split in production and decay channels. Call getHiggsSignalYieldScale. Return 1 for backgrounds.
        """
        if not self.DC.isSignal[process]: return 1
        processSource = process
        decaySource   = self.options.fileName+":"+bin # by default, decay comes from the datacard name or bin label
        if "_" in process: (processSource, decaySource) = process.split("_")
        if processSource not in ["ggh", "bbh", "ggA", "bbA", "ggH", "bbH"]:
            raise RuntimeError("Validation Error: signal process %s not among the allowed ones." % processSource)
        foundDecay = None
        for D in [ "htautau", "Atautau", "Htautau", "hbb", "htt", "hmm" ]:
            if D in decaySource:
                if foundDecay: raise RuntimeError("Validation Error: decay string %s contains multiple known decay names" % decaySource)
                foundDecay = D
        if not foundDecay: raise RuntimeError("Validation Error: decay string %s does not contain any known decay name" % decaySource)
        foundEnergy = None
        for D in [ "7TeV", "8TeV", "13TeV" ]:
            if D in decaySource:
                if foundEnergy: raise RuntimeError("Validation Error: decay string %s contains multiple known energies" % decaySource)
                foundEnergy = D
        if not foundEnergy:
            foundEnergy = "7TeV" ## To ensure backward compatibility
            print("Warning: decay string %s does not contain any known energy, assuming %s" % (decaySource, foundEnergy))
        return self.getHiggsSignalYieldScale(processSource, foundDecay, foundEnergy)


class FloatingMSSMXSHiggs(MSSMLikeHiggsModel):
    """
    Trivial model to float ggH and bbH independently. At the moment only ggH and bbh are supported. Extensions to the other
    production channels channels are given in comments. Also the principle how to deal with manipulations of the POI's and
    other defined roofit variables are shown in comments. 
    """
    def __init__(self):
        MSSMLikeHiggsModel.__init__(self) # not using 'super(x,self).__init__' since I don't understand it
        #self.tanb   = None
        self.modes    = [ "ggH", "bbH" ]
        self.mHRange  = []
        self.ggHRange = ['0','20']
        self.bbHRange = ['0','20']
    def setPhysicsOptions(self,physOptions):
        """
        Options are: modes. Examples for options like mARange and tanb are given in comments. 
        """
        for po in physOptions:
            #if po.startswith("tanb="): self.tanb = po.replace("tanb=", "")
            if po.startswith("modes="): self.modes = po.replace("modes=","").split(",")
            #if po.startswith("mARange="):
            #    self.mARange = po.replace("mARange=","").split(":")
            #    if len(self.mARange) != 2:
            #        raise RuntimeError, "Definition of mA range requires two extrema, separated by ':'"
            #    elif float(self.mARange[0]) >= float(self.mARange[1]):
            #        raise RuntimeError, "Extrema for mA range defined with inverterd order. Second element must be larger than first element"
            if po.startswith("ggHRange="):
                self.ggHRange = po.replace("ggHRange=","").split(":")
                if len(self.ggHRange) != 2:
                    raise RuntimeError("ggH signal strength range requires minimal and maximal value")
                elif float(self.ggHRange[0]) >= float(self.ggHRange[1]):
                    raise RuntimeError("minimal and maximal range swapped. Second value must be larger first one")
            if po.startswith("bbHRange="):
                self.bbHRange = po.replace("bbHRange=","").split(":")
                if len(self.bbHRange) != 2:
                    raise RuntimeError("bbH signal strength range requires minimal and maximal value")
                elif float(self.bbHRange[0]) >= float(self.bbHRange[1]):
                    raise RuntimeError("minimal and maximal range swapped. Second value must be larger first one")
    def doParametersOfInterest(self):
        """
        Create POI and other parameters, and define the POI set. E.g. Evaluate cross section for given values of mA and tanb
        """
        ## Example: evaluate cross sections for given values of tanb and mA, the names of the variables are ggH_xsec and bbH_xsec,
        ## the values are given by the value in brakets. In principle three values can be passed on: value, lower bound and upper
        ## bound.
        #
        #mssm_scan = mssm_xsec_tools("{CMSSW_BASE}/src/{PATH}".format(CMSSW_BASE=os.environ['CMSSW_BASE'], PATH="HiggsAnalysis/HiggsToTauTau/data/out.mhmax-mu+200-7TeV-nnlo.root"))
        #mssm_xsec = mssm_scan.query(self.options.mass, float(self.tanb))
        #self.modelBuilder.doVar("bbH_xsec[%g]" % (mssm_xsec['higgses']['A']['xsec']['santander']*mssm_xsec['higgses']['A']['BR']))
        #self.modelBuilder.doVar("ggH_xsec[%g]" % (mssm_xsec['higgses']['A']['xsec']['ggF'      ]*mssm_xsec['higgses']['A']['BR']))
        #
        ## Define signal strengths on ggH and bbH as POI, NOTE: the range of the POIs is defined here
        self.modelBuilder.doVar("r_ggH[%s,%s,%s]" % (str((float(self.ggHRange[0])+float(self.ggHRange[1]))/2.), self.ggHRange[0], self.ggHRange[1]));
        self.modelBuilder.doVar("r_bbH[%s,%s,%s]" % (str((float(self.bbHRange[0])+float(self.bbHRange[1]))/2.), self.bbHRange[0], self.bbHRange[1]));
        poi = ",".join(["r_"+m for m in self.modes])
        ## Define Higgs boson mass as another parameter. It will be floating if mARange is set otherwise it will be treated
        ## as fixed. NOTE: this is only left here as an extended example. It's not useful to have mA floating at the moment.
        if self.modelBuilder.out.var("MH"):
            if len(self.mHRange):
                print('MH will be left floating within', self.mHRange[0], 'and', self.mHRange[1])
                self.modelBuilder.out.var("MH").setRange(float(self.mHRange[0]),float(self.mHRange[1]))
                self.modelBuilder.out.var("MH").setConstant(False)
                poi+=',MH'
            elif self.options.mass != 0:
                print('MH will be assumed to be', self.options.mass)
                self.modelBuilder.out.var("MH").removeRange()
                self.modelBuilder.out.var("MH").setVal(self.options.mass)
        else:
            if len(self.mHRange):
                print('MH will be left floating within', self.mHRange[0], 'and', self.mHRange[1])
                self.modelBuilder.doVar("MH[%s,%s]" % (self.mHRange[0],self.mHRange[1]))
                poi+=',MH'
            else:
                print('MH (not there before) will be assumed to be', self.options.mass)
                self.modelBuilder.doVar("MH[%g]" % self.options.mass)
        ## define set of POIs
        self.modelBuilder.doSet("POI",poi)
    def getHiggsSignalYieldScale(self,production,decay, energy):
        if production == "ggH" or production == "bbH":
            ## This is an example how to multiply the yields r_ggH and r_bbH with the roofit variables ggH_xsec and bbH_xsec
            ## that have been defined above, with the help of a roofit expression.
            #
            #self.modelBuilder.factory_('expr::%s_yield("@0*@1", r_%s, %s_xsec)' % (production, production, production))
            #
            ## This is the trivial model that we follow now. We just pass on the values themselves. Yes this is just a
            ## trivial renaming, but we leave it in as an example. Instead also r_ggH and r_bbH could be passed on directly
            ## in the return function instead of the newly defined variables ggH_yields or bbH_yield.
            self.modelBuilder.factory_('expr::%s_yield("@0", r_%s)' % (production, production))
            return "%s_yield" % production
        ## This just corresponds to entry points to extend the model to other production channels like qqH, ttH, VH.
        #
        #if production == "qqH": return ("r_qqH" if "qqH" in self.modes else 1)
        #if production == "ttH": return ("r_ttH" if "ttH" in self.modes else 1)
        #if production in [ "WH", "ZH", "VH" ]: return ("r_VH" if "VH" in self.modes else 1)
        #
        raise RuntimeError("Unknown production mode '%s'" % production)




#BR Charged Higgs
brChargedHiggs = BRChargedHiggs()

#Model independent xs*BR limits
floatingMSSMXSHiggs = FloatingMSSMXSHiggs()
