import ROOT
import os



# Can use to return all hists in a dir
def get_Keys_Of_Class( file_, dir_, class_ ) :
    keys = []
    d = file_.Get( dir_ )
    allKeys = d.GetListOfKeys()

    #print "keys of class"
    for k in allKeys :
        if k.GetClassName() == class_ :
            keys.append( k )

    return keys

if '__main__' in __name__ :
    channels = ['tt','et','mt','em','ttbar']
    base = os.getenv('CMSSW_BASE')
    print base
    base += '/src/CombineHarvester/HTTSM2016/shapes/USCMS/'

    for channel in channels :
        fileName = base+'htt_%s.inputs-sm-13TeV-2D.root' % channel
        file = ROOT.TFile( fileName, "UPDATE" )
        print file
        catBases = ["vbf","boosted","0jet"]
        if channel in ['tt',] :
            nList = []
            for c in catBases :
                nList.append(c)
                nList.append(c+'_qcd_cr')
            catBases = list(nList)
        if channel in ['et','mt'] :
            nList = []
            for c in catBases :
                nList.append(c)
                nList.append('antiiso_'+c+'_cr')
                nList.append('wjets_'+c+'_cr')
            catBases = list(nList)
        if channel == 'ttbar' :
            catBases.append('all')
            

        for catBase in catBases :
            cat = channel+'_'+catBase
            print cat
            if channel == "tt" :
                histKeys = get_Keys_Of_Class( file, cat, "TH1D" )
            else :
                histKeys = get_Keys_Of_Class( file, cat, "TH1F" )

            for k in histKeys :
                name = k.GetName()
                #if 'HWW_qq125' in name :
                #if 'HWW_gg125' in name :
                if 'ggH' in name and not 'hww' in name :
                    #newName = name.replace('HWW_qq125', 'qqH_hww125')
                    #newName = name.replace('HWW_gg125', 'ggH_hww125')
                    newName = name.replace('ggH', 'ggH_htt')
                    print "Swap:",name," --> ",newName
                    k.SetName(newName)
                    k.SetTitle(newName)
                    k.Write('', ROOT.TObject.kOverwrite)
                    print "final name:",k.GetName()

                if 'qqH' in name and not 'hww' in name :
                    newName = name.replace('qqH', 'qqH_htt')
                    print "Swap:",name," --> ",newName
                    k.SetName(newName)
                    k.SetTitle(newName)
                    k.Write('', ROOT.TObject.kOverwrite)
                    print "final name:",k.GetName()

                if 'ZH' in name and not 'hww' in name :
                    newName = name.replace('ZH', 'ZH_htt')
                    print "Swap:",name," --> ",newName
                    k.SetName(newName)
                    k.SetTitle(newName)
                    k.Write('', ROOT.TObject.kOverwrite)
                    print "final name:",k.GetName()

                if 'WH' in name and not 'hww' in name :
                    newName = name.replace('WH', 'WH_htt')
                    print "Swap:",name," --> ",newName
                    k.SetName(newName)
                    k.SetTitle(newName)
                    k.Write('', ROOT.TObject.kOverwrite)
                    print "final name:",k.GetName()


