import CombineHarvester.CombineTools.ch as ch

def AddSystematics(cb):
  
  signal = cb.cp().signals().process_set()
  #rateParams
  cb.cp().channel(['Zee','Zmm']).process(['TT']).AddSyst(cb,
     'SF_TT_norm_high_Zll', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7],1.0))

  cb.cp().channel(['Zee','Zmm']).process(['Zj0b']).AddSyst(cb,
     'SF_Zj0b_norm_high_Zll', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7],1.0))

  cb.cp().channel(['Zee','Zmm']).process(['Zj1b']).AddSyst(cb,
     'SF_Zj1b_norm_high_Zll', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7],1.0))

  cb.cp().channel(['Zee','Zmm']).process(['Zj2b']).AddSyst(cb,
     'SF_Zj2b_norm_high_Zll', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7],1.0))

  cb.cp().channel(['Zee','Zmm']).process(['TT']).AddSyst(cb,
     'SF_TT_norm_low_Zll', 'rateParam', ch.SystMap('bin_id')
     ([2,4,6,8],1.0))

  cb.cp().channel(['Zee','Zmm']).process(['Zj0b']).AddSyst(cb,
     'SF_Zj0b_norm_low_Zll', 'rateParam', ch.SystMap('bin_id')
     ([2,4,6,8],1.0))

  cb.cp().channel(['Zee','Zmm']).process(['Zj1b']).AddSyst(cb,
     'SF_Zj1b_norm_low_Zll', 'rateParam', ch.SystMap('bin_id')
     ([2,4,6,8],1.0))

  cb.cp().channel(['Zee','Zmm']).process(['Zj2b']).AddSyst(cb,
     'SF_Zj2b_norm_low_Zll', 'rateParam', ch.SystMap('bin_id')
     ([2,4,6,8],1.0))

  cb.cp().channel(['Znn']).process(['TT']).AddSyst(cb,
     'SF_TT_Znn', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7],1.0))

  cb.cp().channel(['Znn']).process(['Zj0b']).AddSyst(cb,
     'SF_Zj0b_Znn', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7],1.0))

  cb.cp().channel(['Znn']).process(['Zj1b']).AddSyst(cb,
     'SF_Zj1b_Znn', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7],1.0))

  cb.cp().channel(['Znn']).process(['Zj2b']).AddSyst(cb,
     'SF_Zj2b_Znn', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7],1.0))
  
 #In the official cards these rateParams are also applied to Z->nn, why?
  cb.cp().channel(['Wen','Wmn','Znn']).process(['TT']).AddSyst(cb,
     'SF_TT_Wln', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,6,7],1.0))

  cb.cp().channel(['Wen','Wmn','Znn']).process(['Wj0b']).AddSyst(cb,
     'SF_Wj0b_Wln', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,6,7],1.0))

  cb.cp().channel(['Wen','Wmn','Znn']).process(['Wj1b']).AddSyst(cb,
     'SF_Wj1b_Wln', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,6,7],1.0))

  cb.cp().channel(['Wen','Wmn','Znn']).process(['Wj2b']).AddSyst(cb,
     'SF_Wj2b_Wln', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,6,7],1.0))


  #Set a sensible default for Z->ee/Z->mumu rate params.... althought this doesn't work atm
  for syst in cb.cp().channel(['Zee','Zmm']).syst_type(["rateParam"]).syst_name_set():
    cb.GetParameter(syst).set_range(0.0,5.0)

  #... and take the ranges from the cards for the other channels
  for syst in cb.cp().channel(['Znn']).syst_type(["rateParam"]).syst_name_set():
    if 'Znn' in syst:
      cb.GetParameter(syst).set_range(0.3,3.0)

  for syst in cb.cp().channel(['Wen','Wmn']).syst_type(["rateParam"]).syst_name_set():
    cb.GetParameter(syst).set_range(0.2,5.0)

  #Theory uncertainties
  cb.cp().AddSyst(cb,
      'pdf_qqbar', 'lnN', ch.SystMap('channel','bin_id','process') 
       (['Zee','Zmm','Znn'], [1,2,3,4,5,6,7,8], ['ZH_hbb','WH_hbb'], 1.023) 
       (['Zee','Zmm'], [1,2,3,4,5,6,7,8], ['Zj0b','Zj1b','Zj2b','VVLF','VVHF'], 1.01)
       (['Znn'],[1,3,5,7],['VVLF','VVHF'],1.01)
       (['Wen','Wmn'],[1,3,5,6,7],['ZH_hbb','WH_hbb','VVLF','VVHF'],1.01)) 

  cb.cp().AddSyst(cb,
      'pdf_gg', 'lnN', ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm','Znn'],[1,2,3,4,5,6,7,8],['ggZH_hbb'], 1.18)
      (['Zee','Zmm','Znn'],[1,2,3,4,5,6,7,8],['TT','s_Top','QCD'], 1.01)
      (['Wen','Wmn'], [1,3,5,6,7], ['s_Top'],1.01))

  #This uncertainty is in the workspace/combined card in the HCG repo but *not* in the per-channel cards committed there
  cb.cp().channel(['Zee','Zmm','Znn']).process(signal).AddSyst(cb,
      'BR_hbb', 'lnN', ch.SystMap()(1.024))

  #This uncertainty is in the workspace/combined card in the HCG repo but *not* in the per-channel cards committed there
  cb.cp().channel(['Zee','Zmm','Znn']).process(['WH_hbb','ZH_hbb']).AddSyst(cb,
      'pdf_HIGGS_qqbar', 'lnN', ch.SystMap()(1.023))
  
  cb.cp().AddSyst(cb,
      'QCDscale_VH', 'lnN', ch.SystMap('channel','bin_id','process') 
      (['Zee','Zmm','Znn'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','WH_hbb'], 1.04)) 

  cb.cp().AddSyst(cb,
      'QCDscale_VH_ggZHacceptance_highPt', 'lnN', ch.SystMap('channel','bin_id','process') 
      (['Zee','Zmm'],[1,3,5,7],['ggZH_hbb'], 1.32)
      (['Znn'],[1,3,5,7],['ggZH_hbb'], 1.32)) 

  cb.cp().AddSyst(cb,
      'QCDscale_VH_ggZHacceptance_lowPt', 'lnN', ch.SystMap('channel','bin_id','process') 
      (['Zee','Zmm'],[2,4,6,8],['ggZH_hbb'], 1.32)
      (['Znn'],[1,3,5,7],['ggZH_hbb'],1.32)) 

  cb.cp().AddSyst(cb,
      'QCDscale_ttbar', 'lnN', ch.SystMap('channel','bin_id','process') 
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['s_Top'], 1.06)
      (['Znn'],[1,3,5,7],['TT'],1.06)) 

  cb.cp().AddSyst(cb,
      'QCDscale_VV', 'lnN', ch.SystMap('channel','bin_id','process') 
      (['Zee','Zmm','Znn'],[1,2,3,4,5,6,7,8],['VVLF','VVHF'], 1.04)) 

  cb.cp().AddSyst(cb,
      'CMS_vhbb_boost_EWK_13TeV', 'lnN', ch.SystMap('channel','bin_id','process') 
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb'], 1.02)
      (['Znn'],[1,3,5,7],['ZH_hbb','WH_hbb','ggZH_hbb'],1.02)
      (['Wen','Wmn'],[1,3,5,7],['WH_hbb','ZH_hbb'],1.02)) 

  cb.cp().AddSyst(cb,
      'CMS_vhbb_boost_QCD_13TeV', 'lnN', ch.SystMap('channel','bin_id','process') 
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb'], 1.05)
      (['Znn'],[1,3,5,7],['ZH_hbb','WH_hbb','ggZH_hbb'],1.05)) 

  cb.cp().AddSyst(cb,
      'CMS_vhbb_VV', 'lnN', ch.SystMap('channel','bin_id','process') 
      (['Zee','Zmm','Znn','Wen','Wmn'],[1,2,3,4,5,6,7,8],['VVLF','VVHF'], 1.15)) 

  cb.cp().AddSyst(cb,
      'CMS_vhbb_ST', 'lnN', ch.SystMap('channel','bin_id','process') 
      (['Zee','Zmm','Znn','Wen','Wmn'],[1,2,3,4,5,6,7,8],['s_Top'], 1.15)) 

  cb.cp().process(['ZH_hbb']).AddSyst(cb,
      'CMS_vhbb_LHE_weights_pdf_ZH', 'lnN', ch.SystMap('channel','bin_id') 
      (['Zee','Zmm','Znn','Wen','Wmn'],[1,2,3,4,5,6,7,8],1.01)) 

  cb.cp().process(['WH_hbb']).AddSyst(cb,
      'CMS_vhbb_LHE_weights_pdf_WH', 'lnN', ch.SystMap('channel','bin_id') 
      (['Znn','Wen','Wmn'],[1,3,5,6,7],1.01)) 

  cb.cp().process(['TT']).AddSyst(cb,
      'CMS_vhbb_LHE_weights_pdf_TT', 'lnN', ch.SystMap('channel','bin_id') 
      (['Zee','Zmm','Znn','Wen','Wmn'],[1,2,3,4,5,6,7,8],1.005)) 

  cb.cp().process(['Zj0b']).AddSyst(cb,
      'CMS_vhbb_LHE_weights_pdf_Zj0b', 'lnN', ch.SystMap('channel','bin_id') 
      (['Zee','Zmm','Znn'],[1,2,3,4,5,6,7,8],1.05)
      (['Wen','Wmn'],[3,5,6,7],1.05)) 

  cb.cp().process(['Zj1b']).AddSyst(cb,
      'CMS_vhbb_LHE_weights_pdf_Zj1b', 'lnN', ch.SystMap('channel','bin_id') 
      (['Zee','Zmm','Znn'],[1,2,3,4,5,6,7,8],1.03)
      (['Wen','Wmn'],[3,5,6,7],1.03)) 

  cb.cp().process(['Zj2b']).AddSyst(cb,
      'CMS_vhbb_LHE_weights_pdf_Zj2b', 'lnN', ch.SystMap('channel','bin_id') 
      (['Zee','Zmm','Znn'],[1,2,3,4,5,6,7,8],1.02)
      (['Wen','Wmn'],[3,5,6,7],1.02)) 

  cb.cp().process(['Wj0b']).AddSyst(cb,
      'CMS_vhbb_LHE_weights_pdf_Wj0b', 'lnN', ch.SystMap('channel','bin_id') 
      (['Znn'],[1,3,5,7],1.05)
      (['Wen','Wmn'],[3,5,6,7],1.05)) 

  cb.cp().process(['Wj1b']).AddSyst(cb,
      'CMS_vhbb_LHE_weights_pdf_Wj1b', 'lnN', ch.SystMap('channel','bin_id') 
      (['Znn','Wen','Wmn'],[1,3,5,6,7],1.03)) 

  cb.cp().process(['Wj2b']).AddSyst(cb,
      'CMS_vhbb_LHE_weights_pdf_Wj2b', 'lnN', ch.SystMap('channel','bin_id') 
      (['Znn','Wen','Wmn'],[1,3,5,6,7],1.02)) 


  cb.cp().process(['VVHF']).AddSyst(cb,
      'CMS_vhbb_LHE_weights_pdf_VVHF', 'lnN', ch.SystMap('channel','bin_id') 
      (['Zee','Zmm','Znn'],[1,2,3,4,5,6,7,8],1.02)
      (['Wen','Wmn'],[1,3,5,6,7],1.02)) 

  cb.cp().process(['VVLF']).AddSyst(cb,
      'CMS_vhbb_LHE_weights_pdf_VVLF', 'lnN', ch.SystMap('channel','bin_id') 
      (['Zee','Zmm','Znn'],[1,2,3,4,5,6,7,8],1.03)
      (['Wen','Wmn'],[3,5,6,7],1.02)) 
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muR_ZH','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm','Znn','Wen','Wmn'],[1,2,3,4,5,6,7,8],['ZH_hbb'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muF_ZH','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm','Znn','Wen','Wmn'],[1,2,3,4,5,6,7,8],['ZH_hbb'],1.0))

  cb.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muR_WH','shape',ch.SystMap('channel','bin_id','process')
      (['Znn','Wen','Wmn'],[1,2,3,4,5,6,7,8],['WH_hbb'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muF_WH','shape',ch.SystMap('channel','bin_id','process')
      (['Znn','Wen','Wmn'],[1,2,3,4,5,6,7,8],['WH_hbb'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muR_ggZH','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm','Znn'],[1,2,3,4,5,6,7,8],['ggZH_hbb'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muF_ggZH','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm','Znn'],[1,2,3,4,5,6,7,8],['ggZH_hbb'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muR_Zj0b','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm','Znn'],[1,2,3,4,5,6,7,8],['Zj0b'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['Zj0b'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muF_Zj0b','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm','Znn'],[1,2,3,4,5,6,7,8],['Zj0b'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['Zj0b'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muR_Zj1b','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm','Znn'],[1,2,3,4,5,6,7,8],['Zj1b'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['Zj1b'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muF_Zj1b','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm','Znn'],[1,2,3,4,5,6,7,8],['Zj1b'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['Zj1b'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muR_Zj2b','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm','Znn'],[1,2,3,4,5,6,7,8],['Zj2b'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['Zj2b'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muF_Zj2b','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm','Znn'],[1,2,3,4,5,6,7,8],['Zj2b'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['Zj2b'],1.0))

  cb.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muR_Wj0b','shape',ch.SystMap('channel','bin_id','process')
      (['Znn','Wen','Wmn'],[3,5,6,7],['Wj0b'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muF_Wj0b','shape',ch.SystMap('channel','bin_id','process')
      (['Znn','Wen','Wmn'],[3,5,6,7],['Wj0b'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muR_Wj1b','shape',ch.SystMap('channel','bin_id','process')
      (['Znn'],[3,5,7],['Wj1b'],1.0)
      (['Wen','Wmn'],[1,3,5,6,7],['Wj1b'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muF_Wj1b','shape',ch.SystMap('channel','bin_id','process')
      (['Znn'],[3,5,7],['Wj1b'],1.0)
      (['Wen','Wmn'],[1,3,5,6,7],['Wj1b'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muR_Wj2b','shape',ch.SystMap('channel','bin_id','process')
      (['Znn'],[3,5,7],['Wj2b'],1.0)
      (['Wen','Wmn'],[1,3,5,6,7],['Wj2b'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muF_Wj2b','shape',ch.SystMap('channel','bin_id','process')
      (['Znn'],[3,5,7],['Wj2b'],1.0)
      (['Wen','Wmn'],[1,3,5,6,7],['Wj2b'],1.0))
  
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muR_TT','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm','Znn','Wen','Wmn'],[1,2,3,4,5,6,7,8],['TT'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muF_TT','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm','Znn','Wen','Wmn'],[1,2,3,4,5,6,7,8],['TT'],1.0))

  cb.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muR_VVHF','shape',ch.SystMap('channel','bin_id','process')
      (['Wen','Wmn'],[1,3,5,6,7],['VVHF'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muF_VVHF','shape',ch.SystMap('channel','bin_id','process')
      (['Wen','Wmn'],[1,3,5,6,7],['VVHF'],1.0))

  cb.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muR_VVLF','shape',ch.SystMap('channel','bin_id','process')
      (['Wen','Wmn'],[3,5,6,7],['VVLF'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muF_VVLF','shape',ch.SystMap('channel','bin_id','process')
      (['Wen','Wmn'],[3,5,6,7],['VVLF'],1.0))

  cb.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muR_QCD','shape',ch.SystMap('channel','bin_id','process')
      (['Znn'],[1,3,5,7],['QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muF_QCD','shape',ch.SystMap('channel','bin_id','process')
      (['Znn'],[1,3,5,7],['QCD'],1.0))

  
  
  #Experimental uncertainties
  cb.cp().process(signal + ['s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b','QCD']).AddSyst(
        cb, 'lumi_13TeV','lnN', ch.SystMap('channel')
        (['Zee','Zmm','Znn'],1.026)
        (['Wen','Wmn'],1.025))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_puWeight','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'], [1],['ZH_hbb','WH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_ptwweights_tt','shape',ch.SystMap('channel','bin_id','process')
      (['Wen','Wmn'],[1,3,5,6,7],['TT'],1.0))

  cb.cp().AddSyst(cb,
      'CMS_vhbb_ptwweights_whf','shape',ch.SystMap('channel','bin_id','process')
      (['Wen','Wmn'],[1,3,5,6,7],['s_Top','Wj1b','Wj2b'],1.0))

  cb.cp().AddSyst(cb,
      'CMS_vhbb_ptwweights_wlf','shape',ch.SystMap('channel','bin_id','process')
      (['Wen','Wmn'],[3,5,6,7],['Wj0b'],1.0))

  cb.cp().AddSyst(cb,
      'CMS_vhbb_eff_e_Wln_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0))

  cb.cp().AddSyst(cb,
      'CMS_vhbb_eff_m_Wln_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0))


  cb.cp().AddSyst(cb,
      'CMS_vhbb_eff_e_trigger_Zll_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_eff_e_MVAID_Zll_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj1b','Zj2b','TT','VVLF'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_eff_e_tracker_Zll_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0))

  cb.cp().AddSyst(cb,
      'CMS_vhbb_eff_m_trigger_Zll_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0))

  cb.cp().AddSyst(cb,
      'CMS_vhbb_eff_m_MVAID_Zll_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0))

  cb.cp().AddSyst(cb,
      'CMS_vhbb_eff_m_tracker_Zll_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0))

  cb.cp().AddSyst(cb,
      'CMS_vhbb_eff_m_ISO_Zll_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0))

  cb.cp().channel(['Znn']).process(signal+['VVHF','VVLF','s_Top','QCD']).AddSyst(cb,
      'CMS_vhbb_trigger_MET_13TeV','lnN',ch.SystMap('bin_id')
      ([1,3,5,7],1.02))


  cb.cp().AddSyst(cb,
      'CMS_vhbb_EWK_Zll','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb'],1.0))
  
  #Jet energy scale
  cb.cp().AddSyst(cb,
      'CMS_vhbb_res_j_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_PileUpDataMC_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_PileUpPtRef_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))

  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_PileUpPtBB_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_PileUpPtEC1_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))

  #Why is this only applied in W->lnu?
  cb.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_PileUpPtEC2_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_RelativeJEREC1_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_RelativeFSR_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_RelativeStatFSR_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_RelativeStatEC_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_RelativePtBB_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_RelativePtEC1_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0))
      #(['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0) #In the official cards uploaded to the HCG repo this is commented - why?
      #(['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))

  #Why is this only applied in W->lnu?
  cb.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_RelativePtEC2_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_AbsoluteScale_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_AbsoluteMPFBias_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_AbsoluteStat_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_SinglePionECAL_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_SinglePionHCAL_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_Fragmentation_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_TimePtEta_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_FlavorQCD_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  
  #b-tagging uncertainties
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightJES_pt0_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightJES_pt0_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightJES_pt0_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightJES_pt1_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightJES_pt1_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightJES_pt1_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightJES_pt2_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightJES_pt2_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightJES_pt2_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightJES_pt3_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightJES_pt3_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightJES_pt3_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightJES_pt4_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightJES_pt4_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightJES_pt4_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLF_pt0_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLF_pt0_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLF_pt0_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLF_pt1_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLF_pt1_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLF_pt1_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLF_pt2_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLF_pt2_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLF_pt2_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLF_pt3_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLF_pt3_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLF_pt3_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLF_pt4_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLF_pt4_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLF_pt4_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHF_pt0_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHF_pt0_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHF_pt0_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHF_pt1_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHF_pt1_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHF_pt1_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHF_pt2_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHF_pt2_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHF_pt2_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHF_pt3_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHF_pt3_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHF_pt3_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHF_pt4_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHF_pt4_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHF_pt4_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats1_pt0_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats1_pt0_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats1_pt0_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats1_pt1_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats1_pt1_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats1_pt1_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats1_pt2_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats1_pt2_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats1_pt2_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats1_pt3_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats1_pt3_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats1_pt3_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats1_pt4_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats1_pt4_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats1_pt4_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats2_pt0_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats2_pt0_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats2_pt0_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats2_pt1_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats2_pt1_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats2_pt1_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats2_pt2_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats2_pt2_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats2_pt2_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats2_pt3_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats2_pt3_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats2_pt3_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats2_pt4_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats2_pt4_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats2_pt4_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats1_pt0_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats1_pt0_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats1_pt0_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats1_pt1_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats1_pt1_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats1_pt1_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats1_pt2_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats1_pt2_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats1_pt2_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats1_pt3_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats1_pt3_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats1_pt3_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats1_pt4_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats1_pt4_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats1_pt4_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats2_pt0_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats2_pt0_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats2_pt0_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats2_pt1_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats2_pt1_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats2_pt1_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats2_pt2_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats2_pt2_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats2_pt2_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats2_pt3_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats2_pt3_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats2_pt3_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats2_pt4_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats2_pt4_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats2_pt4_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr1_pt0_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr1_pt0_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr1_pt0_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr1_pt1_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr1_pt1_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr1_pt1_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr1_pt2_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr1_pt2_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr1_pt2_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr1_pt3_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr1_pt3_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr1_pt3_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr1_pt4_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr1_pt4_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr1_pt4_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr2_pt0_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr2_pt0_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr2_pt0_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr2_pt1_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr2_pt1_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr2_pt1_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr2_pt2_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr2_pt2_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr2_pt2_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr2_pt3_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr2_pt3_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr2_pt3_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))

  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr2_pt4_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))

  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr2_pt4_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))

  cb.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr2_pt4_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen','Wmn'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen','Wmn'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','VVHF','VVLF','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))

def AddBinByBinSystematics(cb):

  for i in range(1,8):
    cb.cp().process(['TT']).channel(['Wen']).bin_id([1]).AddSyst(cb,
      'CMS_vhbb_statTT_WenHighPt_bin'+str(i)+'_13TeV','shape',ch.SystMap()(1.0))

  cb.cp().process(['VVHF']).channel(['Wen']).bin_id([1]).AddSyst(cb,
    'CMS_vhbb_statVVHF_WenHighPt_bin10_13TeV','shape',ch.SystMap()(1.0))

  for i in [4,6]:
    cb.cp().process(['VVLF']).channel(['Wen']).bin_id([1]).AddSyst(cb,
      'CMS_vhbb_statVVLF_WenHighPt_bin'+str(i)+'_13TeV','shape',ch.SystMap()(1.0))

  for i in [1,2,3,4,5,6,9,10]:
    cb.cp().process(['Wj0b']).channel(['Wen']).bin_id([1]).AddSyst(cb,
      'CMS_vhbb_statWj0b_WenHighPt_bin'+str(i)+'_13TeV','shape',ch.SystMap()(1.0))

  cb.cp().process(['Wj1b']).channel(['Wen']).bin_id([1]).AddSyst(cb,
    'CMS_vhbb_statWj1b_WenHighPt_bin1_13TeV','shape',ch.SystMap()(1.0))

  for i in [9,10]:
    cb.cp().process(['ZH_hbb']).channel(['Wen']).bin_id([1]).AddSyst(cb,
      'CMS_vhbb_statZH_hbb_WenHighPt_bin'+str(i)+'_13TeV','shape',ch.SystMap()(1.0))

  for i in [1,5]:
    cb.cp().process(['Zj0b']).channel(['Wen']).bin_id([1]).AddSyst(cb,
      'CMS_vhbb_statZj0b_WenHighPt_bin'+str(i)+'_13TeV','shape',ch.SystMap()(1.0))

  for i in [1,2,3,9]:
    cb.cp().process(['Zj1b']).channel(['Wen']).bin_id([1]).AddSyst(cb,
      'CMS_vhbb_statZj1b_WenHighPt_bin'+str(i)+'_13TeV','shape',ch.SystMap()(1.0))

  for i in [1,2,3,5]:
    cb.cp().process(['Zj2b']).channel(['Wen']).bin_id([1]).AddSyst(cb,
      'CMS_vhbb_statZj2b_WenHighPt_bin'+str(i)+'_13TeV','shape',ch.SystMap()(1.0))

  for i in [3,4,5,7,8,9]:
    cb.cp().process(['s_Top']).channel(['Wen']).bin_id([1]).AddSyst(cb,
      'CMS_vhbb_stats_Top_WenHighPt_bin'+str(i)+'_13TeV','shape',ch.SystMap()(1.0))

  for i in range(1,10):
    cb.cp().process(['TT']).channel(['Wmn']).bin_id([1]).AddSyst(cb,
      'CMS_vhbb_statTT_WmnHighPt_bin'+str(i)+'_13TeV','shape',ch.SystMap()(1.0))

  for i in [7,8,10]:
    cb.cp().process(['VVHF']).channel(['Wmn']).bin_id([1]).AddSyst(cb,
      'CMS_vhbb_statVVHF_WmnHighPt_bin'+str(i)+'_13TeV','shape',ch.SystMap()(1.0))

  for i in [1,3,4,5,9]:
    cb.cp().process(['VVLF']).channel(['Wmn']).bin_id([1]).AddSyst(cb,
      'CMS_vhbb_statVVLF_WmnHighPt_bin'+str(i)+'_13TeV','shape',ch.SystMap()(1.0))

  for i in range(1,11):
    cb.cp().process(['Wj0b']).channel(['Wmn']).bin_id([1]).AddSyst(cb,
      'CMS_vhbb_statWj0b_WmnHighPt_bin'+str(i)+'_13TeV','shape',ch.SystMap()(1.0))

  cb.cp().process(['Wj1b']).channel(['Wmn']).bin_id([1]).AddSyst(cb,
    'CMS_vhbb_statWj1b_WmnHighPt_bin2_13TeV','shape',ch.SystMap()(1.0))

  cb.cp().process(['Wj2b']).channel(['Wmn']).bin_id([1]).AddSyst(cb,
    'CMS_vhbb_statWj2b_WmnHighPt_bin1_13TeV','shape',ch.SystMap()(1.0))

  for i in [9,10]:
    cb.cp().process(['ZH_hbb']).channel(['Wmn']).bin_id([1]).AddSyst(cb,
      'CMS_vhbb_statZH_hbb_WmnHighPt_bin'+str(i)+'_13TeV','shape',ch.SystMap()(1.0))

  cb.cp().process(['Zj0b']).channel(['Wmn']).bin_id([1]).AddSyst(cb,
    'CMS_vhbb_statZj0b_WmnHighPt_bin3_13TeV','shape',ch.SystMap()(1.0))

  for i in [1,3]:
    cb.cp().process(['Zj1b']).channel(['Wmn']).bin_id([1]).AddSyst(cb,
      'CMS_vhbb_statZj1b_WmnHighPt_bin'+str(i)+'_13TeV','shape',ch.SystMap()(1.0))

  for i in range(1,4):
    cb.cp().process(['Zj2b']).channel(['Wmn']).bin_id([1]).AddSyst(cb,
      'CMS_vhbb_statZj2b_WmnHighPt_bin'+str(i)+'_13TeV','shape',ch.SystMap()(1.0))

  for i in [1,2,3,4,7,8]:
    cb.cp().process(['s_Top']).channel(['Wmn']).bin_id([1]).AddSyst(cb,
      'CMS_vhbb_stats_Top_WmnHighPt_bin'+str(i)+'_13TeV','shape',ch.SystMap()(1.0))

  cb.cp().process(['ggZH_hbb']).channel(['Zee']).bin_id([1]).AddSyst(cb,
    'CMS_vhbb_stats_bin1_ggZH_hbb_ZeeHighPt_13TeV','shape',ch.SystMap()(1.0))

  for i in range(1,15):
    cb.cp().process(['Zj0b']).channel(['Zee']).bin_id([1]).AddSyst(cb,
      'CMS_vhbb_stats_bin'+str(i)+'_Zj0b_ZeeHighPt_13TeV','shape',ch.SystMap()(1.0))

  for i in [4,5,6,7,8,9,10,12]:
    cb.cp().process(['Zj1b']).channel(['Zee']).bin_id([1]).AddSyst(cb,
      'CMS_vhbb_stats_bin'+str(i)+'_Zj1b_ZeeHighPt_13TeV','shape',ch.SystMap()(1.0))

  for i in [2,3,4,5,6,7]:
    cb.cp().process(['Zj2b']).channel(['Zee']).bin_id([1]).AddSyst(cb,
      'CMS_vhbb_stats_bin'+str(i)+'_Zj2b_ZeeHighPt_13TeV','shape',ch.SystMap()(1.0))

  for i in range(3,13):
    cb.cp().process(['TT']).channel(['Zee']).bin_id([1]).AddSyst(cb,
      'CMS_vhbb_stats_bin'+str(i)+'_TT_ZeeHighPt_13TeV','shape',ch.SystMap()(1.0))

  for i in [1,4,6,9,12,14]:
    cb.cp().process(['VVLF']).channel(['Zee']).bin_id([1]).AddSyst(cb,
      'CMS_vhbb_stats_bin'+str(i)+'_VVLF_ZeeHighPt_13TeV','shape',ch.SystMap()(1.0))

  for i in [2,3,14]:
    cb.cp().process(['VVHF']).channel(['Zee']).bin_id([1]).AddSyst(cb,
      'CMS_vhbb_stats_bin'+str(i)+'_VVHF_ZeeHighPt_13TeV','shape',ch.SystMap()(1.0))

  for i in range(6,12):
    cb.cp().process(['s_Top']).channel(['Zee']).bin_id([1]).AddSyst(cb,
      'CMS_vhbb_stats_bin'+str(i)+'_s_Top_ZeeHighPt_13TeV','shape',ch.SystMap()(1.0))

  for i in range(1,14):
    cb.cp().process(['Zj0b']).channel(['Zee']).bin_id([2]).AddSyst(cb,
      'CMS_vhbb_stats_bin'+str(i)+'_Zj0b_ZeeLowPt_13TeV','shape',ch.SystMap()(1.0))

  for i in range(1,15):
    cb.cp().process(['Zj1b']).channel(['Zee']).bin_id([2]).AddSyst(cb,
      'CMS_vhbb_stats_bin'+str(i)+'_Zj1b_ZeeLowPt_13TeV','shape',ch.SystMap()(1.0))

  for i in range(1,14):
    cb.cp().process(['Zj2b']).channel(['Zee']).bin_id([2]).AddSyst(cb,
      'CMS_vhbb_stats_bin'+str(i)+'_Zj2b_ZeeLowPt_13TeV','shape',ch.SystMap()(1.0))

  for i in range(1,15):
    cb.cp().process(['TT']).channel(['Zee']).bin_id([2]).AddSyst(cb,
      'CMS_vhbb_stats_bin'+str(i)+'_TT_ZeeLowPt_13TeV','shape',ch.SystMap()(1.0))

  for i in [2,3,4,5,6,7,8,14]:
    cb.cp().process(['VVLF']).channel(['Zee']).bin_id([2]).AddSyst(cb,
      'CMS_vhbb_stats_bin'+str(i)+'_VVLF_ZeeLowPt_13TeV','shape',ch.SystMap()(1.0))

  cb.cp().process(['VVHF']).channel(['Zee']).bin_id([2]).AddSyst(cb,
    'CMS_vhbb_stats_bin1_VVHF_ZeeLowPt_13TeV','shape',ch.SystMap()(1.0))

  for i in range(1,12):
    cb.cp().process(['s_Top']).channel(['Zee']).bin_id([2]).AddSyst(cb,
      'CMS_vhbb_stats_bin'+str(i)+'_s_Top_ZeeLowPt_13TeV','shape',ch.SystMap()(1.0))

  cb.cp().process(['ZH_hbb']).channel(['Zmm']).bin_id([1]).AddSyst(cb,
    'CMS_vhbb_stats_bin1_ZH_hbb_ZuuHighPt_13TeV','shape',ch.SystMap()(1.0))

  cb.cp().process(['ggZH_hbb']).channel(['Zmm']).bin_id([1]).AddSyst(cb,
    'CMS_vhbb_stats_bin1_ggZH_hbb_ZuuHighPt_13TeV','shape',ch.SystMap()(1.0))

  for i in [1,2,3,4,5,6,7,8,9,10,11,12,14]:
    cb.cp().process(['Zj0b']).channel(['Zmm']).bin_id([1]).AddSyst(cb,
      'CMS_vhbb_stats_bin'+str(i)+'_Zj0b_ZuuHighPt_13TeV','shape',ch.SystMap()(1.0))

  for i in range(2,11):
    cb.cp().process(['Zj1b']).channel(['Zmm']).bin_id([1]).AddSyst(cb,
      'CMS_vhbb_stats_bin'+str(i)+'_Zj1b_ZuuHighPt_13TeV','shape',ch.SystMap()(1.0))

  for i in range(4,7):
    cb.cp().process(['Zj2b']).channel(['Zmm']).bin_id([1]).AddSyst(cb,
      'CMS_vhbb_stats_bin'+str(i)+'_Zj2b_ZuuHighPt_13TeV','shape',ch.SystMap()(1.0))

  for i in range(2,13):
    cb.cp().process(['TT']).channel(['Zmm']).bin_id([1]).AddSyst(cb,
      'CMS_vhbb_stats_bin'+str(i)+'_TT_ZuuHighPt_13TeV','shape',ch.SystMap()(1.0))

  for i in [1,2,3,4,5,7,13,14]:
    cb.cp().process(['VVLF']).channel(['Zmm']).bin_id([1]).AddSyst(cb,
      'CMS_vhbb_stats_bin'+str(i)+'_VVLF_ZuuHighPt_13TeV','shape',ch.SystMap()(1.0))

  cb.cp().process(['VVHF']).channel(['Zmm']).bin_id([1]).AddSyst(cb,
    'CMS_vhbb_stats_bin2_VVHF_ZuuHighPt_13TeV','shape',ch.SystMap()(1.0))

  for i in range(3,12):
    cb.cp().process(['s_Top']).channel(['Zmm']).bin_id([1]).AddSyst(cb,
      'CMS_vhbb_stats_bin'+str(i)+'_s_Top_ZuuHighPt_13TeV','shape',ch.SystMap()(1.0))

  for i in range(1,15):
    cb.cp().process(['Zj0b']).channel(['Zmm']).bin_id([2]).AddSyst(cb,
      'CMS_vhbb_stats_bin'+str(i)+'_Zj0b_ZuuLowPt_13TeV','shape',ch.SystMap()(1.0))

  for i in range(1,15):
    cb.cp().process(['Zj1b']).channel(['Zmm']).bin_id([2]).AddSyst(cb,
      'CMS_vhbb_stats_bin'+str(i)+'_Zj1b_ZuuLowPt_13TeV','shape',ch.SystMap()(1.0))

  for i in range(2,14):
    cb.cp().process(['Zj2b']).channel(['Zmm']).bin_id([2]).AddSyst(cb,
      'CMS_vhbb_stats_bin'+str(i)+'_Zj2b_ZuuLowPt_13TeV','shape',ch.SystMap()(1.0))

  for i in range(1,15):
    cb.cp().process(['TT']).channel(['Zmm']).bin_id([2]).AddSyst(cb,
      'CMS_vhbb_stats_bin'+str(i)+'_TT_ZuuLowPt_13TeV','shape',ch.SystMap()(1.0))

  for i in [3,4,5,6,13,14]:
    cb.cp().process(['VVLF']).channel(['Zmm']).bin_id([2]).AddSyst(cb,
      'CMS_vhbb_stats_bin'+str(i)+'_VVLF_ZuuLowPt_13TeV','shape',ch.SystMap()(1.0))

  cb.cp().process(['VVHF']).channel(['Zmm']).bin_id([2]).AddSyst(cb,
    'CMS_vhbb_stats_bin1_VVHF_ZuuLowPt_13TeV','shape',ch.SystMap()(1.0))

  for i in range(1,14):
    cb.cp().process(['s_Top']).channel(['Zmm']).bin_id([2]).AddSyst(cb,
      'CMS_vhbb_stats_bin'+str(i)+'_s_Top_ZuuLowPt_13TeV','shape',ch.SystMap()(1.0))

  for i in [20,25,27,28]:
    cb.cp().process(['VVLF']).channel(['Znn']).bin_id([1]).AddSyst(cb,
      'CMS_vhbb_stats_bin'+str(i)+'_VVLF_Znn_13TeV_Signal','shape',ch.SystMap()(1.0))

  cb.cp().process(['Zj1b']).channel(['Znn']).bin_id([1]).AddSyst(cb,
    'CMS_vhbb_stats_bin35_Zj1b_Znn_13TeV_Signal','shape',ch.SystMap()(1.0))

  for i in [1,2,3,4,6,7,8,9,10,11,12,13,14,15,17,18,20,22,24,25,26,27,28,31,32]:
    cb.cp().process(['Wj0b']).channel(['Znn']).bin_id([1]).AddSyst(cb,
      'CMS_vhbb_stats_bin'+str(i)+'_Wj0b_Znn_13TeV_Signal','shape',ch.SystMap()(1.0))

  for i in [1,2,3,4,5,7,9,10,11,14,15,19,21,24,26,28,29,31,32]:
    cb.cp().process(['Wj1b']).channel(['Znn']).bin_id([1]).AddSyst(cb,
      'CMS_vhbb_stats_bin'+str(i)+'_Wj1b_Znn_13TeV_Signal','shape',ch.SystMap()(1.0))

  for i in [1,2,3,4,5,6,8,9,10,11,12,13,14,15,17,18,19,20,22,23,24,27,31,32,33,35]:
    cb.cp().process(['Wj2b']).channel(['Znn']).bin_id([1]).AddSyst(cb,
      'CMS_vhbb_stats_bin'+str(i)+'_Wj2b_Znn_13TeV_Signal','shape',ch.SystMap()(1.0))
