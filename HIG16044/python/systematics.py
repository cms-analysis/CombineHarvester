import CombineHarvester.CombineTools.ch as ch

def AddSystematics(cb):
  src = cb.cp()
  
  signal = src.cp().signals().process_set()
  #rateParams
  src.cp().channel(['Zee','Zmm']).process(['TT']).AddSyst(cb,
     'SF_TT_norm_high_Zll', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7],1.0))

  src.cp().channel(['Zee','Zmm']).process(['Zj0b']).AddSyst(cb,
     'SF_Zj0b_norm_high_Zll', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7],1.0))

  src.cp().channel(['Zee','Zmm']).process(['Zj1b']).AddSyst(cb,
     'SF_Zj1b_norm_high_Zll', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7],1.0))

  src.cp().channel(['Zee','Zmm']).process(['Zj2b']).AddSyst(cb,
     'SF_Zj2b_norm_high_Zll', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7],1.0))

  src.cp().channel(['Zee','Zmm']).process(['TT']).AddSyst(cb,
     'SF_TT_norm_low_Zll', 'rateParam', ch.SystMap('bin_id')
     ([2,4,6,8],1.0))

  src.cp().channel(['Zee','Zmm']).process(['Zj0b']).AddSyst(cb,
     'SF_Zj0b_norm_low_Zll', 'rateParam', ch.SystMap('bin_id')
     ([2,4,6,8],1.0))

  src.cp().channel(['Zee','Zmm']).process(['Zj1b']).AddSyst(cb,
     'SF_Zj1b_norm_low_Zll', 'rateParam', ch.SystMap('bin_id')
     ([2,4,6,8],1.0))

  src.cp().channel(['Zee','Zmm']).process(['Zj2b']).AddSyst(cb,
     'SF_Zj2b_norm_low_Zll', 'rateParam', ch.SystMap('bin_id')
     ([2,4,6,8],1.0))

  src.cp().channel(['Znn']).process(['TT']).AddSyst(cb,
     'SF_TT_Znn', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7],1.0))

  src.cp().channel(['Znn']).process(['Zj0b']).AddSyst(cb,
     'SF_Zj0b_Znn', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7],1.0))

  src.cp().channel(['Znn']).process(['Zj1b']).AddSyst(cb,
     'SF_Zj1b_Znn', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7],1.0))

  src.cp().channel(['Znn']).process(['Zj2b']).AddSyst(cb,
     'SF_Zj2b_Znn', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,7],1.0))

  src.cp().channel(['Wen']).process(['TT']).AddSyst(cb,
     'SF_TT_Wln', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,6,7],1.0))

  src.cp().channel(['Wen']).process(['Wj0b']).AddSyst(cb,
     'SF_Wj0b_Wln', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,6,7],1.0))

  src.cp().channel(['Wen']).process(['Wj1b']).AddSyst(cb,
     'SF_Wj1b_Wln', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,6,7],1.0))

  src.cp().channel(['Wen']).process(['Wj2b']).AddSyst(cb,
     'SF_Wj2b_Wln', 'rateParam', ch.SystMap('bin_id')
     ([1,3,5,6,7],1.0))



  #Theory uncertainties
  src.cp().AddSyst(cb,
      'pdf_qqbar', 'lnN', ch.SystMap('channel','bin_id','process') 
       (['Zee','Zmm','Znn'], [1,2,3,4,5,6,7,8], ['ZH_hbb','WH_hbb'], 1.023) 
       (['Zee','Zmm'], [1,2,3,4,5,6,7,8], ['Zj0b','Zj1b','Zj2b','VVLF','VVHF'], 1.01)
       (['Znn'],[1,3,5,7],['VVLF','VVHF'],1.01)
       (['Wen'],[1,3,5,6,7],['ZH_hbb','WH_hbb','VVLF','VVHF',1.01)) 

  src.cp().AddSyst(cb,
      'pdf_gg', 'lnN', ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm','Znn'],[1,2,3,4,5,6,7,8],['ggZH_hbb'], 1.18)
      (['Zee','Zmm','Znn'],[1,2,3,4,5,6,7,8],['TT','s_Top','QCD'], 1.01)
      (['Wen', [1,3,5,6,7], ['s_Top'],1.01))
  
  src.cp().AddSyst(cb,
      'QCDScale_VH', 'lnN', ch.SystMap('channel','bin_id','process') 
      (['Zee','Zmm','Znn'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','WH_hbb'], 1.04)) 

  src.cp().AddSyst(cb,
      'QCDScale_VH_ggZHacceptance_highPt', 'lnN', ch.SystMap('channel','bin_id','process') 
      (['Zee','Zmm'],[1,3,5,7],['ggZH_hbb'], 1.32)
      (['Znn'],[1,3,5,7],['ggZH_hbb'], 1.32)) 

  src.cp().AddSyst(cb,
      'QCDScale_VH_ggZHacceptance_lowPt', 'lnN', ch.SystMap('channel','bin_id','process') 
      (['Zee','Zmm'],[2,4,6,8],['ggZH_hbb'], 1.32)
      (['Znn'],[1,3,5,7],['ggZH_hbb'],1.32)) 

  src.cp().AddSyst(cb,
      'QCDScale_ttbar', 'lnN', ch.SystMap('channel','bin_id','process') 
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['s_Top'], 1.06)
      (['Znn'],[1,3,5,7],['TT'],1.06)) 

  src.cp().AddSyst(cb,
      'QCDScale_VV', 'lnN', ch.SystMap('channel','bin_id','process') 
      (['Zee','Zmm','Znn'],[1,2,3,4,5,6,7,8],['VVLF','VVHF'], 1.04)) 

  src.cp().AddSyst(cb,
      'CMS_vhbb_boost_EWK_13TeV', 'lnN', ch.SystMap('channel','bin_id','process') 
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb'], 1.02)
      (['Znn'],[1,3,5,7],['ZH_hbb','WH_hbb','ggZH_hbb'],1.02)
      (['Wen'],[1,3,5,7],['WH_hbb','ZH_hbb'],1.02)) 

  src.cp().AddSyst(cb,
      'CMS_vhbb_boost_QCD_13TeV', 'lnN', ch.SystMap('channel','bin_id','process') 
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb'], 1.05)
      (['Znn'],[1,3,5,7],['ZH_hbb','WH_hbb','ggZH_hbb'],1.05)) 

  src.cp().AddSyst(cb,
      'CMS_vhbb_VV', 'lnN', ch.SystMap('channel','bin_id','process') 
      (['Zee','Zmm','Znn','Wen'],[1,2,3,4,5,6,7,8],['VVLF','VVHF'], 1.15)) 

  src.cp().AddSyst(cb,
      'CMS_vhbb_ST', 'lnN', ch.SystMap('channel','bin_id','process') 
      (['Zee','Zmm','Znn','Wen'],[1,2,3,4,5,6,7,8],['s_Top'], 1.15)) 

  src.cp().process(['ZH_hbb']).AddSyst(cb,
      'CMS_vhbb_LHE_weights_pdf_ZH', 'lnN', ch.SystMap('channel','bin_id') 
      (['Zee','Zmm','Znn','Wen'],[1,2,3,4,5,6,7,8],1.01)) 

  src.cp().process(['WH_hbb']).AddSyst(cb,
      'CMS_vhbb_LHE_weights_pdf_WH', 'lnN', ch.SystMap('channel','bin_id') 
      (['Znn','Wen'],[1,3,5,6,7],1.01)) 

  src.cp().process(['TT']).AddSyst(cb,
      'CMS_vhbb_LHE_weights_pdf_TT', 'lnN', ch.SystMap('channel','bin_id') 
      (['Zee','Zmm','Znn','Wen'],[1,2,3,4,5,6,7,8],1.005)) 

  src.cp().process(['Zj0b']).AddSyst(cb,
      'CMS_vhbb_LHE_weights_pdf_Zj0b', 'lnN', ch.SystMap('channel','bin_id') 
      (['Zee','Zmm','Znn'],[1,2,3,4,5,6,7,8],1.05)
      (['Wen'],[3,5,6,7],1.05)) 

  src.cp().process(['Zj1b']).AddSyst(cb,
      'CMS_vhbb_LHE_weights_pdf_Zj1b', 'lnN', ch.SystMap('channel','bin_id') 
      (['Zee','Zmm','Znn'],[1,2,3,4,5,6,7,8],1.03)
      (['Wen'],[5,6,7],1.03)) 

  src.cp().process(['Zj2b']).AddSyst(cb,
      'CMS_vhbb_LHE_weights_pdf_Zj2b', 'lnN', ch.SystMap('channel','bin_id') 
      (['Zee','Zmm','Znn'],[1,2,3,4,5,6,7,8],1.02)
      (['Wen'],[5,6,7],1.02)) 

  src.cp().process(['Wj0b']).AddSyst(cb,
      'CMS_vhbb_LHE_weights_pdf_Wj0b', 'lnN', ch.SystMap('channel','bin_id') 
      (['Znn'],[1,3,5,7],1.05)
      (['Wen'],[5,6,7],1.05)) 

  src.cp().process(['Wj1b']).AddSyst(cb,
      'CMS_vhbb_LHE_weights_pdf_Wj1b', 'lnN', ch.SystMap('channel','bin_id') 
      (['Znn','Wen'],[1,3,5,6,7],1.03)) 

  src.cp().process(['Wj2b']).AddSyst(cb,
      'CMS_vhbb_LHE_weights_pdf_Wj2b', 'lnN', ch.SystMap('channel','bin_id') 
      (['Znn','Wen'],[1,3,5,6,7],1.02)) 


  src.cp().process(['VVHF']).AddSyst(cb,
      'CMS_vhbb_LHE_weights_pdf_VVHF', 'lnN', ch.SystMap('channel','bin_id') 
      (['Zee','Zmm','Znn'],[1,2,3,4,5,6,7,8],1.02)
      (['Wen'],[1,5,6,7],1.02)) 

  src.cp().process(['VVLF']).AddSyst(cb,
      'CMS_vhbb_LHE_weights_pdf_VVLF', 'lnN', ch.SystMap('channel','bin_id') 
      (['Zee','Zmm','Znn'],[1,2,3,4,5,6,7,8],1.03)
      (['Wen'],[5,6,7],1.02)) 
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muR_ZH','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm','Znn','Wen'],[1,2,3,4,5,6,7,8],['ZH_hbb'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muF_ZH','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm','Znn','Wen'],[1,2,3,4,5,6,7,8],['ZH_hbb'],1.0))

  src.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muR_WH','shape',ch.SystMap('channel','bin_id','process')
      (['Znn','Wen'],[1,2,3,4,5,6,7,8],['WH_hbb'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muF_WH','shape',ch.SystMap('channel','bin_id','process')
      (['Znn','Wen'],[1,2,3,4,5,6,7,8],['WH_hbb'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muR_ggZH','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm','Znn'],[1,2,3,4,5,6,7,8],['ggZH_hbb'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muF_ggZH','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm','Znn'],[1,2,3,4,5,6,7,8],['ggZH_hbb'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muR_Zj0b','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm','Znn'],[1,2,3,4,5,6,7,8],['Zj0b'],1.0)
      (['Wen'],[3,5,6,7],['Zj0b'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muF_Zj0b','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm','Znn'],[1,2,3,4,5,6,7,8],['Zj0b'],1.0)
      (['Wen'],[3,5,6,7],['Zj0b'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muR_Zj1b','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm','Znn'],[1,2,3,4,5,6,7,8],['Zj1b'],1.0)
      (['Wen'],[3,5,6,7],['Zj1b'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muF_Zj1b','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm','Znn'],[1,2,3,4,5,6,7,8],['Zj1b'],1.0)
      (['Wen'],[3,5,6,7],['Zj1b'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muR_Zj2b','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm','Znn'],[1,2,3,4,5,6,7,8],['Zj2b'],1.0)
      (['Wen'],[3,5,6,7],['Zj2b'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muF_Zj2b','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm','Znn'],[1,2,3,4,5,6,7,8],['Zj2b'],1.0)
      (['Wen'],[3,5,6,7],['Zj2b'],1.0))

  src.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muR_Wj0b','shape',ch.SystMap('channel','bin_id','process')
      (['Znn','Wen'],[3,5,6,7],['Wj0b'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muF_Wj0b','shape',ch.SystMap('channel','bin_id','process')
      (['Znn','Wen'],[3,5,6,7],['Wj0b'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muR_Wj1b','shape',ch.SystMap('channel','bin_id','process')
      (['Znn'],[3,5,7],['Wj1b'],1.0)
      (['Wen'],[1,3,5,6,7],['Wj1b'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muF_Wj1b','shape',ch.SystMap('channel','bin_id','process')
      (['Znn'],[3,5,7],['Wj1b'],1.0)
      (['Wen'],[1,3,5,6,7],['Wj1b'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muR_Wj2b','shape',ch.SystMap('channel','bin_id','process')
      (['Znn'],[3,5,7],['Wj2b'],1.0)
      (['Wen'],[1,3,5,6,7],['Wj2b'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muF_Wj2b','shape',ch.SystMap('channel','bin_id','process')
      (['Znn'],[3,5,7],['Wj2b'],1.0)
      (['Wen'],[1,3,5,6,7],['Wj2b'],1.0))
  
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muR_TT','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm','Znn','Wen'],[1,2,3,4,5,6,7,8],['TT'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muF_TT','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm','Znn','Wen'],[1,2,3,4,5,6,7,8],['TT'],1.0))

  src.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muR_VVHF','shape',ch.SystMap('channel','bin_id','process')
      (['Wen'],[1,3,5,6,7],['VVHF'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muF_VVHF','shape',ch.SystMap('channel','bin_id','process')
      (['Wen'],[1,3,5,6,7],['VVHF'],1.0))

  src.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muR_VVLF','shape',ch.SystMap('channel','bin_id','process')
      (['Wen'],[3,5,6,7],['VVLF'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muF_VVLF','shape',ch.SystMap('channel','bin_id','process')
      (['Wen'],[3,5,6,7],['VVLF'],1.0))

  src.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muR_QCD','shape',ch.SystMap('channel','bin_id','process')
      (['Znn'],[1,3,5,7],['QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_LHE_weights_scale_muF_QCD','shape',ch.SystMap('channel','bin_id','process')
      (['Znn'],[1,3,5,7],['QCD'],1.0))

  
  
  #Experimental uncertainties
  src.cp().process(signal + ['s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b','QCD']).AddSyst(
        cb, 'lumi_13TeV','lnN', ch.SystMap('channel')
        (['Zee','Zmm','Znn'],1.026)
        (['Wen','Wmn'],1.025))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_puWeight','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'], [1],['ZH_hbb','WH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_ptwweights_tt','shape',ch.SystMap('channel','bin_id','process')
      (['Wen'],[1,3,5,6,7],['TT'],1.0))

  src.cp().AddSyst(cb,
      'CMS_vhbb_ptwweights_whf','shape',ch.SystMap('channel','bin_id','process')
      (['Wen'],[1,3,5,6,7],['s_Top','Wj1b','Wj2b'],1.0))

  src.cp().AddSyst(cb,
      'CMS_vhbb_ptwweights_wlf','shape',ch.SystMap('channel','bin_id','process')
      (['Wen'],[3,5,6,7],['Wj0b'],1.0))

  src.cp().AddSyst(cb,
      'CMS_vhbb_eff_e_Wln_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0))

  src.cp().AddSyst(cb,
      'CMS_vhbb_eff_e_trigger_Zll_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_eff_e_MVAID_Zll_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj1b','Zj2b','TT','VVLF'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_eff_e_tracker_Zll_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0))

  src.cp().AddSys5,t(cb,
      'CMS_vhbb_eff_m_trigger_Zll_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0))

  src.cp().AddSyst(cb,
      'CMS_vhbb_eff_m_MVAID_Zll_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0))

  src.cp().AddSyst(cb,
      'CMS_vhbb_eff_m_tracker_Zll_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0))

  src.cp().AddSyst(cb,
      'CMS_vhbb_eff_m_ISO_Zll_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0))

  src.cp().channel(['Znn']).process(signal+['VVHF','VVLF','s_Top','QCD']).AddSyst(cb,
      'CMS_vhbb_trigger_MET_13TeV','lnN',ch.SystMap('bin_id')
      ([1,3,5,7],1.02))


  src.cp().AddSyst(cb,
      'CMS_vhbb_EWK_Zll','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb'],1.0))
  
  #Jet energy scale
  src.cp().AddSyst(cb,
      'CMS_vhbb_res_j_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_PileUpDataMC_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_PileUpPtRef_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))

  
  src.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_PileUpPtBB_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_PileUpPtEC1_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_RelativeJEREC1_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_RelativeFSR_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_RelativeStatFSR_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_RelativeStatEC_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_RelativePtBB_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_RelativePtEC1_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_AbsoluteScale_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_AbsoluteMPFBias_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_AbsoluteStat_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_SinglePionECAL_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_SinglePionHCAL_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_Fragmentation_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_TimePtEta_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_scale_j_FlavorQCD_13TeV','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  
  #b-tagging uncertainties
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightJES_pt0_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightJES_pt0_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightJES_pt0_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightJES_pt1_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightJES_pt1_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightJES_pt1_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightJES_pt2_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightJES_pt2_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightJES_pt2_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightJES_pt3_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightJES_pt3_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightJES_pt3_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightJES_pt4_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightJES_pt4_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightJES_pt4_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLF_pt0_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLF_pt0_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLF_pt0_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLF_pt1_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLF_pt1_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLF_pt1_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLF_pt2_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLF_pt2_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLF_pt2_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLF_pt3_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLF_pt3_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLF_pt3_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLF_pt4_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLF_pt4_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLF_pt4_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHF_pt0_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHF_pt0_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHF_pt0_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHF_pt1_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHF_pt1_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHF_pt1_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHF_pt2_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHF_pt2_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHF_pt2_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHF_pt3_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHF_pt3_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHF_pt3_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHF_pt4_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHF_pt4_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHF_pt4_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats1_pt0_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats1_pt0_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats1_pt0_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats1_pt1_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats1_pt1_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats1_pt1_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats1_pt2_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats1_pt2_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats1_pt2_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats1_pt3_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats1_pt3_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats1_pt3_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats1_pt4_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats1_pt4_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats1_pt4_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats2_pt0_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats2_pt0_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats2_pt0_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats2_pt1_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats2_pt1_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats2_pt1_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats2_pt2_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats2_pt2_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats2_pt2_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats2_pt3_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats2_pt3_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats2_pt3_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats2_pt4_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats2_pt4_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightLFStats2_pt4_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats1_pt0_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats1_pt0_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats1_pt0_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats1_pt1_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats1_pt1_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats1_pt1_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats1_pt2_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats1_pt2_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats1_pt2_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats1_pt3_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats1_pt3_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats1_pt3_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats1_pt4_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats1_pt4_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats1_pt4_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats2_pt0_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats2_pt0_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats2_pt0_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats2_pt1_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats2_pt1_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats2_pt1_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats2_pt2_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats2_pt2_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats2_pt2_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats2_pt3_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats2_pt3_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats2_pt3_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats2_pt4_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats2_pt4_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightHFStats2_pt4_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr1_pt0_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr1_pt0_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr1_pt0_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr1_pt1_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr1_pt1_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr1_pt1_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr1_pt2_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr1_pt2_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr1_pt2_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr1_pt3_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr1_pt3_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr1_pt3_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr1_pt4_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr1_pt4_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr1_pt4_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr2_pt0_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr2_pt0_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr2_pt0_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr2_pt1_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr2_pt1_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr2_pt1_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr2_pt2_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr2_pt2_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr2_pt2_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr2_pt3_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr2_pt3_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
  
  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr2_pt3_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))

  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr2_pt4_eta1','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))

  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr2_pt4_eta2','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))

  src.cp().AddSyst(cb,
      'CMS_vhbb_bTagWeightcErr2_pt4_eta3','shape',ch.SystMap('channel','bin_id','process')
      (['Zee','Zmm'],[1,2,3,4,5,6,7,8],['ZH_hbb','ggZH_hbb','Zj0b','Zj1b','Zj2b','TT','VVLF'],1.0)
      (['Wen'],[1],['ZH_hbb','WH_hbb','s_Top','TT','Wj1b','Wj2b','VVHF'],1.0)
      (['Wen'],[3,5,6,7],['ZH_hbb','WH_hbb','s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],1.0)
      (['Znn'],[1],['ZH_hbb','ggZH_hbb','WH_hbb','Zj0b','Zj1b','Zj2b','TT','QCD'],1.0)
      (['Znn'], [3,5,7], signal+['Zj0b','Zj1b','Zj2b','Wj0b','Wj1b','Wj2b','TT','s_Top','QCD'],1.0))
