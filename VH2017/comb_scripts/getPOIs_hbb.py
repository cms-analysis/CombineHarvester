#!/usr/bin/env python
getPOIs = { 
    "A1_hbb": {
        "POIs": {
            "mu_BR_bb": {"range":[0,3], "points":30}
            },
        "POIsNominal": {
            "mu_BR_bb": 1.0
            },
        "POIsFix":{},
        "UseWsp": "A1"
    },
    "A1_hbb_5P": {
        "POIs": {
            "mu_XS_VBF_BR_bb": {"range":[-5,7], "points":30},
            "mu_XS_ggFbbH_BR_bb": {"range":[-5,9], "points":30},
            "mu_XS_WH_BR_bb": {"range":[-0.5,3], "points":30},
            "mu_XS_ZH_BR_bb": {"range":[-0.5,3], "points":30},
            "mu_XS_ttHtH_BR_bb": {"range":[-0.5,3], "points":30}
            },
        "POIsNominal" : {
            "mu_XS_VBF_BR_bb": 1.0,
            "mu_XS_ggFbbH_BR_bb": 1.0,
            "mu_XS_WH_BR_bb": 1.0,
            "mu_XS_ZH_BR_bb": 1.0,
            "mu_XS_ttHtH_BR_bb": 1.0,
        },
        "POIsFix":{},
        "UseWsp": "A1"
    }
}
def GetWsp(model):
    if model in getPOIs and 'UseWsp' in getPOIs[model]:
        return getPOIs[model]['UseWsp']
    else:
        return model

def GetPOIsList(model, sep=',', onlyScanPOIs=False):
    POIs = getPOIs[model]["POIs"].keys()
    if onlyScanPOIs and 'ScanPOIs' in getPOIs[model]:
        POIs = getPOIs[model]['ScanPOIs']
    return sep.join(POIs)

def GetPOIRanges(model):
    poiRanges = ':'.join(['%s=%g,%g' % (POI, d["range"][0], d["range"][1]) for POI, d in getPOIs[model]["POIs"].iteritems()])
    #return poiRanges + ':qcdeff=0.0001,1.0:r0p1=0.9,1.4:r1p0=0.8,1.3:r1p1=0.4,0.6:r2p0=1.0,3.0:r2p1=-1.0,-0.3:b0_selVBF_CAT4=0.0,20.0:SF_TT_Znn_2017=0.5,1.5:SF_TT_high_Zll_2017=0.3,1.6:SF_TT_low_Zll_2017=0.5,1.5:SF_TT_norm_high_Zll=0.5,1.5:SF_TT_norm_low_Zll=0.5,1.5:SF_Zj0b_norm_high_Zll=0.5,1.5:SF_Zj0b_norm_low_Zll=0.5,1.5:SF_Zj1b_Znn=0.3,1.8:SF_Zj1b_Znn_2017=0.3,1.8:SF_Zj1b_high_Zll_2017=0.6,1.9:SF_Zj1b_low_Zll_2017=0.3,1.7:SF_Zj1b_norm_high_Zll=0.5,1.5:SF_Zj1b_norm_low_Zll=0.5,1.5:SF_Zj2b_Znn=0.7,1.6:SF_Zj2b_Znn_2017=0.7,1.7:SF_Zj2b_high_Zll_2017=0.3,1.4:SF_Zj2b_low_Zll_2017=0.3,1.6:SF_Zj2b_norm_high_Zll=0.7,2:SF_Zj2b_norm_low_Zll=0.6,1.6:bgnorm_ddQCD_fh_j7_t3=0.9,1.1:bgnorm_ddQCD_fh_j7_t4=0.8,1.2:bgnorm_ddQCD_fh_j8_t3=0.9,1.1:bgnorm_ddQCD_fh_j8_t4=0.9,1.1:bgnorm_ddQCD_fh_j9_t3=0.95,1.15:bgnorm_ddQCD_fh_j9_t4=0.9,1.1'
    return poiRanges + ':qcdeff=0.0001,1.0:r0p1=0.9,1.4:r1p0=0.8,1.3:r1p1=0.4,0.6:r2p0=1.0,3.0:r2p1=-1.0,-0.3:b0_selVBF_CAT4=0.0,20.0'

def SetSMVals(model):
    set_args = []
    for POI in getPOIs[model]["POIs"]:
        defVal = 1.0
        if 'SMVals' in getPOIs[model] and POI in getPOIs[model]['SMVals']:
            defVal = getPOIs[model]['SMVals'][POI]
        set_args.append('%s=%g' % (POI, defVal))
    return ','.join(set_args)

def SetNominalVals(model):
    set_args = []
    for POI in getPOIs[model]["POIs"]:
        defVal = 1.0
        if 'POIsNominal' in getPOIs[model] and POI in getPOIs[model]['POIsNominal']:
            defVal = getPOIs[model]['POIsNominal'][POI]
            set_args.append('%s=%g' % (POI, defVal))
    return ','.join(set_args)

def GetFreezeList(model):
    return ','.join(list(getPOIs[model]['POIsFix'])) 

def GetGeneratePOIs(model):
    doPOIs = getPOIs[model]["POIs"].keys()
    if 'ScanPOIs' in getPOIs[model]:
        doPOIs = getPOIs[model]['ScanPOIs']
    ret = 'P:n::'
    ret += ':'.join(['%s,%s' % (X,X) for X in doPOIs])
    return ret

def GetRangeGeneratePOIs(model):
    doPOIs = getPOIs[model]["POIs"].keys()
    for POI, d in getPOIs[model]["POIs"].iteritems():
        if 'scan' not in d:
            return GetGeneratePOIs(model)
    if 'ScanPOIs' in getPOIs[model]:
        doPOIs = getPOIs[model]['ScanPOIs']
    ret = 'P:n:centeredRange::'
    ret += ':'.join(['%s,%s,%f' % (X,X, getPOIs[model]["POIs"][X]['scan']) for X in doPOIs])
    return ret

def GetMinimizerOpts(label='Default'):
  #return '--floatOtherPOIs 1 --useAttributes 1 --noMCbonly 1 --cminDefaultMinimizerStrategy 0 --cminApproxPreFitTolerance=100 --cminFallbackAlgo "Minuit2,migrad,1:0.1" --cminFallbackAlgo "Minuit2,migrad,0:1.0" --cminFallbackAlgo "Minuit2,migrad,1:1.0" --cminFallbackAlgo "Minuit2,migrad,0:5.0" --X-rtd MINIMIZER_MaxCalls=9999999 --X-rtd MINIMIZER_analytic --X-rtd FAST_VERTICAL_MORPH'
  return '--noMCbonly 1 --cminDefaultMinimizerStrategy 0 --cminApproxPreFitTolerance=100 --cminFallbackAlgo Minuit2,migrad,1:0.1 --cminFallbackAlgo Minuit2,migrad,0:0.5 --cminFallbackAlgo Minuit2,migrad,1:0.5 --cminFallbackAlgo Minuit2,migrad,0:1.0 --cminFallbackAlgo Minuit2,migrad,1:1.0 --X-rtd MINIMIZER_MaxCalls=999999999 --X-rtd MINIMIZER_analytic --X-rtd FAST_VERTICAL_MORPH --X-rtd ADDNLL_RECURSIVE=0 --useAttributes 1'

if __name__ == "__main__":
    import sys
    model = getPOIs[sys.argv[1]]

    if sys.argv[2] == '-m':
        print GetWsp(sys.argv[1])

    if sys.argv[2] == '-p':
        print GetPOIsList(sys.argv[1])

    if sys.argv[2] == '-P':
        print GetPOIsList(sys.argv[1], sep=' ', onlyScanPOIs=True)

    if sys.argv[2] == '-r':
        print GetPOIRanges(sys.argv[1])
    
    if sys.argv[2] == '-R':
        print GetPOISpecialRanges(sys.argv[1], sys.argv[3])

    if sys.argv[2] == '-s':
        print SetSMVals(sys.argv[1])

    if sys.argv[2] == '-n':
        print SetNominalVals(sys.argv[1])

    if sys.argv[2] == '-f':
        print GetFreezeList(sys.argv[1])

    if sys.argv[2] == '-g':
        print GetGeneratePOIs(sys.argv[1])
    
    if sys.argv[2] == '-G':
        print GetRangeGeneratePOIs(sys.argv[1])
    
    if sys.argv[2] == '-F':
        flist = GetFreezeList(sys.argv[1])
        if flist == '':
            print ''
        else:
            print ',' + GetFreezeList(sys.argv[1])

    if sys.argv[2] == '-O':
        print GetMinimizerOpts()
