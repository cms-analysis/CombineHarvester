#!/bin/bash
declare -A ds

d='output/' 
ds_nosys=( ${d}'2018-05-28_17h12m52_lumi-36.9_nosyst/'    ${d}'2018-05-28_21h31m42_lumi-300.0_nosyst/'    ${d}'2018-05-29_06h49m00_lumi-3000.0_nosyst/' )
ds_nosca=( ${d}'2018-05-28_17h26m20_lumi-36.9/'           ${d}'2018-05-28_21h45m09_lumi-300.0/'           ${d}'2018-05-29_07h02m42_lumi-3000.0/' )
ds_scall=( ${d}'2018-05-29_14h11m23_lumi-36.9_scale-all/' ${d}'2018-05-29_16h20m33_lumi-300.0_scale-all/' ${d}'2018-05-29_13h29m05_lumi-3000.0_scale-all/' )
ds_scbbb=( ${d}'2018-05-28_19h03m17_lumi-36.9_scale-bbb/' ${d}'2018-05-29_01h57m17_lumi-300.0_scale-bbb/' ${d}'2018-05-29_17h45m29_lumi-3000.0_scale-bbb/' )

modes=( 'no-systematics' 'no-scaling'  'scale-all' 'scale-bbb' )
lumi=(  '36.9_fb^{-1}'   '300_fb^{-1}' '3000_fb^{-1}'          )
ds[no-systematics]=ds_nosys[@]
ds[no-scaling]=ds_nosca[@]
ds[scale-all]=ds_scall[@]
ds[scale-bbb]=ds_scbbb[@]

for m in ${modes[@]}; do 
    i=0
    for d in ${!ds[$m]}; do ds_[i]=$d; let i=$i+1; done

    for p in 'ggH' 'bbH'; do
	title_left="${p}, `echo $m | tr - ' '`"
	echo "##### $title_left #####"
	lterm=''
	for i in `seq 0 $(( ${#lumi[@]} - 1 ))`; do
	    lterm+=${ds_[$i]}${p}'_cmb.json:exp0:Title='"\"${lumi[$i]}\""
	    lterm+=" "
	done
#	echo $lterm
	python scripts/plotMSSMLimits.py --logy --logx --show exp0 $lterm --cms-sub="Preliminary" -o output/${m}_${p} --process=${p:0:2}'#phi' --title-right="13 TeV" --use-hig-17-020-style --auto-style --ratio-to ${ds_[0]}${p}'_cmb.json:exp0' --title-left="$title_left"
    done
done


#    python scripts/plotMSSMLimits.py --logy --logx --show exp0 ${ds_unsc[0]}${p}'_cmb.json:exp0:Title="36.9 fb^{-1}"' ${ds_unsc[1]}${p}'_cmb.json:exp0:Title="300/fb"' ${ds_unsc[2]}${p}'_cmb.json:exp0:Title="3000/fb"' --cms-sub="Preliminary" -o output/noscale_${p} --process=${p:0:2}'#phi' --title-right="13 TeV" --use-hig-17-020-style --auto-style --ratio-to ${ds_unsc[0]}${p}'_cmb.json:exp0' --title-left=''${p}', unscaled'

