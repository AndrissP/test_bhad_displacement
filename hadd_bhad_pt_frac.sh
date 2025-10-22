b_meson_types=(511 513 515 521 523 525 531 533 535 541 543 553 555)
# dir=res_res_bhad_frac/Py/2000toInf
dir=res_bhad_frac/Py/2000toInf


for bmes in ${b_meson_types[@]}; do
    hadd -f ${dir}/pt_frac_${bmes}_2000toInf.root ${dir}/pt_frac_${bmes}_2000toInf_*.root
    # hadd -f ${dir}/pt_frac_${bmes}_2d_2000toInf.root ${dir}/pt_frac_${bmes}_2d_2000toInf_*.root
done