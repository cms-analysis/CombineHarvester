import ROOT
import re

def split_vals(vals):
    """Converts a string '1:3|1,4,5' into a list [1, 2, 3, 4, 5]"""
    res = set()
    first = vals.split(',')
    for f in first:
        second = re.split('[:|]', f)
        # print second
        if len(second) == 1:
            res.add(second[0])
        if len(second) == 3:
            x1 = float(second[0])
            ndigs = '0'
            split_step = second[2].split('.')
            if len(split_step) == 2:
                ndigs = len(split_step[1])
            fmt = '%.' + str(ndigs) + 'f'
            while x1 < float(second[1]) + 0.001:
                res.add(fmt % x1)
                x1 += float(second[2])
    return sorted([x for x in res], key=lambda x: float(x))


def list_from_workspace(file, workspace, set):
    """Create a list of strings from a RooWorkspace set"""
    res = []
    wsFile = ROOT.TFile(file)
    argSet = wsFile.Get(workspace).set(set)
    it = argSet.createIterator()
    var = it.Next()
    while var:
        res.append(var.GetName())
        var = it.Next()
    return res


def prefit_from_workspace(file, workspace, params):
    """Given a list of params, return a dictionary of [-1sig, nominal, +1sig]"""
    res = {}
    wsFile = ROOT.TFile(file)
    ws = wsFile.Get(workspace)
    for p in params:
        var = ws.var(p)
        res[p] = [
            var.getVal() + var.getErrorLo(), var.getVal(), var.getVal() + var.getErrorHi()]
    return res


def get_singles_results(file, scanned, columns):
    """Extracts the output from the MultiDimFit singles mode
    Note: relies on the list of parameters that were run (scanned) being correct"""
    res = {}
    f = ROOT.TFile(file)
    if f is None or f.IsZombie():
        return None
    t = f.Get("limit")
    for i, param in enumerate(scanned):
        res[param] = {}
        for col in columns:
            allvals = [getattr(evt, col) for evt in t]
            res[param][col] = [
                allvals[i * 2 + 2], allvals[0], allvals[i * 2 + 1]]
    return res
