import ROOT as R
import os
from functools import partial
from array import array
import re

COL_STORE = []

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

def DrawCMSLogo(pad, cmsText, extraText, iPosX, relPosX, relPosY, relExtraDY, extraText2='', cmsTextSize=0.8):
  pad.cd()
  cmsTextFont = 62 # default is helvetic-bold

  writeExtraText = len(extraText) > 0
  writeExtraText2 = len(extraText2) > 0
  extraTextFont = 52

  # text sizes and text offsets with respect to the top frame
  # in unit of the top margin size
  lumiTextOffset = 0.2
  # cmsTextSize = 0.8
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
  # if (iPosX == 0): relPosX = 0.14
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
      if writeExtraText2: latex.DrawLatex(posX_, posY_ - 1.8 * relExtraDY * cmsTextSize * t, extraText2)
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
    new_idx = R.gROOT.GetListOfColors().GetLast() + 1
    trans = R.TColor(new_idx, adapt.GetRed(), adapt.GetGreen(), adapt.GetBlue(), '', alpha)
    COL_STORE.append(trans)
    trans.SetName('userColor%i' % new_idx)
    return new_idx

def TFileIsGood(filename):
    # if not os.path.exists(filename): return False
    fin = R.TFile(filename)
    if not fin: return False
    if fin and not fin.IsOpen():
      return False
    elif fin and fin.IsOpen() and fin.IsZombie():
      fin.Close()
      return False
    elif fin and fin.IsOpen() and fin.TestBit(R.TFile.kRecovered):
      fin.Close()
      # don't consider a recovered file to be ok
      return False
    else:
      fin.Close()
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

def RemoveSmallDelta(graph, val):
    for i in xrange(graph.GetN()):
        diff = abs(graph.GetY()[i])
        if diff < val:
            print '[RemoveSmallDelta] Removing point (%f, %f)' % (graph.GetX()[i], graph.GetY()[i])
            graph.RemovePoint(i)
            RemoveSmallDelta(graph, val)
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

def TwoPadSplitColumns(split_point, gap_left, gap_right) :
    left = R.TPad('left', 'left', 0., 0., 1., 1.)
    left.SetRightMargin(1 - split_point + gap_right)
    left.SetFillStyle(4000)
    left.Draw()
    right = R.TPad('right', 'right', 0., 0., 1., 1.)
    right.SetLeftMargin(split_point + gap_left)
    right.SetFillStyle(4000)
    right.Draw()
    left.cd()
    result = [left,right]
    return result

def ImproveMinimum(graph, func, doIt = False):
    fit_x = 0.
    fit_y = 999.
    fit_i = 0
    for i in xrange(graph.GetN()):
        if graph.GetY()[i] < fit_y:
            fit_i= i
            fit_x = graph.GetX()[i]
            fit_y = graph.GetY()[i]
    if fit_i == 0 or fit_i == (graph.GetN() - 1):
      if doIt:
        min_x = graph.GetX()[fit_i]
        min_y = graph.GetY()[fit_i]
        for i in xrange(graph.GetN()):
          before = graph.GetY()[i]
          graph.GetY()[i] -= min_y
          after = graph.GetY()[i]
          print 'Point %i, before=%f, after=%f' % (i, before, after)
      return (fit_x, fit_y)
    search_min = fit_i-2 if fit_i >= 2 else fit_i-1
    search_max = fit_i+2 if fit_i+2 < graph.GetN() else fit_i+1
    min_x = func.GetMinimumX(graph.GetX()[search_min], graph.GetX()[search_max])
    min_y = func.Eval(min_x)
    print '[ImproveMinimum] Fit minimum was (%f, %f)' % (fit_x, fit_y)
    print '[ImproveMinimum] Better minimum was (%f, %f)' % (min_x, min_y)
    if doIt:
      for i in xrange(graph.GetN()):
        before = graph.GetY()[i]
        graph.GetY()[i] -= min_y
        after = graph.GetY()[i]
        print 'Point %i, before=%f, after=%f' % (i, before, after)
      graph.Set(graph.GetN()+1)
      graph.SetPoint(graph.GetN()-1, min_x, 0)
      graph.Sort()
    return (min_x, min_y)



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


def FixTopRange(pad, fix_y, fraction):
  hobj = GetAxisHist(pad)
  ymin = hobj.GetMinimum()
  hobj.SetMaximum((fix_y - fraction * ymin) / (1. - fraction))
  if R.gPad.GetLogy():
    if ymin == 0.:
      print 'Cannot adjust log-scale y-axis range if the minimum is zero!'
      return
    maxval = (math.log10(fix_y) - fraction * math.log10(ymin)) / (1 - fraction)
    maxval = math.pow(10, maxval)
    hobj.SetMaximum(maxval)

def GetPadYMaxInRange(pad, x_min, x_max):
  pad_obs = pad.GetListOfPrimitives()
  if pad_obs is None: return 0.
  h_max = -99999.
  for obj in pad_obs:
    if obj.InheritsFrom(R.TH1.Class()):
      hobj = obj
      for j in xrange(1, hobj.GetNbinsX()):
        if (hobj.GetBinLowEdge(j) + hobj.GetBinWidth(j) < x_min or
            hobj.GetBinLowEdge(j) > x_max): continue
        if (hobj.GetBinContent(j) + hobj.GetBinError(j) > h_max):
          h_max = hobj.GetBinContent(j) + hobj.GetBinError(j)

    if obj.InheritsFrom(R.TGraph.Class()):
      gobj = obj
      n = gobj.GetN()
      for k in xrange(0, n):
        x = gobs.GetX()[k]
        y = gobs.GetY()[k]
        if x < x_min or x > x_max: continue
        if y > h_max: h_max = y
  return h_max

def GetPadYMax(pad):
  pad_obs = pad.GetListOfPrimitives()
  if pad_obs is None: return 0.
  xmin = GetAxisHist(pad).GetXaxis().GetXmin()
  xmax = GetAxisHist(pad).GetXaxis().GetXmax()
  return GetPadYMaxInRange(pad, xmin, xmax)

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
    return min_y

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


def TH2FromTGraph2D(graph, method='BinEdgeAligned',
                    force_x_width=None,
                    force_y_width=None):
    """Build an empty TH2 from the set of points in a TGraph2D

    There is no unique way to define a TH2 binning given an arbitrary
    TGraph2D, therefore this function supports multiple named methods:

     - `BinEdgeAligned` simply takes the sets of x- and y- values in the
       TGraph2D and uses these as the bin edge arrays in the TH2. The
       implication of this is that when filling the bin contents interpolation
       will be required when evaluating the TGraph2D at the bin centres.
     - `BinCenterAligned` will try to have the TGraph2D points at the bin
       centers, but this will only work completely correctly when the input
       point spacing is regular. The algorithm first identifies the bin width
       as the smallest interval between points on each axis. The start
       position of the TH2 axis is then defined as the lowest value in the
       TGraph2D minus half this width, and the axis continues with regular
       bins until the graph maximum is passed.

    Args:
        graph (TGraph2D): Should have at least two unique x and y values,
            otherwise we can't define any bins
        method (str): The binning algorithm to use
        force_x_width (bool): Override the derived x-axis bin width in the
            CenterAligned method
        force_y_width (bool): Override the derived y-axis bin width in the
            CenterAligned method

    Raises:
        RuntimeError: If the method name is not recognised

    Returns:
        TH2F: The exact binning of the TH2F depends on the chosen method
    """
    x_vals = set()
    y_vals = set()

    for i in xrange(graph.GetN()):
        x_vals.add(graph.GetX()[i])
        y_vals.add(graph.GetY()[i])

    x_vals = sorted(x_vals)
    y_vals = sorted(y_vals)
    if method == 'BinEdgeAligned':
        h_proto = R.TH2F('prototype', '',
                         len(x_vals) - 1, array('d', x_vals),
                         len(y_vals) - 1, array('d', y_vals))
    elif method == 'BinCenterAligned':
        x_widths = []
        y_widths = []
        for i in xrange(1, len(x_vals)):
            x_widths.append(x_vals[i] - x_vals[i-1])
        for i in xrange(1, len(y_vals)):
            y_widths.append(y_vals[i] - y_vals[i-1])
        x_min = min(x_widths) if force_x_width is None else force_x_width
        y_min = min(y_widths) if force_y_width is None else force_y_width
        x_bins = int(((x_vals[-1] - (x_vals[0] - 0.5*x_min))/x_min) + 0.5)
        y_bins = int(((y_vals[-1] - (y_vals[0] - 0.5*y_min))/y_min) + 0.5)
        print '[TH2FromTGraph2D] x-axis binning: (%i, %g, %g)' % (x_bins, x_vals[0] - 0.5*x_min, x_vals[0] - 0.5*x_min + x_bins*x_min)
        print '[TH2FromTGraph2D] y-axis binning: (%i, %g, %g)' % (y_bins, y_vals[0] - 0.5*y_min, y_vals[0] - 0.5*y_min + y_bins*y_min)
        # Use a number slightly smaller than 0.49999 because the TGraph2D interpolation
        # is fussy about evaluating on the boundary
        h_proto = R.TH2F('prototype', '',
                         x_bins, x_vals[0] - 0.49999*x_min, x_vals[0] - 0.50001*x_min + x_bins*x_min,
                         y_bins, y_vals[0] - 0.49999*y_min, y_vals[0] - 0.50001*y_min + y_bins*y_min)
    else:
        raise RuntimeError(
            '[TH2FromTGraph2D] Method %s not supported' % method)
    h_proto.SetDirectory(0)
    return h_proto


def contourFromTH2(h2in, threshold, minPoints=10, frameValue = 1000.):
  # // http://root.cern.ch/root/html/tutorials/hist/ContourList.C.html
  contoursList = [threshold]
  contours = array('d', contoursList)
  # if (h2in.GetNbinsX() * h2in.GetNbinsY()) > 10000: minPoints = 50
  # if (h2in.GetNbinsX() * h2in.GetNbinsY()) <= 100: minPoints = 10

  h2 = frameTH2D(h2in, threshold, frameValue)

  h2.SetContour(1, contours)

  # Draw contours as filled regions, and Save points
  # backup = R.gPad # doesn't work in pyroot, backup behaves like a ref to gPad
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
    print '>> Contour %d has %d Graphs' % (i, contLevel.GetSize())
    for j in xrange(contLevel.GetSize()):
      gr1 = contLevel.At(j)
      print'\t Graph %d has %d points' % (j, gr1.GetN())
      if gr1.GetN() > minPoints: ret.Add(gr1.Clone())
      # // break;
  # backup.cd()
  canv.Close()
  return ret


def frameTH2D(hist, threshold, frameValue=1000):
  # Now supports variable-binned histograms First adds a narrow frame (1% of
  # of bin widths) around the outside with same values as the real edge. Then
  # adds another frame another frame around this one filled with some chosen
  # value that will make the contours close

  # Get lists of the bin edges
  x_bins = [hist.GetXaxis().GetBinLowEdge(x) for x in xrange(1, hist.GetNbinsX()+2)]
  y_bins = [hist.GetYaxis().GetBinLowEdge(y) for y in xrange(1, hist.GetNbinsY()+2)]

  # New bin edge arrays will need an extra four values
  x_new = [0.]*(len(x_bins)+4)
  y_new = [0.]*(len(y_bins)+4)

  # Calculate bin widths at the edges
  xw1 = x_bins[1]  - x_bins[0]
  xw2 = x_bins[-1] - x_bins[-2]
  yw1 = y_bins[1]  - y_bins[0]
  yw2 = y_bins[-1] - y_bins[-2]

  # Set the edges of the outer framing bins and the adjusted
  # edge of the real edge bins
  x_new[0]  = x_bins[0]  - 2 * xw1*0.01
  x_new[1]  = x_bins[0]  - 1 * xw1*0.01
  x_new[-1] = x_bins[-1] + 2 * xw2*0.01
  x_new[-2] = x_bins[-1] + 1 * xw2*0.01
  y_new[0]  = y_bins[0]  - 2 * yw1*0.01
  y_new[1]  = y_bins[0]  - 1 * yw1*0.01
  y_new[-1] = y_bins[-1] + 2 * yw2*0.01
  y_new[-2] = y_bins[-1] + 1 * yw2*0.01

  # Copy the remaining bin edges from the hist
  for i in xrange(0, len(x_bins)):
    x_new[i+2] = x_bins[i]
  for i in xrange(0, len(y_bins)):
    y_new[i+2] = y_bins[i]

  # print x_new
  # print y_new

  framed = R.TH2D('%s framed' % hist.GetName(), '%s framed' % hist.GetTitle(), len(x_new)-1, array('d', x_new), len(y_new)-1, array('d', y_new))
  framed.SetDirectory(0)

  for x in xrange(1, framed.GetNbinsX()+1):
    for y in xrange(1, framed.GetNbinsY()+1):
      if x == 1 or x == framed.GetNbinsX() or y == 1 or y == framed.GetNbinsY():
        # This is a a frame bin
        framed.SetBinContent(x, y, frameValue)
      else:
        # adjust x and y if we're in the first frame so as to copy the output
        # values from the real TH2
        ux = x
        uy = y
        if x == 2:
          ux += 1
        elif x == (len(x_new)-2):
          ux -= 1
        if y == 2:
          uy += 1
        elif y == (len(y_new)-2):
          uy -= 1
        framed.SetBinContent(x, y, hist.GetBinContent(ux-2, uy-2))
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
        if i == 0 or i == 1: xbins_new[i] = xbins[i] - ((xbins[i+1]-xbins[i])/2) + 1E-5
        else: xbins_new[i] = xbins[i] - ((xbins[i+1]-xbins[i])/2) 
    xbins_new[len(xbins)-1] = xbins[len(xbins)-2] + ((xbins[len(xbins)-2]-xbins[len(xbins)-3])/2) 
    xbins_new[len(xbins)] = xbins[len(xbins)-1] + ((xbins[len(xbins)-1]-xbins[len(xbins)-2])/2) - 1E-5 
    
    ybins_new=[None]*(len(ybins)+1)
    for i in xrange(len(ybins)-1):
        if i == 0 or i == 1: ybins_new[i] = ybins[i] - ((ybins[i+1]-ybins[i])/2) + 1E-5
        else: ybins_new[i] = ybins[i] - ((ybins[i+1]-ybins[i])/2)
    ybins_new[len(ybins)-1] = ybins[len(ybins)-2] + ((ybins[len(ybins)-2]-ybins[len(ybins)-3])/2) 
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

def LimitTGraphFromJSON(js, label):
    xvals = []
    yvals = []
    for key in js:
        xvals.append(float(key))
        yvals.append(js[key][label])
    graph = R.TGraph(len(xvals), array('d', xvals), array('d', yvals))
    graph.Sort()
    return graph

def LimitBandTGraphFromJSON(js, central, lo, hi):
    xvals = []
    yvals = []
    yvals_lo = []
    yvals_hi = []
    for key in js:
        xvals.append(float(key))
        yvals.append(js[key][central])
        yvals_lo.append(js[key][central] - js[key][lo])
        yvals_hi.append(js[key][hi] - js[key][central])
    graph = R.TGraphAsymmErrors(len(xvals), array('d', xvals), array('d', yvals), array('d', [0]), array('d', [0]), array('d', yvals_lo), array('d', yvals_hi))
    graph.Sort()
    return graph

def GraphDifference(graph1,graph2,relative):
    xvals =[]
    yvals =[]
    if graph1.GetN() != graph2.GetN():
        return graph1
    for i in range(graph1.GetN()):
        xvals.append(graph1.GetX()[i])
        if relative :
            yvals.append(2*abs(graph1.GetY()[i]-graph2.GetY()[i])/(graph1.GetY()[i]+graph2.GetY()[i]))
        else: 
            yvals.append(2*(graph1.GetY()[i]-graph2.GetY()[i])/(graph1.GetY()[i]+graph2.GetY()[i]))

    diff_graph = R.TGraph(len(xvals),array('d',xvals),array('d',yvals))
    diff_graph.Sort()
    return diff_graph 

def Set(obj, **kwargs):
  for key, value in kwargs.iteritems():
    getattr(obj, 'Set'+key)(value)

def SetBirdPalette():
  nRGBs = 9
  stops   = array('d', [0.0000, 0.1250, 0.2500, 0.3750, 0.5000, 0.6250, 0.7500, 0.8750, 1.0000])
  red     = array('d', [0.2082, 0.0592, 0.0780, 0.0232, 0.1802, 0.5301, 0.8186, 0.9956, 0.9764])
  green   = array('d', [0.1664, 0.3599, 0.5041, 0.6419, 0.7178, 0.7492, 0.7328, 0.7862, 0.9832])
  blue    = array('d', [0.5293, 0.8684, 0.8385, 0.7914, 0.6425, 0.4662, 0.3499, 0.1968, 0.0539])
  R.TColor.CreateGradientColorTable(nRGBs, stops, red, green, blue, 255, 1)

def bestFit(tree, x, y, cut):
  nfind = tree.Draw(y+":"+x, cut + "deltaNLL == 0")
  gr0 = R.TGraph(1)
  if (nfind == 0):
    gr0.SetPoint(0,-999,-999)
  else:
    grc = R.gROOT.FindObject("Graph").Clone()
    if (grc.GetN() > 1): grc.Set(1)
    gr0.SetPoint(0,grc.GetXmax(),grc.GetYmax())
  gr0.SetMarkerStyle(34)
  gr0.SetMarkerSize(2.0)
  return gr0

def treeToHist2D(t, x, y, name, cut, xmin, xmax, ymin, ymax, xbins, ybins):
    t.Draw("2*deltaNLL:%s:%s>>%s_prof(%d,%10g,%10g,%d,%10g,%10g)" % (y, x, name, xbins, xmin, xmax, ybins, ymin, ymax), cut + "deltaNLL != 0", "PROF")
    prof = R.gROOT.FindObject(name+"_prof")
    h2d = R.TH2D(name, name, xbins, xmin, xmax, ybins, ymin, ymax)
    for ix in xrange(1,xbins+1):
        for iy in xrange(1,ybins+1):
            z = prof.GetBinContent(ix,iy)
            if (z != z) or (z>4294967295): # protect against NANs
                z=0
            h2d.SetBinContent(ix, iy, z)
    h2d.GetXaxis().SetTitle(x)
    h2d.GetYaxis().SetTitle(y)
    h2d.SetDirectory(0)
    h2d = NewInterpolate(h2d)
    return h2d

# Functions 'NewInterpolate' and 'rebin' are taken, translated and modified into python from:
# https://indico.cern.ch/event/256523/contribution/2/attachments/450198/624259/07JUN2013_cawest.pdf
# http://hep.ucsb.edu/people/cawest/interpolation/interpolate.h
def NewInterpolate(hist):
  histCopy = hist.Clone()

  # make temporary histograms to store the results of both steps
  hist_step1 = histCopy.Clone()
  hist_step1.Reset()
  hist_step2 = histCopy.Clone()
  hist_step2.Reset()

  nBinsX = histCopy.GetNbinsX()
  nBinsY = histCopy.GetNbinsY()

  xMin=1
  yMin=1
  xMax=histCopy.GetNbinsX()+1
  yMax=histCopy.GetNbinsY()+1
   
  for i in xrange(1,nBinsX+1):
    for j in xrange(1,nBinsY+1):
      # do not extrapolate outside the scan
      if (i<xMin) or (i>xMax) or (j<yMin) or (j>yMax): continue 
      binContent = histCopy.GetBinContent(i, j)
      binContentNW = histCopy.GetBinContent(i+1, j+1)
      binContentSE = histCopy.GetBinContent(i-1, j-1)
      binContentNE = histCopy.GetBinContent(i+1, j-1)
      binContentSW = histCopy.GetBinContent(i-1, j+1)
      binContentUp = histCopy.GetBinContent(i, j+1)
      binContentDown = histCopy.GetBinContent(i, j-1)
      binContentLeft = histCopy.GetBinContent(i-1, j)
      binContentRight = histCopy.GetBinContent(i+1, j)
      nFilled = 0
      if(binContentNW>0): nFilled+=1
      if(binContentSE>0): nFilled+=1
      if(binContentNE>0): nFilled+=1
      if(binContentSW>0): nFilled+=1
      if(binContentUp>0): nFilled+=1
      if(binContentDown>0): nFilled+=1
      if(binContentRight>0): nFilled+=1
      if(binContentLeft>0): nFilled+=1
      # if we are at an empty bin and there are neighbors
      # in specified direction with non-zero entries
      if(binContent==0) and (nFilled>1):
	# average over non-zero entries
	binContent = (binContentNW+binContentSE+binContentNE+binContentSW+binContentUp+binContentDown+binContentRight+binContentLeft)/nFilled
	hist_step1.SetBinContent(i,j,binContent)

   # add result of interpolation
  histCopy.Add(hist_step1)

  for i in xrange(1,nBinsX):
    for j in xrange(1,nBinsY):
      if(i<xMin) or (i>xMax) or (j<yMin) or (j>yMax): continue
      binContent = histCopy.GetBinContent(i, j)
      # get entries for "Swiss Cross" average
      binContentUp = histCopy.GetBinContent(i, j+1)
      binContentDown = histCopy.GetBinContent(i, j-1)
      binContentLeft = histCopy.GetBinContent(i-1, j)
      binContentRight = histCopy.GetBinContent(i+1, j)
      nFilled=0
      if(binContentUp>0): nFilled+=1
      if(binContentDown>0): nFilled+=1
      if(binContentRight>0): nFilled+=1
      if(binContentLeft>0): nFilled+=1
      if(binContent==0) and (nFilled>0):
        # only average over non-zero entries
        binContent = (binContentUp+binContentDown+binContentRight+binContentLeft)/nFilled
        hist_step2.SetBinContent(i,j,binContent)
  # add "Swiss Cross" average
  histCopy.Add(hist_step2)

  return histCopy

def rebin(hist):
  histName = hist.GetName()
  histName+="_rebin"

#  # bin widths are needed so as to not shift histogram by half a bin with each rebinning
#  # assume constant binning
#  binWidthX = hist.GetXaxis().GetBinWidth(1)
#  binWidthY = hist.GetYaxis().GetBinWidth(1)

#  histRebinned = R.TH2F(histName, histName, 2*hist.GetNbinsX(), hist.GetXaxis().GetXmin()+binWidthX/4, hist.GetXaxis().GetXmax()+binWidthX/4, 2*hist.GetNbinsY(), hist.GetYaxis().GetXmin()+binWidthY/4, hist.GetYaxis().GetXmax()+binWidthY/4)
  histRebinned = R.TH2F(histName, histName, 2*hist.GetNbinsX()-1, hist.GetXaxis().GetXmin(), hist.GetXaxis().GetXmax(), 2*hist.GetNbinsY()-1, hist.GetYaxis().GetXmin(), hist.GetYaxis().GetXmax())

  # copy results from previous histogram
  for iX in xrange(1,hist.GetNbinsX()+1):
    for iY in xrange(1,hist.GetNbinsY()+1):
      binContent = hist.GetBinContent(iX, iY)
      histRebinned.SetBinContent(2*iX-1, 2*iY-1, binContent)
  histRebinned.SetMaximum(hist.GetMaximum())
  histRebinned.SetMinimum(hist.GetMinimum())
  
  # use interpolation to re-fill histogram
  histRebinnedInterpolated = NewInterpolate(histRebinned)
  
  return histRebinnedInterpolated
