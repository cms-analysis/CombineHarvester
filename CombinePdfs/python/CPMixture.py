from HiggsAnalysis.CombinedLimit.PhysicsModel import PhysicsModel
import math

class CPMixture(PhysicsModel):
	def __init__(self):
	  PhysicsModel.__init__(self)
          self.constrain_ggHYield  = False
          self.lumi_scale = None
          self.muV_JHU = False
          self.new_def = False

	def setPhysicsOptions(self, physOptions):
                for po in physOptions:
                  if po.startswith("constrain_ggHYield"):
                    self.constrain_ggHYield = True
                  if po.startswith("muV_JHU"):
                    self.muV_JHU = True 
                  if po.startswith("new_def"):
                    self.new_def = True
                  if po.startswith('lumiScale='):
                    self.lumi_scale = po.replace('lumiScale=', '')

	def doParametersOfInterest(self):
		"""Create POI and other parameters, and define the POI set."""
		# --- POI and other parameters ----
	        
                poiNames = []
                
                self.modelBuilder.doVar('alpha[0,0,1]') 
                poiNames.append('alpha')
                self.modelBuilder.doVar('muF[1,0,4]')
                poiNames.append('muF')
		self.modelBuilder.doVar('muV[1,0,4]')
                poiNames.append('muV')
                self.modelBuilder.doSet('POI', ','.join(poiNames))

                params = {
                           'a_tilde' : 1.0, # Values of a_tilde and b_tilde specific to settings used to produce maximum-mixing MC for ggH
                           'b_tilde' : 1.0, 
                           'vbf_a_tilde' : 1.0, # Values of a_tilde and b_tilde specific to settings used to produce maximum-mixing MC for VBF
                           'vbf_b_tilde' : 0.297979018705,   
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
                
                # JHU samples have constant XS that does not depend on alpha. If the constrain_ggHYield option is set then add a scaling as a function of alpha -> XS = cos^2(alpha) + (3/2)^2*sin^2(alpha) to match MG5 XS                
                if self.constrain_ggHYield:
                  self.modelBuilder.factory_('expr::xs_sf("@0*@0 + @1*@1*{ps_sm_xs_ratio}", a, b)'.format(**params))
                  self.modelBuilder.factory_('expr::muF_xs_sf("@0*@1", muF, xs_sf)')
                  cps = ['sm_scaling', 'ps_scaling', 'mm_scaling']
                  for cp in cps:
                    self.modelBuilder.factory_('expr::muF_xs_sf_{cp}("@0*@1", muF_xs_sf, {cp})'.format(cp=cp))
                
                 
                # Add parameter f to float VBF shape for different CP mixtures
                # Scanning f between -1 and 1. Sign of f only determins whether the interference is positive or negative
                self.modelBuilder.doVar('f[0,-1,1]')
                poiNames.append('f')
                #self.modelBuilder.factory_('expr::sign("f/abs(f)", f)'.format(**params))
                #self.modelBuilder.factory_('expr::absf("abs(f)", f)'.format(**params))  
                # 
                #self.modelBuilder.factory_('expr::vbf_sm_scaling("1-@0-@1*sqrt(@0*(1-@0))*{vbf_a_tilde}/{vbf_b_tilde}", absf, sign)'.format(**params))
                #self.modelBuilder.factory_('expr::vbf_ps_scaling("@0-@1*sqrt(@0*(1-@0))*{vbf_b_tilde}/{vbf_a_tilde}", absf, sign)'.format(**params))
                #self.modelBuilder.factory_('expr::vbf_mm_scaling("@1*sqrt(@0*(1-@0))/({vbf_a_tilde}*{vbf_b_tilde})", absf, sign)'.format(**params))
                
                self.modelBuilder.factory_('expr::signf("@0/abs(@0)", f)')

                if not self.new_def:
                  # VBF definition of a3 and a1:
                  self.modelBuilder.factory_('expr::a1("sqrt(1-abs(@0))", f)')
                  self.modelBuilder.factory_('expr::a3("@0*sqrt(abs(@1))", signf, f)') 
                
                if self.new_def:
                  # Our definition of a1 and a3
                  self.modelBuilder.factory_('expr::a1("sqrt( (1-abs(@0))*@1 )", f, muV)')
                  self.modelBuilder.factory_('expr::a3("@0*sqrt( abs(@1)*@2 )*{vbf_b_tilde}", signf, f, muV)'.format(**params))

                self.modelBuilder.factory_('expr::vbf_sm_scaling("@0*@0 -@0*@1*{vbf_a_tilde}/{vbf_b_tilde}", a1, a3)'.format(**params))
                self.modelBuilder.factory_('expr::vbf_ps_scaling("@1*@1-@0*@1*{vbf_b_tilde}/{vbf_a_tilde}", a1, a3)'.format(**params))
                self.modelBuilder.factory_('expr::vbf_mm_scaling("@0*@1/({vbf_a_tilde}*{vbf_b_tilde})", a1, a3)'.format(**params))                

                if not self.new_def:
                  vbf_cps = ['vbf_sm_scaling', 'vbf_ps_scaling', 'vbf_mm_scaling']
                  for cp in vbf_cps: 
                    if not self.muV_JHU: 
                      self.modelBuilder.factory_('expr::ratioXS_JHU_SM("(1-@0+@0/({vbf_b_tilde}*{vbf_b_tilde})",absf)'.format(**params))
                      self.modelBuilder.factory_('expr::muV_{cp}("@0*@1/@2", muV, {cp}, ratioXS_JHU_SM)'.format(cp=cp))
                    else: self.modelBuilder.factory_('expr::muV_{cp}("@0*@1", muV, {cp})'.format(cp=cp))
                
                # if lumiScale=X option is set then scale all templates by X value
                if self.lumi_scale is not None:
                  self.modelBuilder.factory_('expr::lumi_scaling("@0",{lumi_scale})'.format(lumi_scale=self.lumi_scale))
                  self.modelBuilder.factory_('expr::muF_lumi_scaling("@0*@1", muF, lumi_scaling)')
                  self.modelBuilder.factory_('expr::muV_lumi_scaling("@0*@1", muV, lumi_scaling)')
                  for cp in cps:
                    self.modelBuilder.factory_('expr::muF_{cp}_lumi_scaling("@0*@1*@2", muF, {cp}, lumi_scaling)'.format(cp=cp))
                  for cp in vbf_cps:
                    self.modelBuilder.factory_('expr::muV_{cp}_lumi_scaling("@0*@1*@2", muF, {cp}, lumi_scaling)'.format(cp=cp))

	def getYieldScale(self, bin, process):
		if self.DC.isSignal[process]:
			scalings = []	
			if 'ggH' in process: 
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
                  if any(x in process for x in ['WH','ZH']) and not 'hww' in process:
                      scalings.append('muV')
                  if "qqH" in process and not 'hww' in process and not self.new_def:
                      scalings.append('muV')
                  if "qqHsm" in process:
                    scalings.append('vbf_sm_scaling')
                  elif "qqHps" in process:
                    scalings.append('vbf_ps_scaling')
                  elif "qqHmm" in process:
                    scalings.append('vbf_mm_scaling')

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


