Post-fit Distributions {#post-fit-shapes}
=========================================

**File**: CombineTools/test/PostFitShapes.cpp

The program `PostFitShapes` is used to dump a set of pre- and post-fit distributions from a datacard. There is no need to specify which categories or processes to extract, this will be done automatically and so should work for any shape-based analysis. The effect of all normalisation and shape uncertainties is evaluated. In addition, there is an option to calculate post-fit/pre-fit scale factors for each background and the total background uncertainty in each category. This numbers can then be used as input for producing post-fit control distributions.

\warning Take care if the datacard contains `rateParam` terms. These are currently not considered when evaluating process rates and shapes. See the alternative program `PostFitShapesFromWorkspace`, which implicitly evaluates all normalisation terms in the workspace, including those originally created by `rateParam` directives.

The following options are available:

    Configuration:
    -d [ --datacard ] arg      The datacard .txt file [REQUIRED]
    -o [ --output ] arg        Name of the output root file to create [REQUIRED]
    -f [ --fitresult ] arg     Path to a RooFitResult, only needed for postfit
    -m [ --mass ] arg          Signal mass point of the input datacard
    --postfit [=arg(=1)] (=0)  Create post-fit histograms in addition to pre-fit
    --sampling [=arg(=1)] (=0) Use the cov. matrix sampling method for the
                               post-fit uncertainty
    --samples arg (=0)         Number of samples to make in each evaluate call
    --print [=arg(=1)] (=0)    Print tables of background shifts and relative
                               uncertainties
    Example usage:
    PostFitShapes -d htt_mt_125.txt -o htt_mt_125_shapes.root -m 125 \
        -f mlfit.root:fit_s --postfit --sampling --print

\warning The option `--sampling` is not used by default, but you should probably use it if you are producing post-fit distributions. Without this the uncertainty will be calculated assuming no correlations between nuisance parameters - this would be extremely rare in an typical fit.

The output root file will have the following directory structure:

    output.root:
        bin_1_prefit/
            TH1F data_obs
            TH1F process_1
            TH1F process_2
            ...
            TH1F process_i
            TH1F TotalBkg
            TH1F TotalSig
        bin_1_postfit/
            TH1F data_obs
            TH1F process_1
            TH1F process_2
            ...
            TH1F process_i
            TH1F TotalBkg
            TH1F TotalSig
        ...
        bin_i_prefit/
            ...
        bin_i_postfit/
            ...

\warning In the post-fit output the signal histograms are not scaled to the fitted signal strength, rather a signal strength r=1 is assumed. It follows that the uncertainty on the signal processes does not include the uncertainty on this signal strength parameter.

\note This program only produces the histograms - you will need to provide your own plotting script!



