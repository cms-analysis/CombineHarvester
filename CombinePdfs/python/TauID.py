from HiggsAnalysis.CombinedLimit.PhysicsModel import PhysicsModel
import math

class TauID(PhysicsModel):
	def __init__(self):
	  PhysicsModel.__init__(self)
          self.useMC = False
          self.fitEff = False
	def setPhysicsOptions(self, physOptions):
                for po in physOptions:
                  if po.startswith("useMC"):
                    self.useMC = True
                  if po.startswith("fitEff"):
                    self.fitEff = True

	def doParametersOfInterest(self):
		"""Create POI and other parameters, and define the POI set."""
		# --- POI and other parameters ----
	        
                poiNames = []
               
                self.modelBuilder.doVar('SF[1,0.5,1.5]') 
                poiNames.append('SF')
                self.modelBuilder.factory_('expr::SF_fail("(1-@0)", SF)')
                self.modelBuilder.doSet('POI', ','.join(poiNames))
                
	def getYieldScale(self, bin, process):
                scalings = []
                if bin in ['htt_mt_1_13TeV','htt_et_1_13TeV']:
                  if self.fitEff:
                    if 'ZTT' in process or 'TTT' in process or 'VVT' in process:
                      scalings.append('SF')
                  else:
                    if 'ZTT_pass' in process: 
                      scalings.append('SF')
                    if self.useMC and ('VVTpass' in process or 'TTTpass' in process):
                      scalings.append('SF')
                    if 'fail' in process: return 0
                if bin in ['htt_mt_2_13TeV','htt_et_2_13TeV']:
                  if self.fitEff:
                    if 'ZTT' in process or 'TTT' in process or 'VVT' in process:
                      scalings.append('SF_fail')
                  else:
                    if 'ZTT_pass' in process:
                      scalings.append('SF_fail')
                    if self.useMC and ('VVTpass' in process or 'TTTpass' in process):
                      scalings.append('SF_fail') 
                if len(scalings)>0:
                  scaling = '_'.join(scalings)
                  print 'Scaling %s/%s as %s' % (bin, process, scaling)
                  return scaling
                else: 
                  return 1

TauID = TauID()


