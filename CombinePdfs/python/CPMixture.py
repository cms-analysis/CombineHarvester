from HiggsAnalysis.CombinedLimit.PhysicsModel import PhysicsModel
import math

class CPMixture(PhysicsModel):
	def __init__(self):
	  PhysicsModel.__init__(self)
          self.constrain_ggHYield  = False
          self.kappa = False
          self.lumi_scale = None

	def setPhysicsOptions(self, physOptions):
                for po in physOptions:
                  if po.startswith("constrain_ggHYield"):
                    self.constrain_ggHYield = True
                  if po.startswith("kappa"):
                    self.kappa = True

	def doParametersOfInterest(self):
		"""Create POI and other parameters, and define the POI set."""
		# --- POI and other parameters ----
	        
                poiNames = []
                
                if not self.kappa:
                  self.modelBuilder.doVar('alpha[0,0,1]') 
                  poiNames.append('alpha')
                  self.modelBuilder.doVar('muF[1,0,4]')
                  poiNames.append('muF')
                else:
                  print 'Use kappa parameterisation'
                  self.modelBuilder.doVar('kappaA[0,0,2]')
                  self.modelBuilder.doVar('kappaH[1,0,2]')
                  poiNames.append('kappaA')
                  poiNames.append('kappaH') 
                  self.modelBuilder.factory_('expr::alpha("3/2*@0/@1", kappaA, kappaH)')
                  self.modelBuilder.factory_('expr::muF("@1*@1 + 9/4*@0*@0", kappaA, kappaH)')

		self.modelBuilder.doVar('muV[1,0,4]')
                self.modelBuilder.doVar('f[0,-1,1]')

                self.modelBuilder.doSet('POI', ','.join(poiNames))

                params = {
                           'pi': math.pi, 
                           'ps_sm_xs_ratio' : 2.25,
                           'qqh_sigma1' : 0.2371314,
                           'qqh_sigma3' : 2.6707,
                           'a1_qqh_mm' : 1.0,
                           'a3_qqh_mm' : 0.297979018705,
                         }

                self.modelBuilder.factory_('expr::a1("sqrt(@0)*cos(@1*{pi}/2)", muF, alpha)'.format(**params))
                self.modelBuilder.factory_('expr::a3("sqrt(@0)*sin(@1*{pi}/2)", muF, alpha)'.format(**params))
                self.modelBuilder.factory_('expr::sm_scaling("@0*@0 - @0*@1", a1, a3)')
                self.modelBuilder.factory_('expr::ps_scaling("@1*@1 - @0*@1", a1, a3)')
                self.modelBuilder.factory_('expr::mm_scaling("2*@0*@1", a1, a3)')
 
                # JHU samples have constant XS that does not depend on alpha. If the constrain_ggHYield option is set then add a scaling as a function of alpha -> XS = cos^2(alpha) + (3/2)^2*sin^2(alpha) to match MG5 XS                
                if self.constrain_ggHYield:
                  self.modelBuilder.factory_('expr::xs_sf("@0*@0 + @1*@1*{ps_sm_xs_ratio}", a1, a3)'.format(**params))
                  cps = ['sm_scaling', 'ps_scaling', 'mm_scaling']
                  for cp in cps:
                    self.modelBuilder.factory_('expr::xs_sf_{cp}("@0*@1", xs_sf, {cp})'.format(cp=cp))
                
                # define scaling for VBF templates as a function of muV/f 
                self.modelBuilder.factory_('expr::signf("@0/abs(@0)", f)')

                # VBF definition of a1 and a3
                self.modelBuilder.factory_('expr::a1_qqh("sqrt( (1-abs(@0))*@1 )", f, muV)')
                self.modelBuilder.factory_('expr::a3_qqh("@0*sqrt( abs(@1)*@2*{qqh_sigma1}/{qqh_sigma3} )", signf, f, muV)'.format(**params))

                self.modelBuilder.factory_('expr::vbf_sm_scaling("@0*@0 -@0*@1*{a1_qqh_mm}/{a3_qqh_mm}", a1_qqh, a3_qqh)'.format(**params))
                self.modelBuilder.factory_('expr::vbf_ps_scaling("@1*@1-@0*@1*{a3_qqh_mm}/{a1_qqh_mm}", a1_qqh, a3_qqh)'.format(**params))
                self.modelBuilder.factory_('expr::vbf_mm_scaling("@0*@1/({a1_qqh_mm}*{a3_qqh_mm})", a1_qqh, a3_qqh)'.format(**params))                

	def getYieldScale(self, bin, process):
		scalings = []	
		if 'ggH' in process and 'hww' not in process: 
                  if self.constrain_ggHYield:
                    scalings.append('xs_sf')
                  if "ggHsm" in process or "ggH2jsm" in process:
    		    scalings.append('sm_scaling')
		  elif "ggHps" in process or "ggH2jps" in process:
		    scalings.append('ps_scaling')
		  elif "ggHmm" in process or "ggH2jmm" in process:
                    scalings.append('mm_scaling')
                  elif 'ggH_ph' in process:
                    scalings.append('muF')  
                   

                if any(x in process for x in ['WH','ZH']) and not 'hww' in process:
                    scalings.append('muV')
                if "qqHsm" in process:
                  scalings.append('vbf_sm_scaling')
                elif "qqHps" in process:
                  scalings.append('vbf_ps_scaling')
                elif "qqHmm" in process:
                  scalings.append('vbf_mm_scaling')

                if scalings:
                  scaling = '_'.join(scalings)
                  print 'Scaling %s/%s as %s' % (bin, process,scaling)
                  return scaling
                else:
                  return 1

CPMixture = CPMixture()


