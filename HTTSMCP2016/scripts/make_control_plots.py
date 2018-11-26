import os

bins = ['100','101','102','103','104','105','106','107','108']
chans = ['em', 'mt', 'et', 'tt']

chans=['em']

plots = {}
plots['100'] = 'pt_1'
plots['101'] = 'pt_2'
plots['102'] = 'met'
plots['103'] = 'pt_tt'
plots['104'] = 'm_vis'
plots['105'] = 'mjj'
plots['106'] = 'sjdphi'
plots['107'] = 'n_jets'
plots['108'] = 'm_sv'

modes=['1','2','3']
year='2016'

for chn in chans:
  
  lep1=''
  lep2=''
  chn_label=''

  if chn == 'em':
    lep1 = 'e'
    lep2 = '#mu'
    chn_lab='e_{}#mu_{}'
  if chn == 'et':
    lep1 = 'e'
    lep2 = '#tau_{h}'
    chn_lab='e_{}#tau_{h}'
  if chn == 'mt':
    lep1 = '#mu'
    lep2 = '#tau_{h}'
    chn_lab='#mu_{}#tau_{h}'
  if chn == 'tt':
    lep1 = '#tau_{h}_{1}'
    lep2 = '#tau_{h}_{2}'
    chn_lab='#tau_{h}#tau_{h}'

  x_labels = {}
  x_labels['100'] = 'p_{T}^{%s} (GeV)' % lep1
  x_labels['101'] = 'p_{T}^{%s} (GeV)' % lep2
  x_labels['102'] = 'p_{T}^{miss} (GeV)'
  x_labels['103'] = 'p_{T}^{#tau#tau} (GeV)' 
  x_labels['104'] = 'm_{#tau#tau}^{vis} (GeV)'
  x_labels['105'] = 'm_{jj} (GeV)'
  x_labels['106'] = '#Delta#phi_{jj}'
  x_labels['107'] = 'N_{jets}'
  x_labels['108'] = 'm_{#tau#tau} (GeV)'

  for x in bins:

    for mode in modes:

      x_title = x_labels[x]
      y_title = 'dN/d%s' % x_title.split(' ')[0]
      if '(GeV)' in x_title: y_title+=' (1/GeV)'
  
      extra=''
  
      if 'm_sv' in plots[x]: extra=' --custom_x_range --x_axis_min=50 --x_axis_max=300 '
      if 'pt_1' in plots[x]: 
        if chn == 'em': extra=' --custom_x_range --x_axis_min=10 --x_axis_max=100 '
        if chn == 'et' or chn =='mt': extra=' --custom_x_range --x_axis_min=20 --x_axis_max=100 '
        if chn == 'tt': extra=' --custom_x_range --x_axis_min=50 --x_axis_max=100 '
      if 'pt_2' in plots[x]: 
        if chn == 'em': extra=' --custom_x_range --x_axis_min=10 --x_axis_max=100 '
        if chn == 'et' or chn =='mt': extra=' --custom_x_range --x_axis_min=30 --x_axis_max=100 '
        if chn == 'tt': extra=' --custom_x_range --x_axis_min=40 --x_axis_max=100 '
      if 'met' in plots[x]: 
        extra=' --custom_x_range --x_axis_min=0 --x_axis_max=100 '

      if 'sjdphi' in plots[x]: extra+= ' --extra_pad=0.5 '
  
      mode_str=''
      if mode == '2': mode_str='lowmsv_'
      if mode == '3': mode_str='himsv_'
  
      outname='%s_%s_%s%s' % (plots[x], chn, mode_str, year)
  
      command='python $CMSSW_BASE/src/CombineHarvester/HTTSMCP2016/scripts/postFitControlPlot.py -f shapes_%s_control_2016_%s.root  --file_dir=%s_13TeV_prefit --mode prefit --no_signal --ratio --x_title="%s" --y_title="%s" --outname="%s" --channel_label="%s" %s' % (chn, mode, x, x_title, y_title, outname, chn_lab, extra)
 
      print command 

      os.system(command)
