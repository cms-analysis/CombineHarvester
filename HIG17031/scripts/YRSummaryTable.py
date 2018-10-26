#!/usr/bin/env python
import argparse
import json
import math
# import pprint
import ROOT
import CombineHarvester.CombineTools.plotting as plot

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.TH1.AddDirectory(0)


def Translate(name, ndict):
    return ndict[name] if name in ndict else name


def ErrVal(poi_dict, error_label, warn=False, handleZero=False, scale=1.0):
    err_hi = poi_dict['%sHi' % error_label]
    err_lo = poi_dict['%sLo' % error_label]
    if poi_dict['ValidErrorHi'] and poi_dict['ValidErrorLo']:
        if err_hi == 0.0:
            print '%sHi is exactly zero' % error_label
            if handleZero:
                print 'Replacing with %sLo = %.4f' % (error_label, err_lo * -1.)
                err_hi = err_lo * -1.
        if err_lo == 0.0:
            print '%sLo is exactly zero' % error_label
            if handleZero:
                print 'Replacing with %sHi = %.4f' % (error_label, err_hi * -1.)
                err_lo = err_hi * -1.
        err = (err_hi - err_lo) / 2.
    elif poi_dict['ValidErrorHi'] and not poi_dict['ValidErrorLo']:
        print 'ErrorLo is not valid!'
        err = err_hi
    elif not poi_dict['ValidErrorHi'] and poi_dict['ValidErrorLo']:
        print 'ErrorHi is not valid!'
        err = -1. * err_lo
    else:
        print 'Neither ErrorLo or ErrorHi is valid!'
        err = 0.
    return err * scale


def ErrStr(poi_dict, error_label, fmt='%.1f'):
    # return '%.1f' % (100. * ErrVal(poi_dict, error_label))
    return fmt % (100. * poi_dict['%sSym' % error_label])

parser = argparse.ArgumentParser()

parser.add_argument('--model')
parser.add_argument('--height', type=int, default=600, help='Label next to the CMS logo')
parser.add_argument('--x-range', default='0,10', help='Label next to the CMS logo')
parser.add_argument('--translate')
parser.add_argument('--indir', default='plots-proj')
parser.add_argument('--scenarios', default='S1,S2')
parser.add_argument('--breakdown', default='Stat,SigInc,SigAcc,BkgTh,Exp')
parser.add_argument('--output', default='main_table_A1_5D.tex')
parser.add_argument('--POIs', default=None)
parser.add_argument('--subline', default=None)
parser.add_argument('--postfix', default=None)
parser.add_argument('--lumi', default='3000')
parser.add_argument('--y-label-size', default=0.08, type=float)
parser.add_argument('--translate-root')
parser.add_argument('--sync-stat', action='store_true')
parser.add_argument('--sync-bkgth', action='store_true')
parser.add_argument('--extra-label', default='')
parser.add_argument('--handle-zero-in-breakdown', action='store_true')
parser.add_argument('--convert-to-abs', default=None)
# parser.add_argument('--dump-json', default=None)

POIs = []
args = parser.parse_args()
breakdown = args.breakdown.split(',')
scenarios = args.scenarios.split(',')
lumis = args.lumi.split(',')

# Dictionary to translate parameter names
translate = {}
if args.translate is not None:
    with open(args.translate) as jsonfile:
        translate = json.load(jsonfile)


comb_strategy = {
    'Stat': 'combine',
    'SigInc': 'average',
    'SigAcc': 'average',
    'SigTh': 'average',
    'BkgTh': 'average',
    'Exp': 'combine'
}

X = dict()

with open('yr_cms_%s.json' % (args.model,)) as jsonfile:
    X['cms'] = json.load(jsonfile)

with open('yr_atlas_%s.json' % (args.model,)) as jsonfile:
    X['atlas'] = json.load(jsonfile)

l = args.lumi

X['combined'] = dict()
X['combined'][l] = dict()

# Get a list of POIs

for experiment in ['cms', 'atlas']:
    for POI in X[experiment][l][scenarios[0]].keys():
        if POI not in POIs:
            POIs.append(POI)

if args.POIs is not None:
    POIs = args.POIs.split(',')

for s in scenarios:
    X['combined'][l][s] = dict()
    for P in POIs:
        X['combined'][l][s][P] = dict()
        total_val = 0.
        total_val_c = 0.
        total_val_a = 0.
        for b in breakdown:
            if P in X['cms'][l][s]:
                c_val = X['cms'][l][s][P]['%sSym' % b]
            else:
                c_val = X['atlas'][l][s][P]['%sSym' % b]
            if P in X['atlas'][l][s]:
                a_val = X['atlas'][l][s][P]['%sSym' % b]
            else:
                a_val = X['cms'][l][s][P]['%sSym' % b]
            if comb_strategy[b] == 'average':
                val = (c_val + a_val) / 2.
            elif comb_strategy[b] == 'combine':
                val = math.sqrt(1. / ((1. / math.pow(c_val, 2)) + (1. / math.pow(a_val, 2))))
            print '%-10s %-20s %-15s %-10s CMS: %-4.3f ATLAS: %-4.3f Combined: %-4.3f' % (s, P, b, comb_strategy[b], c_val, a_val, val)
            total_val += math.pow(val, 2)
            total_val_c += math.pow(c_val, 2)
            total_val_a += math.pow(a_val, 2)
            X['combined'][l][s][P]['%sSym' % b] = val
        X['combined'][l][s][P]['ErrorSym'] = math.sqrt(total_val)
        # print 'SUM CMS: %-4.3f (%-4.3f) ATLAS %-4.3f (%-4.3f)' % (X['cms'][l][s][P]['ErrorSym'], math.sqrt(total_val_c), X['atlas'][l][s][P]['ErrorSym'], math.sqrt(total_val_a))
# Make the combination

# for l in lumis:
#     X[l] = dict()
#     for s in scenarios:
#         with open('%s/prefit_asimov_%s_%s.json' % (args.indir, s, l)) as jsonfile:
#             X[l][s] = json.load(jsonfile)[args.model]
#             if len(POIs) == 0:
#                 POIs = X[l][s].keys()

# print '\n'.join(POIs)

# if args.POIs is not None:
#     POIs = args.POIs.split(',')


# if args.convert_to_abs is not None:
#     with open(args.convert_to_abs) as jsonfile:
#         scaler = json.load(jsonfile)
# else:
#     scaler = {}
#     scaler['scalings'] = {}
#     for P in POIs:
#         scaler['scalings'][P] = [100.0]

# # Now go through all the input and symmetrise
# for l in lumis:
#     for s in scenarios:
#         for P in POIs:
#             print '>> Processing %s, %s, %s, Error' % (l, s, P)
#             X[l][s][P]['ErrorSym'] = ErrVal(X[l][s][P], 'Error', warn=True, handleZero=args.handle_zero_in_breakdown, scale=(scaler['scalings'][P][0] / 100.))
#             for b in breakdown:
#                 print '>> Processing %s, %s, %s, %s' % (l, s, P, b)
#                 X[l][s][P]['%sSym' % b] = ErrVal(X[l][s][P], b, warn=True, handleZero=args.handle_zero_in_breakdown, scale=(scaler['scalings'][P][0] / 100.))


# if args.sync_stat and 'Stat' in breakdown:
#     for l in lumis:
#         ref_s = scenarios[0]
#         for s in scenarios[1:]:
#             for P in POIs:
#                 curr_val = X[l][s][P]['StatSym']
#                 new_val = X[l][ref_s][P]['StatSym']
#                 print '>> Updating %s, %s, %s, Stat from %.4f to %.4f' % (l, s, P, curr_val, new_val)
#                 X[l][s][P]['StatSym'] = new_val

# if args.sync_bkgth and 'BkgTh' in breakdown:
#     for l in lumis:
#         ref_s = scenarios[0]
#         for s in scenarios[1:]:
#             for P in POIs:
#                 curr_val = X[l][s][P]['BkgThSym']
#                 ref_val = X[l][ref_s][P]['BkgThSym']
#                 if curr_val > ref_val:
#                     print '>> Updating %s, %s, %s, BkgTh from %.4f to %.4f' % (l, s, P, curr_val, ref_val)
#                     X[l][s][P]['BkgThSym'] = ref_val


# if args.dump_json is not None:
#     with open(args.dump_json, 'w') as outjson:
#         json.dump(
#             X, outjson, sort_keys=True, indent=4, separators=(',', ': '))

# nsubrows = len(scenarios)
# nsubcols = len(breakdown) + 1
# nbigcols = len(lumis)
# bigcol_header = 'c@{\hskip 0.15in} ' + ('c ' * (nsubcols - 1))

# if args.convert_to_abs:
#     full_header = '@{} l c c ' + ' @{\hskip 0.3in} '.join([bigcol_header] * nbigcols) + '@{}'
# else:
#     full_header = '@{} l c ' + ' @{\hskip 0.3in} '.join([bigcol_header] * nbigcols) + '@{}'

# plain = []
# output = []
# output.append('\\begin{tabular}{%s}' % full_header)
# output.append(' \\hline')
# hsections = []
# for i, l in enumerate(lumis):
#     if i < (len(lumis) - 1):
#         hsections.append('\\multicolumn{%i}{c@{\hskip 0.3in}}{%s $\\text{fb}^{-1}$}' % (nsubcols, l))
#     else:
#         hsections.append('\\multicolumn{%i}{c}{%s $\\text{fb}^{-1}$}' % (nsubcols, l))
# if args.convert_to_abs:
#     output.append('  &  &  & ' + ' & '.join(hsections) + ' \\\\')
#     output.append(('  & SM pred. [%s] &  & ' % scaler['units'][args.model]) + ' & '.join((['Total'] + breakdown) * nbigcols) + ' \\\\')
# else:
#     output.append('  &  & ' + ' & '.join(hsections) + ' \\\\')
#     output.append('  &  & ' + ' & '.join((['Total'] + breakdown) * nbigcols) + ' \\\\')
# output.append(' \\hline')


# for POI in POIs:
#     fmt = '%.1f'
#     if args.convert_to_abs:
#         fmt = '%.2f'
#     for i, s in enumerate(scenarios):
#         line = ''
#         pline = ''
#         if i == 0:
#             line += '\\multirow{%i}{*}{$%s$}' % (nsubrows, Translate(POI, translate))
#             pline += '|$%-40s$| %-5s | ' % (Translate(POI, translate), s)
#             if args.convert_to_abs:
#                 if POI in scaler['format']:
#                     fmt = scaler['format'][POI]
#                 nominal_sm = scaler['scalings'][POI][0]
#                 nominal_err = 0.
#                 for x in scaler['scalings'][POI][1:]:
#                     err = nominal_sm * x / 100.
#                     nominal_err += (err * err)
#                 nominal_err = math.sqrt(nominal_err)
#                 err_sm = [x * x * nominal_sm * nominal_sm for x in scaler['scalings'][POI][1:]]
#                 line += (' & \\multirow{%i}{*}{$' + fmt + '\\pm' + fmt + '$}') % (nsubrows, nominal_sm, nominal_err)
#         else:
#             line += '                       '
#             pline += '|%-40s  | %-5s | ' % ('', s)
#             if args.convert_to_abs:
#                 line += ' & '

#         line += ' & %s ' % s
#         for l in lumis:
#             line += ' & %s' % ErrStr(X[l][s][POI], 'Error', fmt=fmt)
#             pline += '%10s | ' % ErrStr(X[l][s][POI], 'Error', fmt=fmt)
#             for b in breakdown:
#                 line += '& %s ' % ErrStr(X[l][s][POI], b, fmt=fmt)
#                 pline += '%10s | ' % ErrStr(X[l][s][POI], b, fmt=fmt)
#         if i == len(scenarios) - 1:
#             line += ' \\\\[4pt]'
#         else:
#             line += ' \\\\[1pt]'
#         output.append(line)
#         plain.append(pline)

# output.append('\\hline')
# output.append('\\end{tabular}')

# print '\n'.join(output)
# print '\n'.join(plain)

# with open(args.output, 'w') as out_file:
#     out_file.write('\n'.join(output))


########################################################################
# Summary plot
########################################################################
scenarios = ['S1', 'S2']

translate = {}
if args.translate_root is not None:
    with open(args.translate_root) as jsonfile:
        translate = json.load(jsonfile)

POIs = list(reversed(POIs))

default_bar_styles = {
    'cms': {
        'S1': {
            'LineWidth': 1,
            'LineColor': ROOT.kRed,
            'MarkerSize': 0
        },
        'S2': {
            'LineWidth': 2,
            'LineColor': ROOT.kRed,
            'MarkerSize': 0
        },
        'Stat': {
            'LineWidth': 2,
            'LineColor': ROOT.kBlue,
            'MarkerSize': 0
        }
    },
    'atlas': {
        'S1': {
            'LineWidth': 1,
            'LineColor': ROOT.kBlue,
            'MarkerSize': 0
        },
        'S2': {
            'LineWidth': 2,
            'LineColor': ROOT.kBlue,
            'MarkerSize': 0
        },
        'Stat': {
            'LineWidth': 2,
            'LineColor': ROOT.kBlue,
            'MarkerSize': 0
        }
    },
    'combined': {
        'S1': {
            'LineWidth': 3,
            'LineColor': ROOT.kBlack,
            'MarkerSize': 0
        },
        'S2': {
            'LineWidth': 5,
            'LineColor': ROOT.kBlack,
            'MarkerSize': 0
        },
        'Stat': {
            'LineWidth': 3,
            'LineColor': ROOT.kBlue,
            'MarkerSize': 0
        }
    }
}

offsets = {
    'combined': 0.5,
    'cms': 0.12,
    'atlas': 0.30
}

plot.ModTDRStyle(l=0.18, b=0.10, height=args.height, t=0.06)
# ROOT.gStyle.SetNdivisions(510, 'XYZ')

if args.subline is None:
    subline = 'HL-LHC Projection'
    extra = ''
else:
    subline = args.subline
    extra = '_' + subline.lower()

for l in lumis:
    postfix = ''
    if args.postfix is not None:
        postfix = args.postfix
    canv = ROOT.TCanvas('yr_combined_summary_%s_%s%s' % (args.model, l, postfix), 'summary_%s_%s%s' % (args.model, l, postfix))
    pads = plot.OnePad()
    # pads[0].SetGrid(1, 0)
    pads[0].SetTickx(1)

    drawlist = []

    N = len(POIs)
    ntop = 1
    if N > 6:
        ntop = 2

    xmin = float(args.x_range.split(',')[0])
    xmax = float(args.x_range.split(',')[1])

    hframe = ROOT.TH2F("hframe", "hframe", 6, xmin, xmax, N + ntop, 0, N + ntop)

    relabel = {}

    for i, POI in enumerate(POIs):
        hframe.GetYaxis().SetBinLabel(i + 1, Translate(POI, translate))

    hframe.GetYaxis().LabelsOption('v')
    plot.Set(hframe.GetYaxis(), LabelSize=args.y_label_size, TickLength=0.)
    plot.Set(hframe.GetXaxis(), Title='Expected uncertainty', TickLength=0.01)

    hframe.Draw()
    graphs = []
    textline = {}
    for experiment in ['combined', 'atlas', 'cms']:
        for s in scenarios:
            gr_bar = ROOT.TGraphAsymmErrors(N)
            plot.Set(gr_bar, **default_bar_styles[experiment][s])
            for i, POI in enumerate(POIs):
                if POI not in X[experiment][l][s]:
                    continue
                # print 'Doing scenario %s, POI %s' % (s, POI)
                gr_bar.SetPoint(i, 0, float(i)+offsets[experiment])
                err_lo = 0.
                if s == 'Stat':
                    err_hi = X[experiment][l][scenarios[0]][POI]['StatSym']
                else:
                    err_hi = X[experiment][l][s][POI]['ErrorSym']
                gr_bar.SetPointError(i, err_lo, err_hi, 0., 0.)
                if experiment == 'combined':
                    if POI not in textline:
                        textline[POI] = list()
                    # textline[POI].append('#pm%.2f (%s)' % (err_hi, s))
                    textline[POI].append('%.3f (%s)' % (err_hi, s))
            graphs.append(gr_bar)

    ROOT.gStyle.SetEndErrorSize(4)
    for gr in graphs:
        gr.Draw('PSAME')
    pads[0].RedrawAxis()

    textline_box = ROOT.TLatex()
    plot.Set(textline_box, TextFont=42, TextAlign=12, TextSize=0.025)

    for i, POI in enumerate(POIs):
        textline_box.DrawLatex(0.67 * xmax, float(i) + 0.5, '; '.join(reversed(textline[POI])))


    # title_box = ROOT.TPaveText(xmin + (xmax-xmin)*0.01, float(N+1)-0.6, xmin + (xmax-xmin)*0.65, float(N+1)-0.2, 'NB')
    # title_box = ROOT.TPaveText(0.2, 0.85, 0.6, 0.92, 'NBNDC')
    title_box = ROOT.TPaveText(0.2, 0.80, 0.6, 0.92, 'NBNDC')
    title_box.SetTextFont(42)
    title_box.SetTextAlign(12)

    # title_box.AddText('#scale[1.4]{#bf{CMS}} #it{%s}' % subline)
    title_box.AddText('#scale[1.4]{#bf{ATLAS} and #bf{CMS}}')
    title_box.AddText('#it{%s}' % subline)
    plot.DrawTitle(pads[0], '%s fb^{-1}' % l, 3)
    title_box.SetMargin(0.0)
    title_box.Draw()

    if args.extra_label != '':
        plot.Set(textline_box, TextFont=42, TextAlign=12, TextSize=0.035)
        textline_box.DrawLatexNDC(0.2, 0.78, args.extra_label)
    # frame_h = 1. - pads[0].GetBottomMargin() - pads[0].GetTopMargin()
    # frame_frac = pads[0].GetBottomMargin() + (frame_h * ((float(N)+0.2)/float(N+1)))
    legend = ROOT.TLegend(0.6, 0.80, 0.95, 0.93, '', 'NBNDC')
    for i, s in enumerate(scenarios):
        if s == 'Stat':
            s = 'w/ Stat. uncert. only'
        if s in ['S1']:
            s = 'w/ Run 2 syst. uncert.'
        if s in ['S2']:
            s = 'w/ YR18 syst. uncert.'
        legend.AddEntry(graphs[i], s, 'L')
    # legend.SetNColumns(2)
    legend.Draw()

    legend_expt = ROOT.TLegend(0.64, 0.78, 0.95, 0.81, '', 'NBNDC')
    legend_expt.SetNColumns(2)
    legend_expt.AddEntry(graphs[3], 'ATLAS', "L")
    legend_expt.AddEntry(graphs[5], 'CMS', "L")
    legend_expt.Draw()

    canv.Print('.pdf')
    canv.Print('.png')

