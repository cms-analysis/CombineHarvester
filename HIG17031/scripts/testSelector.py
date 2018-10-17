#!/usr/bin/env python
import ROOT
import re

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

# The selector string the user supplies
selector = 'rgx{x.*} || (rgx{y.*} && {const}) || attr{nuisance}'

# We convert it to an actual C++ function
selector = re.sub(r'rgx{(.*?)}', r'std::regex_match(x.GetName(), std::regex("\1"))', selector)
selector = re.sub(r'{const}', r'x.isConstant()', selector)
selector = re.sub(r'attr{(.*?)}', r'x.getAttribute("\1")', selector)

print selector

# Create the selector function using the C++ interpreter
ROOT.gROOT.ProcessLine('#include<regex>')
ROOT.gInterpreter.Declare("bool TestVar(RooRealVar &x) { return %s; };" % selector)


# Test 1
testVar = ROOT.RooRealVar("xyz", "", 1, 0, 1)
print 'Test 1: ', ROOT.TestVar(testVar)

# Test 2
testVar = ROOT.RooRealVar("yzx", "", 1, 0, 1)
print 'Test 2: ', ROOT.TestVar(testVar)

# Test 3
testVar = ROOT.RooRealVar("yzx", "", 1, 0, 1)
testVar.setConstant(True)
print 'Test 3: ', ROOT.TestVar(testVar)

# Test 4
testVar = ROOT.RooRealVar("yzx", "", 1, 0, 1)
testVar.setAttribute('nuisance')
print 'Test 4: ', ROOT.TestVar(testVar)

# Test 5
testVar = ROOT.RooRealVar("yzx", "", 1, 0, 1)
testVar.setAttribute('other')
print 'Test 5: ', ROOT.TestVar(testVar)