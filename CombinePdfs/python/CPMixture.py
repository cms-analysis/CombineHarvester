from HiggsAnalysis.CombinedLimit.PhysicsModel import PhysicsModel
import math

class CPMixture(PhysicsModel):
	def __init__(self):
	  PhysicsModel.__init__(self)
          self.constrain_ggHYield  = False
          self.sm_xs = 1.
          self.ps_xs = 910./922.

	def setPhysicsOptions(self, physOptions):
                for po in physOptions:
                  if po.startswith("constrain_ggHYield"):
                    self.constrain_ggHYield = True

	def doParametersOfInterest(self):
		"""Create POI and other parameters, and define the POI set."""
		# --- POI and other parameters ----
	        
                poiNames = []
                
                self.modelBuilder.doVar('alpha[0,0,1]') 
                poiNames.append('alpha')
		self.modelBuilder.doVar('muF[1,0,20]')
                if not self.constrain_ggHYield: poiNames.append('muF')
		self.modelBuilder.doVar('muV[1,0,20]')
                poiNames.append('muV')
                self.modelBuilder.doSet('POI', ','.join(poiNames))

                maxmix = {
                           'a_tilde' : 1.0,
                           'b_tilde' : 1.0
                         }
			
		self.modelBuilder.factory_('expr::a("cos(@0*{pi}/2)", alpha)'.format(pi=math.pi))
		self.modelBuilder.factory_('expr::b("sin(@0*{pi}/2)", alpha)'.format(pi=math.pi))
	        
		self.modelBuilder.factory_('expr::sm_scaling("@0*@0-@0*@1*{a_tilde}/{b_tilde}", a, b)'.format(**maxmix))
		self.modelBuilder.factory_('expr::ps_scaling("@1*@1-@0*@1*{b_tilde}/{a_tilde}", a, b)'.format(**maxmix))
                self.modelBuilder.factory_('expr::mm_scaling("@0*@1/({a_tilde}*{b_tilde})", a, b)'.format(**maxmix))

                if self.constrain_ggHYield:
                  self.modelBuilder.factory_('expr::xs_scaling("@0*@0*{sm_xs} +@1*@1*{ps_xs}", a, b)'.format(sm_xs=self.sm_xs,ps_xs=self.ps_xs))
                
                cps = ['sm_scaling', 'ps_scaling', 'mm_scaling'] 
                for cp in cps:
                  self.modelBuilder.factory_('expr::muF_{cp}("@0*@1", muF, {cp})'.format(cp=cp)
                  if self.constrain_ggHYield:
                    self.modelBuilder.factory_('expr::muF_{cp}_xs_scaling("@0*@1*@2", muF, {cp}, xs_scaling)'.format(cp=cp) 

	def getYieldScale(self, bin, process):
		if self.DC.isSignal[process]:
			scalings = []	
			if 'ggh' in process.lower(): 
                          if not self.constrain_ggHYield: 
                            scalings.append('muF')
                          if "f0" in process.lower():
    			    scalings.append('sm_scaling')
			  elif "f1" in process.lower():
			    scalings.append('ps_scaling')
			  elif "f0p5" in process.lower(): 
                            scalings.append('mm_scaling') 
                          if self.constrain_ggHYield: 
                            scalings.append('xs_scaling')
                        elif any(x in process.lower() for x in ['qqH','WH','ZH']): scalings.append('muV')
                        
                        scaling = '_'.join(scalings)
                        print 'Scaling %s/%s as %s' % (bin, process, scaling)  
			return scaling
		
		else: return 1

CPMixture = CPMixture()


