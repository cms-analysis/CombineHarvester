from HiggsAnalysis.CombinedLimit.PhysicsModel import PhysicsModel
import math

class CPMixture(PhysicsModel):
	def __init__(self):
	  PhysicsModel.__init__(self)
          self.constrain_ggHYield  = False
          self.float_muF = False
          self.float_muV = False
          self.floatVBFshape = False
          self.lumi_scale = None

	def setPhysicsOptions(self, physOptions):
                for po in physOptions:
                  if po.startswith("constrain_ggHYield"):
                    self.constrain_ggHYield = True
                  if po.startswith("float_muF"):
                    self.float_muF = True
                  if po.startswith('lumiScale='):
                    self.lumi_scale = po.replace('lumiScale=', '')
                  if po.startswith("float_muV"):
                    self.float_muV = True
                  if po.startswith("floatVBFshape"):
                    self.floatVBFshape = True

	def doParametersOfInterest(self):
		"""Create POI and other parameters, and define the POI set."""
		# --- POI and other parameters ----
	        
                poiNames = []
                
                self.modelBuilder.doVar('alpha[0,0,1]') 
                poiNames.append('alpha')
                self.modelBuilder.doVar('muF[1,0,4]')
                if not self.constrain_ggHYield or self.float_muF: 
                  poiNames.append('muF')
		self.modelBuilder.doVar('muV[1,0,4]')
                poiNames.append('muV')
                self.modelBuilder.doSet('POI', ','.join(poiNames))

                params = {
                           'a_tilde' : 1.0,
                           'b_tilde' : 1.0,
                           'ps_sm_xs_ratio': 2.25
                         }

		self.modelBuilder.factory_('expr::a("cos(@0*{pi}/2)", alpha)'.format(pi=math.pi))
		self.modelBuilder.factory_('expr::b("sin(@0*{pi}/2)", alpha)'.format(pi=math.pi))
                
                self.modelBuilder.factory_('expr::sm_scaling("@0*@0-@0*@1*{a_tilde}/{b_tilde}", a, b)'.format(**params))
                self.modelBuilder.factory_('expr::ps_scaling("@1*@1-@0*@1*{b_tilde}/{a_tilde}", a, b)'.format(**params))
                self.modelBuilder.factory_('expr::mm_scaling("@0*@1/({a_tilde}*{b_tilde})", a, b)'.format(**params))

                cps = ['sm_scaling', 'ps_scaling', 'mm_scaling']
                for cp in cps:
                  self.modelBuilder.factory_('expr::muF_{cp}("@0*@1", muF, {cp})'.format(cp=cp))
                
                if self.constrain_ggHYield:
                  self.modelBuilder.factory_('expr::xs_sf("@0*@0 + @1*@1*{ps_sm_xs_ratio}", a, b)'.format(**params))
                  self.modelBuilder.factory_('expr::muF_xs_sf("@0*@1", muF, xs_sf)')
                  cps = ['sm_scaling', 'ps_scaling', 'mm_scaling']
                  for cp in cps:
                    self.modelBuilder.factory_('expr::muF_xs_sf_{cp}("@0*@1", muF_xs_sf, {cp})'.format(cp=cp))

                if self.lumi_scale is not None:
                  self.modelBuilder.factory_('expr::lumi_scaling("@0",{lumi_scale})'.format(lumi_scale=self.lumi_scale))
                  self.modelBuilder.factory_('expr::muF_lumi_scaling("@0*@1", muF, lumi_scaling)')
                  self.modelBuilder.factory_('expr::muV_lumi_scaling("@0*@1", muV, lumi_scaling)')
                  for cp in cps:
                    self.modelBuilder.factory_('expr::muF_{cp}_lumi_scaling("@0*@1*@2", muF, {cp}, lumi_scaling)'.format(cp=cp))

  

	def getYieldScale(self, bin, process):
		if self.DC.isSignal[process]:
			scalings = []	
			if 'ggH' in process: 
                          if not self.constrain_ggHYield or self.float_muF:
                            scalings.append('muF')
                          if self.constrain_ggHYield:
                            scalings.append('xs_sf')
                          if "ggHsm" in process:
    			    scalings.append('sm_scaling')
			  elif "ggHps" in process:
			    scalings.append('ps_scaling')
			  elif "ggHmm" in process: 
                            scalings.append('mm_scaling') 
                        if self.lumi_scale is not None: scalings.append('lumi_scaling')                        

                        scaling = '_'.join(scalings)
                        print 'Scaling %s/%s as %s' % (bin, process, scaling)  
			return scaling
		
		else: 
                  scalings = []
                  if any(x in process for x in ['qqH','WH','ZH']) and not 'hww' in process:
                          scalings.append('muV')
                  if self.lumi_scale is not None: 
                          scalings.append('lumi_scaling')

                  if scalings:
                    scaling = '_'.join(scalings)
                    print 'Scaling %s/%s as %s' % (bin, process,scaling)
                    return scaling
                  else:
                    #print 'Scaling %s/%s as 1' % (bin, process)
                    return 1

CPMixture = CPMixture()


