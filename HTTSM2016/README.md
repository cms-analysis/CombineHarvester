The input shape files for this analysis are stored in an external repository. On a machine with a kerberos token for CERN access (e.g. lxplus), the simplest, and password-free way to get the repository is:

    git clone https://:@gitlab.cern.ch:8443/cms-htt/SM-PAS-2016.git shapes

Otherwise normal https access requiring a username and password can be done with:

    git clone https://gitlab.cern.ch/cms-htt/SM-PAS-2016.git shapes

New files as well as updates should be pushed directly to the master branch. To avoid creating unnecessary merge commit, please always do git pull with the --rebase option:

    git pull --rebase
 
This will only fall back to a merge when rebasing your local changes is not possible.






PLOTTING:
You can find a plotting tool for SM-HTT here scripts/plotter.py.  There is a good deal of parameters such as the number of times a 2D distribution is unrolled and such which are stored in an external varCfg file: scripts/varCfgPlotter.py.  If the binning changes, it will be helpful to updated this file for aesthetics sake.  Other details such as default input files for each channel and which shapes are merged into a single plotted histo are also contained here.

Example usage:

    python scripts/plotter.py --channel em --isLog 0

This can handle prefit and postfit plotting by adjusting the --prefix default

    python scripts/plotter.py --channel em --isLog 0 --prefix prefit_

This will append to each category TDirectory it searches for prefit_, giving prefit_tt_VBF for example.  This does not handle postfit plots for the non-fitted variable currently.
