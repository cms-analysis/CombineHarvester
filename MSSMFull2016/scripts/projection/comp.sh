#!/bin/bash

d='output/'
ds_nosys=( ${d}'2018-05-28_17h12m52_lumi-36.9_nosyst/' ${d}'2018-05-28_21h31m42_lumi-300.0_nosyst/' ${d}'2018-05-29_06h49m00_lumi-3000.0_nosyst/' )
ds_unsc=(  ${d}'2018-05-28_17h26m20_lumi-36.9/' ${d}'2018-05-28_21h45m09_lumi-300.0/' ${d}'2018-05-29_07h02m42_lumi-3000.0/' )

for p in 'ggH' 'bbH'; do
    python scripts/plotMSSMLimits.py --logy --logx --show exp0 ${ds_nosys[0]}${p}'_cmb.json:exp0:Title="36.9 fb^{-1}"' ${ds_nosys[1]}${p}'_cmb.json:exp0:Title="300/fb"' ${ds_nosys[2]}${p}'_cmb.json:exp0:Title="3000/fb"' --cms-sub="Preliminary" -o output/nosyst_${p} --process=${p:0:2}'#phi' --title-right="13 TeV" --use-hig-17-020-style --auto-style --ratio-to ${ds_nosys[0]}${p}'_cmb.json:exp0' --title-left=''${p}', no systematics'

    python scripts/plotMSSMLimits.py --logy --logx --show exp0 ${ds_unsc[0]}${p}'_cmb.json:exp0:Title="36.9 fb^{-1}"' ${ds_unsc[1]}${p}'_cmb.json:exp0:Title="300/fb"' ${ds_unsc[2]}${p}'_cmb.json:exp0:Title="3000/fb"' --cms-sub="Preliminary" -o output/noscale_${p} --process=${p:0:2}'#phi' --title-right="13 TeV" --use-hig-17-020-style --auto-style --ratio-to ${ds_unsc[0]}${p}'_cmb.json:exp0' --title-left=''${p}', unscaled'
done




