import os

chns = ['et','mt']
cats = ['1','8','9']
crs  = ['far','near']
#tauiso = ['nominaltauiso','vloosetau','loosetau','antiisotau']
modes = ['prefit','postfit']

for chn in chns:
  for cat in cats:
    for cr in crs:
#      for iso in tauiso:
      os.system("PostFitShapesFromWorkspace -d output/qcd_1209_%(cr)s/htt_%(chn)s_%(cat)s_13TeV/htt_%(chn)s_%(cat)s_13TeV.txt -w output/qcd_1209_%(cr)s/htt_%(chn)s_%(cat)s_13TeV/ws.root -o %(cr)s_%(chn)s_%(cat)s_shapes.root --print  --postfit --sampling -f output/qcd_1209_%(cr)s/htt_%(chn)s_%(cat)s_13TeV/mlfit.Test.root:fit_s"%vars())
      for mode in modes: 
        os.system('python scripts/QCDStudyPostFitPlot.py --file=%(cr)s_%(chn)s_%(cat)s_shapes.root --ratio --extra_pad=0.3 --custom_x_range --x_axis_max=250 --x_axis_min=0.0 --dir="htt_%(chn)s_%(cat)s_13TeV" --mode=%(mode)s'%vars())

