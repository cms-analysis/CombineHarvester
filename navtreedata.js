/*
 @licstart  The following is the entire license notice for the JavaScript code in this file.

 The MIT License (MIT)

 Copyright (C) 1997-2020 by Dimitri van Heesch

 Permission is hereby granted, free of charge, to any person obtaining a copy of this software
 and associated documentation files (the "Software"), to deal in the Software without restriction,
 including without limitation the rights to use, copy, modify, merge, publish, distribute,
 sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all copies or
 substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
 BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
 DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

 @licend  The above is the entire license notice for the JavaScript code in this file
*/
var NAVTREE =
[
  [ "CombineHarvester", "index.html", [
    [ "Introduction", "index.html", [
      [ "Getting started", "index.html#getting-started", null ],
      [ "High-level tools", "index.html#high-level-tools", null ],
      [ "Other comments", "index.html#note", null ]
    ] ],
    [ "Examples Part I", "intro1.html", [
      [ "Parsing a single card", "intro1.html#ex1-p1", null ],
      [ "Parsing multiple cards", "intro1.html#ex1-p2", null ],
      [ "Filtering", "intro1.html#ex1-p3", null ],
      [ "Yields, copying and sets", "intro1.html#ex1-p4", null ]
    ] ],
    [ "Examples Part II", "intro2.html", [
      [ "Defining categories and processes", "intro2.html#ex2-p1", null ],
      [ "Creating systematics", "intro2.html#ex2-p2", null ],
      [ "Extracting shape inputs", "intro2.html#ex2-p3", null ],
      [ "Adding bin-by-bin uncertainties", "intro2.html#ex2-p4", null ],
      [ "Writing datacards", "intro2.html#ex2-p5", null ]
    ] ],
    [ "Examples Part III", "intro3.html", null ],
    [ "Python Interface", "python-interface.html", [
      [ "Constructors and copying", "python-interface.html#py-constr-copy", null ],
      [ "Logging and Printing", "python-interface.html#py-log-print", null ],
      [ "Datacards", "python-interface.html#py-datacards", [
        [ "Parsing specifying metadata", "python-interface.html#py-datacards-meta", null ],
        [ "Parsing with pattern substitution", "python-interface.html#py-datacards-pat-sub", null ],
        [ "Writing", "python-interface.html#py-datacards-writing", null ]
      ] ],
      [ "Filtering", "python-interface.html#py-filtering", null ],
      [ "Set producers", "python-interface.html#py-sets", null ],
      [ "Modifications", "python-interface.html#py-modifications", null ],
      [ "Rate and shape evaluation", "python-interface.html#py-eval", null ],
      [ "Datacard creation", "python-interface.html#py-creation", null ],
      [ "Class: CardWriter", "python-interface.html#py-card-writer", null ],
      [ "Class: BinByBinFactory", "python-interface.html#py-bbbfactory", null ]
    ] ],
    [ "Post-fit Distributions", "post-fit-shapes-ws.html", null ],
    [ "Limits", "limits.html", [
      [ "Limits in models with one POI", "limits.html#limits-one-POI", [
        [ "Creating the datacards", "limits.html#limits-creating-the-datacards", null ],
        [ "Building the workspaces", "limits.html#limits-building-the-workspaces", null ],
        [ "Calculating limits", "limits.html#limits-calculating-limits", null ],
        [ "Collect the output", "limits.html#limits-collecting", null ],
        [ "Plotting", "limits.html#limits-plotting", null ],
        [ "Workflow with RooMorphingPdf datacards", "limits.html#limits-morphing-cards", null ]
      ] ],
      [ "Limit as a function of some other variable", "limits.html#autotoc_md0", null ],
      [ "Limits in models with more than one POI", "limits.html#limits-more-POIs", [
        [ "Expected limits: pre-fit vs post-fit", "limits.html#limits-pre-vs-post", null ],
        [ "Signal injected limits", "limits.html#autotoc_md1", null ]
      ] ]
    ] ],
    [ "RooMorphingPdf", "intro_morph.html", [
      [ "BuildRooMorphing function", "intro_morph.html#BuildRooMorph", null ],
      [ "Example usage for SM analysis", "intro_morph.html#SMMorph", null ],
      [ "Creating 1 or 3 Higgs bosons for an MSSM analysis", "intro_morph.html#MSSMMorph", null ],
      [ "Applying a model at text2workspace step", "intro_morph.html#MSSMModel", null ]
    ] ],
    [ "Reproducing Run 1 H->tautau results", "introrun1_h_t_t.html", [
      [ "Systematics for legacy H->tautau results", "introrun1_h_t_t.html#run1HTTsystematics", null ],
      [ "Legacy SM H->tautau results", "introrun1_h_t_t.html#run1HTTSM", null ],
      [ "Run 1 H->hh->bbtautau and A->Zh->lltautau results", "introrun1_h_t_t.html#run1HTTHhhAZh", null ],
      [ "MSSM update H->tautau results", "introrun1_h_t_t.html#run1HTTMSSM", null ]
    ] ],
    [ "Charged Higgs datacards with RooMorphingPdf", "md_docs__charged_higgs.html", [
      [ "Getting the cards", "md_docs__charged_higgs.html#autotoc_md2", null ],
      [ "Build a RooMorphingPdf version", "md_docs__charged_higgs.html#autotoc_md3", null ],
      [ "Reproduce limits in HIG-14-020", "md_docs__charged_higgs.html#autotoc_md4", null ]
    ] ],
    [ "BSM Model independent Limits using MorphingMSSMUpdate", "_m_s_s_m_update_no_model.html", [
      [ "Creating datacards", "_m_s_s_m_update_no_model.html#MSSMUpdate-p1", null ],
      [ "Scaling the workspace accordingly", "_m_s_s_m_update_no_model.html#MSSMUpdate-p2", null ],
      [ "Calculating values", "_m_s_s_m_update_no_model.html#MSSMUpdate-p3", null ],
      [ "Collecting the results in a single file", "_m_s_s_m_update_no_model.html#MSSMUpdate-p4", null ],
      [ "Plotting the limits", "_m_s_s_m_update_no_model.html#MSSMUpdate-p5", null ]
    ] ],
    [ "BSM Model independent Limits using MorphingHhh or MorphingAZh", "_model_indep_hhh_a_zh.html", [
      [ "Creating datacards", "_model_indep_hhh_a_zh.html#Hhh-Azh-p1", null ],
      [ "Creating the workspace", "_model_indep_hhh_a_zh.html#Hhh-Azh-p2", null ],
      [ "Calculating values", "_model_indep_hhh_a_zh.html#Hhh-Azh-p3", null ]
    ] ],
    [ "Model dependent Limits using MorphingMSSMUpdate", "_m_s_s_m_update_model_dep.html", [
      [ "Creating datacards", "_m_s_s_m_update_model_dep.html#p1", null ],
      [ "Scaling the workspace accordingly", "_m_s_s_m_update_model_dep.html#p2", null ],
      [ "Calculating values", "_m_s_s_m_update_model_dep.html#p3", null ],
      [ "Collecting the results in a single file", "_m_s_s_m_update_model_dep.html#p4", null ],
      [ "Plotting the limits", "_m_s_s_m_update_model_dep.html#p5", null ]
    ] ],
    [ "Calculating grids of CLs values using toys", "md_docs__hybrid_new_grid.html", null ],
    [ "Deprecated List", "deprecated.html", null ],
    [ "Namespaces", "namespaces.html", [
      [ "Namespace List", "namespaces.html", "namespaces_dup" ],
      [ "Namespace Members", "namespacemembers.html", [
        [ "All", "namespacemembers.html", null ],
        [ "Functions", "namespacemembers_func.html", null ],
        [ "Typedefs", "namespacemembers_type.html", null ]
      ] ]
    ] ],
    [ "Data Structures", "annotated.html", [
      [ "Data Structures", "annotated.html", "annotated_dup" ],
      [ "Class Hierarchy", "hierarchy.html", "hierarchy" ],
      [ "Data Fields", "functions.html", [
        [ "All", "functions.html", "functions_dup" ],
        [ "Functions", "functions_func.html", "functions_func" ],
        [ "Variables", "functions_vars.html", null ],
        [ "Typedefs", "functions_type.html", null ],
        [ "Related Functions", "functions_rela.html", null ]
      ] ]
    ] ],
    [ "Files", "files.html", [
      [ "File List", "files.html", "files_dup" ],
      [ "Globals", "globals.html", [
        [ "All", "globals.html", null ],
        [ "Functions", "globals_func.html", null ],
        [ "Macros", "globals_defs.html", null ]
      ] ]
    ] ]
  ] ]
];

var NAVTREEINDEX =
[
"_a_zh_systematics_8cc.html",
"_process_8cc.html#a8b80f6510601d33e773f90b1160d5463",
"classch_1_1_combine_harvester.html#aadea1e068eb474ba7919b1894033e3d3",
"functions_g.html",
"structch_1_1syst_1_1era.html#a3efbe3d6162bf81819ebc883e6c6ffda"
];

var SYNCONMSG = 'click to disable panel synchronisation';
var SYNCOFFMSG = 'click to enable panel synchronisation';