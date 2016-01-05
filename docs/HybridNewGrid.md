# Calculating grids of CLs values using toys

The following are basic instructions for using the **HybridNewGrid** method of `combineTool.py`. In a similar fashion to the **AsymptoticGrid** method most of the settings are  specified in a json file. An example is given in `CombinePdfs/scripts/mssm_hybrid_grid.json`:

```json
{
  "verbose" : false,
  "opts" : "--testStat=TEV --frequentist --singlePoint 1.0 --saveHybridResult --clsAcc 0 --fullBToys --fork 0",
  "POIs" : ["mA", "tanb"],
  "grids" : [
    ["580:600:20", "10:30:4", ""]
  ],
  "toys_per_cycle"  : 500,
  "min_toys"        : 500,
  "max_toys"        : 5000,
  "signif"          : 3.0,
  "CL"              : 0.95,
  "contours"        : ["obs", "exp-2", "exp-1", "exp0", "exp+1", "exp+2"],
  "make_plots"      : false,
  "plot_settings" : {
      "one_sided"     : false,
      "model_label"   : "m_{H}^{mod+}",
      "poi_labels"    : ["m_{A}", "tan#beta"],
      "null_label"    : "SM",
      "alt_label"     : "MSSM",
      "cms_subtitle"  : "Internal",
      "formats"       : [".pdf", ".png"]
  },
  "zipfile"         : "collected.zip",
  "output"          : "HybridNewGridMSSM.root",
  "output_incomplete" : true
}
```

The `combineTool.py` method is then invoked as follows:

```sh
combineTool.py -M HybridNewGrid scripts/mssm_hybrid_grid.json --cycles [cycles] -d [workspace]
```

This method will generate the specified number of toy cycles for each model point, where one cycle implies one run of combine with a new random seed. The setting `toys_per_cycle` controls the number of background-only and signal+background toys that will be generated in each combine job. Several options are also provided which can be used concentrate the generation of toys around the relevant observed and expected exclusion contours. These specify a set of criteria which, when fulfilled, prevent the creation of any further combine jobs for that model point. These settings are:

 - `min_toys`: Require that at least this many toys are run at each point
 - `max_toys`: When this number of toys is reached do not run any more jobs, even if other criteria are still not fulfilled
 - `signif`: Require that the CLs value at each point is at least this many standard deviations from the specified confidence level value (1 - CL), i.e. `abs(CLs - (1-CL)) / ClsErr > signif`, where `CLsErr` is the statistical uncertainty on the CLs value. This criteria must be met for observed and/or expected quantiles listed in `contours`. Essentially this requires the probablity of the CLs value we have determined being on the wrong side of the critical CLs value to be very small.
 
The `combineTool.py` command above can be repeatedly invoked until a sufficient number of points have met the chosen criteria. At any point the TGraph2Ds of the CLs values can be produced by adding the option `--output`. To just check the progress of the points run with `--cycles 0`. It is possible to choose if model points which have not yet met these criteria should be included in the output graphs with the option `output_incomplete`. When set to `false` only the points passing the validation will be included.

Plots of the test statistic distributions at each model point can be created by setting the option `make_plots` to `true`.

Due to the potentially huge number of output files expected for large grids, and because this can cause problems for some networked file-systems, it is possible to automatically transfer the output to a single zip file and have ROOT read the files directly from this archive. This is enable by setting the value of `zipfile` to any non-empty string. Each time `combineTool.py` is invoked it will first look for output files in the given zip file (creating it if it doesn't already exist), then it will look for any other files in the local directory and append these to the zip file before deleting the local version.