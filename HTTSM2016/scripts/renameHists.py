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
    base += '/src/CombineHarvester/HTTSM2016/shapes/USCMS/JES/'

    for channel in channels :
        fileName = base+'htt_%s.inputs-sm-13TeV-2D.root' % channel
        file = ROOT.TFile( fileName, "UPDATE" )
        print file
        catBases = ["vbf","boosted","0jet"]
        if channel in ['et','mt'] :
            nList = []
            catBases = ["vbf","boosted","0jet"]
            for c in catBases :
                nList.append(c)
                nList.append('antiiso_'+c+'_cr')
                nList.append('wjets_'+c+'_cr')
            catBases = list(nList)
        if channel == 'ttbar' :
            catBases.append('all')
            

        for catBase in catBases :
            if channel == 'tt' and catBase == 'vbf' : catBase = 'VBF'
            cat = channel+'_'+catBase
            print cat
            if channel == "tt" :
                histKeys = get_Keys_Of_Class( file, cat, "TH1D" )
            else :
                histKeys = get_Keys_Of_Class( file, cat, "TH1F" )

            for k in histKeys :
                name = k.GetName()
                if 'CMS_scale_j_' in name :
                    newName = name.replace('j_13TeV', 'j_'+cat+'_13TeV')
                    print "Swap:",name," --> ",newName
                    k.SetName(newName)
                    k.SetTitle(newName)
                    k.Write('', ROOT.TObject.kOverwrite)
                    print "final name:",k.GetName()




