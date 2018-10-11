from HiggsAnalysis.CombinedLimit.PhysicsModel import PhysicsModel
import math

class CPMixture(PhysicsModel):
	def __init__(self):
	  PhysicsModel.__init__(self)
          self.fit_2D = False

	def setPhysicsOptions(self, physOptions):
                for po in physOptions:
                   if po.startswith("fit_2D"):
                     self.fit_2D = True


	def doParametersOfInterest(self):
		"""Create POI and other parameters, and define the POI set."""
		# --- POI and other parameters ----
	        
                poiNames = []
 
                self.modelBuilder.doVar('alpha[0,0,1]') 
                poiNames.append('alpha')
                self.modelBuilder.doVar('mutautau[1,0.21,1.53]') #0.83
                self.modelBuilder.doVar('kappag[1,0.89,1.53]') #1.17
                self.modelBuilder.doVar('kappaW[1,0.9,1]') # 1
                self.modelBuilder.doVar('kappaZ[1,0.73,1.07]') #0.89
                if not self.fit_2D:
                  self.modelBuilder.factory_('expr::muggH("@0*@0*@1", kappag, mutautau)')
                else:
                  self.modelBuilder.doVar('muggH[1,0,2]')
                  poiNames.append('muggH')

                self.modelBuilder.factory_('expr::muVBF("(0.73*@0*@0 + 0.27*@1*@1)*@2", kappaW, kappaZ, mutautau)')
                self.modelBuilder.factory_('expr::muWH("@0*@0*@1", kappaW, mutautau)')
                self.modelBuilder.factory_('expr::muZH("@0*@0*@1", kappaZ, mutautau)')

                self.modelBuilder.doSet('POI', ','.join(poiNames))

                params = {
                           'pi': math.pi, 
                         }

                self.modelBuilder.factory_('expr::a1("sqrt(@0)*cos(@1*{pi}/2)", muggH, alpha)'.format(**params))
                self.modelBuilder.factory_('expr::a3("sqrt(@0)*sin(@1*{pi}/2)", muggH, alpha)'.format(**params))
                self.modelBuilder.factory_('expr::sm_scaling("@0*@0 - @0*@1", a1, a3)')
                self.modelBuilder.factory_('expr::ps_scaling("@1*@1 - @0*@1", a1, a3)')
                self.modelBuilder.factory_('expr::mm_scaling("2*@0*@1", a1, a3)')

	def getYieldScale(self, bin, process):
		scalings = []
		if 'ggH' in process and 'hww' not in process: 
                  if "ggHsm" in process or "ggH2jsm" in process:
    		    scalings.append('sm_scaling')
		  elif "ggHps" in process or "ggH2jps" in process:
		    scalings.append('ps_scaling')
		  elif "ggHmm" in process or "ggH2jmm" in process:
                    scalings.append('mm_scaling')
                  elif 'ggH_ph' in process:
                    scalings.append('muggH')  
                   

                if 'qqH' in process and 'hww' not in process:
                    scalings.append('muVBF') 
                if 'WH' in process and 'hww' not in process:
                    scalings.append('muWH')
                if 'ZH' in process and 'hww' not in process:
                    scalings.append('muZH')

                if scalings:
                  scaling = '_'.join(scalings)
                  print 'Scaling %s/%s as %s' % (bin, process,scaling)
                  return scaling
                else:
                  return 1

CPMixture = CPMixture()


