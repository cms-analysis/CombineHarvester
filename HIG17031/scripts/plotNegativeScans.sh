#!/bin/bash


#K1_mm
INPUT="Mar26/results"; OUTPUT="Mar26/plots/kappas_neg"; M=K1_mm; mkdir -p ${OUTPUT}/${M}; for W in observed postfit_asimov; do COL=1; case ${W} in prefit_asimov) COL=4; EXTRA='--main-label "SM Expected" --main-color 4';; postfit_asimov) COL=2; EXTRA='--main-label "SM Expected" --main-color 2';; *) EXTRA="";; esac; for P in $(./getPOIs_hmm.py ${M} -P); do eval python scripts/plot1DScan.py -o scan_neg_${W}_${M}_${P} --POI ${P} --model ${M} --others \
\"${INPUT}/scan.neg.${M}_N1.${W}.nominal.${P}.root:#kappa_{W}\>0, \#kappa_{Z}\>0, \#kappa_{b}\>0:4\" \
\"${INPUT}/scan.neg.${M}_N2.${W}.nominal.${P}.root:#kappa_{W}\<0, \#kappa_{Z}\>0, \#kappa_{b}\>0:30\" \
\"${INPUT}/scan.neg.${M}_N3.${W}.nominal.${P}.root:#kappa_{W}\>0, \#kappa_{Z}\<0, \#kappa_{b}\>0:46\" \
\"${INPUT}/scan.neg.${M}_N4.${W}.nominal.${P}.root:#kappa_{W}\<0, \#kappa_{Z}\<0, \#kappa_{b}\>0:40\" \
\"${INPUT}/scan.neg.${M}_N5.${W}.nominal.${P}.root:#kappa_{W}\>0, \#kappa_{Z}\>0, \#kappa_{b}\<0:2\" \
\"${INPUT}/scan.neg.${M}_N6.${W}.nominal.${P}.root:#kappa_{W}\<0, \#kappa_{Z}\>0, \#kappa_{b}\<0:8\" \
\"${INPUT}/scan.neg.${M}_N7.${W}.nominal.${P}.root:#kappa_{W}\>0, \#kappa_{Z}\<0, \#kappa_{b}\<0:24\" \
\"${INPUT}/scan.neg.${M}_N8.${W}.nominal.${P}.root:#kappa_{W}\<0, \#kappa_{Z}\<0, \#kappa_{b}\<0:6\" \
\"${INPUT}/scan.${M}_N1.${W}.fr.all.${P}.root:#kappa_{W}\>0, \#kappa_{Z}\>0, \#kappa_{b}\>0:4\" \
\"${INPUT}/scan.${M}_N2.${W}.fr.all.${P}.root:#kappa_{W}\<0, \#kappa_{Z}\>0, \#kappa_{b}\>0:30\" \
\"${INPUT}/scan.${M}_N3.${W}.fr.all.${P}.root:#kappa_{W}\>0, \#kappa_{Z}\<0, \#kappa_{b}\>0:46\" \
\"${INPUT}/scan.${M}_N4.${W}.fr.all.${P}.root:#kappa_{W}\<0, \#kappa_{Z}\<0, \#kappa_{b}\>0:40\" \
\"${INPUT}/scan.${M}_N5.${W}.fr.all.${P}.root:#kappa_{W}\>0, \#kappa_{Z}\>0, \#kappa_{b}\<0:2\" \
\"${INPUT}/scan.${M}_N6.${W}.fr.all.${P}.root:#kappa_{W}\<0, \#kappa_{Z}\>0, \#kappa_{b}\<0:8\" \
\"${INPUT}/scan.${M}_N7.${W}.fr.all.${P}.root:#kappa_{W}\>0, \#kappa_{Z}\<0, \#kappa_{b}\<0:24\" \
\"${INPUT}/scan.${M}_N8.${W}.fr.all.${P}.root:#kappa_{W}\<0, \#kappa_{Z}\<0, \#kappa_{b}\<0:6\" \
-m ${INPUT}/scan.neg.${M}_N1.${W}.nominal.${P}.root --remove-near-min 0.8 --y-max 70 ${EXTRA} --envelope --chop 150  --no-input-label --translate pois.json --json ${OUTPUT}/neg_${W}.json  --hide-envelope --breakdown "Syst,Stat" --meta "Types:${W},POIs:${P}" --outdir ${OUTPUT}/${M}; done; done


# Version excluding:
INPUT="Mar26/results"; OUTPUT="Mar26/plots/kappas_neg_no_Wt"; M=K1_mm; mkdir -p ${OUTPUT}/${M}; for W in observed postfit_asimov; do COL=1; case ${W} in prefit_asimov) COL=4; EXTRA='--main-label "SM Expected" --main-color 4';; postfit_asimov) COL=2; EXTRA='--main-label "SM Expected" --main-color 2';; *) EXTRA="";; esac; for P in $(./getPOIs_hmm.py ${M} -P); do eval python scripts/plot1DScan.py -o scan_neg_${W}_${M}_${P} --POI ${P} --model ${M} --others \
\"${INPUT}/scan.neg.${M}_N1.${W}.nominal.${P}.root:#kappa_{W}\>0, \#kappa_{Z}\>0, \#kappa_{b}\>0:4\" \
\"${INPUT}/scan.neg.${M}_N3.${W}.nominal.${P}.root:#kappa_{W}\>0, \#kappa_{Z}\<0, \#kappa_{b}\>0:46\" \
\"${INPUT}/scan.neg.${M}_N5.${W}.nominal.${P}.root:#kappa_{W}\>0, \#kappa_{Z}\>0, \#kappa_{b}\<0:2\" \
\"${INPUT}/scan.neg.${M}_N7.${W}.nominal.${P}.root:#kappa_{W}\>0, \#kappa_{Z}\<0, \#kappa_{b}\<0:24\" \
\"${INPUT}/scan.${M}_N1.${W}.fr.all.${P}.root:#kappa_{W}\>0, \#kappa_{Z}\>0, \#kappa_{b}\>0:4\" \
\"${INPUT}/scan.${M}_N3.${W}.fr.all.${P}.root:#kappa_{W}\>0, \#kappa_{Z}\<0, \#kappa_{b}\>0:46\" \
\"${INPUT}/scan.${M}_N5.${W}.fr.all.${P}.root:#kappa_{W}\>0, \#kappa_{Z}\>0, \#kappa_{b}\<0:2\" \
\"${INPUT}/scan.${M}_N7.${W}.fr.all.${P}.root:#kappa_{W}\>0, \#kappa_{Z}\<0, \#kappa_{b}\<0:24\" \
-m ${INPUT}/scan.neg.${M}_N1.${W}.nominal.${P}.root --remove-near-min 0.8 --y-max 70 ${EXTRA} --envelope --chop 100  --no-input-label --translate pois.json --json ${OUTPUT}/neg_${W}.json  --hide-envelope --breakdown "Syst,Stat" --meta "Types:${W},POIs:${P}" --outdir ${OUTPUT}/${M}; done; done

#######################################
# Plotting envelope for L1
INPUT="Mar26/results"; OUTPUT="Mar26/plots/kappas_neg"; M=L1; mkdir -p ${OUTPUT}/${M}; for W in observed postfit_asimov; do COL=1; case ${W} in prefit_asimov) COL=4; EXTRA='--main-label "SM Expected" --main-color 4';; postfit_asimov) COL=2; EXTRA='--main-label "SM Expected" --main-color 2';; *) EXTRA="";; esac; for P in $(./getPOIs_hmm.py ${M} -P); do eval python scripts/plot1DScan.py -o scan_neg_${W}_${M}_${P} --POI ${P} --model ${M} --others \
\"${INPUT}/scan.neg.${M}_N1.${W}.nominal.${P}.root:#lambda_{WZ}\>0, \#\lambda_{tg}\>0:4\" \
\"${INPUT}/scan.neg.${M}_N2.${W}.nominal.${P}.root:#lambda_{WZ}\<0, \#\lambda_{tg}\>0:30\" \
\"${INPUT}/scan.neg.${M}_N3.${W}.nominal.${P}.root:#lambda_{WZ}\>0, \#\lambda_{tg}\<0:46\" \
\"${INPUT}/scan.neg.${M}_N4.${W}.nominal.${P}.root:#lambda_{WZ}\<0, \#\lambda_{tg}\<0:40\" \
\"${INPUT}/scan.${M}_N1.${W}.fr.all.${P}.root:#lambda_{WZ}\>0, \#\lambda_{tg}\>0:4\" \
\"${INPUT}/scan.${M}_N2.${W}.fr.all.${P}.root:#lambda_{WZ}\<0, \#\lambda_{tg}\>0:30\" \
\"${INPUT}/scan.${M}_N3.${W}.fr.all.${P}.root:#lambda_{WZ}\>0, \#\lambda_{tg}\<0:46\" \
\"${INPUT}/scan.${M}_N4.${W}.fr.all.${P}.root:#lambda_{WZ}\<0, \#\lambda_{tg}\<0:40\" \
-m ${INPUT}/scan.neg.${M}_N1.${W}.nominal.${P}.root --remove-near-min 0.8 --y-max 20 ${EXTRA} --envelope --chop 25  --no-input-label --translate pois.json --json ${OUTPUT}/neg_${W}.json --hide-envelope --breakdown "Syst,Stat" --meta "Types:${W},POIs:${P}" --outdir ${OUTPUT}/${M}; done; done

# Version excluding:
INPUT="Mar26/results"; OUTPUT="Mar26/plots/kappas_neg_no_Wt"; M=L1; mkdir -p ${OUTPUT}/${M}; for W in observed postfit_asimov; do COL=1; case ${W} in prefit_asimov) COL=4; EXTRA='--main-label "SM Expected" --main-color 4';; postfit_asimov) COL=2; EXTRA='--main-label "SM Expected" --main-color 2';; *) EXTRA="";; esac; for P in $(./getPOIs_hmm.py ${M} -P); do eval python scripts/plot1DScan.py -o scan_neg_${W}_${M}_${P} --POI ${P} --model ${M} --others \
\"${INPUT}/scan.neg.${M}_N1.${W}.nominal.${P}.root:#lambda_{WZ}\>0, \#\lambda_{tg}\>0:4\" \
\"${INPUT}/scan.neg.${M}_N4.${W}.nominal.${P}.root:#lambda_{WZ}\<0, \#\lambda_{tg}\<0:40\" \
\"${INPUT}/scan.${M}_N1.${W}.fr.all.${P}.root:#lambda_{WZ}\>0, \#\lambda_{tg}\>0:4\" \
\"${INPUT}/scan.${M}_N4.${W}.fr.all.${P}.root:#lambda_{WZ}\<0, \#\lambda_{tg}\<0:40\" \
-m ${INPUT}/scan.neg.${M}_N1.${W}.nominal.${P}.root --remove-near-min 0.8 --y-max 20 ${EXTRA} --envelope --chop 25  --no-input-label --translate pois.json --json ${OUTPUT}/neg_${W}.json --hide-envelope --breakdown "Syst,Stat" --meta "Types:${W},POIs:${P}" --outdir ${OUTPUT}/${M}; done; done

#######################################
# Plotting envelope for K2
INPUT="Mar26/results"; OUTPUT="Mar26/plots/kappas_neg"; for M in K2 K2Width; do mkdir -p ${OUTPUT}/${M}; for W in observed postfit_asimov; do COL=1; case ${W} in prefit_asimov) COL=4; EXTRA='--main-label "SM Expected" --main-color 4';; postfit_asimov) COL=2; EXTRA='--main-label "SM Expected" --main-color 2';; *) EXTRA="";; esac; for P in $(./getPOIs_hmm.py ${M} -P); do eval python scripts/plot1DScan.py -o scan_neg_${W}_${M}_${P} --POI ${P} --model ${M} --others \
\"${INPUT}/scan.neg.${M}_N1.${W}.nominal.${P}.root:#kappa_{W}\>0, \#kappa_{Z}\>0:4\" \
\"${INPUT}/scan.neg.${M}_N2.${W}.nominal.${P}.root:#kappa_{W}\<0, \#kappa_{Z}\>0:30\" \
\"${INPUT}/scan.neg.${M}_N3.${W}.nominal.${P}.root:#kappa_{W}\>0, \#kappa_{Z}\<0:46\" \
\"${INPUT}/scan.neg.${M}_N4.${W}.nominal.${P}.root:#kappa_{W}\<0, \#kappa_{Z}\<0:40\" \
\"${INPUT}/scan.${M}_N1.${W}.fr.all.${P}.root:#kappa_{W}\>0, \#kappa_{Z}\>0:4\" \
\"${INPUT}/scan.${M}_N2.${W}.fr.all.${P}.root:#kappa_{W}\<0, \#kappa_{Z}\>0:30\" \
\"${INPUT}/scan.${M}_N3.${W}.fr.all.${P}.root:#kappa_{W}\>0, \#kappa_{Z}\<0:46\" \
\"${INPUT}/scan.${M}_N4.${W}.fr.all.${P}.root:#kappa_{W}\<0, \#kappa_{Z}\<0:40\" \
-m ${INPUT}/scan.neg.${M}_N1.${W}.nominal.${P}.root --remove-near-min 0.8 --y-max 20 ${EXTRA} --envelope --chop 25  --no-input-label --translate pois.json --json ${OUTPUT}/neg_${W}.json --hide-envelope --breakdown "Syst,Stat" --meta "Types:${W},POIs:${P}" --outdir ${OUTPUT}/${M}; done; done; done

# Version excluding
INPUT="Mar26/results"; OUTPUT="Mar26/plots/kappas_neg_no_Wt"; for M in K2 K2Width; do mkdir -p ${OUTPUT}/${M}; for W in observed postfit_asimov; do COL=1; case ${W} in prefit_asimov) COL=4; EXTRA='--main-label "SM Expected" --main-color 4';; postfit_asimov) COL=2; EXTRA='--main-label "SM Expected" --main-color 2';; *) EXTRA="";; esac; for P in $(./getPOIs_hmm.py ${M} -P); do eval python scripts/plot1DScan.py -o scan_neg_${W}_${M}_${P} --POI ${P} --model ${M} --others \
\"${INPUT}/scan.neg.${M}_N1.${W}.nominal.${P}.root:#kappa_{W}\>0, \#kappa_{Z}\>0:4\" \
\"${INPUT}/scan.neg.${M}_N3.${W}.nominal.${P}.root:#kappa_{W}\>0, \#kappa_{Z}\<0:46\" \
\"${INPUT}/scan.${M}_N1.${W}.fr.all.${P}.root:#kappa_{W}\>0, \#kappa_{Z}\>0:4\" \
\"${INPUT}/scan.${M}_N3.${W}.fr.all.${P}.root:#kappa_{W}\>0, \#kappa_{Z}\<0:46\" \
-m ${INPUT}/scan.neg.${M}_N1.${W}.nominal.${P}.root --remove-near-min 0.8 --y-max 20 ${EXTRA} --envelope --chop 25  --no-input-label --translate pois.json --json ${OUTPUT}/neg_${W}.json --hide-envelope --breakdown "Syst,Stat" --meta "Types:${W},POIs:${P}" --outdir ${OUTPUT}/${M}; done; done; done


#######################################
# Plotting envelope for K2Inv,K2Undet
INPUT="Mar26/results"; OUTPUT="Mar26/plots/kappas_neg"; for M in K2Inv K2Undet K2InvWidth K2UndetWidth; do mkdir -p ${OUTPUT}/${M}; for W in observed postfit_asimov; do COL=1; case ${W} in prefit_asimov) COL=4; EXTRA='--main-label "SM Expected" --main-color 4';; postfit_asimov) COL=2; EXTRA='--main-label "SM Expected" --main-color 2';; *) EXTRA="";; esac; for P in $(./getPOIs_hmm.py ${M} -P); do eval python scripts/plot1DScan.py -o scan_neg_${W}_${M}_${P} --POI ${P} --model ${M} --others \
\"${INPUT}/scan.neg.${M}_N1.${W}.nominal.${P}.root:#kappa_{W}\>0, \#kappa_{Z}\>0:4\"  \
\"${INPUT}/scan.neg.${M}_N4.${W}.nominal.${P}.root:#kappa_{W}\<0, \#kappa_{Z}\<0:40\" \
\"${INPUT}/scan.${M}_N1.${W}.fr.all.${P}.root:#kappa_{W}\>0, \#kappa_{Z}\>0:4\"  \
\"${INPUT}/scan.${M}_N4.${W}.fr.all.${P}.root:#kappa_{W}\<0, \#kappa_{Z}\<0:40\" \
-m ${INPUT}/scan.neg.${M}_N1.${W}.nominal.${P}.root --remove-near-min 0.8 --y-max 20 ${EXTRA} --envelope --chop 25  --no-input-label --translate pois.json --json ${OUTPUT}/neg_${W}.json --hide-envelope  --breakdown "Syst,Stat" --meta "Types:${W},POIs:${P}" --outdir ${OUTPUT}/${M}; done; done; done

# Version excluding
INPUT="Mar26/results"; OUTPUT="Mar26/plots/kappas_neg_no_Wt"; for M in K2Inv K2Undet K2InvWidth K2UndetWidth; do mkdir -p ${OUTPUT}/${M}; for W in observed postfit_asimov; do COL=1; case ${W} in prefit_asimov) COL=4; EXTRA='--main-label "SM Expected" --main-color 4';; postfit_asimov) COL=2; EXTRA='--main-label "SM Expected" --main-color 2';; *) EXTRA="";; esac; for P in $(./getPOIs_hmm.py ${M} -P); do eval python scripts/plot1DScan.py -o scan_neg_${W}_${M}_${P} --POI ${P} --model ${M} --others \
\"${INPUT}/scan.neg.${M}_N1.${W}.nominal.${P}.root:#kappa_{W}\>0, \#kappa_{Z}\>0:4\"  \
\"${INPUT}/scan.${M}_N1.${W}.fr.all.${P}.root:#kappa_{W}\>0, \#kappa_{Z}\>0:4\"  \
-m ${INPUT}/scan.neg.${M}_N1.${W}.nominal.${P}.root --remove-near-min 0.8 --y-max 20 ${EXTRA} --envelope --chop 25  --no-input-label --translate pois.json --json ${OUTPUT}/neg_${W}.json --hide-envelope  --breakdown "Syst,Stat" --meta "Types:${W},POIs:${P}" --outdir ${OUTPUT}/${M}; done; done; done

#######################################
# Plotting envelope for L2_ldu
INPUT="Mar26/results"; OUTPUT="Mar26/plots/kappas_neg"; for M in L2_ldu; do mkdir -p ${OUTPUT}/${M}; for W in observed postfit_asimov; do COL=1; case ${W} in prefit_asimov) COL=4; EXTRA='--main-label "SM Expected" --main-color 4';; postfit_asimov) COL=2; EXTRA='--main-label "SM Expected" --main-color 2';; *) EXTRA="";; esac; for P in $(./getPOIs_hmm.py ${M} -P); do eval python scripts/plot1DScan.py -o scan_neg_${W}_${M}_${P} --POI ${P} --model ${M} --others \
\"${INPUT}/scan.neg.${M}_N1.${W}.nominal.${P}.root:#lambda_{du}\>0, \#\lambda_{Vu}\>0:4\" \
\"${INPUT}/scan.neg.${M}_N2.${W}.nominal.${P}.root:#lambda_{du}\<0, \#\lambda_{Vu}\>0:30\" \
\"${INPUT}/scan.neg.${M}_N3.${W}.nominal.${P}.root:#lambda_{du}\>0, \#\lambda_{Vu}\<0:46\" \
\"${INPUT}/scan.neg.${M}_N4.${W}.nominal.${P}.root:#lambda_{du}\<0, \#\lambda_{Vu}\<0:40\" \
\"${INPUT}/scan.${M}_N1.${W}.fr.all.${P}.root:#lambda_{du}\>0, \#\lambda_{Vu}\>0:4\" \
\"${INPUT}/scan.${M}_N2.${W}.fr.all.${P}.root:#lambda_{du}\<0, \#\lambda_{Vu}\>0:30\" \
\"${INPUT}/scan.${M}_N3.${W}.fr.all.${P}.root:#lambda_{du}\>0, \#\lambda_{Vu}\<0:46\" \
\"${INPUT}/scan.${M}_N4.${W}.fr.all.${P}.root:#lambda_{du}\<0, \#\lambda_{Vu}\<0:40\" \
-m ${INPUT}/scan.neg.${M}_N1.${W}.nominal.${P}.root --remove-near-min 0.8 --y-max 70 ${EXTRA} --envelope --chop 100  --no-input-label --translate pois.json --json ${OUTPUT}/neg_${W}.json --hide-envelope  --breakdown "Syst,Stat" --meta "Types:${W},POIs:${P}" --outdir ${OUTPUT}/${M}; done; done; done

# Version excluding
INPUT="Mar26/results"; OUTPUT="Mar26/plots/kappas_neg_no_Wt"; for M in L2_ldu; do mkdir -p ${OUTPUT}/${M}; for W in observed postfit_asimov; do COL=1; case ${W} in prefit_asimov) COL=4; EXTRA='--main-label "SM Expected" --main-color 4';; postfit_asimov) COL=2; EXTRA='--main-label "SM Expected" --main-color 2';; *) EXTRA="";; esac; for P in $(./getPOIs_hmm.py ${M} -P); do eval python scripts/plot1DScan.py -o scan_neg_${W}_${M}_${P} --POI ${P} --model ${M} --others \
\"${INPUT}/scan.neg.${M}_N1.${W}.nominal.${P}.root:#lambda_{du}\>0, \#\lambda_{Vu}\>0:4\" \
\"${INPUT}/scan.neg.${M}_N2.${W}.nominal.${P}.root:#lambda_{du}\<0, \#\lambda_{Vu}\>0:30\" \
\"${INPUT}/scan.${M}_N1.${W}.fr.all.${P}.root:#lambda_{du}\>0, \#\lambda_{Vu}\>0:4\" \
\"${INPUT}/scan.${M}_N2.${W}.fr.all.${P}.root:#lambda_{du}\<0, \#\lambda_{Vu}\>0:30\" \
-m ${INPUT}/scan.neg.${M}_N1.${W}.nominal.${P}.root --remove-near-min 0.8 --y-max 70 ${EXTRA} --envelope --chop 100  --no-input-label --translate pois.json --json ${OUTPUT}/neg_${W}.json --hide-envelope  --breakdown "Syst,Stat" --meta "Types:${W},POIs:${P}" --outdir ${OUTPUT}/${M}; done; done; done

#######################################
# Plotting envelope for L2flipped_ldu
INPUT="Mar26/results"; OUTPUT="Mar26/plots/kappas_neg"; for M in L2flipped_ldu; do mkdir -p ${OUTPUT}/${M}; for W in observed postfit_asimov; do COL=1; case ${W} in prefit_asimov) COL=4; EXTRA='--main-label "SM Expected" --main-color 4';; postfit_asimov) COL=2; EXTRA='--main-label "SM Expected" --main-color 2';; *) EXTRA="";; esac; for P in $(./getPOIs_hmm.py ${M} -P); do eval python scripts/plot1DScan.py -o scan_neg_${W}_${M}_${P} --POI ${P} --model ${M} --others \
\"${INPUT}/scan.neg.${M}_N1.${W}.nominal.${P}.root:#lambda_{du}\>0, \#\lambda_{Vu}\>0:4\" \
\"${INPUT}/scan.neg.${M}_N2.${W}.nominal.${P}.root:#lambda_{du}\<0, \#\lambda_{Vu}\>0:30\" \
\"${INPUT}/scan.neg.${M}_N3.${W}.nominal.${P}.root:#lambda_{du}\>0, \#\lambda_{Vu}\<0:46\" \
\"${INPUT}/scan.neg.${M}_N4.${W}.nominal.${P}.root:#lambda_{du}\<0, \#\lambda_{Vu}\<0:40\" \
\"${INPUT}/scan.${M}_N1.${W}.fr.all.${P}.root:#lambda_{du}\>0, \#\lambda_{Vu}\>0:4\" \
\"${INPUT}/scan.${M}_N2.${W}.fr.all.${P}.root:#lambda_{du}\<0, \#\lambda_{Vu}\>0:30\" \
\"${INPUT}/scan.${M}_N3.${W}.fr.all.${P}.root:#lambda_{du}\>0, \#\lambda_{Vu}\<0:46\" \
\"${INPUT}/scan.${M}_N4.${W}.fr.all.${P}.root:#lambda_{du}\<0, \#\lambda_{Vu}\<0:40\" \
-m ${INPUT}/scan.neg.${M}_N1.${W}.nominal.${P}.root --remove-near-min 0.8 --y-max 70 ${EXTRA} --envelope --chop 100  --no-input-label --translate pois.json --json ${OUTPUT}/neg_${W}.json --hide-envelope  --breakdown "Syst,Stat" --meta "Types:${W},POIs:${P}" --outdir ${OUTPUT}/${M}; done; done; done

# Version excluding
INPUT="Mar26/results"; OUTPUT="Mar26/plots/kappas_neg_no_Wt"; for M in L2flipped_ldu; do mkdir -p ${OUTPUT}/${M}; for W in observed postfit_asimov; do COL=1; case ${W} in prefit_asimov) COL=4; EXTRA='--main-label "SM Expected" --main-color 4';; postfit_asimov) COL=2; EXTRA='--main-label "SM Expected" --main-color 2';; *) EXTRA="";; esac; for P in $(./getPOIs_hmm.py ${M} -P); do eval python scripts/plot1DScan.py -o scan_neg_${W}_${M}_${P} --POI ${P} --model ${M} --others \
\"${INPUT}/scan.neg.${M}_N1.${W}.nominal.${P}.root:#lambda_{du}\>0, \#\lambda_{Vu}\>0:4\" \
\"${INPUT}/scan.neg.${M}_N4.${W}.nominal.${P}.root:#lambda_{du}\<0, \#\lambda_{Vu}\<0:40\" \
\"${INPUT}/scan.${M}_N1.${W}.fr.all.${P}.root:#lambda_{du}\>0, \#\lambda_{Vu}\>0:4\" \
\"${INPUT}/scan.${M}_N4.${W}.fr.all.${P}.root:#lambda_{du}\<0, \#\lambda_{Vu}\<0:40\" \
-m ${INPUT}/scan.neg.${M}_N1.${W}.nominal.${P}.root --remove-near-min 0.8 --y-max 70 ${EXTRA} --envelope --chop 100  --no-input-label --translate pois.json --json ${OUTPUT}/neg_${W}.json --hide-envelope  --breakdown "Syst,Stat" --meta "Types:${W},POIs:${P}" --outdir ${OUTPUT}/${M}; done; done; done

#######################################
# Plotting envelope for L2_llq
INPUT="Mar26/results"; OUTPUT="Mar26/plots/kappas_neg"; for M in L2_llq; do mkdir -p ${OUTPUT}/${M}; for W in observed postfit_asimov; do COL=1; case ${W} in prefit_asimov) COL=4; EXTRA='--main-label "SM Expected" --main-color 4';; postfit_asimov) COL=2; EXTRA='--main-label "SM Expected" --main-color 2';; *) EXTRA="";; esac; for P in $(./getPOIs_hmm.py ${M} -P); do eval python scripts/plot1DScan.py -o scan_neg_${W}_${M}_${P} --POI ${P} --model ${M} --others \
\"${INPUT}/scan.neg.${M}_N1.${W}.nominal.${P}.root:#lambda_{lq}\>0, \#\lambda_{Vq}\>0:4\" \
\"${INPUT}/scan.neg.${M}_N2.${W}.nominal.${P}.root:#lambda_{lq}\<0, \#\lambda_{Vq}\>0:30\" \
\"${INPUT}/scan.neg.${M}_N3.${W}.nominal.${P}.root:#lambda_{lq}\>0, \#\lambda_{Vq}\<0:46\" \
\"${INPUT}/scan.neg.${M}_N4.${W}.nominal.${P}.root:#lambda_{lq}\<0, \#\lambda_{Vq}\<0:40\" \
\"${INPUT}/scan.${M}_N1.${W}.fr.all.${P}.root:#lambda_{lq}\>0, \#\lambda_{Vq}\>0:4\" \
\"${INPUT}/scan.${M}_N2.${W}.fr.all.${P}.root:#lambda_{lq}\<0, \#\lambda_{Vq}\>0:30\" \
\"${INPUT}/scan.${M}_N3.${W}.fr.all.${P}.root:#lambda_{lq}\>0, \#\lambda_{Vq}\<0:46\" \
\"${INPUT}/scan.${M}_N4.${W}.fr.all.${P}.root:#lambda_{lq}\<0, \#\lambda_{Vq}\<0:40\" \
-m ${INPUT}/scan.neg.${M}_N1.${W}.nominal.${P}.root --remove-near-min 0.8 --y-max 70 ${EXTRA} --envelope --chop 100  --no-input-label --translate pois.json --json ${OUTPUT}/neg_${W}.json --hide-envelope  --breakdown "Syst,Stat" --meta "Types:${W},POIs:${P}" --outdir ${OUTPUT}/${M}; done; done; done

# Version excluding
INPUT="Mar26/results"; OUTPUT="Mar26/plots/kappas_neg_no_Wt"; for M in L2_llq; do mkdir -p ${OUTPUT}/${M}; for W in observed postfit_asimov; do COL=1; case ${W} in prefit_asimov) COL=4; EXTRA='--main-label "SM Expected" --main-color 4';; postfit_asimov) COL=2; EXTRA='--main-label "SM Expected" --main-color 2';; *) EXTRA="";; esac; for P in $(./getPOIs_hmm.py ${M} -P); do eval python scripts/plot1DScan.py -o scan_neg_${W}_${M}_${P} --POI ${P} --model ${M} --others \
\"${INPUT}/scan.neg.${M}_N1.${W}.nominal.${P}.root:#lambda_{lq}\>0, \#\lambda_{Vq}\>0:4\" \
\"${INPUT}/scan.neg.${M}_N2.${W}.nominal.${P}.root:#lambda_{lq}\<0, \#\lambda_{Vq}\>0:30\" \
\"${INPUT}/scan.${M}_N1.${W}.fr.all.${P}.root:#lambda_{lq}\>0, \#\lambda_{Vq}\>0:4\" \
\"${INPUT}/scan.${M}_N2.${W}.fr.all.${P}.root:#lambda_{lq}\<0, \#\lambda_{Vq}\>0:30\" \
-m ${INPUT}/scan.neg.${M}_N1.${W}.nominal.${P}.root --remove-near-min 0.8 --y-max 70 ${EXTRA} --envelope --chop 100  --no-input-label --translate pois.json --json ${OUTPUT}/neg_${W}.json --hide-envelope  --breakdown "Syst,Stat" --meta "Types:${W},POIs:${P}" --outdir ${OUTPUT}/${M}; done; done; done