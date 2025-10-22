#! /bin/bash
## usage example:  ./get_file_names.sh /QCD_HT2000toInf_TuneCH3_13TeV-madgraphMLM-herwig7/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/AODSIM QCD_Her_2000toInf_AOD.txt
queryName=$1

out_file='fileNames.txt'
out_file=$2
rm -f ${out_file}

# queryName="dataset=/QCD_HT*to*0_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*v8-v1*/NANO*" 
# queryName="/TT_TuneCH3_13TeV-powheg-herwig7/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM"

dasgoclient -query="file dataset=$queryName" >> ${out_file}
#dasgoclient -query=$queryName \
#  >> ${out_file}

