Post-fit Distributions {#post-fit-shapes-ws}
=========================================

**File**: CombineTools/test/PostFitShapesFromWorkspace.cpp

The program `PostFitShapesFromWorkspace` is used to dump a set of pre- and post-fit distributions from a datacard. There is no need to specify which categories or processes to extract, this will be done automatically and so should work for any shape-based analysis. The effect of all normalisation and shape uncertainties is evaluated. In addition, there is an option to calculate post-fit/pre-fit scale factors for each background and the total background uncertainty in each category. This numbers can then be used as input for producing post-fit control distributions.


The following options are available:

    Configuration:
      -w [ --workspace ] arg           The input workspace-containing file [REQUIRED]
      --dataset arg (=data_obs)        The input dataset name
      -d [ --datacard ] arg            The input datacard, only used for rebinning
      -o [ --output ] arg              Name of the output root file to create [REQUIRED]
      -f [ --fitresult ] arg           Path to a RooFitResult, only needed for postfit
      -m [ --mass ] arg                Signal mass point of the input datacard
      --postfit [=arg(=1)] (=0)        Create post-fit histograms in addition to pre-fit
      --sampling [=arg(=1)] (=0)       Use the cov. matrix sampling method for the post-fit
                                       uncertainty
      --samples arg (=500)             Number of samples to make in each evaluate call
      --print [=arg(=1)] (=0)          Print tables of background shifts and relative
                                       uncertainties
      --freeze arg                     Format PARAM1,PARAM2=X,PARAM3=Y where the values X and Y
                                       are optional
      --covariance [=arg(=1)] (=0)     Save the covariance and correlation matrices of the
                                       process yields
      --skip-prefit [=arg(=1)] (=0)    Skip the pre-fit evaluation
      --skip-proc-errs [=arg(=1)] (=0) Skip evaluation of errors on individual processes
      --total-shapes [=arg(=1)] (=0)   Save signal- and background shapes added for all
                                       channels/categories
      --reverse-bins arg               List of bins to reverse the order for
    
    Example usage:
    PostFitShapesFromWorkspace -d htt_mt_125.txt -w htt_mt_125.root -o htt_mt_125_shapes.root \
        -m 125 -f mlfit.root:fit_s --postfit --sampling --print


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


\note This program only produces the histograms - you will need to provide your own plotting script!



