import CombineHarvester.CombineTools.plotting as plot
import ROOT
import argparse
import json

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
plot.ModTDRStyle()

# CHANNELS = {
#     'et': 'e_{}#tau_{h}',
#     'mt': '#mu_{}#tau_{h}',
#     'em': 'e#mu',
#     'tt': '#tau_{h}#tau_{h}',
#     'mm': '#mu#mu'
# }

# LAYOUTS = {
#     "generic": [
#         ('QCD', {
#             'entries': ['QCD'],
#             'legend': 'QCD multijet',
#             'color': ROOT.TColor.GetColor(250, 202, 255)
#         }
#         ),
#         ('TT', {
#             'entries': ['TT'],
#             'legend': 't#bar{t}',
#             'color': ROOT.TColor.GetColor(155, 152, 204)
#         }
#         ),
#         ('EWK', {
#             'entries': ['W', 'VV'],
#             'legend': 'Electroweak',
#             'color': ROOT.TColor.GetColor(222, 90, 106)
#         }
#         ),
#         ('ZLL', {
#             'entries': ['ZL', 'ZJ'],
#             'legend': 'Z#rightarrowll',
#             'color': ROOT.TColor.GetColor(100, 192, 232)
#         }
#         ),
#         ('ZTT', {
#             'entries': ['ZTT'],
#             'legend': 'Z#rightarrow#tau#tau',
#             'color': ROOT.TColor.GetColor(248, 206, 104)
#         }
#         )
#     ]
# }

# # customise the layouts for each channel
# LAYOUTS['mt'] = deepcopy(LAYOUTS['generic'])
# LAYOUTS['et'] = deepcopy(LAYOUTS['generic'])
# LAYOUTS['tt'] = deepcopy(LAYOUTS['generic'])

# LAYOUTS['em'] = deepcopy(LAYOUTS['generic'])
# dict(LAYOUTS['em'])['ZLL']['entries'] = ['ZLL']

# LAYOUTS['mm'] = deepcopy(LAYOUTS['generic'])
# dict(LAYOUTS['mm'])['ZLL']['entries'] = ['ZLL']

parser = argparse.ArgumentParser()
# parser.add_argument('--input', '-i', help='Output of PostFitShapes or PostFitShapesFromWorkspace, specified as FILE:BIN')
parser.add_argument('--output', '-o', default=None, help='Output name')
# parser.add_argument('--channel', '-c', default='mt', choices=['mt', 'et', 'em', 'tt', 'mm'], help='Channel')
# parser.add_argument('--x-title', default='m_{ll}', help='x-axis variable, without GeV')
# parser.add_argument('--logy', action='store_true')
# parser.add_argument('--y-min', type=float, default=1)

args = parser.parse_args()

with open('xsec_res_svfit.json') as jsonfile:
    js = json.load(jsonfile)['ztt_xsec']

# Canvas and pads
canv = ROOT.TCanvas(args.output, args.output)
pads = plot.OnePad()
pads[0].SetTicks(1, -1)

axis = ROOT.TH2F('axis', '', 1, 1, 3, 9, 0, 9)
plot.Set(axis.GetYaxis(), LabelSize=0)
plot.Set(axis.GetXaxis(), Title='#sigma(pp#rightarrowZ/#gamma*) #times B(Z/#gamma*#rightarrow#tau#tau) [nb]')
axis.Draw()

theory_band = ROOT.TBox()
plot.Set(theory_band, FillColor=ROOT.kYellow)
plot.DrawVerticalBand(pads[0], theory_band, 2.0084-0.076, 2.0084+0.076)

theory_line = ROOT.TLine()
plot.Set(theory_line, LineColor=ROOT.kRed, LineStyle=2, LineWidth=2)
plot.DrawVerticalLine(pads[0], theory_line, 2.0084)

gr = ROOT.TGraphAsymmErrors(6)
plot.Set(gr, LineWidth=2, LineColor=ROOT.kBlue)

gr_stat = ROOT.TGraphAsymmErrors(6)
plot.Set(gr_stat, LineWidth=2)

y_pos = 7.5
x_text = 2.4

latex = ROOT.TLatex()
plot.Set(latex, TextAlign=12, TextSize=0.035)

gr.SetPoint(0, js['r']['Val'], y_pos)
gr.SetPointError(0, -1.*js['r']['ErrorLo'], js['r']['ErrorHi'], 0, 0)
gr_stat.SetPoint(0, js['r']['Val'], y_pos)
gr_stat.SetPointError(0, -1.*js['r']['SystLo'], js['r']['SystHi'], 0, 0)

latex.DrawLatex(x_text, y_pos, 'Combined')

i = 1
y_pos -= 1.0
order = ['et', 'mt', 'mm', 'em', 'tt']

chn_dict = {
    'et': '#tau_{e}#tau_{h}',
    'mt': '#tau_{#mu}#tau_{h}',
    'mm': '#tau_{#mu}#tau_{#mu}',
    'em': '#tau_{e}#tau_{#mu}',
    'tt': '#tau_{h}#tau_{h}'
}

for chn in order:
    key = 'r_%s' % chn
    gr.SetPoint(i, js[key]['Val'], y_pos)
    gr.SetPointError(i, -1.*js[key]['ErrorLo'], js[key]['ErrorHi'], 0, 0)
    gr_stat.SetPoint(i, js[key]['Val'], y_pos)
    gr_stat.SetPointError(i, -1.*js[key]['SystLo'], js[key]['SystHi'], 0, 0)
    latex.DrawLatex(x_text, y_pos, chn_dict[chn])

    i += 1
    y_pos -= 1.

gr.Draw('SAMEP')
gr_stat.Draw('SAMEP')


legend = ROOT.TLegend(0.18, 0.13, 0.45, 0.22, '', 'NBNDC')

legend.AddEntry(gr, 'Total uncertainty', 'LP')
legend.AddEntry(gr_stat, 'Systematic uncertainty', 'LP')
legend.Draw()
# # Get the data and create axis hist
# h_data = file.Get('%s/data_obs' % folder)
# h_axes = [h_data.Clone() for x in pads]
# for h in h_axes:
#     h.Reset()

# h_tot = file.Get('%s/TotalProcs' % folder)
# h_tot.SetFillColor(plot.CreateTransparentColor(12, 0.3))
# h_tot.SetMarkerSize(0)

# plot.StandardAxes(h_axes[0].GetXaxis(), h_axes[0].GetYaxis(), args.x_title, 'GeV', fmt='.0f')
# h_axes[0].Draw()

# # A dict to keep track of the hists
# h_store = {}

# layout = LAYOUTS[args.channel]

# stack = ROOT.THStack()


# for ele in layout:
#     info = ele[1]
#     hist = file.Get('%s/%s' % (folder, info['entries'][0]))
#     plot.Set(hist, FillColor=info['color'], Title=info['legend'])
#     if len(info['entries']) > 1:
#         for other in info['entries'][1:]:
#             hist.Add(file.Get('%s/%s' % (folder, other)))
#     h_store[ele[0]] = hist
#     stack.Add(hist)

# legend.AddEntry(h_data, 'Observed', 'PL')
# for ele in reversed(layout):
#     legend.AddEntry(h_store[ele[0]], '', 'F')
# legend.AddEntry(h_tot, 'Uncertainty', 'F')

# stack.Draw('HISTSAME')
# h_tot.Draw("E2SAME")
# h_data.Draw('SAME')

# if args.logy:
#     h_axes[0].SetMinimum(args.y_min)
#     pads[0].SetLogy(True)

# plot.FixTopRange(pads[0], plot.GetPadYMax(pads[0]), 0.30)
# legend.Draw()
# plot.FixBoxPadding(pads[0], legend, 0.05)

# # Do the ratio plot
# pads[1].cd()
# pads[1].SetGrid(0, 1)
# h_axes[1].Draw()

# r_data = plot.MakeRatioHist(h_data, h_tot, True, False)
# r_tot = plot.MakeRatioHist(h_tot, h_tot, True, False)
# r_tot.Draw('E2SAME')
# r_data.Draw('SAME')

# plot.SetupTwoPadSplitAsRatio(
#     pads, plot.GetAxisHist(
#         pads[0]), plot.GetAxisHist(pads[1]), 'Obs/Exp', True, 0.61, 1.39)

# Go back and tidy up the axes and frame
pads[0].cd()
pads[0].GetFrame().Draw()
pads[0].RedrawAxis()

# CMS logo
plot.DrawCMSLogo(pads[0], 'CMS', 'Preliminary', 11, 0.045, 0.05, 1.0, '', 1.0)
plot.DrawTitle(pads[0], '2.3 fb^{-1} (13 TeV)', 3)

# latex = ROOT.TLatex()
# plot.Set(latex, NDC=None, TextFont=42, TextSize=0.08)
# latex.DrawLatex(0.67, 0.57, CHANNELS[args.channel])
plot.DrawTitle(pads[0], '2.3 fb^{-1} (13 TeV)', 3)

# ... and we're done
canv.Print('.png')
canv.Print('.pdf')


