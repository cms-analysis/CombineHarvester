#!/usr/bin/env python
import argparse
import json
import math


def Translate(name, ndict):
    return ndict[name] if name in ndict else name


parser = argparse.ArgumentParser()

parser.add_argument('--model')
parser.add_argument('--obs-run2', default=None)
parser.add_argument('--exp-run2', default=None)
parser.add_argument('--obs-run1', default=None)
parser.add_argument('--exp-run1', default=None)
parser.add_argument('--add-run1', action='store_true')
parser.add_argument('--translate')

args = parser.parse_args()


MODS = ['A1_ttH_5D', 'A1_ttH_E', 'A1_ttH']

ORDER = {
    'A1_ttH_5D': ['mu_XS_ttH_BR_%s' % x for x in ['ZZ', 'WW', 'gamgam', 'tautau', 'bb']],
    'A1_ttH_E': ['mu_XS8_ttH', 'mu_XS13_ttH'],
    'A1_ttH': ['mu_XS_ttH']
}

TRANSLATE = {
    'mu_XS_ttH_BR_ZZ': '\\mu_{\\text{ttH}}^{\\text{ZZ}}',
    'mu_XS_ttH_BR_WW': '\\mu_{\\text{ttH}}^{\\text{WW}}',
    'mu_XS_ttH_BR_gamgam': '\\mu_{\\text{ttH}}^{\\gamma\\gamma}',
    'mu_XS_ttH_BR_tautau': '\\mu_{\\text{ttH}}^{\\tau\\tau}',
    'mu_XS_ttH_BR_bb': '\\mu_{\\text{ttH}}^{\\text{bb}}',
    'mu_XS8_ttH': '\\mu_{\\text{ttH}}^{\\text{7+8 TeV}}',
    'mu_XS13_ttH': '\\mu_{\\text{ttH}}^{\\text{13 TeV}}',
    'mu_XS_ttH': '\\mu_{\\text{ttH}}'
}

for i, model in enumerate(MODS):
    run2model = model
    if args.model == 'K2_BSM':
        run2model = 'K2Inv'
        run2model = 'K2Inv'

    # Dictionary to translate parameter names
    translate = {}
    if args.translate is not None:
        with open(args.translate) as jsonfile:
            translate = json.load(jsonfile)
    translate = TRANSLATE

    obs_run2 = {}
    if args.obs_run2 is not None:
        with open(args.obs_run2) as jsonfile:
            obs_run2 = json.load(jsonfile)[run2model]

    exp_run2 = {}
    if args.exp_run2 is not None:
        with open(args.exp_run2) as jsonfile:
            exp_run2 = json.load(jsonfile)[run2model]


    obs_run1 = {}
    if args.obs_run1 is not None:
        with open(args.obs_run1) as jsonfile:
            obs_run1 = json.load(jsonfile)[model]

    exp_run1 = {}
    if args.exp_run1 is not None:
        with open(args.exp_run1) as jsonfile:
            exp_run1 = json.load(jsonfile)[model]

    # POIs = exp_run2.keys()
    POIs = ORDER[model]

    # print """\\begin{table}[h!]
    # \\centering
    # """

    if i == 0:
        structure = '@{} l r@{}l c c c c '
        if args.add_run1:
            structure += 'r@{}l c c c c '
        structure += '@{}'
        print '\\begin{tabular}{%s}' % structure
        print ' \\hline'

        model_str = args.model.replace('_', '\\_')

        if args.add_run1:
            print '\\textbf{%s Model}  & \\multicolumn{6}{c}{Run1+13 TeV} & \\multicolumn{6}{c}{13 TeV}  \\\\' % model_str
            print ' \\hline'
            print '           &            &                 & \\multicolumn{4}{c}{Uncertainty} &               &              & \\multicolumn{4}{c}{Uncertainty}  \\\\'
            print 'Parameters & \\multicolumn{2}{c}{Best-fit} & Stat. & Exp. & BkgTh. & SigTh.                  & \\multicolumn{2}{c}{Best-fit} & Stat. & Exp. & BkgTh. & SigTh.                   \\\\'
        else:
            # print '\\textbf{%s Model}  & \\multicolumn{6}{c}{Run1+13 TeV} \\\\' % model_str
            # print ' \\hline'
            print '           &            &                 & \\multicolumn{4}{c}{Uncertainty} \\\\'
            print 'Parameters & \\multicolumn{2}{c}{Best-fit} & Stat. & Exp. & BkgTh. & SigTh. \\\\'

    print '\\hline\\\\ [-1.5ex]'

    for POI in POIs:
        line = '\\multirow{2}{*}{$%s$} & ' % Translate(POI, translate)
        if args.obs_run2 is not None:
            # line += ' $^{%+.2f}_{%+.2f}$ & $^{%+.2f}_{%+.2f}$ ' % (obs_run2[POI]['StatHi'], obs_run2[POI]['StatLo'], obs_run2[POI]['SystHi'], obs_run2[POI]['SystHi'])
            if POI == 'mu_XS_ttH_BR_ZZ':
                blank ='-0.00'
                line += '$%.2f$ & {}$^{%+.2f}_{%s}$ & ' % (obs_run2[POI]['Val'], obs_run2[POI]['ErrorHi'], blank)
                line += ' $^{%+.2f}_{%s}$ & $^{%+.2f}_{%s}$ & $^{%+.2f}_{%s}$ & $^{%+.2f}_{%s}$ ' % (obs_run2[POI]['StatHi'], blank, obs_run2[POI]['ExpHi'], blank, obs_run2[POI]['BkgThHi'], blank, obs_run2[POI]['SigThHi'], blank)
            else:
                line += '$%.2f$ & {}$^{%+.2f}_{%+.2f}$ & ' % (obs_run2[POI]['Val'], obs_run2[POI]['ErrorHi'], obs_run2[POI]['ErrorLo'])
                line += ' $^{%+.2f}_{%+.2f}$ & $^{%+.2f}_{%+.2f}$ & $^{%+.2f}_{%+.2f}$ & $^{%+.2f}_{%+.2f}$ ' % (obs_run2[POI]['StatHi'], obs_run2[POI]['StatLo'], obs_run2[POI]['ExpHi'], obs_run2[POI]['ExpLo'], obs_run2[POI]['BkgThHi'], obs_run2[POI]['BkgThLo'],  obs_run2[POI]['SigThHi'], obs_run2[POI]['SigThLo'])
        else:
            line += '$x.xx$ & {}$^{+x.xx}_{-x.xx}$ & '
            line += ' $^{+x.xx}_{-x.xx}$ & $^{+x.xx}_{-x.xx}$ '
        if args.add_run1:
            if args.obs_run1 is not None and obs_run1.has_key(POI):
                errorHi = obs_run1[POI]['ErrorHi']
                errorLo = obs_run1[POI]['ErrorLo']
                statHi = obs_run1[POI]['StatHi'] if 'StatHi' in obs_run1[POI] else 0.0
                statLo = obs_run1[POI]['StatLo'] if 'StatLo' in obs_run1[POI] else 0.0
                if 'SystHi' not in obs_run1[POI]:
                    if 'StatHi' not in obs_run1[POI]:
                        systHi = 0.0
                        systLo = 0.0
                    else:
                        systHi = math.sqrt(errorHi * errorHi - statHi * statHi)
                        systLo = math.sqrt(errorLo * errorLo - statLo * statLo)
                else:
                    systHi = obs_run1[POI]['SystHi']
                    systLo = obs_run1[POI]['SystLo']
                line += ' & $%.2f$ & {}$^{%+.2f}_{%+.2f}$ & ' % (obs_run1[POI]['Val'], errorHi, errorLo)
                # line += '  $^{%+.2f}_{%+.2f}$ & $^{%+.2f}_{%+.2f}$ ' % (statHi, statLo, systHi, systLo)
                line += ' $^{%+.2f}_{%+.2f}$ & $^{%+.2f}_{%+.2f}$ & $^{%+.2f}_{%+.2f}$ & $^{%+.2f}_{%+.2f}$ ' % (obs_run1[POI]['StatHi'], obs_run1[POI]['StatLo'], obs_run1[POI]['ExpHi'], obs_run1[POI]['ExpLo'], obs_run1[POI]['BkgThHi'], obs_run1[POI]['BkgThLo'],  obs_run1[POI]['SigThHi'], obs_run1[POI]['SigThLo'])

            else:
                line += ' & $x.xx$ & {}$^{+x.xx}_{-x.xx}$ & '
                line += '  $^{+x.xx}_{-x.xx}$ & $^{+x.xx}_{-x.xx}$ '
        line += ' \\\\[1pt]'
        print line

        # Expected limits
        line = '    & '
        if args.exp_run2 is not None:
            line += '$\\Big($  & {}$^{%+.2f}_{%+.2f}\\Big)$ & ' % (exp_run2[POI]['ErrorHi'], exp_run2[POI]['ErrorLo'])
            line += ' $\\Big($$^{%+.2f}_{%+.2f}$$\\Big)$ & $\\Big($$^{%+.2f}_{%+.2f}$$\\Big)$ & $\\Big($$^{%+.2f}_{%+.2f}$$\\Big)$ & $\\Big($$^{%+.2f}_{%+.2f}$$\\Big)$ ' % (exp_run2[POI]['StatHi'], exp_run2[POI]['StatLo'], exp_run2[POI]['ExpHi'], exp_run2[POI]['ExpLo'], exp_run2[POI]['BkgThHi'], exp_run2[POI]['BkgThLo'],  exp_run2[POI]['SigThHi'], exp_run2[POI]['SigThLo'])
        else:
            line += '$\\Big($  & {}$^{+x.xx}_{-x.xx}\\Big)$ & '
            line += ' $\\Big($$^{+x.xx}_{-x.xx}$$\\Big)$ & $\\Big($$^{+x.xx}_{-x.xx}$$\\Big)$ '
        if args.add_run1:
            if args.exp_run1 is not None and exp_run1.has_key(POI):
                errorHi = exp_run1[POI]['ErrorHi']
                errorLo = exp_run1[POI]['ErrorLo']
                statHi = exp_run1[POI]['StatHi'] if 'StatHi' in exp_run1[POI] else 0.0
                statLo = exp_run1[POI]['StatLo'] if 'StatLo' in exp_run1[POI] else 0.0
                if 'SystHi' not in exp_run1[POI]:
                    if 'StatHi' not in exp_run1[POI]:
                        systHi = 0.0
                        systLo = 0.0
                    else:
                        systHi = math.sqrt(errorHi * errorHi - statHi * statHi)
                        systLo = math.sqrt(errorLo * errorLo - statLo * statLo)
                else:
                    systHi = exp_run1[POI]['SystHi']
                    systLo = exp_run1[POI]['SystLo']
                line += ' & $\\Big($  & {}$^{%+.2f}_{%+.2f}\\Big)$ & ' % (errorHi, errorLo)
                # line += '  $\\Big($$^{%+.2f}_{%+.2f}$$\\Big)$ & $\\Big($$^{%+.2f}_{%+.2f}$$\\Big)$ ' % (statHi, statLo, systHi, systLo)
                line += ' $\\Big($$^{%+.2f}_{%+.2f}$$\\Big)$ & $\\Big($$^{%+.2f}_{%+.2f}$$\\Big)$ & $\\Big($$^{%+.2f}_{%+.2f}$$\\Big)$ & $\\Big($$^{%+.2f}_{%+.2f}$$\\Big)$ ' % (exp_run1[POI]['StatHi'], exp_run1[POI]['StatLo'], exp_run1[POI]['ExpHi'], exp_run1[POI]['ExpLo'], exp_run1[POI]['BkgThHi'], exp_run1[POI]['BkgThLo'],  exp_run1[POI]['SigThHi'], exp_run1[POI]['SigThLo'])

            else:
                line += ' & $\\Big($  & {}$^{+x.xx}_{-x.xx}\\Big)$ & '
                line += '  $\\Big($$^{+x.xx}_{-x.xx}$$\\Big)$ & $\\Big($$^{+x.xx}_{-x.xx}$$\\Big)$ '
        line += ' \\\\[5pt]'
        # The expected
        print line
    if i == (len(MODS) - 1):
        print '\\hline'
        print '\\end{tabular}'
# caption_txt = 'Best-fit values and $\pm 1\sigma$ uncertainties for the parameters of the %s model. The expected uncertainties, evaluated on an asimov dataset are given in brackets.' % (model_str)
# if args.add_run1:
#     caption_txt += ' For comparison, the results from the Run 1 combination are also given.'
# print '\\caption{%s}' % caption_txt
# print '\\label{tab:results_%s}' % (args.model)
# print '\\vspace{0.5cm}'
# print '\\end{table}'


"""
\begin{table}[h!]
% \vspace{0.5cm}
% \scriptsize
% \singlespacing
\centering
\begin{tabular}{@{}l r@{}l c c r@{}l c c @{}}
 \hline
 \textbf{K1 Model}  & \multicolumn{4}{c}{Run 2}                                         & \multicolumn{4}{c}{Run 1}                                       \\
 \hline
           &            &                 & \multicolumn{2}{c}{Uncertainty} &               &              & \multicolumn{2}{c}{Uncertainty}  \\
Parameters & \multicolumn{2}{c}{Best-fit} & Stat. & Syst.                   & \multicolumn{2}{c}{Best-fit} & Stat. & Syst.                    \\
\hline\\ [-1.5ex]
\multirow{2}{*}{$\kappa_{Z}$} & $1.00$   & {}$^{+0.00}_{-0.00}$      & $^{+0.00}_{-0.00}$ & $^{+0.00}_{-0.00}$ & $1.00$   & {}$^{+0.00}_{-0.00}$      & $^{+0.00}_{-0.00}$ & $^{+0.00}_{-0.00}$ \\[2pt]
                              & $\Big($  & {}$^{+0.00}_{-0.00}\Big)$ & $^{+0.00}_{-0.00}$ & $^{+0.00}_{-0.00}$ & $\Big($  & {}$^{+0.00}_{-0.00}\Big)$ & $^{+0.00}_{-0.00}$ & $^{+0.00}_{-0.00}$ \\[8pt]
\multirow{2}{*}{$\kappa_{W}$} & $1.00$   & {}$^{+0.00}_{-0.00}$      & $^{+0.00}_{-0.00}$ & $^{+0.00}_{-0.00}$ & $1.00$   & {}$^{+0.00}_{-0.00}$      & $^{+0.00}_{-0.00}$ & $^{+0.00}_{-0.00}$ \\[2pt]
                              & $\Big($  & {}$^{+0.00}_{-0.00}\Big)$ & $^{+0.00}_{-0.00}$ & $^{+0.00}_{-0.00}$ & $\Big($  & {}$^{+0.00}_{-0.00}\Big)$ & $^{+0.00}_{-0.00}$ & $^{+0.00}_{-0.00}$ \\[8pt]
\hline
\end{tabular}
\caption{This is clearly a load of text which describes the contents of the tables.}
\label{tab:event_yields}
\vspace{0.5cm}
\end{table}
"""
