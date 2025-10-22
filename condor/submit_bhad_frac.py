outDIR="/eos/home-a/anpotreb/lxplus/top/C10629_TopMass/src/test_bhad_displacement/res_bhad_frac/"
logDIR="/afs/cern.ch/user/a/anpotreb/condor/bhad_fractions/"
sample=$1
HTbin=$2

mkdir -p $logDIR                                                        
echo sample = ${sample}
echo HT_bin = ${HTbin}
logDIR=${logDIR}/${sample}_${HTbin}/

echo outDIR = ${outDIR}
echo logDIR = ${logDIR}
mkdir -p $logDIR 
rm -f ${logDIR}* 
mkdir -p ${outDIR}
submitFile=submit.sub
cp ${submitFile} $logDIR
executable=run_bhad_frac.sh
cp ${executable} $logDIR

outDIR=${outDIR}/${sample}/${HTbin}
mkdir -p ${outDIR}

filename=QCD_${sample}_${HTbin}_AOD.txt

echo filename = ${filename}

Njobs=$(cat ../${filename} | wc -l)
# Njobs=5
echo Njobs = ${Njobs}
cd $logDIR

sed -i -e "s|QUEUE|${Njobs}|g" ${submitFile}
sed -i -e "s|LOGDIR|${logDIR}|g" ${submitFile} 
sed -i -e "s|EXECUTABLE|${executable}|g" ${submitFile}
sed -i -e "s|OUTDIR|${outDIR}|g" ${submitFile}
sed -i -e "s|FILENAME|${filename}|g" ${submitFile}
sed -i -e "s|SAMPLE|${sample}|g" ${submitFile}
sed -i -e "s|HTBIN|${HTbin}|g" ${submitFile}
sed -i -e "s|JOBFLAVOUR|espresso|g" ${submitFile}
#  sed -i -e "s|CONFIG|runRivetAnalyzer_template.py|g" ${submitFile}
condor_submit ${submitFile}
cd -
