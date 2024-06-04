#! /usr/bin/env python

from os import path
from DataFormats.FWLite import Events, Handle
handle = Handle('vector<reco::GenParticle>')
label = 'prunedGenParticles'

def test_FWLite(events):
    num_events = events.size()
    print("Number of events: ", num_events)
    ii = 0
    for event in events:
        ii+=1
        if ii>10:
            break
        event.getByLabel(label, handle)
        genParts = handle.product()
        print("genParts.size(): ", genParts.size())
    return

filedir = '/eos/cms/store/user/anpotreb/QCD_MINIAOD_test'
#   inputfiles = ['/afs/cern.ch/user/a/anpotreb/public/QCD_HT1000to1500_example.root' ]
inputfiles = ['root://xrootd-cms.infn.it///store/mc/RunIISummer20UL16MiniAODAPVv2/QCD_HT1000to1500_TuneCH3_13TeV-madgraphMLM-herwig7/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v2/2530000/0610108D-7DC6-4A43-B32F-56B08555C20E.root' ]

for inputfile in inputfiles:
    if not path.exists(inputfile):
        print('No input file found!')

    print("loading file: ", inputfile) 
    events = Events(inputfile)
    test_FWLite(events)

