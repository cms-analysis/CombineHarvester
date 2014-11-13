Introduction {#mainpage}
========================

[TOC]

Build System {#build}
=====================
The code within the directory `CombineHarvester` is organised into a set of packages, each contained within a subdirectory, that produce shared libraries and executable programs. Currently there is just one package: `CombineHarvester/CombineTools`, which contains the core part of this framework and some example programs. In the future, each analysis will create their own package where all the specific datacard configuration, plotting routines and other scripts can be stored and developed. While the CMSSW environment is required to use this framework, the source code is not compiled with scram but rather using a make-based build system. Each package should contain at least this standard set of folders which are used by the build system:

    makefile      : symlink to CombineHarvester/mk/makefile
    Rules.mk      : makefile fragment to store list of subpackages and dependencies
    interface/    : header files
    src/          : source code (.cc) to be compiled to the shared library
    obj/          : used by the build system
    lib/          : used by the build system
    test/         : code for executable programs (.cpp)
    bin/          : programs compiled from test directory located here

 The `makefile` is located in `CombineHarvester/mk`, with a symbolic link added to the root directory of each package. This defines a number of special targets that can be built by running: `make [target]`

  * `make dir` or just `make`: Only compile the code in the current directory, including the minimum set of dependencies in other packages if necessary.
  * `make tree`: Compile the code in the current directory, and recursively into all sub-directories starting from this one (as defined in each `Rules.mk` file)
  * `make all`: Compile every package recursively starting from the top directory
  * `make clean`: Removes every file in the `bin`, `obj` and `lib` directories in the current package
  * `make clean_tree`: Also cleans packages in sub-directories
  * `make clean_all`: Clean every package recursively starting from the top directory
  * `make bin/[program]` Shortcut target for each executable in the current directory. This provides a quick way to update a single program.

On machines with multiple processor cores add the `-j[n]` option to compile with *n* threads. By default the makefile will just print a summary of each operation to the screen. To print the full command for each step add the option `V=1`. The option `DEBUG=1` can also be added which will cause make to print a list of the targets it finds as it scans directories.

A first example {#ex-first}
===========================
Have a look at the file CombineTools/test/Example.cpp, this contains detailed comments on some of the basic datacard-creation features. The program `CombineTools/bin/Example` can be run without any options.

\warning You must first ensure the [auxiliaries](https://github.com/roger-wolf/HiggsAnalysis-HiggsToTauTau-auxiliaries) repository is located at `$CMSSW_BASE/src/auxiliaries` and up-to-date. The input root files will be sourced from here.

Example: SM Legacy Analysis {#ex-sm-legacy}
===========================================
The program `CombineTools/bin/SMLegacyExample` creates a set of datacards that mirror those used in HIG-13-004. It is intended as a more complex example of several steps in the datacard creation process:

  * Defining analysis categories, signal and background processes
  * Adding systematic uncertainties (see `CombineTools/src/HttSystematics_SMLegacy.cc`)
  * Extracting the corresponding histograms
  * Scaling signal rates to the SM cross sections
  * Applying bin-by-bin merging and creating uncertainties
  * Pruning the set of bin-by-bin nuisances
  * Writing the datacard `.txt` and `.root` files


Example: MSSM Yield Tables {#ex-mssm-table}
===========================================
The example script `CombineTools/scripts/yield_tables_mssm_example.sh` uses the program `CombineTools/test/MSSMYieldTable.cpp` to produce the tables included in HIG-13-021. To use it you must first copy this folder containing the input datacards:

    cd CombineTools
    cp -r /afs/cern.ch/work/a/agilbert/public/CombineTools/data/mssm-paper-cmb ./data/

