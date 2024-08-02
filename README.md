# test_bhad_displacement

### Setup/test
```
cmssw-el7
scramv1 project -n CMSSW10629_b_had_displacement CMSSW CMSSW_10_6_29
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd CMSSW10629_b_had_displacement/src
cmsenv
```

Run as 
```
python get_displacement.py -s Her
```
locally.
The output is saved under `Res`
"histograms1_<HTbin>_<id>.root": b-hadron displacement histogram in narrow bins
"histograms2_<HTbin>_<id>.root": b-hadron displacement histogram in wide bins
"histograms3_<HTbin>_<id>.root": b-hadron displacement vs jet energy response
"histograms4_<HTbin>_<id>.root": b-hadron transverse displacement histogram in narrow bins
"histograms5_<HTbin>_<id>.root": b-hadron transverse displacement vs jet energy response

### Run on condor
The script can be run on condor.
```
exit
```

Exit from the singularity if still on it.
```
cd condor
./submit.sh Her HT1000to1500
./submit.sh Py HT1000to1500
```

### Plotting
After condor the output histograms have to be merged:
```
hadd res/Py/2000toInf/histograms4_2000toInf.root res/Py/2000toInf/histograms4_2000toInf_*.root
hadd res/Py/2000toInf/histograms5_2000toInf.root res/Py/2000toInf/histograms5_2000toInf_*.root
hadd res/Her/2000toInf/histograms4_2000toInf.root res/Her/2000toInf/histograms4_2000toInf_*.root
hadd res/Her/2000toInf/histograms5_2000toInf.root res/Her/2000toInf/histograms5_2000toInf_*.root
```

Plot the histograms with
```
python plot_transverse_displacement.py
```
Output is stored under `pdfs/`
