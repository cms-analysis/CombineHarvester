from HiggsAnalysis.CombinedLimit.PhysicsModel import PhysicsModel
import math

class CPMixture(PhysicsModel):
    def __init__(self):
        PhysicsModel.__init__(self)
        self.sm_fix = False

    def setPhysicsOptions(self, physOptions):
        for po in physOptions:
            if po.startswith("sm_fix"):
                self.sm_fix = True

    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""
        # --- POI and other parameters ----
            
        poiNames = []
 
        self.modelBuilder.doVar('alpha[0,0,1]') 
        poiNames.append('alpha')

        self.modelBuilder.doVar('mutautau[1,0,10]')
        self.modelBuilder.doVar('muV[1,0,10]')
        self.modelBuilder.doVar('muggH[1,0,10]')

        self.modelBuilder.doSet('POI', ','.join(poiNames))

        self.modelBuilder.doVar('Zero[0]')

        self.modelBuilder.doSet('POI', ','.join(poiNames))

        params = {
                'pi': math.pi,
                }

        self.modelBuilder.factory_('expr::a1("sqrt(@0)*cos(@1*{pi}/2)", muggH, alpha)'.format(**params))
        self.modelBuilder.factory_('expr::a3("sqrt(@0)*sin(@1*{pi}/2)", muggH, alpha)'.format(**params))
        self.modelBuilder.factory_('expr::sm_scaling("@0*@0 - @0*@1", a1, a3)')
        self.modelBuilder.factory_('expr::ps_scaling("@1*@1 - @0*@1", a1, a3)')
        self.modelBuilder.factory_('expr::mm_scaling("2*@0*@1", a1, a3)')

        self.modelBuilder.factory_('expr::muV_mutautau("@0*@1", muV, mutautau)')
        self.modelBuilder.factory_('expr::muggH_mutautau("@0*@1", muggH, mutautau)')

    def getYieldScale(self, bin_, process):

        scalings = []
        if 'ggH' in process and 'hww' not in process:
            if "ggHsm" in process or "ggH2jsm" in process:
                scalings.append('sm_scaling')
            elif "ggHps" in process or "ggH2jps" in process:
                scalings.append('ps_scaling')
            elif "ggHmm" in process or "ggH2jmm" in process:
                scalings.append('mm_scaling')
            elif 'ggH_ph' in process:
                scalings.append('muggH_mutautau')

        if ('qqH' in process or 'WH' in process or 'ZH' in process) and 'hww' not in process:
          scalings.append('muV_mutautau')

        if scalings:
            scaling = '_'.join(scalings)

            if self.sm_fix:
                if "_1_13TeV" in bin_ or "_2_13TeV" in bin_:
                    if "ggHsm" in process:
                        scaling = "muggH_mutautau"
                    elif "ggHmm" in process or "ggHps" in process:
                        scaling = "Zero"

            print 'Scaling %s/%s as %s' % (bin_, process,scaling)
            return scaling
        else:
            return 1

CPMixture = CPMixture()


