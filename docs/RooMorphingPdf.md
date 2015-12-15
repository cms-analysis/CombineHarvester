RooMorphingPdf {#introMorph}
=========================


BuildRooMorphing function {#BuildRooMorph}
=========================

**File**: CombinePdfs/src/MorphFunctions.cc

The PDF which is used for the signal is a custom RooFit PDF. Its application is
made via the datacard production code, with a call to a function named
BuildRooMorphing. Here we highlight some of the important features of this
function. For a greater level of detail we recommend the reader look at the code
itself, which is well commented.

The arguments to the function are as follows:

\snippet CombinePdfs/src/MorphFunctions.cc part1

The options to this function are as follows:

* A RooWorkspace to be passed to the function.
* The Combine Harvester instance, already setup with all the necessary channels,
categories and systematics as described in the previous sections.
* The process upon which the morphing is to be applied, each signal
process.
* A RooAbsReal which controls the signal mass.
* The "norm_prefix" is an optional additional prefix to add to the normalisation term
controlling the PDF.
* The "allow_morph" option controls whether the PDF is
designed such that for masses inbetween those for which signal templates are
available the signal yield and shape are taken via interpolation, or whether the
nearest template is simply taken.
* Simply controls the verbose output of the code
* The option "force_template_limit" is an optional setting to force the
normalisation of the PDF to go to zero outside of the range of available masses.
* An optional TFile to contain debug information.

The first step of the function is to work out the list of available masspoints
for the signal process, and sort and count them:

\snippet CombinePdfs/src/MorphFunctions.cc part2

Then it is necessary to track all the information on the systematics affecting
the signal process. This is done separately for the shape and normalisation
systematics. After some manipulation of this information (including special
treatment for the case where a shape systematic also alters the normalisation,
i.e. has a value different from 1.00), it is possible to build a RooArgList of
the parameters controlling the vertical template morphing which is internally
used by combine to apply the effect of the shape systematics to the signal.

\snippet CombinePdfs/src/MorphFunctions.cc part3

Note that the above code takes care over the possibility that the shape
systematics are not the same for all masspoints - this is not currently
supported in this function. The created "ss_list" is used later to create the
vertical template morphing PDFs.

For the normalisation systematics we must consider separately the two cases: 1)
in the first case the uncertainty is the same for each masspoint, so we can
leave this in the datacard in the usual way, but in case 2) where the
uncertainty is not the same for each masspoint, we have to include this
information in the signal PDF by creating a RooFit object that makes the
uncertainty a function off mass. Finally a list is built of all objects required
for the interpolation.

A 1D spline is built directly from the array of rates and masses:

\snippet CombinePdfs/src/MorphFunctions.cc part4

Here the option "force_template_limit" allows the user to use an alternative
rate array where the rate falls to 0 for masses only very slightly outside of
those in the mass array. Then a normalisation term is built which contains all
the terms which go into the normalisation - the original rate and the
normalisation systematics. The array of vertical morphing PDFs is also built
using the information from earlier. Finally, the RooMorphingPdf is built with
the following obtained information:

\snippet CombinePdfs/src/MorphFunctions.cc part5

with the arguments:
* xvar :       the fixed "CMS_th1x" x-axis variable with uniform integer binning
* mass_var:    the floating mass value for the interpolation
* vpdf_list:   the list of vertical-interpolation pdfs
* m_vec:       the corresponding list of mass points
* allow_morph: if false will just evaluate to the closest pdf in mass
* data_hist.GetXaxis(): The original (non-uniform) target binning
* proc_hist.GetXaxis(): The original (non-uniform) morphing binning

The final two arguments are needed to support the possibility that the signal
template being interpolated has a finer binning than the target binning for the
fit. in order to avoid known problems with the RMS of a peaking distribution
not being morphed smoothly from mass point to mass point if the binning is too
wide. A RooProduct is added for the normalisation of this PDF:

\snippet CombinePdfs/src/MorphFunctions.cc part6

The creation of this term is very important. When building the workspace, this
term will be searched for and tied to the PDF. It is possible at the workspace
building step to add additional terms to those normalisation term, for example a
scaling for cross-section times branching ratio. Example usage of this will be
discussed later.

The final step in the function is to tidy up the CH instance before it is
returned to the main code to write out the datacards. The signal yield in the
datacards is replaced with a single value of 1.0, such that the normalisation
will now be read from the normalisation object just created.

Example usage for SM analysis {#SMMorph}
=========================

The code to produce SM datacards is almost exactly the same as the example
described previously with the exception of a few additional lines to call the
BuildRooMorphing function. The call to BuildRooMorphing is as follows:

\snippet CombinePdfs/bin/SMLegacyMorphing.cpp part1

A single call is made for each signal process of each channel and category. The
produced workspace is then imported into the CH instance and the created PDFs
extracted. The workspace is stored in the shape file created for the limit
calculations alongside the text datacards.

For cases like the SM analysis, this method can be used simply to produce one
combined workspace for all masses, making the mass a continous parameter of the
workspace. The rest of the calculations of the statistical results on the
workspace are unchanged, except for the requirement to tell combine to fix the
mass rather than float it. The workspace is build using the command:

text2workspace.py -b combinedCard.txt -o combinedCard.root
 --default-morphing shape2

 Note that mass is not specified here, since we want to build a combined
 workspace for all possible masses. Then, to run the maximum likelihood fit for a
 given mass:

 combine -M MaxLikelihoodFit --freezeNuisances MH -m 125 combinedCard.root

 where in this case the mass must be specified.

Creating 1 or 3 Higgs bosons for an MSSM analysis {#MSSMMorph}
=========================

For an MSSM or 2HDM interpretation, datacards must be setup containing 3 neutral Higgs
bosons. The extension of the previous description to create datacards with
three Higgs bosons in and a signal PDF for each is simple:

\snippet Run1BSMComb/bin/MorphingMSSMUpdate.cpp part4

In this case the BuildRooMorphing function is passed the signal process
corresponding to each of the three Higgs bosons, each controlled by their
separate mass terms. Note the option "mass", which if set to "MH" will only
build the datacards with one Higgs boson - this is reserved for the case of
running the single resonance model independent limits and will instead place
only one Higgs boson in the datacards.

Applying a model at text2workspace step {#MSSMModel}
=========================

Having produced datacards containing signal PDFs for the appropriate number of
Higgs bosons, we can go one step further and make extra use of the normalisation
term associated with the PDFs. One specific use of this, as discussed in the
introduction, is in the model dependent exclusions provided for example in the
MSSM H->tautau analysis. In this case, each point in mA-tanb
phase space has a different signal model containing contributions from the three
Higgs bosons. At each point the masses of the Higgs bosons and the
cross-sections times branching ratios are different. The normal procedure in
this case would be to produce a workspace for each model point with a specific
signal template built and added by hand.

Now that we have RooMorphingPdfs we can do this in a more clever way, by
attaching terms controlling the normalisation of the signal to its normalisation
term. This can be done within the text2workspace.py step, where the .txt
datacard is converted into a RooWorkspace as input to combine. In this step, it
is possible to apply a physics model which performs some scaling and
manipulation to the different quantities in the datacards. By designing an
appropriate physics model, we can add terms to the normalisation to control the
cross section times branching ratio of the three Higgs bosons.
These can be added as a function of mA and tanb which can be
made parameters of the workspace as RooRealVars:

\snippet CombinePdfs/python/MSSM.py part1

The histograms containing the information on the different cross-sections and
branching ratios are included as TH2Ds inside a file for a particular model.
These are read in and turned into a RooHistFunc via a helper function called
doHistFunc:

\snippet CombinePdfs/python/MSSM.py part2

Note the option 'interpolate' which is off by default - this allows the
possibility of interpolating the model inputs to reach values beyond the
granularity that is provided.

RooHistFuncs are then built for the mass terms controlling the two Higgs bosons
which are not the A boson (since this is already controlled by the parameter
mA, as well as the cross-section and branching ratio, for example using
terms:

\snippet CombinePdfs/python/MSSM.py part3

In this code snippet, 'era' controls the centre of mass energy of the model,
currently either 7TeV, 8TeV or 13TeV. Note that theoretical uncertainties,
which are also provided from the model inputs as a function of mA and
tanb, are applied at this stage as well by building the relevant terms
and adding them to the workspace. Finally the relevant parameters are combined
to give a complete term used to control the normalisation of the signal.


