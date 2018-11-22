from HiggsAnalysis.CombinedLimit.PhysicsModel import PhysicsModel
import math

class CPMixture(PhysicsModel):
    def __init__(self):
        PhysicsModel.__init__(self)
        self.sm_fix = True

    def setPhysicsOptions(self, physOptions):
        for po in physOptions:
            if po.startswith("no_sm_fix"):
                self.sm_fix = False

    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""
        # --- POI and other parameters ----
            
        poiNames = []
 
        self.modelBuilder.doVar('alpha[0,0,1]') 
        poiNames.append('alpha')

        self.modelBuilder.doVar('mutautau[1,0,10]')
        self.modelBuilder.doVar('muV[1,0,10]')
        self.modelBuilder.doVar('muggH[1,0,10]')
        self.modelBuilder.doVar('f[0,-1,1]')

        self.modelBuilder.doSet('POI', ','.join(poiNames))

        self.modelBuilder.doVar('Zero[0]')

        self.modelBuilder.doSet('POI', ','.join(poiNames))

        params = {
                'pi': math.pi,
                'qqh_sigma1' : 0.2371314,
                'qqh_sigma3' : 2.6707, 
                'zh_sigma1' : 0.0554268,
                'zh_sigma3' : 2.6708711,
                'wh_sigma1' : 0.08607456,
                'wh_sigma3' : 5.6330289,
                'a1_qqh_mm' : 1.0,
                'a3_qqh_mm' : 0.297979018705,
                'a1_zh_mm' : 1.0,
                'a3_zh_mm' : 0.144057,
                'a1_wh_mm' : 1.0,
                'a3_wh_mm' : 0.1236136,
                'sm_evt_2016': 1612810.,
                'mm_evt_2016': 1728080.,
                'ps_evt_2016': 1751196.,
                'sm_evt_2017': 6802377.,
                'mm_evt_2017': 1803052.,
                'ps_evt_2017': 1879685.,
        }

        self.modelBuilder.factory_('expr::muV_mutautau("@0*@1", muV, mutautau)')
        self.modelBuilder.factory_('expr::muggH_mutautau("@0*@1", muggH, mutautau)')

        self.modelBuilder.factory_('expr::a1("sqrt(@0)*cos(@1*{pi}/2)", muggH_mutautau, alpha)'.format(**params))
        self.modelBuilder.factory_('expr::a3("sqrt(@0)*sin(@1*{pi}/2)", muggH_mutautau, alpha)'.format(**params))
        self.modelBuilder.factory_('expr::sm_scaling("@0*@0 - @0*@1", a1, a3)')
        self.modelBuilder.factory_('expr::ps_scaling("@1*@1 - @0*@1", a1, a3)')
        self.modelBuilder.factory_('expr::mm_scaling("2*@0*@1", a1, a3)')

        # For the 0jet and boosted categories since all templates should be the same for SM, MM, and PS sum together all the templates but weight by event numbers in the samples

        self.modelBuilder.doVar('expr::muggH_mutautau_sm_01jetnorm_2016("@0*{sm_evt_2016}/({sm_evt_2016}+{mm_evt_2016}+{ps_evt_2016})", muggH_mutautau)'.format(**params))
        self.modelBuilder.doVar('expr::muggH_mutautau_mm_01jetnorm_2016("@0*{mm_evt_2016}/({sm_evt_2016}+{mm_evt_2016}+{ps_evt_2016})", muggH_mutautau)'.format(**params))
        self.modelBuilder.doVar('expr::muggH_mutautau_ps_01jetnorm_2016("@0*{ps_evt_2016}/({sm_evt_2016}+{mm_evt_2016}+{ps_evt_2016})", muggH_mutautau)'.format(**params))
        self.modelBuilder.doVar('expr::muggH_mutautau_sm_01jetnorm_2017("@0*{sm_evt_2017}/({sm_evt_2017}+{mm_evt_2017}+{ps_evt_2017})", muggH_mutautau)'.format(**params))
        self.modelBuilder.doVar('expr::muggH_mutautau_mm_01jetnorm_2017("@0*{mm_evt_2017}/({sm_evt_2017}+{mm_evt_2017}+{ps_evt_2017})", muggH_mutautau)'.format(**params))
        self.modelBuilder.doVar('expr::muggH_mutautau_ps_01jetnorm_2017("@0*{ps_evt_2017}/({sm_evt_2017}+{mm_evt_2017}+{ps_evt_2017})", muggH_mutautau)'.format(**params))

        # define scaling for JHU VBF/VH templates as a function of muV,mutautau, and fa3 - this uses VBF definition of fa3 
        self.modelBuilder.factory_('expr::signf("@0/abs(@0)", f)')  

        self.modelBuilder.factory_('expr::a1_qqh("sqrt( (1-abs(@0))*@1 )", f, muV_mutautau)')
        self.modelBuilder.factory_('expr::a3_qqh("@0*sqrt( abs(@1)*@2*{qqh_sigma1}/{qqh_sigma3} )", signf, f, muV_mutautau)'.format(**params))

        self.modelBuilder.factory_('expr::vbf_sm_scaling("@0*@0 -@0*@1*{a1_qqh_mm}/{a3_qqh_mm}", a1_qqh, a3_qqh)'.format(**params))
        self.modelBuilder.factory_('expr::vbf_ps_scaling("@1*@1-@0*@1*{a3_qqh_mm}/{a1_qqh_mm}", a1_qqh, a3_qqh)'.format(**params))
        self.modelBuilder.factory_('expr::vbf_mm_scaling("@0*@1/({a1_qqh_mm}*{a3_qqh_mm})", a1_qqh, a3_qqh)'.format(**params)) 

        self.modelBuilder.factory_('expr::f_zh("@0*{zh_sigma3}*{qqh_sigma1}/({zh_sigma1}*{qqh_sigma3})", f)'.format(**params))
        self.modelBuilder.factory_('expr::a1_zh("sqrt( (1-abs(@0))*@1 )", f_zh, muV_mutautau)')
        self.modelBuilder.factory_('expr::a3_zh("@0*sqrt( abs(@1)*@2*{zh_sigma1}/{zh_sigma3} )", signf, f_zh, muV_mutautau)'.format(**params))

        self.modelBuilder.factory_('expr::zh_sm_scaling("@0*@0 -@0*@1*{a1_zh_mm}/{a3_zh_mm}", a1_zh, a3_zh)'.format(**params))
        self.modelBuilder.factory_('expr::zh_ps_scaling("@1*@1-@0*@1*{a3_zh_mm}/{a1_zh_mm}", a1_zh, a3_zh)'.format(**params))
        self.modelBuilder.factory_('expr::zh_mm_scaling("@0*@1/({a1_zh_mm}*{a3_zh_mm})", a1_zh, a3_zh)'.format(**params))

        self.modelBuilder.factory_('expr::f_wh("@0*{wh_sigma3}*{qqh_sigma1}/({wh_sigma1}*{qqh_sigma3})", f)'.format(**params))
        self.modelBuilder.factory_('expr::a1_wh("sqrt( (1-abs(@0))*@1 )", f_wh, muV_mutautau)')
        self.modelBuilder.factory_('expr::a3_wh("@0*sqrt( abs(@1)*@2*{zh_sigma1}/{zh_sigma3} )", signf, f_wh, muV_mutautau)'.format(**params))

        self.modelBuilder.factory_('expr::wh_sm_scaling("@0*@0 -@0*@1*{a1_wh_mm}/{a3_wh_mm}", a1_wh, a3_wh)'.format(**params))
        self.modelBuilder.factory_('expr::wh_ps_scaling("@1*@1-@0*@1*{a3_wh_mm}/{a1_wh_mm}", a1_wh, a3_wh)'.format(**params))
        self.modelBuilder.factory_('expr::wh_mm_scaling("@0*@1/({a1_wh_mm}*{a3_wh_mm})", a1_wh, a3_wh)'.format(**params))

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
            if "qqHsm" in process or "ggH2jsm" in process:
                scalings.append('sm_scaling')
            elif "qqHps" in process or "ggH2jps" in process:
                scalings.append('ps_scaling')
            elif "qqHmm" in process:
                scalings.append('mm_scaling')
            else:
               scalings.append('muV_mutautau')

        if scalings:
            scaling = '_'.join(scalings)

            if self.sm_fix:
                if "_1_13TeV" in bin_ or "_2_13TeV" in bin_:
                    year = '2016'
                    if '2017' in bin_: year = '2017' 
                    if "ggHsm" in process: scaling = "muggH_mutautau_sm_01jetnorm_%s" % year
                    elif "ggHmm" in process: scaling = "muggH_mutautau_mm_01jetnorm_%s" % year
                    elif "ggHps" in process: scaling = "muggH_mutautau_ps_01jetnorm_%s" % year

            print 'Scaling %s/%s as %s' % (bin_, process,scaling)
            return scaling
        else:
            return 1

CPMixture = CPMixture()


