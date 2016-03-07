# import os
import ROOT
import CombineHarvester.CombineTools.plotting as plot
import argparse

def read(filename, tree):
    result = []
    f = ROOT.TFile(filename)
    t = f.Get(tree)
    for evt in t:
        result.append((evt.mu, evt.muLoErr, evt.muHiErr, evt.muErr))
    # print result
    return result


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='input file')
# parser.add_argument('--files', '-f', help='named input scans')
# parser.add_argument('--multi', type=int, default=1, help='scale number of bins')
# parser.add_argument('--thin', type=int, default=1, help='thin graph points')
# parser.add_argument('--order', default='b,tau,Z,gam,W,comb')
# parser.add_argument('--x-range', default=None)
# parser.add_argument('--x-axis', default='#kappa_{V}')
# parser.add_argument('--y-axis', default='#kappa_{F}')
# parser.add_argument('--axis-hist', default=None)
# parser.add_argument('--layout', type=int, default=1)
args = parser.parse_args()

res = read(args.input, 'tree_fit_sb')

n_in = 0
n_tot = 0
truth = 1.0

for r in res:
    n_tot += 1
    if r[3] == 0:
        continue        
    # is_in = abs((1-r[0])/r[3]) < 1.
    if r[0] < truth:
        is_in = (r[0]+r[2]) >= truth
    else:
        is_in = (r[0]-r[1]) <= truth
    if is_in:
        n_in += 1

print n_in
print n_tot
print float(n_in)/float(n_tot)
