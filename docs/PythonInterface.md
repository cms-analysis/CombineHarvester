Python Interface {#python-interface}
====================================

[TOC]
The C++ CombineHarvester class and a number of other tools have a python interface available. The module containing this interface can be imported like any other CMSSW python module:

    import CombineHarvester.CombineTools.ch as ch

The sections below summarise the methods that are currently supported.

Constructors and copying {#py-constr-copy}
==========================================
C++:

    ch::CombineHarvester cb;
    ch::CombineHarvester cb_shallow_copy = cb.cp();
    ch::CombineHarvester cb_deep_copy = cb.deep();

Python:

    cb = ch.CombineHarvester()
    cb_shallow_copy = cb.cp()
    cb_deep_copy = cb.deep()

Logging and Printing {#py-log-print}
====================================
C++:

    cb.PrintAll();
    cb.PrintObs();
    cb.PrintProcs();
    cb.PrintSysts();
    cb.PrintParams();
    cb.SetVerbosity(1);
    cb.Verbosity();

Python:

    cb.PrintAll()
    cb.PrintObs()
    cb.PrintProcs()
    cb.PrintSysts()
    cb.PrintParams()
    cb.SetVerbosity(1)
    cb.Verbosity()

Datacards {#py-datacards}
=========================

Parsing specifying metadata  {#py-datacards-meta}
-------------------------------------------------
C++:

    cb.ParseDatacard("datacard.txt", "htt", "8TeV", "mt", 6, "125");

Python:

    cb.ParseDatacard("datacard.txt", "htt", "8TeV", "mt", 6, "125")

Metadata parameters also have default values and can be named explicitly:

    cb.ParseDatacard("datacard.txt", analysis = "htt", mass = "125")

Parsing with pattern substitution {#py-datacards-pat-sub}
---------------------------------------------------------
C++:

    cb.ParseDatacard("htt_mt_8_8TeV.txt", "$ANALYSIS_$CHANNEL_$BINID_$ERA.txt");

Python (note the different method name):

    cb.QuickParseDatacard("htt_mt_8_8TeV.txt", "$ANALYSIS_$CHANNEL_$BINID_$ERA.txt")

Writing {#py-datacards-writing}
-------------------------------
C++:

    cb.WriteDatacard("card.txt", "file.root"); // or
    ...
    TFile out("file.root", "recreate");
    cb.WriteDatacard("card.txt", out);

Python (second method not yet available):

    cb.WriteDatacard("card.txt", "file.root")

Filtering {#py-filtering}
=========================
All of the basic filter methods can be called and chained in a similar way in both interfaces. For example:

C++:

    cb.bin({"muTau_vbf"}).era({"7TeV", "8TeV"}).signals().process({"ggH"}, false);

Python:

    cb.bin(['muTau_vbf']).era(['7TeV', '8TeV']).signals().process(['ggH'], False)

The generic filter methods (FilterAll, FilterObs, FilterProcs, FilterSysts) have also been adapted to accept python functions, e.g.

C++:

    cb.FilterAll([](ch::Object const* obj) {
      return obj->mass() == "110" || obj->mass() == "145";
      });

Python:

    cb.FilterAll(lambda obj : obj.mass() in ['110', '145'])

Set producers {#py-sets}
========================

All basic set producer methods are available.

C++:

    set<string> bins = cb.bin_set();
    for (auto p : cb.process_set()) {
      ...
    }

Python:

    bins = cb.bin_set()
    for p in cb.process_set():
        ...

The generic methods are available too, and accept a generic function object.

C++:

    set<string> bins = cb.SetFromAll(std::mem_fn(&ch::Object::bin));
    set<string> some_set = cb.SetFromProcs([](ch::Process const* p) {
            return p->process() + "_" + p->bin();
        });

Python:

    bins = cb.SetFromAll(ch.Object.bin)
    some_set = cb.SetFromProcs(lambda x : x.process() + '_' + x.bin())

Modifications {#py-modifications}
=================================

The `GetParameter`, and `UpdateParameters` methods that use `ch::Parameter` objects are not available (and may be deprecated soon anyway). The `UpdateParameters` method taking a `RooFitResult` is available however.

C++:

    TFile f("mlfit.root");
    RooFitResult *res = (RooFitResult*)f.Get("fit_s");
    cb.UpdateParameters(*res);

Python:

    import ROOT as R
    f = R.TFile("mlfit.root")
    res = f.Get("fit_s")
    cb.UpdateParameters(res)

The generic ForEach methods are also available and can take arbitrary python functions as input.

C++:

    void SwitchToSignal(ch::Process const* p) {
        if (p->process() == "ggH_hww125") p->set_signal(true);
    }
    cb.ForEachProc(SwitchToSignal);

Python:

    def SwitchToSignal(p):
        if p.process() == 'ggH_hww125': p.set_signal(True)
    cb.ForEachProc(SwitchToSignal)

Rate and shape evaluation {#py-eval}
====================================

All methods are supported with a similar interface.

C++:

    double a = cb.GetObservedRate();
    double b = cb.GetRate();
    double c = cb.GetUncertainty();
    double d = cb.GetUncertainty(res, 500);
    TH1F e = cb.GetObservedShape();
    TH1F f = cb.GetShape();
    TH1F g = cb.GetShapeWithUncertainty(res, 500);

Python:

    import ROOT as R
    a = cb.GetObservedRate()
    b = cb.GetRate()
    c = cb.GetUncertainty()
    d = cb.GetUncertainty(res, 500)
    e = cb.GetObservedShape()
    f = cb.GetShape()
    g = cb.GetShapeWithUncertainty(res, 500)

Datacard creation {#py-creation}
================================

Creating observation and process entries is supported.

C++:

    cb.AddObservations({"*"}, {"htt"}, {"8TeV"}, {"mt", "et"}, {{0, "0jet"}, {1, "1jet"}})
    cb.AddProcesses({"*"}, {"htt"}, {"8TeV"}, {"mt", "et"}, {"ZTT", "ZL", "ZJ"}, {{0, "0jet"}, {1, "1jet"}}, false)
Python:

    cb.AddObservations(['*'], ['htt'], ['8TeV'], ['mt', 'et'], [(0, "0jet"), (1, "1jet")])
    cb.AddProcesses(['*'], ['htt'], ['8TeV'], ['mt', 'et'], ['ZTT', 'ZL', 'ZJ'], [(0, "0jet"), (1, "1jet")], False)
    ## or with default values:
    cb.AddProcesses(procs = ['ZTT', 'ZL', ZJ'], bin = [(0, "0jet"), (1, "1jet")], signal=False)

As is bin-by-bin creating and merging, but note that these methods have been deprecated in favour of the standalone ch::BinByBinFactory class (see below).

C++:

    cb.MergeBinErrors(0.1, 0.5);
    cb.AddBinByBin(0.1, true, cb);

Python:

    cb.MergeBinErrors(0.1, 0.5)
    cb.AddBinByBin(0.1, True, cb)

The creation of Systematic entries with the `AddSyst` method is supported, though has a slightly different syntax due to the heavy template usage in the C++ version.

C++:

    cb.cp().process({"WH", "ZH"}).AddSyst(
      cb, "QCDscale_VH", "lnN", SystMap<channel, era, bin_id>::init
        ({"mt"}, {"7TeV", "8TeV"},  {1, 2},               1.010)
        ({"mt"}, {"7TeV", "8TeV"},  {3, 4, 5, 6, 7},      1.040)
        ({"et"}, {"7TeV"},          {1, 2, 3, 5, 6, 7},   1.040)
        ({"et"}, {"8TeV"},          {1, 2},               1.010)
        ({"et"}, {"8TeV"},          {3, 5, 6, 7},         1.040));

Python:

    cb.cp().process(['WH', 'ZH']).AddSyst(
      cb, "QCDscale_VH", "lnN", ch.SystMap('channel', 'era', 'bin_id')
        (['mt'], ['7TeV', '8TeV'],  [1, 2],               1.010)
        (['mt'], ['7TeV', '8TeV'],  [3, 4, 5, 6, 7],      1.040)
        (['et'], ['7TeV'],          [1, 2, 3, 5, 6, 7],   1.040)
        (['et'], ['8TeV'],          [1, 2],               1.010)
        (['et'], ['8TeV'],          [3, 5, 6, 7],         1.040))

Note that asymmetric uncertainties are created in a different way in Python or C++:

C++:

    cb.cp().process({"WH", "ZH"}).AddSyst(
      cb, "QCDscale_VH", "lnN", SystMapAsymm<channel, era, bin_id>::init
        ({"mt"}, {"7TeV", "8TeV"}, {1, 2}, 0.91, 1.05));

Python:

    cb.cp().process(['WH', 'ZH']).AddSyst(
      cb, "QCDscale_VH", "lnN", ch.SystMap('channel', 'era', 'bin_id')
        (['mt'], ['7TeV', '8TeV'], [1, 2], (0.91, 1.05)))

The ExtractPdfs, ExtractData and AddWorkspace methods are not currently supported.

Class: CardWriter {#py-card-writer}
================================
The ch::CardWriter class has an identical interface in python.

C++:

    ch::CardWriter writer("$TAG/$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt",
                          "$TAG/common/$ANALYSIS_$CHANNEL.input_$ERA.root");
    writer.WriteCards("LIMITS/cmb", cb);

Python:

    writer = ch.CardWriter('$TAG/$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt',
                           '$TAG/common/$ANALYSIS_$CHANNEL.input_$ERA.root')
    writer.WriteCards('LIMITS/cmb', cb)

Class: BinByBinFactory {#py-bbbfactory}
=======================================
The ch::BinByBinFactory class has an identical interface in python.

C++:

    auto bbb = ch::BinByBinFactory()
        .SetAddThreshold(0.1)
        .SetMergeThreshold(0.5)
        .SetFixNorm(true);
    bbb.MergeBinErrors(cb.cp().backgrounds());
    bbb.AddBinByBin(cb.cp().backgrounds(), cb);

Python:

    bbb = ch.BinByBinFactory()
    bbb.SetAddThreshold(0.1).SetMergeThreshold(0.5).SetFixNorm(True)
    bbb.MergeBinErrors(cb.cp().backgrounds())
    bbb.AddBinByBin(cb.cp().backgrounds(), cb)
