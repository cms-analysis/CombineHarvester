### Nov 13, 2016
### File to store all of the configurations for the
### SM HTT prefit/postfit plotter
###
###
# FIXME FIXME FIXME
# Once the most updated root files are uploaded, the default paths can be set
# in getFile()
# ETau, MuTau and EMu need to double check getBinMap() whic
# provides the number of times unrolled and number of mass bins per
# unroll and labeling

from collections import OrderedDict

# Provide the category names (folder names)
# where we should look for histograms
def getCategories( channel="tt", prefix="" ) :
    preCategories=["_0jet","_boosted","_VBF"] 
    categories=[prefix+channel+cat for cat in preCategories]
    return categories


# Provide standard mapping to our files
# this can be overridden with --inputFile
def getFile( channel ) :
    fileMap = {
        "et" : "shapes/USCMS/htt_et.inputs-sm-13TeV-mvis.root", # Not up to date
        "mt" : "shapes/USCMS/htt_mt.inputs-sm-13TeV-mvis.root", # Not up to date
        "em" : "shapes/USCMS/htt_em.inputs-sm-13TeV-mvis.root", # Not up to date
        "tt" : "../../SM-PAS-2016/USCMS/htt_tt.inputs-sm-13TeV-svfitmass2D-20161103.root",
        #"tt" : "shapes/USCMS/htt_tt.inputs-sm-13TeV-svfitmass2D.root", # Not up to date
    }
    return fileMap[ channel ]

def getInfoMap( higgsSF ) :
    infoMap = OrderedDict()
    # Name : Add these shapes [...], legend name, leg type, fill color
    infoMap["data_obs"] = [["data_obs",],"Observed","elp",1]
    infoMap["ZTT"] = [["ZTT"],"Z#rightarrow#tau_{#mu}#tau_{h}","f","#ffcc66"]
    infoMap["ZJ"] = [["ZJ","ZL","ZLL"],"DY others","f","#4496c8"]
    infoMap["TT"] = [["TTT","TTJ"],"t#bar{t}+jets","f","#9999cc"]
    infoMap["VV"] = [["VV",],"Diboson","f","#12cadd"]
    infoMap["W"] = [["W",],"Electroweak","f","#de5a6a"]
    infoMap["QCD"] = [["QCD",],"QCD multijet","f","#ffccff"]
    infoMap["qqH125"] = [["qqH125",],"qqH 125 (X%i)"%higgsSF,"l","#4faf4e"]
    infoMap["ggH125"] = [["ggH125",],"ggh 125 (X%i)"%higgsSF,"l","#5911ff"]
    return infoMap


def getBackgrounds() :    
    bkgs=["QCD", "VV", "TT", "W", "ZJ", "ZTT"]
    return bkgs

def getSignals() :
    signals=["qqH125", "ggH125"]
    return signals

# Labeling map, this provides, for each channel
# and category :
# unrolling binning in "binning"
# the number of times unrolled in a variable "nx"
# the number of mass bins per unroll "ny"
# and labeling for the divider lines
def getBinMap() :
    binMap = {
    # FIXME    "et" : {
    # FIXME        "et_0jet" : {
    # FIXME            "nx" : 5,
    # FIXME            "ny" : 30, #FIXME
    # FIXME            "binning" : [15,25,35,45,55],
    # FIXME            "name" : "p_{T}(#mu)",
    # FIXME        },
    # FIXME        "et_boosted" : {
    # FIXME            "nx" : 7,
    # FIXME            "ny" : 12, #FIXME
    # FIXME            "binning" : [0,100,150,200,250,300,350],
    # FIXME            "name" : "p_{T}(H)",
    # FIXME        },
    # FIXME        "et_VBF" : {
    # FIXME            "nx" : 4,
    # FIXME            "ny" : 1, #FIXME
    # FIXME            "binning" : [300,700,1100,1500],
    # FIXME            "name" : "m_{jj}",
    # FIXME        },
    # FIXME    }, # end 'et'
    # FIXME    "mt" : {
    # FIXME        "mt_0jet" : {
    # FIXME            "nx" : 5,
    # FIXME            "ny" : 30, #FIXME
    # FIXME            "binning" : [15,25,35,45,55],
    # FIXME            "name" : "p_{T}(#mu)",
    # FIXME        },
    # FIXME        "mt_boosted" : {
    # FIXME            "nx" : 7,
    # FIXME            "ny" : 12, #FIXME
    # FIXME            "binning" : [0,100,150,200,250,300,350],
    # FIXME            "name" : "p_{T}(H)",
    # FIXME        },
    # FIXME        "mt_VBF" : {
    # FIXME            "nx" : 4,
    # FIXME            "ny" : 1, #FIXME
    # FIXME            "binning" : [300,700,1100,1500],
    # FIXME            "name" : "m_{jj}",
    # FIXME        },
    # FIXME    }, # end 'mt'
        "em" : {
            "em_0jet" : {
                "nx" : 5,
                "ny" : 30, #FIXME
                "binning" : [15,25,35,45,55],
                "name" : "p_{T}(#mu)",
            },
            "em_boosted" : {
                "nx" : 7,
                "ny" : 12, #FIXME
                "binning" : [0,100,150,200,250,300,350],
                "name" : "p_{T}(H)",
            },
            "em_VBF" : {
                "nx" : 4,
                "ny" : 1, #FIXME
                "binning" : [300,700,1100,1500],
                "name" : "m_{jj}",
            },
        }, # end 'em'
        "tt" : {
            "tt_0jet" : {
                "nx" : 1,
                "ny" : 30,
                "binning" : [0,],
                "name" : "N/A",
            },
            "tt_boosted" : {
                "nx" : 4,
                "ny" : 12,
                "binning" : [0,100,170,300],
                "name" : "p_{T}(H)",
            },
            "tt_VBF" : {
                "nx" : 4,
                "ny" : 12,
                "binning" : [0,300,500,800],
                "name" : "m_{jj}",
            },
        }, # end 'tt'
    }
    return binMap





