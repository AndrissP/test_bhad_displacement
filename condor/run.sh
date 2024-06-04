#!/bin/bash

echo
echo 'CONDOR-START---------------'
source /cvmfs/cms.cern.ch/cmsset_default.sh

ID=$1
OUTDIR=$2
filenames_txt=$3
sample=$4
HT_bin=$5

CERTDIR=$(readlink -f /afs/cern.ch/user/a/anpotreb/k5-ca-proxy.pem )
export X509_USER_PROXY=${CERTDIR}
voms-proxy-info -all
voms-proxy-info -all -file ${CERTDIR}


cd /eos/home-a/anpotreb/lxplus/top/C10629_TopMass/src/test_bhad_displacement
# eval `scramv1 runtime -sh` #cmsenv
eval $(scram ru -sh)
# cd $TOPDIR


echo 'ID = '$ID
echo 'OUTDIR = '$OUTDIR
# echo 'jobName = '$jobName

# bin_options=("HT1000to1500" "HT1500to2000" "HT2000toInf")
# run_bins=${bin_options[${ID}]}
fileName=$(sed "$((${ID}+1))q;d" ${filenames_txt})
echo Running bins: $HT_bin
echo 'fileName = '$fileName

# outFile=${YODADIR}'/MC_TTBAR_'${ID}'.yoda'

python get_displacement.py -b ${HT_bin} -o ${OUTDIR} -i ${fileName} -s ${sample} -d ${ID}

echo 'CONDOR-FINISHED---------------'
echo

