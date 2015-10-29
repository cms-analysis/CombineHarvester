from HiggsAnalysis.CombinedLimit.PhysicsModel import *
import os
import ROOT
import math
import itertools

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
            raise RuntimeError, "Validation Error: signal process %s not among the allowed ones." % processSource
        foundDecay = None
        for D in [ "htautau", "Atautau", "Htautau", "hbb", "htt", "hmm" ]:
            if D in decaySource:
                if foundDecay: raise RuntimeError, "Validation Error: decay string %s contains multiple known decay names" % decaySource
                foundDecay = D
        if not foundDecay: raise RuntimeError, "Validation Error: decay string %s does not contain any known decay name" % decaySource
        foundEnergy = None
        for D in [ "7TeV", "8TeV" ]:
            if D in decaySource:
                if foundEnergy: raise RuntimeError, "Validation Error: decay string %s contains multiple known energies" % decaySource
                foundEnergy = D
        if not foundEnergy:
            foundEnergy = "7TeV" ## To ensure backward compatibility
            print "Warning: decay string %s does not contain any known energy, assuming %s" % (decaySource, foundEnergy)
        return self.getHiggsSignalYieldScale(processSource, foundDecay, foundEnergy)

class FloatingMSSMXSHiggs(MSSMLikeHiggsModel):
    """
    Trivial model to float ggA and bbA independently. At the moment only ggA and bbh are supported. Extensions to the other
    production channels channels are given in comments. Also the principle how to deal with manipulations of the POI's and
    other defined roofit variables are shown in comments. 
    """
    def __init__(self):
        MSSMLikeHiggsModel.__init__(self) # not using 'super(x,self).__init__' since I don't understand it
        self.modes    = [ "ggA", "bbA" ]
        self.mARange  = []
        self.ggARange = ['0','20']
        self.bbARange = ['0','20']
    def setPhysicsOptions(self,physOptions):
        """
        Options are: modes. Examples for options like mARange are given in comments. 
        """
        for po in physOptions:
            if po.startswith("modes="): self.modes = po.replace("modes=","").split(",")
            if po.startswith("mARange="):
                self.mARange = po.replace("mARange=","").split(":")
                if len(self.mARange) != 2:
                    raise RuntimeError, "Definition of mA range requires two extrema, separated by ':'"
                elif float(self.mARange[0]) >= float(self.mARange[1]):
                    raise RuntimeError, "Extrema for mA range defined with inverterd order. Second element must be larger than first element"
            if po.startswith("ggARange="):
                self.ggARange = po.replace("ggARange=","").split(":")
                if len(self.ggARange) != 2:
                    raise RuntimeError, "ggA signal strength range requires minimal and maximal value"
                elif float(self.ggARange[0]) >= float(self.ggARange[1]):
                    raise RuntimeError, "minimal and maximal range swapped. Second value must be larger first one"
            if po.startswith("bbARange="):
                self.bbARange = po.replace("bbARange=","").split(":")
                if len(self.bbARange) != 2:
                    raise RuntimeError, "bbA signal strength range requires minimal and maximal value"
                elif float(self.bbARange[0]) >= float(self.bbARange[1]):
                    raise RuntimeError, "minimal and maximal range swapped. Second value must be larger first one"                 
    def doParametersOfInterest(self):
        """
        Create POI and other parameters, and define the POI set. E.g. Evaluate cross section for given values of mA and tanb
        """
        # Define signal strengths on ggA and bbA as POI, NOTE: the range of the POIs is defined here
        self.modelBuilder.doVar("r_ggA[%s,%s,%s]" % (str((float(self.ggARange[0])+float(self.ggARange[1]))/2.), self.ggARange[0], self.ggARange[1]));
        self.modelBuilder.doVar("r_bbA[%s,%s,%s]" % (str((float(self.bbARange[0])+float(self.bbARange[1]))/2.), self.bbARange[0], self.bbARange[1]));
        self.modelBuilder.doVar("r_ggh[0]" );
        self.modelBuilder.doVar("r_bbh[0]" );
        self.modelBuilder.doVar("r_ggH[0]" );
        self.modelBuilder.doVar("r_bbH[0]" );
        poi = ",".join(["r_"+m for m in self.modes])
        ## Define Higgs boson mass as another parameter. It will be floating if mARange is set otherwise it will be treated
        ## as fixed. NOTE: this is only left here as an extended example. It's not useful to have mA floating at the moment.
        if self.modelBuilder.out.var("mA"):
            if len(self.mARange):
                print 'mA will be left floating within', self.mARange[0], 'and', self.mARange[1]
                self.modelBuilder.out.var("mA").setRange(float(self.mARange[0]),float(self.mARange[1]))
                self.modelBuilder.out.var("mA").setConstant(False)
                poi+=',mA'
            else:
                print 'mA will be assumed to be', self.options.mass
                self.modelBuilder.out.var("mA").removeRange()
                self.modelBuilder.out.var("mA").setVal(self.options.mass)
        else:
            if len(self.mARange):
                print 'mA will be left floating within', self.mARange[0], 'and', self.mARange[1]
                self.modelBuilder.doVar("mA[%s,%s]" % (self.mARange[0],self.mARange[1]))
                poi+=',mA'
            else:
                print 'mA (not there before) will be assumed to be', self.options.mass
                self.modelBuilder.doVar("mA[%g]" % self.options.mass)
        if self.modelBuilder.out.var("mh"):
            self.modelBuilder.out.var("mh").removeRange()
            self.modelBuilder.out.var("mh").setVal(340)
        if self.modelBuilder.out.var("mH"):
             self.modelBuilder.out.var("mH").removeRange()
             self.modelBuilder.out.var("mH").setVal(340)   
        ## define set of POIs
        self.modelBuilder.doSet("POI",poi)
    def getHiggsSignalYieldScale(self,production,decay, energy):
        if production == "ggh" or production == "bbh" or production == "ggA" or production == "bbA" or  production == "ggH" or production == "bbH" :
            ## This is the trivial model that we follow now. We just pass on the values themselves. Yes this is just a
            ## trivial renaming, but we leave it in as an example. Instead also r_ggA and r_bbA could be passed on directly
            ## in the return function instead of the newly defined variables ggA_yields or bbA_yield.
            self.modelBuilder.factory_('expr::%s_yield("@0", r_%s)' % (production, production))
            return "%s_yield" % production
        raise RuntimeError, "Unknown production mode '%s'" % production

#BR Charged Higgs
brChargedHiggs = BRChargedHiggs()

#Model independent xs*BR limits
floatingMSSMXSHiggs = FloatingMSSMXSHiggs()
