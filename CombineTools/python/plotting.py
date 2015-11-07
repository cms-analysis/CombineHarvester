import CombineHarvester.CombineTools.ch as ch
import ROOT as R
import os
from functools import partial
from array import array
import re
import collections

def SetTDRStyle():
  # For the canvas:
  R.gStyle.SetCanvasBorderMode(0)
  R.gStyle.SetCanvasColor(R.kWhite)
  R.gStyle.SetCanvasDefH(600)  # Height of canvas
  R.gStyle.SetCanvasDefW(600)  # Width of canvas
  R.gStyle.SetCanvasDefX(0)    # POsition on screen
  R.gStyle.SetCanvasDefY(0)

  # For the Pad:
  R.gStyle.SetPadBorderMode(0)
  # R.gStyle.SetPadBorderSize(Width_t size = 1)
  R.gStyle.SetPadColor(R.kWhite)
  R.gStyle.SetPadGridX(False)
  R.gStyle.SetPadGridY(False)
  R.gStyle.SetGridColor(0)
  R.gStyle.SetGridStyle(3)
  R.gStyle.SetGridWidth(1)

  # For the frame:
  R.gStyle.SetFrameBorderMode(0)
  R.gStyle.SetFrameBorderSize(1)
  R.gStyle.SetFrameFillColor(0)
  R.gStyle.SetFrameFillStyle(0)
  R.gStyle.SetFrameLineColor(1)
  R.gStyle.SetFrameLineStyle(1)
  R.gStyle.SetFrameLineWidth(1)

  # For the histo:
  # R.gStyle.SetHistFillColor(1)
  # R.gStyle.SetHistFillStyle(0)
  R.gStyle.SetHistLineColor(1)
  R.gStyle.SetHistLineStyle(0)
  R.gStyle.SetHistLineWidth(1)
  # R.gStyle.SetLegoInnerR(Float_t rad = 0.5)
  # R.gStyle.SetNumberContours(Int_t number = 20)

  R.gStyle.SetEndErrorSize(2)
  # R.gStyle.SetErrorMarker(20)
  # R.gStyle.SetErrorX(0.)

  R.gStyle.SetMarkerStyle(20)

  # For the fit/function:
  R.gStyle.SetOptFit(1)
  R.gStyle.SetFitFormat('5.4g')
  R.gStyle.SetFuncColor(2)
  R.gStyle.SetFuncStyle(1)
  R.gStyle.SetFuncWidth(1)

  # For the date:
  R.gStyle.SetOptDate(0)
  # R.gStyle.SetDateX(Float_t x = 0.01)
  # R.gStyle.SetDateY(Float_t y = 0.01)

  # For the statistics box:
  R.gStyle.SetOptFile(0)
  R.gStyle.SetOptStat(0);  # To display the mean and RMS:   SetOptStat('mr')
  R.gStyle.SetStatColor(R.kWhite)
  R.gStyle.SetStatFont(42)
  R.gStyle.SetStatFontSize(0.025)
  R.gStyle.SetStatTextColor(1)
  R.gStyle.SetStatFormat('6.4g')
  R.gStyle.SetStatBorderSize(1)
  R.gStyle.SetStatH(0.1)
  R.gStyle.SetStatW(0.15)
  # R.gStyle.SetStatStyle(Style_t style = 1001)
  # R.gStyle.SetStatX(Float_t x = 0)
  # R.gStyle.SetStatY(Float_t y = 0)

  # Margins:
  R.gStyle.SetPadTopMargin(0.05)
  R.gStyle.SetPadBottomMargin(0.13)
  R.gStyle.SetPadLeftMargin(0.16)
  R.gStyle.SetPadRightMargin(0.02)

  # For the Global title:
  R.gStyle.SetOptTitle(0)
  R.gStyle.SetTitleFont(42)
  R.gStyle.SetTitleColor(1)
  R.gStyle.SetTitleTextColor(1)
  R.gStyle.SetTitleFillColor(10)
  R.gStyle.SetTitleFontSize(0.05)
  # R.gStyle.SetTitleH(0); # Set the height of the title box
  # R.gStyle.SetTitleW(0); # Set the width of the title box
  # R.gStyle.SetTitleX(0); # Set the position of the title box
  # R.gStyle.SetTitleY(0.985); # Set the position of the title box
  # R.gStyle.SetTitleStyle(Style_t style = 1001)
  # R.gStyle.SetTitleBorderSize(2)

  # For the axis titles:
  R.gStyle.SetTitleColor(1, 'XYZ')
  R.gStyle.SetTitleFont(42, 'XYZ')
  R.gStyle.SetTitleSize(0.06, 'XYZ')
  # Another way to set the size?
  # R.gStyle.SetTitleXSize(Float_t size = 0.02)
  # R.gStyle.SetTitleYSize(Float_t size = 0.02)
  R.gStyle.SetTitleXOffset(0.9)
  R.gStyle.SetTitleYOffset(1.25)
  # R.gStyle.SetTitleOffset(1.1, 'Y'); # Another way to set the Offset

  # For the axis labels:

  R.gStyle.SetLabelColor(1, 'XYZ')
  R.gStyle.SetLabelFont(42, 'XYZ')
  R.gStyle.SetLabelOffset(0.007, 'XYZ')
  R.gStyle.SetLabelSize(0.05, 'XYZ')

  # For the axis:

  R.gStyle.SetAxisColor(1, 'XYZ')
  R.gStyle.SetStripDecimals(True)
  R.gStyle.SetTickLength(0.03, 'XYZ')
  R.gStyle.SetNdivisions(510, 'XYZ')
  R.gStyle.SetPadTickX(1)
  R.gStyle.SetPadTickY(1)

  # Change for log plots:
  R.gStyle.SetOptLogx(0)
  R.gStyle.SetOptLogy(0)
  R.gStyle.SetOptLogz(0)

  # Postscript options:
  R.gStyle.SetPaperSize(20., 20.)
  # R.gStyle.SetLineScalePS(Float_t scale = 3)
  # R.gStyle.SetLineStyleString(Int_t i, const char* text)
  # R.gStyle.SetHeaderPS(const char* header)
  # R.gStyle.SetTitlePS(const char* pstitle)

  # R.gStyle.SetBarOffset(Float_t baroff = 0.5)
  # R.gStyle.SetBarWidth(Float_t barwidth = 0.5)
  # R.gStyle.SetPaintTextFormat(const char* format = 'g')
  # R.gStyle.SetPalette(Int_t ncolors = 0, Int_t* colors = 0)
  # R.gStyle.SetTimeOffset(Double_t toffset)
  # R.gStyle.SetHistMinimumZero(kTRUE)

  R.gStyle.SetHatchesLineWidth(5)
  R.gStyle.SetHatchesSpacing(0.05)

def ModTDRStyle(width=600, height=600, t=0.06, b=0.12, l=0.16, r=0.04):
  SetTDRStyle()

  # Set the default canvas width and height in pixels
  R.gStyle.SetCanvasDefW(width)
  R.gStyle.SetCanvasDefH(height)

  # Set the default margins.
  # These are given as fractions of the pad height for `Top` and `Bottom` and
  # the pad width for `Left` and `Right`. But we want to specify all of these
  # as fractions of the shortest length.
  def_w = float(R.gStyle.GetCanvasDefW())
  def_h = float(R.gStyle.GetCanvasDefH())

  scale_h = (def_w / def_h) if (def_h > def_w) else 1.
  scale_w = (def_h / def_w) if (def_w > def_h) else 1.

  def_min = def_h if (def_h < def_w) else def_w

  R.gStyle.SetPadTopMargin(t * scale_h);      # default 0.05
  R.gStyle.SetPadBottomMargin(b * scale_h);   # default 0.13
  R.gStyle.SetPadLeftMargin(l * scale_w);     # default 0.16
  R.gStyle.SetPadRightMargin(r * scale_w);    # default 0.02
  # But note the new CMS style sets these:
  # 0.08, 0.12, 0.12, 0.04

  # Set number of axis tick divisions
  R.gStyle.SetNdivisions(506, 'XYZ') # default 510

  # Some marker properties not set in the default tdr style
  R.gStyle.SetMarkerColor(R.kBlack)
  R.gStyle.SetMarkerSize(1.0)


  R.gStyle.SetLabelOffset(0.007, 'YZ')
  # This is an adhoc adjustment to scale the x-axis label
  # offset when we strect plot vertically
  # Will also need to increase if first x-axis label has more than one digit
  R.gStyle.SetLabelOffset(0.005 * (3. - 2. / scale_h), 'X')

  # In this next part we do a slightly involved calculation to set the axis
  # title offsets, depending on the values of the TPad dimensions and margins.
  # This is to try and ensure that regardless of how these pad values are set,
  # the axis titles will be located towards the edges of the canvas and not get
  # pushed off the edge - which can often happen if a fixed value is used.
  title_size = 0.05
  title_px = title_size * def_min
  label_size = 0.04
  R.gStyle.SetTitleSize(title_size, 'XYZ')
  R.gStyle.SetLabelSize(label_size, 'XYZ')

  R.gStyle.SetTitleXOffset(0.5 * scale_h *
                          (1.2 * (def_h * b * scale_h - 0.6 * title_px)) /
                          title_px)
  R.gStyle.SetTitleYOffset(0.5 * scale_w *
                          (1.2 * (def_w * l * scale_w - 0.6 * title_px)) /
                          title_px)

  # Only draw ticks where we have an axis
  R.gStyle.SetPadTickX(0)
  R.gStyle.SetPadTickY(0)
  R.gStyle.SetTickLength(0.02, 'XYZ')

  R.gStyle.SetLegendBorderSize(0)
  R.gStyle.SetLegendFont(42)
  R.gStyle.SetLegendFillColor(0)
  R.gStyle.SetFillColor(0)

  R.gROOT.ForceStyle()

def DrawCMSLogo(pad, cmsText, extraText, iPosX, relPosX, relPosY, relExtraDY):
  pad.cd()
  cmsTextFont = 62 # default is helvetic-bold

  writeExtraText = len(extraText) > 0
  extraTextFont = 52

  # text sizes and text offsets with respect to the top frame
  # in unit of the top margin size
  lumiTextOffset = 0.2
  cmsTextSize = 0.8
  # float cmsTextOffset    = 0.1;  // only used in outOfFrame version

  # ratio of 'CMS' and extra text size
  extraOverCmsTextSize = 0.76

  outOfFrame = False
  if iPosX / 10 == 0:
    outOfFrame = True

  alignY_ = 3
  alignX_ = 2
  if (iPosX / 10 == 0): alignX_ = 1
  if (iPosX == 0): alignX_ = 1
  if (iPosX == 0): alignY_ = 1
  if (iPosX / 10 == 1): alignX_ = 1
  if (iPosX / 10 == 2): alignX_ = 2
  if (iPosX / 10 == 3): alignX_ = 3
  if (iPosX == 0): relPosX = 0.14
  align_ = 10 * alignX_ + alignY_

  l = pad.GetLeftMargin()
  t = pad.GetTopMargin()
  r = pad.GetRightMargin()
  b = pad.GetBottomMargin()

  latex = R.TLatex()
  latex.SetNDC()
  latex.SetTextAngle(0)
  latex.SetTextColor(R.kBlack)

  extraTextSize = extraOverCmsTextSize * cmsTextSize;
  pad_ratio = (float(pad.GetWh()) * pad.GetAbsHNDC()) / (float(pad.GetWw()) * pad.GetAbsWNDC())
  if (pad_ratio < 1.): pad_ratio = 1.


  if outOfFrame:
    latex.SetTextFont(cmsTextFont)
    latex.SetTextAlign(11)
    latex.SetTextSize(cmsTextSize * t * pad_ratio)
    latex.DrawLatex(l, 1 - t + lumiTextOffset * t, cmsText)


  posX_ = 0;
  if iPosX % 10 <= 1:
    posX_ = l + relPosX * (1 - l - r)
  elif (iPosX % 10 == 2):
    posX_ = l + 0.5 * (1 - l - r)
  elif (iPosX % 10 == 3):
    posX_ = 1 - r - relPosX * (1 - l - r)

  posY_ = 1 - t - relPosY * (1 - t - b)
  if not outOfFrame:
    latex.SetTextFont(cmsTextFont)
    latex.SetTextSize(cmsTextSize * t * pad_ratio)
    latex.SetTextAlign(align_)
    latex.DrawLatex(posX_, posY_, cmsText)
    if writeExtraText:
      latex.SetTextFont(extraTextFont)
      latex.SetTextAlign(align_)
      latex.SetTextSize(extraTextSize * t * pad_ratio)
      latex.DrawLatex(posX_, posY_ - relExtraDY * cmsTextSize * t, extraText)
  elif writeExtraText:
    if iPosX == 0:
      posX_ = l + relPosX * (1 - l - r)
      posY_ = 1 - t + lumiTextOffset * t
    latex.SetTextFont(extraTextFont)
    latex.SetTextSize(extraTextSize * t * pad_ratio)
    latex.SetTextAlign(align_)
    latex.DrawLatex(posX_, posY_, extraText)

def PositionedLegend(width, height, pos, offset):
  o = offset
  w = width
  h = height
  l = R.gPad.GetLeftMargin()
  t = R.gPad.GetTopMargin()
  b = R.gPad.GetBottomMargin()
  r = R.gPad.GetRightMargin()
  if pos == 1:
    return R.TLegend(l + o, 1 - t - o - h, l + o + w, 1 - t - o, '', 'NBNDC')
  if pos == 2:
    c = l + 0.5 * (1 - l - r)
    return R.TLegend(c - 0.5 * w, 1 - t - o - h, c + 0.5 * w, 1 - t - o, '', 'NBNDC')
  if pos == 3 :
    return R.TLegend(1 - r - o - w, 1 - t - o - h, 1 - r - o, 1 - t - o, '', 'NBNDC')
  if pos == 4:
    return R.TLegend(l + o, b + o, l + o + w, b + o + h, '', 'NBNDC')
  if pos == 5:
    c = l + 0.5 * (1 - l - r)
    return R.TLegend(c - 0.5 * w, b + o, c + 0.5 * w, b + o + h, '', 'NBNDC')
  if pos == 6:
    return R.TLegend(1 - r - o - w, b + o, 1 - r - o, b + o + h, '','NBNDC');

def Get(file, obj):
  R.TH1.AddDirectory(False)
  f_in = R.TFile(file)
  res = R.gDirectory.Get(obj)
  f_in.Close()
  return res

def RocCurveFrom1DHists(h_x, h_y, cut_is_greater_than):
  backup = R.TH1.AddDirectoryStatus()
  R.TH1.AddDirectory(False)
  x_den = h_x.Clone()
  x_num = h_x.Clone()
  x_err = R.Double(0.)
  x_int = h_x.IntegralAndError(0, h_x.GetNbinsX() + 1, x_err)
  for i in range(1, h_x.GetNbinsX() + 1):
    x_part_err = R.Double(0.)
    x_part_int = h_x.IntegralAndError(i, h_x.GetNbinsX() + 1, x_part_err) if cut_is_greater_than else h_x.IntegralAndError(0, i, x_part_err)
    x_den.SetBinContent(i, x_int)
    x_den.SetBinError(i, x_err)
    x_num.SetBinContent(i, x_part_int)
    x_num.SetBinError(i, x_part_err)
  y_den = h_y.Clone()
  y_num = h_y.Clone()
  y_err = R.Double(0.)
  y_int = h_y.IntegralAndError(0, h_y.GetNbinsX() + 1, y_err)
  for i in range(1, h_y.GetNbinsX() + 1):
    y_part_err = R.Double(0.)
    y_part_int = h_y.IntegralAndError(i, h_y.GetNbinsX() + 1, y_part_err) if cut_is_greater_than else h_y.IntegralAndError(0, i, y_part_err)
    y_den.SetBinContent(i, y_int)
    y_den.SetBinError(i, y_err)
    y_num.SetBinContent(i, y_part_int)
    y_num.SetBinError(i, y_part_err)
  # x_den.Print('all')
  # x_num.Print('all')
  # y_den.Print('all')
  # y_num.Print('all')
  x_gr = R.TGraphAsymmErrors(x_num, x_den)
  y_gr = R.TGraphAsymmErrors(y_num, y_den)

  res = y_gr.Clone()
  for i in range (0, res.GetN()):
    res.GetX()[i] = x_gr.GetY()[i]
    res.GetEXlow()[i] = x_gr.GetEYlow()[i]
    res.GetEXhigh()[i] = x_gr.GetEYhigh()[i]
  res.Sort()
  R.TH1.AddDirectory(backup)
  return res

def CreateAxisHist(src, at_limits):
  backup = R.gPad
  tmp = R.TCanvas()
  tmp.cd()
  src.Draw('AP')
  result = src.GetHistogram().Clone()
  if (at_limits):
    min = 0.
    max = 0.
    x = R.Double(0.)
    y = R.Double(0.)
    src.GetPoint(0, x, y)
    min = float(x)
    max = float(x)
    for i in range(1, src.GetN()):
      src.GetPoint(i, x, y)
      if x < min: min = float(x)
      if x > max: max = float(x)
    result.GetXaxis().SetLimits(min, max)
  R.gPad = backup
  return result

class MultiGraphPlot:
  def __init__(self, **args):
    self.styler = args.get('styler', ModTDRStyle)
    self.draw = args.get('draw')
    self.outputFileName = args.get('outputFileName','test.pdf')
    self.legend = args.get('legend', None)
    self.pad = args.get('pad', None)
    self.logy = args.get('logy', None)

  def Create(self):
    self.styler()
    if not self.pad:
      self.canv = R.TCanvas('canv', 'canv')
      self.pad = R.TPad('pad', 'pad', 0., 0., 1., 1.)
    self.pad.SetGridx(True)
    self.pad.SetGridy(True)
    self.pad.Draw()
    self.pad.cd()
    self.axis = CreateAxisHist(self.draw[0].src, True)
    self.pad.cd()
    self.axis.GetXaxis().SetLimits(0., 1.)
    self.axis.GetYaxis().SetRangeUser(1E-4, 0.015)
    self.axis.GetXaxis().SetTitle('#tau_{h} Efficiency')
    self.axis.GetYaxis().SetTitle('Jet#rightarrow#tau_{h} Fake Rate')
    self.axis.Draw()
    for d in self.draw:
      ele = d.get()
      ele.Draw(d.drawOpts + 'SAME')
    if self.legend:
      self.leg = self.legend()
      for d in self.draw:
        self.leg.AddEntry(d.src, d.src.GetTitle() if not d.legend else d.legend, 'L')
      self.leg.Draw()
    if self.logy is not None: self.pad.SetLogy(self.logy)
    DrawCMSLogo(self.pad, 'CMS', 'Simulation', 0, 0.045, 0.035, 1.2)
    self.canv.SaveAs(self.outputFileName)

def StyleGraph(obj, **args):
  obj.SetLineColor(args.get('lineColor', 1))
  obj.SetFillColor(args.get('fillColor', 0))
  obj.SetMarkerColor(args.get('markerColor', 1))
  obj.SetMarkerStyle(args.get('markerStyle', 20))
  obj.SetLineWidth(2)

class Graph:
  def __init__(self, **args):
    self.src = args.get('src')
    self.style = args.get('style')
    self.drawOpts = args.get('drawOpts', 'CP')
    self.legend = args.get('legend', None)

  def get(self):
    self.style(self.src)
    return self.src

def CreateTransparentColor(color, alpha):
    adapt   = R.gROOT.GetColor(color)
    new_idx = R.gROOT.GetListOfColors().GetSize() + 1
    trans = R.TColor(new_idx, adapt.GetRed(), adapt.GetGreen(), adapt.GetBlue(), '', alpha)
    trans.SetName('userColor%i' % new_idx)
    return new_idx

def TFileIsGood(filename):
    if not os.path.exists(filename): return False
    fin = R.TFile.Open(filename)
    if fin: R.TFile.Close(fin)
    if not fin: return False
    return True

def MakeTChain(files, tree):
    chain = R.TChain(tree)
    for f in files:
        chain.Add(f)
    return chain

def TGraphFromTree(tree, xvar, yvar, selection):
    tree.Draw(xvar + ':' + yvar, selection, 'goff')
    gr = R.TGraph(tree.GetSelectedRows(), tree.GetV1(), tree.GetV2())
    return gr

def TGraph2DFromTree(tree, xvar,  yvar, zvar, selection):
    tree.Draw(xvar+':'+yvar+':'+zvar, selection, 'goff')
    gr = R.TGraph2D(tree.GetSelectedRows(), tree.GetV1(), tree.GetV2(), tree.GetV3())
    return gr

def ParamFromFilename(filename, param):
    if len(re.findall(param+'\.\d+\.\d+', filename)) :
        num1 = re.findall(param+'\.\d+\.\d+', filename)[0].replace(param+'.','')
        return float(num1)
    elif len(re.findall(param+'\.\d+', filename)) :    
        num1 = re.findall(param + '\.\d+', filename)[0].replace(param+'.','')
        return int(num1)
    else :
        print "Error: parameter " + param + " not found in filename"

def RemoveGraphXDuplicates(graph):
    for i in xrange(graph.GetN() - 1):
        if graph.GetX()[i+1] == graph.GetX()[i]:
            # print 'Removing duplicate point (%f, %f)' % (graph.GetX()[i+1], graph.GetY()[i+1])
            graph.RemovePoint(i+1)
            RemoveGraphXDuplicates(graph)
            break

def RemoveGraphYAll(graph, val):
    for i in xrange(graph.GetN()):
        if graph.GetY()[i] == val:
            print 'Removing point (%f, %f)' % (graph.GetX()[i], graph.GetY()[i])
            graph.RemovePoint(i)
            RemoveGraphYAll(graph, val)
            break

def RemoveGraphYAbove(graph, val):
    for i in xrange(graph.GetN()):
        if graph.GetY()[i] > val:
            # print 'Removing point (%f, %f)' % (graph.GetX()[i], graph.GetY()[i])
            graph.RemovePoint(i)
            RemoveGraphYAbove(graph, val)
            break

def OnePad():
    pad = R.TPad('pad', 'pad', 0., 0., 1., 1.)
    pad.Draw()
    pad.cd()
    result = [pad]
    return result

def TwoPadSplit(split_point, gap_low, gap_high) :
    upper = R.TPad('upper', 'upper', 0., 0., 1., 1.)
    upper.SetBottomMargin(split_point + gap_high)
    upper.SetFillStyle(4000)
    upper.Draw()
    lower = R.TPad('lower', 'lower', 0., 0., 1., 1.)
    lower.SetTopMargin(1 - split_point + gap_low)
    lower.SetFillStyle(4000)
    lower.Draw()
    upper.cd()
    result = [upper,lower]
    return result

def ImproveMinimum(graph, func):
    fit_x = 0.
    fit_y = 0.
    fit_i = 0
    for i in xrange(graph.GetN()):
        if graph.GetY()[i] == 0.:
            fit_i= i
            fit_x = graph.GetX()[i]
            fit_y = graph.GetY()[i]
            break
    if fit_i == 0 or fit_i == (graph.GetN() - 1): return
    min_x = func.GetMinimumX(graph.GetX()[fit_i-1], graph.GetX()[fit_i+1])
    min_y = func.Eval(min_x)
    print '[ImproveMinimum] Fit minimum was (%f, %f)' % (fit_x, fit_y)
    print '[ImproveMinimum] Better minimum was (%f, %f)' % (min_x, min_y)


def FindCrossingsWithSpline(graph, func, yval):
    crossings = []
    intervals = []
    current = None
    for i in xrange(graph.GetN() - 1):
        if (graph.GetY()[i] - yval) * (graph.GetY()[i+1] - yval) < 0.:
            cross = func.GetX(yval, graph.GetX()[i], graph.GetX()[i+1])
            if (graph.GetY()[i] - yval) > 0. and current is None:
                current = {
                  'lo' : cross,
                  'hi' : graph.GetX()[graph.GetN() - 1],
                  'valid_lo' : True,
                  'valid_hi' : False
                }
            if (graph.GetY()[i] - yval) < 0. and current is None:
                current = {
                  'lo' : graph.GetX()[0],
                  'hi' : cross,
                  'valid_lo' : False,
                  'valid_hi' : True
                }
                intervals.append(current)
                current = None
            if (graph.GetY()[i] - yval) < 0. and current is not None:
                current['hi'] = cross
                current['valid_hi'] = True
                intervals.append(current)
                current = None
            # print 'Crossing between: (%f, %f) -> (%f, %f) at %f' % (graph.GetX()[i], graph.GetY()[i], graph.GetX()[i+1], graph.GetY()[i+1], cross)
            crossings.append(cross)
    if current is not None: intervals.append(current)
    if len(intervals) == 0:
      current = {
        'lo' : graph.GetX()[0],
        'hi' : graph.GetX()[graph.GetN() - 1],
        'valid_lo' : False,
        'valid_hi' : False
      }
      intervals.append(current)
    print intervals
    return intervals
    # return crossings

def GetAxisHist(pad):
  pad_obs = pad.GetListOfPrimitives()
  if pad_obs is None: return None
  nextit = R.TIter(pad_obs)
  obj = None
  for obj in pad_obs:
    if obj.InheritsFrom(R.TH1.Class()):
        return obj
    if obj.InheritsFrom(R.TMultiGraph.Class()):
        return obj.GetHistogram()
    if obj.InheritsFrom(R.TGraph.Class()):
        return obj.GetHistogram()
    if obj.InheritsFrom(R.THStack.Class()):
        return hs.GetHistogram()
  return None

def DrawHorizontalLine(pad, line, yval):
  axis = GetAxisHist(pad)
  xmin = axis.GetXaxis().GetXmin()
  xmax = axis.GetXaxis().GetXmax()
  line.DrawLine(xmin, yval, xmax, yval)

def DrawTitle(pad, text, align):
    pad_backup = R.gPad
    pad.cd()
    t = pad.GetTopMargin()
    l = pad.GetLeftMargin()
    r = pad.GetRightMargin()
    
    pad_ratio = (float(pad.GetWh()) * pad.GetAbsHNDC()) / (float(pad.GetWw()) * pad.GetAbsWNDC())
    if pad_ratio < 1.: pad_ratio = 1.
    
    textSize = 0.6
    textOffset = 0.2
    
    latex = R.TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(R.kBlack)
    latex.SetTextFont(42)
    latex.SetTextSize(textSize * t * pad_ratio)
    
    y_off = 1 - t + textOffset * t
    if align == 1: latex.SetTextAlign(11)
    if align == 1: latex.DrawLatex(l, y_off, text)
    if align == 2: latex.SetTextAlign(21)
    if align == 2: latex.DrawLatex(l + (1 - l - r) * 0.5, y_off, text)
    if align == 3: latex.SetTextAlign(31)
    if align == 3: latex.DrawLatex(1 - r, y_off, text)
    pad_backup.cd()

def ReZeroTGraph(gr, doIt=False):
    fit_x = 0.
    fit_y = 0.
    for i in xrange(gr.GetN()):
        if gr.GetY()[i] == 0.:
            fit_x = gr.GetX()[i]
            fit_y = gr.GetY()[i]
            break
    min_x = 0.
    min_y = 0.
    for i in xrange(gr.GetN()):
        if gr.GetY()[i] < min_y:
          min_y = gr.GetY()[i]
          min_x = gr.GetX()[i]
    if min_y < fit_y:
      print '[ReZeroTGraph] Fit minimum was (%f, %f)' % (fit_x, fit_y)
      print '[ReZeroTGraph] Better minimum was (%f, %f)' % (min_x, min_y)
      if doIt:
        for i in xrange(gr.GetN()):
          before = gr.GetY()[i]
          gr.GetY()[i] -= min_y
          after = gr.GetY()[i]
          print 'Point %i, before=%f, after=%f' % (i, before, after)

def RemoveNearMin(graph, val, spacing = None):
    # assume graph is sorted:
    n = graph.GetN()
    if n < 5: return
    if spacing is None:
      spacing = (graph.GetX()[n-1] - graph.GetX()[0]) / float(n - 2)
      # print '[RemoveNearMin] Graph has spacing of %.3f' % spacing
    for i in xrange(graph.GetN()):
        if graph.GetY()[i] == 0.:
            bf = graph.GetX()[i]
            bf_i = i
            # print '[RemoveNearMin] Found best-fit at %.3f' % bf
            break
    for i in xrange(graph.GetN()):
        if i == bf_i: continue
        if abs(graph.GetX()[i] - bf) < (val * spacing):
            print '[RemoveNearMin] Removing point (%f, %f) close to minimum at %f' % (graph.GetX()[i], graph.GetY()[i], bf)
            graph.RemovePoint(i)
            RemoveNearMin(graph, val, spacing)
            break

def contourFromTH2(h2in, threshold, minPoints=10, mult = 1.0):
  # std::cout << "Getting contour at threshold " << threshold << " from "
  #           << h2in->GetName() << std::endl;
  # // http://root.cern.ch/root/html/tutorials/hist/ContourList.C.html
  contoursList = [threshold]
  contours = array('d', contoursList)
  if (h2in.GetNbinsX() * h2in.GetNbinsY()) > 10000: minPoints = 50
  if (h2in.GetNbinsX() * h2in.GetNbinsY()) <= 100: minPoints = 10

  # h2 = h2in.Clone()
  h2 = frameTH2D(h2in, threshold, mult)

  h2.SetContour(1, contours)

  # Draw contours as filled regions, and Save points
  backup = R.gPad
  canv = R.TCanvas('tmp', 'tmp')
  canv.cd()
  h2.Draw('CONT Z LIST')
  R.gPad.Update() # Needed to force the plotting and retrieve the contours in

  conts = R.gROOT.GetListOfSpecials().FindObject('contours')
  contLevel = None

  if conts is None or conts.GetSize() == 0:
    print '*** No Contours Were Extracted!'
    return None
  ret = R.TList()
  for i in xrange(conts.GetSize()):
    contLevel = conts.At(i)
    print 'Contour %d has %d Graphs\n' % (i, contLevel.GetSize())
    for j in xrange(contLevel.GetSize()):
      gr1 = contLevel.At(j)
      print'\t Graph %d has %d points' % (j, gr1.GetN())
      if gr1.GetN() > minPoints: ret.Add(gr1.Clone())
      # // break;
  backup.cd()
  return ret


def frameTH2D(hist, threshold, mult = 1.0):
  # NEW LOGIC:
  #   - pretend that the center of the last bin is on the border if the frame
  #   - add one tiny frame with huge values
  frameValue = 1000
  # if (TString(in->GetName()).Contains("bayes")) frameValue = -1000;

  xw = hist.GetXaxis().GetBinWidth(1)
  yw = hist.GetYaxis().GetBinWidth(1)

  nx = hist.GetNbinsX()
  ny = hist.GetNbinsY()

  x0 = hist.GetXaxis().GetXmin()
  x1 = hist.GetXaxis().GetXmax()

  y0 = hist.GetYaxis().GetXmin()
  y1 = hist.GetYaxis().GetXmax()
  xbins = array('d', [0]*999)
  ybins = array('d', [0]*999)
  eps = 0.1
  # mult = 1.0

  xbins[0] = x0 - eps * xw - xw * mult
  xbins[1] = x0 + eps * xw - xw * mult
  for ix in xrange(2, nx+1): xbins[ix] = x0 + (ix - 1) * xw
  xbins[nx + 1] = x1 - eps * xw + 0.5 * xw * mult
  xbins[nx + 2] = x1 + eps * xw + xw * mult

  ybins[0] = y0 - eps * yw - yw * mult
  ybins[1] = y0 + eps * yw - yw * mult
  for iy in xrange(2, ny+1): ybins[iy] = y0 + (iy - 1) * yw
  ybins[ny + 1] = y1 - eps * yw + yw * mult
  ybins[ny + 2] = y1 + eps * yw + yw * mult

  framed = R.TH2D('%s framed' % hist.GetName(), '%s framed' % hist.GetTitle(), nx + 2, xbins, ny + 2, ybins)

  # Copy over the contents
  for ix in xrange(1, nx+1):
    for iy in xrange(1, ny+1):
      framed.SetBinContent(1 + ix, 1 + iy, hist.GetBinContent(ix, iy))
  
  # Frame with huge values
  nx = framed.GetNbinsX()
  ny = framed.GetNbinsY()
  for ix in xrange(1, nx+1):
    framed.SetBinContent(ix, 1, frameValue)
    framed.SetBinContent(ix, ny, frameValue)

  for iy in xrange(2, ny):
    framed.SetBinContent(1, iy, frameValue)
    framed.SetBinContent(nx, iy, frameValue)

  return framed

def FixOverlay():
  R.gPad.GetFrame().Draw()
  R.gPad.RedrawAxis()

def makeHist1D(name, xbins, graph):
    len_x = graph.GetX()[graph.GetN()-1] - graph.GetX()[0]
    binw_x = (len_x * 0.5 / (float(xbins) - 1.)) - 1E-5
    hist = R.TH1F(name, '', xbins, graph.GetX()[0], graph.GetX()[graph.GetN()-1]+binw_x)
    return hist

def makeHist2D(name, xbins, ybins, graph2d):
    len_x = graph2d.GetXmax() - graph2d.GetXmin()
    binw_x = (len_x * 0.5 / (float(xbins) - 1.)) - 1E-5
    len_y = graph2d.GetYmax() - graph2d.GetYmin()
    binw_y = (len_y * 0.5 / (float(ybins) - 1.)) - 1E-5
    hist = R.TH2F(name, '', xbins, graph2d.GetXmin()-binw_x, graph2d.GetXmax()+binw_x, ybins, graph2d.GetYmin()-binw_y, graph2d.GetYmax()+binw_y)
    return hist

def makeVarBinHist2D(name, xbins, ybins):
    #create new arrays in which bin low edge is adjusted to make measured points at the bin centres
    xbins_new=[None]*(len(xbins)+1)
    for i in xrange(len(xbins)-1):
        xbins_new[i] = xbins[i] - ((xbins[i+1]-xbins[i])/2) + 1E-5
    xbins_new[len(xbins)-1] = xbins[len(xbins)-2] + ((xbins[len(xbins)-2]-xbins[len(xbins)-3])/2) + 1E-5
    xbins_new[len(xbins)] = xbins[len(xbins)-1] + ((xbins[len(xbins)-1]-xbins[len(xbins)-2])/2) - 1E-5 
    
    ybins_new=[None]*(len(ybins)+1)
    for i in xrange(len(ybins)-1):
        ybins_new[i] = ybins[i] - ((ybins[i+1]-ybins[i])/2) + 1E-5
    ybins_new[len(ybins)-1] = ybins[len(ybins)-2] + ((ybins[len(ybins)-2]-ybins[len(ybins)-3])/2) + 1E-5
    ybins_new[len(ybins)] = ybins[len(ybins)-1] + ((ybins[len(ybins)-1]-ybins[len(ybins)-2])/2) - 1E-5
    hist = R.TH2F(name, '', len(xbins_new)-1, array('d',xbins_new), len(ybins_new)-1, array('d',ybins_new))
    return hist

def fillTH2(hist2d, graph):
    for x in xrange(1, hist2d.GetNbinsX()+1):
        for y in xrange(1, hist2d.GetNbinsY()+1):
            xc = hist2d.GetXaxis().GetBinCenter(x)
            yc = hist2d.GetYaxis().GetBinCenter(y)
            val = graph.Interpolate(xc, yc)
            hist2d.SetBinContent(x, y, val)

def higgsConstraint(model, higgstype) :
    higgsBand=R.TGraph2D()
    masslow = 150
    masshigh = 500
    massstep = 10
    n=0
    for mass in range (masslow, masshigh, massstep):
        myfile = open("../../HiggsAnalysis/HiggsToTauTau/data/Higgs125/"+model+"/higgs_"+str(mass)+".dat", 'r')
        for line in myfile:
            tanb = (line.split())[0]
            mh = float((line.split())[1])
            mH = float((line.split())[3])
            if higgstype=="h" :
                 higgsBand.SetPoint(n, mass, float(tanb), mh)
            elif higgstype=="H" :
                 higgsBand.SetPoint(n, mass, float(tanb), mH)
            n=n+1 
        myfile.close()    
    return higgsBand

def MakeErrorBand(LowerGraph, UpperGraph) :
  errorBand = R.TGraphAsymmErrors()
  lower_list=[]; upper_list=[]
  for i in range(LowerGraph.GetN()):
    lower_list.append((float(LowerGraph.GetX()[i]),  float(LowerGraph.GetY()[i])))
    upper_list.append((float(UpperGraph.GetX()[i]),  float(UpperGraph.GetY()[i])))
  lower_list=sorted(set(lower_list))
  upper_list=sorted(set(upper_list))
  for i in range(LowerGraph.GetN()):
    errorBand.SetPoint(i, lower_list[i][0], lower_list[i][1])
    errorBand.SetPointEYlow (i, lower_list[i][1]-lower_list[i][1])
    errorBand.SetPointEYhigh(i, upper_list[i][1]-lower_list[i][1])
  return errorBand

def SortGraph(Graph) :
  sortedGraph = R.TGraph()
  graph_list=[]
  for i in range(Graph.GetN()):
    graph_list.append((float(Graph.GetX()[i]),  float(Graph.GetY()[i])))
  graph_list=sorted(set(graph_list))
  for i in range(Graph.GetN()):
    sortedGraph.SetPoint(i, graph_list[i][0], graph_list[i][1])
  return sortedGraph
