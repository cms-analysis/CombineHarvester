Python Interface {#python-interface}
====================================

The python interface is embedded within the shared library (`CombineTools/lib/libCHCombineTools.so`) that is produced when the code is compiled. Add this directory to your `PYTHONPATH` environment variable so that it can be imported from anywhere. This can also be achieved by doing:

    eval `make env`

Then in a python script you can do, e.g. `import libCHCombineTools as ch`. The sections below summarises the methods that are currently supported.

## Constructors and copying
C++:

    ch::CombineHarvester cb;
    ch::CombineHarvester cb_shallow_copy = cb.cp();
    ch::CombineHarvester cb_deep_copy = cb.deep();

Python:

    cb = ch.CombineHarvester()
    cb_shallow_copy = cb.cp()
    cb_deep_copy = cb.deep()

## Logging and Printing
C++:

    cb.PrintAll();
    cb.PrintObs();
    cb.PrintProcs();
    cb.PrintSysts();
    cb.PrintParams();
    cb.SetVerbosity(1);

Python:

    cb.PrintAll()
    cb.PrintObs()
    cb.PrintProcs()
    cb.PrintSysts()
    cb.PrintParams()
    cb.SetVerbosity(1)

## Datacards

### Parsing specifying metadata
C++:

    cb.ParseDatacard("datacard.txt", "htt", "8TeV", "mt", 6, "125");

Python:

    cb.ParseDatacard("datacard.txt", "htt", "8TeV", "mt", 6, "125")

Metadata parameters also have default values and can be named explicitly:

    cb.ParseDatacard("datacard.txt", analysis = "htt", mass = "125")

### Parsing with pattern substitution
C++:

    cb.ParseDatacard("htt_mt_8_8TeV.txt", "$ANALYSIS_$CHANNEL_$BINID_$ERA.txt");

Python (note the different method name):

    cb.QuickParseDatacard("htt_mt_8_8TeV.txt", "$ANALYSIS_$CHANNEL_$BINID_$ERA.txt")

### Writing
C++:

    cb.WriteDatacard("card.txt", "file.root"); // or
    ...
    TFile out("file.root", "recreate");
    cb.WriteDatacard("card.txt", out);

Python (second method not yet available):

    cb.WriteDatacard("card.txt", "file.root")

## Filtering
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

## Set producers

Only the basic set producer methods are available at the moment. The generic methods (GenerateSetFromObs, GenerateSetFromProcs, GenerateSetFromSysts) will be adapted shortly.

C++:

    set<string> bins = cb.bin_set();
    for (auto p : cb.process_set()) {
      ...
    }

Python:

    bins = cb.bin_set()
    for p in cb.process_set():
        ...

## Modifications

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

## Rate and shape evaluation

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

## Datacard creation

Creating observation and process entries is supported.

C++:

    cb.AddObservations({"*"}, {"htt"}, {"8TeV"}, {"mt", "et"}, {{0, "0jet"}, {1, "1jet"}})
    cb.AddProcesses({"*"}, {"htt"}, {"8TeV"}, {"mt", "et"}, {"ZTT", "ZL", "ZJ"}, {{0, "0jet"}, {1, "1jet"}}, false)
Python:

    cb.AddObservations(['*'], ['htt'], ['8TeV'], ['mt', 'et'], [(0, "0jet"), (1, "1jet")])
    cb.AddProcesses(['*'], ['htt'], ['8TeV'], ['mt', 'et'], ['ZTT', 'ZL', 'ZJ'], [(0, "0jet"), (1, "1jet")], False)
    ## or with default values:
    cb.AddProcesses(procs = ['ZTT', 'ZL', ZJ'], bin = [(0, "0jet"), (1, "1jet")], signal=False)

As is bin-by-bin creating and merging.

C++:

    cb.MergeBinErrors(0.1, 0.5);
    cb.AddBinByBin(0.1, true, cb);

Python:

    cb.MergeBinErrors(0.1, 0.5)
    cb.AddBinByBin(0.1, True, cb)

The AddSyst ExtractPdfs, ExtractData and AddWorkspace methods are not currently supported. The creation of Systematic entries via the [AddSyst](\ref ch::CombineHarvester::AddSyst) method is not trivial to convert to python due to the heavy use of C++ templates. A python equivalent will be made available in a future release.

