The input shape files for this analysis are stored in an external repository. On a machine with a kerberos token for CERN access (e.g. lxplus), the simplest, and password-free way to get the repository is:

    git clone https://:@gitlab.cern.ch:8443/cms-htt/HIG-15-007.git shapes

Otherwise normal https access requiring a username and password can be done with:

    git clone https://gitlab.cern.ch/cms-htt/HIG-15-007.git shapes

New files as well as updates should be pushed directly to the master branch. To avoid creating unnecessary merge commit, please always do git pull with the --rebase option: 

    git pull --rebase
 
This will only fall back to a merge when rebasing your local changes is not possible.
