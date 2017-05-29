import os

chns = ['et','mt']
cats = ['1','8','9']
crs  = ['far','near','all']
#tauiso  = ['loose','tight']
#tauiso = ['nominaltauiso','vloosetau','loosetau','antiisotau']
modes = ['prefit','postfit']

for chn in chns:
  for cat in cats:
    for cr in crs:
#      for iso in tauiso:
      os.system("PostFitShapesFromWorkspace -d output/qcd_osss_full2016_2505_%(cr)s/htt_%(chn)s_%(cat)s_13TeV/htt_%(chn)s_%(cat)s_13TeV.txt -w output/qcd_osss_full2016_2505_%(cr)s/htt_%(chn)s_%(cat)s_13TeV/ws.root -o %(cr)s_%(chn)s_%(cat)s_shapes.root --print  --postfit --sampling -f output/qcd_osss_full2016_2505_%(cr)s/htt_%(chn)s_%(cat)s_13TeV/mlfit.Test.root:fit_s"%vars())
      for mode in modes: 
        os.system('python scripts/QCDStudyPostFitPlot.py --file=%(cr)s_%(chn)s_%(cat)s_shapes.root --ratio --extra_pad=0.3 --custom_x_range --x_axis_max=400 --x_axis_min=0.0 --dir="htt_%(chn)s_%(cat)s_13TeV" --channel=%(chn)s --mode=%(mode)s'%vars())

