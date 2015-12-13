Charged Higgs datacards with RooMorphingPdf
===========================================

# Getting the cards

The cards from the CMS HCG svn need to be copied into the auxiliaries directory:

    cp -r /afs/cern.ch/work/a/agilbert/public/CombineTools/data/HIG-14-020.r6636 $CMSSW_BASE/src/auxiliaries/datacards/

We will only be using the "low-mass" cards (m_H+ < m_top), which are named like `combine_datacard_hplushadronic_m[MASS].txt`, where `[MASS]` ranges from 80 to 160 GeV.

# Build a RooMorphingPdf version

The program `AdaptChargedHiggs` will:

  * parse these cards with CombineHarvester
  * reduce the entries to one set of observations + backgrounds, as these are the same for all mass-points
  * rename the signal processes and signal-affecting shape systematics, as these have the mass value hard-coded and BuildRooMorphing won't realise that they are all the same process which should be combined into one. The signal sis also renamed to get them in the PROD_DECAY form we will use for the model building later
  * Create the RooMorphingPdfs and write out a new single datacard: `output/mssm_nomodel/hplus_tauhad_mssm.txt`

# Reproduce limits in HIG-14-020

To reproduce the model-independent limits from the charged Higgs PAS we will need to use the same physics model that scales the `tt->H+H-bb` and `tt->H+W-bb` processes by the appropriate function of the `t->H+b` branching ratio POI `BR`. This has been adapted from the original version in the combine repository to account for our change of signal process naming:

    text2workspace.py hplus_tauhad_mssm.txt -o hplus_tauhad_mssm.root -P CombineHarvester.CombinePdfs.MSSM:brChargedHiggs

Then we can run the asymptotic limits:

    combineTool.py -M Asymptotic -d hplus_tauhad_mssm.root -m 80:160:10  --freezeNuisances MH --setPhysicsModelParameterRanges BR=0,0.2 --cminDefaultMinimizerType Minuit2 --rAbsAcc 0.00001 -n .ChargedHiggs

A few non-default combine options are used:

|                    Option                   |                                                                                         Reason                                                                                         |
|---------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `--setPhysicsModelParameterRanges BR=0,0.2` | Don't want the range to be too large compared to the typical uncertainty on the limit (can reduce Minuit precision)                                                                    |
| `--cminDefaultMinimizerType Minuit2`        | When doing the fit to get the global observables for the asimov dataset combine uses Minuit not Minuit2 by default - better to always use Minuit2                                      |
| `--rAbsAcc 0.00001`                         | The default absolute uncertainty on the POI value when searching for the limit is too large compared to the small values of `BR` we are probing here - we would get inaccurate limits. |

The output limits are found to be in excellent agreement with the published numbers (dash indicates only available via morphing):

| Mass (GeV) | Median exp. (HIG-14-020) | Median exp. (CH) | Obs. (HIG-14-020) | Obs. (CH) |
|------------|--------------------------|------------------|-------------------|-----------|
|         80 | 0.0111                   |           0.0111 | 0.0121            |    0.0121 |
|         90 | 0.0080                   |           0.0079 | 0.0094            |    0.0095 |
|        100 | 0.0061                   |           0.0061 | 0.0063            |    0.0063 |
|        110 | -                        |           0.0046 | -                 |    0.0043 |
|        120 | 0.0034                   |           0.0034 | 0.0029            |    0.0029 |
|        130 | -                        |           0.0028 | -                 |    0.0023 |
|        140 | 0.0023                   |           0.0023 | 0.0018            |    0.0018 |
|        150 | 0.0021                   |           0.0021 | 0.0015            |    0.0015 |
|        160 | 0.0022                   |           0.0022 | 0.0016            |    0.0016 |
