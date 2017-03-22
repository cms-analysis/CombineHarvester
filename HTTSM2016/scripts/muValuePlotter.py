# This macro makes the muValue v.s. different final state or v.s. different categories.
# The input to this macro is mu_XXX.json which XXX could be either channels or categories
#  python muValuePlotter.py  -o out -t category
#  python muValuePlotter.py  -o out -t channel

import plotting as plot
import ROOT
import argparse
import json

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
plot.ModTDRStyle()



parser = argparse.ArgumentParser()
# parser.add_argument('--input', '-i', help='Output of PostFitShapes or PostFitShapesFromWorkspace, specified as FILE:BIN')
parser.add_argument('--output', '-o', default=None, help='Output name')
parser.add_argument('--typet', '-t', default='cat', help='category or channel')
# parser.add_argument('--channel', '-c', default='mt', choices=['mt', 'et', 'em', 'tt', 'mm'], help='Channel')
# parser.add_argument('--x-title', default='m_{ll}', help='x-axis variable, without GeV')
# parser.add_argument('--logy', action='store_true')
# parser.add_argument('--y-min', type=float, default=1)

args = parser.parse_args()

Type=args.typet

# Canvas and pads
canv = ROOT.TCanvas(args.output, args.output)
pads = plot.OnePad()
pads[0].SetTicks(1, -1)

axis = ROOT.TH2F('axis', '', 1, -.5, 2.5, 10, 0, 10)
plot.Set(axis.GetYaxis(), LabelSize=0)
plot.Set(axis.GetXaxis(), Title='Best fit #mu = #sigma/#sigma_{SM}')
axis.Draw()



y_pos = 8.5
x_text = 1.85

latex = ROOT.TLatex()
latexNum = ROOT.TLatex()
plot.Set(latex, TextAlign=12, TextSize=0.035)
plot.Set(latexNum, TextAlign=12, TextSize=0.025)


Channel_Category_Name={
    'category' : {
        '0jet': '0jet',
        'boosted': 'boosted',
        'vbf': 'vbf',
        'cmb': 'combined'
    },
    'channel' : {
        'et': '#tau_{e}#tau_{h}',
        'mt': '#tau_{#mu}#tau_{h}',
        'em': '#tau_{e}#tau_{#mu}',
        'tt': '#tau_{h}#tau_{h}',
        'cmb': 'combined'
    }
}

i = 0
y_pos -= 1.0

chn = '120.0'

if Type=='channel': proc = ['em','et', 'mt', 'tt','cmb']
elif Type=='category': proc = ['0jet','boosted', 'vbf','cmb']
else:  print 'either select category or channel'

gr = ROOT.TGraphAsymmErrors(len(proc))
plot.Set(gr, LineWidth=2, LineColor=ROOT.kBlue)


for pro in proc:
    with open('Mu_%s.json'%pro) as jsonfile:
        js = json.load(jsonfile)

        mean=round(js[chn]['obs'], 2)
        up= round(js[chn]['exp+1']-mean,2)
        down=round(mean-js[chn]['exp-1'],2)
        
        gr.SetPoint(i, mean, y_pos)
        gr.SetPointError(i,down ,up, 0, 0)
        
        latex.DrawLatex(x_text, y_pos+0.25, Channel_Category_Name[Type][pro])
        latexNum.DrawLatex(x_text, y_pos-0.25, str(mean)+'#splitline{ +%s}{ -%s}'%(str(up),str(down)))
        if pro=='cmb':  combineMu= mean; lowBnad=down; highBand=up;
        i += 1
        y_pos -= 1.5

gr.Draw('SAMEP')


theory_band = ROOT.TBox(combineMu-lowBnad,0,combineMu+highBand,10)
theory_band.SetFillColor(ROOT.kYellow)
theory_band.Draw('same')

l=ROOT.TLine(combineMu,0,combineMu,10)
l.Draw('sameL')

gr.Draw('SAMEP')


legend = ROOT.TLegend(0.18, 0.13, 0.45, 0.22, '', 'NBNDC')
legend.Draw()


# Go back and tidy up the axes and frame
pads[0].cd()
pads[0].GetFrame().Draw()
#pads[0].RedrawAxis()

# CMS logo
plot.DrawCMSLogo(pads[0], 'CMS', 'Preliminary', 11, 0.045, 0.05, 1.0, '', 1.0)
plot.DrawTitle(pads[0], '35.9 fb^{-1} (13 TeV)', 3)


# ... and we're done
canv.Print('.png')
canv.Print('.pdf')


