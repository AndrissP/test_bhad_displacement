#! /usr/bin/env python

import ROOT
import sys
from os import path
from DataFormats.FWLite import Events, Handle
from ROOT.Math import VectorUtil
import numpy as np
# import cmsstyle as CMS
# import os

def is_bhad(pdgId):
    pdgId_str = str(np.abs(pdgId))
    if len(pdgId_str)<3:
        return False
    elif pdgId_str[0]=='5':
        return True
    elif len(pdgId_str)>4 and pdgId_str[-3]=='5':
        return True
    else:
        return False


# infile = 'QCD_HT1000to1500_example.root'
# inputfile = 'QCD_HT1000to1500_Her_example.root'

# if not path.exists(inputfile):
    # print('No input file found!')

# print("loading file: ", inputfile) 
# events = Events(inputfile)
# handle = Handle('float')
# handle = Handle('vector<pat::Muon>')
handle = Handle('vector<reco::GenParticle>')
label = 'prunedGenParticles'
handle_jets = Handle('vector<pat::Jet>')
label_jets = 'slimmedJets'
handle_genjets = Handle('vector<reco::GenJet>')
label_genjets = 'slimmedGenJets'
handle_gen_info = Handle('GenEventInfoProduct')
label_gen_info = 'generator'
# label = 'slimmedMuons'
# label = 'genParticles'
# Define the bin edges
bin_edges = [0.0, 0.5, 1, 2, 5, 10, 20]
# Create an array in ROOT with the bin edges
bin_edges_array = ROOT.std.vector('double')()
for edge in bin_edges:
    bin_edges_array.push_back(edge)

def txt2filesls(dataset_name, Nfiles=5, xrootdstr='root://xrootd-cms.infn.it/'):
    with open(dataset_name) as f:
        rootfiles = f.read().split()
        if Nfiles==-1:
            Nfiles = len(rootfiles)
        rootfiles = rootfiles[:Nfiles]
        has_xrootd = 'root://' in rootfiles[0]
        prepend_str = '' if has_xrootd else xrootdstr
        fileslist = [prepend_str + file for file in rootfiles]
    return fileslist

def get_displacement(events, handle, label, hist, hist2, hist3, hist4, hist5):
    debug_jet_matching = False

    # import pdb; pdb.set_trace()
    num_events = events.size()
    print("Number of events: ", num_events)
    ii = 0
    for event in events:
        # print("Event Nr = ", event.eventAuxiliary().event() )
        ii+=1
        if ii%1000==0:
            print("Event Nr = ", ii )
        # if ii>500:
        #     break
        event.getByLabel(label, handle)
        genParts = handle.product()
        
        event.getByLabel(label_genjets, handle_genjets)
        gen_jets = handle_genjets.product()

        event.getByLabel(label_jets, handle_jets)
        jets = handle_jets.product()

        # import pdb; pdb.set_trace()
        event.getByLabel(label_gen_info, handle_gen_info)
        gen_info = handle_gen_info.product()
        event_weight = gen_info.weight()
        
        # Take only events with (the problemmatic) high pt bottom jet as the loop over the gen particles is very slow

        high_pt_jets = []
        for jet in jets:
            matched_gen = jet.genJet()
            if not matched_gen == None and matched_gen.pt() > 750 and matched_gen.pt() < 1000: # and abs(jet.partonFlavour()) == 5:
                high_pt_jets.append(jet)
        
        if len(high_pt_jets)==0:
            print("No high pt jet found in the event ")
            continue
        # print("len jets = ", len(jets))
        # print("len jets = ", len(high_pt_jets))

        # goodbhads = []
        Nmatched_hads = 0
        for idx in range(genParts.size()):            
            genPart = genParts[idx]
            # genPart.Print()
            vertex = genPart.vertex()
            r = vertex.r()
            x = vertex.x()
            y = vertex.y()
            # if str(np.abs(genPart.pdgId()))[0]=='5':
            #     x = vertex.x()
            #     y = vertex.y()
            #     z = vertex.z()
            #     print("idx = ", idx, "pdgId = ", genPart.pdgId(), "status = ", genPart.status(), "x = ", np.round(x,6), "y = ", np.round(y,6), "z = ", np.round(z,6), "r = ", np.round(r,6), "isPromptDecayed", genPart.isPromptDecayed(), "isPromptFinalState", genPart.isPromptFinalState(), "isLastCopy = ", genPart.isLastCopy())
            #     print("genPart phi = ", np.round(genPart.phi(),5), "genPart eta = ", np.round(genPart.eta(),5), "genPart pt = ", np.round(genPart.pt(),5), "genPart pdgId = ", genPart.pdgId())
            #     for daughter in genPart.daughterRefVector():
            #         print("daughter:     pdgId = ", daughter.pdgId(), "status = ", daughter.status(), "x = ", np.round(daughter.vertex().x(),6), "y = ", np.round(daughter.vertex().y(),6), "z = ", np.round(daughter.vertex().z(),6), "r = ", np.round(daughter.vertex().r(),6), "isPromptDecayed", daughter.isPromptDecayed(), "isPromptFinalState", daughter.isPromptFinalState(), "isLastCopy = ", daughter.isLastCopy())
            #     for mother in genPart.motherRefVector():
            #         print("mother:       pdgId = ", mother.pdgId(), "status = ", mother.status(), "x = ", np.round(mother.vertex().x(),6), "y = ", np.round(mother.vertex().y(),6), "z = ", np.round(mother.vertex().z(),6), "r = ", np.round(mother.vertex().r(),6), "isPromptDecayed", mother.isPromptDecayed(), "isPromptFinalState", mother.isPromptFinalState(), "isLastCopy = ", mother.isLastCopy())
            #     print("  ")
            if is_bhad(genPart.pdgId()) and genPart.isLastCopy():
                # Take only the last b hadrons
                has_bhad_daughter = any(is_bhad(daughter.pdgId()) for daughter in genPart.daughterRefVector())
                if has_bhad_daughter:
                    continue
                # goodbhads.append(genPart)
                # print("jet phi = ", np.round(jet.phi(),5), "jet eta = ", jet.eta(), "jet pt = ", jet.pt())

                # check if the b hadron comes from the high pt jet
                matches_with_jet = False
                # print("genPart phi = ", genPart.phi(), "genPart eta = ", genPart.eta(), "genPart pt = ", genPart.pt())
                matched_jet = None
                for jet in high_pt_jets:
                    # import    pdb; pdb.set_trace()
                    dr = np.sqrt(VectorUtil.DeltaR2(jet.p4(), genPart.p4()))
                    # print("jet phi = ", jet.phi(), "jet eta = ", jet.eta(), "jet pt = ", jet.pt())
                    # print("dr = ", dr  )
                    if dr < 0.2:
                        matches_with_jet = True
                        if debug_jet_matching:
                            if abs(jet.partonFlavour()) == 5:
                                print("The given b hadron correctly matches with a high pt b jet")
                                Nmatched_hads += 1
                                # high_pt_jets.remove(jet)
                            else:
                                print("The given b hadron matches to a jet that is not a b jet")
                        matched_jet = jet
                        break
                # print("ches_with_jet: ", matches_with_jet)
                if not matches_with_jet:
                    # print("ches_with_jet: ", matches_with_jet)
                    continue

                daughter = genPart.daughter(0)
                displacement = np.abs(daughter.vertex().r()-r)   # in cm
                displacement_T = np.sqrt((daughter.vertex().x()-x)**2 + (daughter.vertex().y()-y)**2)   # in cm 
                # print("displacement = ", displacement)
                jet_energy_response = jet.pt() / jet.genJet().pt()

                hist.Fill(displacement) #, event_weight)
                hist2.Fill(displacement) #, event_weight)
                hist3.Fill(displacement, jet_energy_response) #, event_weight)
                hist4.Fill(displacement_T)
                hist5.Fill(displacement_T, jet_energy_response)
                

        if debug_jet_matching:
            Nbjets = 0
            for jet in gen_jets:
                if jet.pt() > 750 and abs(jet.partonFlavour()) == 5:
                    Nbjets += 1
            if not Nbjets == Nmatched_hads:
                print("Error in matching.", "Nbjets = ", Nbjets, "Nmatched_hads = ", Nmatched_hads)

    return hist, hist2, hist3, hist4, hist5, num_events

filedir = '/eos/cms/store/user/anpotreb/QCD_MINIAOD_test'
# inputfiles_Py = ['QCD_HT1000to1500.root']
# inputfiles_Py = ['QCD_HT1000to1500_example.root']
# inputfiles_Py = {"HT1000to1500": [filedir+'/QCD_HT1000to1500.root'],
#                  "HT1500to2000": [filedir+'/QCD_HT1500to2000.root'],
#                  "HT2000toInf":  [filedir+'/QCD_HT2000toInf.root']
#                   }
inputfiles_Py = {"HT1000to1500": txt2filesls('QCD_Py_1000to1500.txt', Nfiles=-1),
                 "HT1500to2000": txt2filesls('QCD_Py_1500to2000.txt', Nfiles=-1),
                 "HT2000toInf":  txt2filesls('QCD_Py_2000toInf.txt', Nfiles=-1)
                  }
# inputfiles_Py = txt2filesls('QCD_Py_1000to1500.txt', Nfiles=2)
# inputfiles_Her = txt2filesls('/afs/cern.ch/user/a/anpotreb/top/JERC/JMECoffea/fileNames/QCD_Herwig_20UL18/QCD_HT1000to1500_20UL18_JMENano_Herwig.txt', Nfiles=2)
# inputfiles_Her = ['QCD_HT1000to1500_Her.root']
# inputfiles_Her = ['QCD_HT1000to1500_Her_example.root']
# inputfiles_Her = {"HT1000to1500": [filedir+'/QCD_HT1000to1500_Her.root'],
#                   "HT1500to2000": [filedir+'/QCD_HT1500to2000_Her.root'],
#                   "HT2000toInf":  [filedir+'/QCD_HT2000toInf_Her.root']
                #   }
inputfiles_Her = {"HT1000to1500": txt2filesls('QCD_Her_1000to1500.txt', Nfiles=-1),
                  "HT1500to2000": txt2filesls('QCD_Her_1500to2000.txt', Nfiles=-1),
                  "HT2000toInf":  txt2filesls('QCD_Her_2000toInf.txt', Nfiles=-1)
                  }

### multiply Herwig by 2000 to match Pythia and Herwig (Herwig to Pythia retio of the sum of weights)
# xsec_Her = {"HT1000to1500": 0.8013*1.35,
#             "HT1500to2000": 0.06815*1.6,
#             "HT2000toInf": 0.01245*1.75}
xsec_Py = {"HT1000to1500": 1118.0,
            "HT1500to2000": 109.8,
            "HT2000toInf": 21.93}

xsec_Her = {"HT1000to1500": 1118.0*1.1,
            "HT1500to2000": 109.8*1.15,
            "HT2000toInf": 21.93*1.2}
# hist_tot
# for HT_bin in inputfiles_Her.keys():

def run_displacement_file(inputfile, sample, HT_bin, out_dir='res', id='0'):
    hist = ROOT.TH1F('lambda_tmp'+'_'+HT_bin+'_'+sample, ';displacement cm;number of gen particles', len(bin_edges)-1, bin_edges_array.data())
    hist2 = ROOT.TH1F('lambda2_tmp'+'_'+HT_bin+'_'+sample, ';displacement cm;number of gen particles', 30, 0, 2.1)
    hist3 = ROOT.TH2F('x_vs_R'+'_'+HT_bin+'_'+sample, 'B-hadron Displacement vs Jet Energy Response', len(bin_edges)-1, bin_edges_array.data(), 30, 0, 2)
    hist4 = ROOT.TH1F('xT_tmp'+'_'+HT_bin+'_'+sample, ';tranverse displacement cm;number of gen particles', len(bin_edges)-1, bin_edges_array.data())
    hist5 = ROOT.TH2F('xT_vs_R'+'_'+HT_bin+'_'+sample, 'B-hadron tranverse Displacement vs Jet Energy Response', len(bin_edges)-1, bin_edges_array.data(), 30, 0, 2)

    xrootdstr='root://xrootd-cms.infn.it/'
    inputfile = xrootdstr + inputfile
    print("loading file: ", inputfile) 
    events = Events(inputfile)
    hist, hist2, hist3, hist4, hist5, num_events = get_displacement(events, handle, label, hist, hist2, hist3, hist4, hist5)
    tot_events = num_events

    if sample == 'Py':
        xsec = xsec_Py
    elif sample == 'Her':
        xsec = xsec_Her
    scale_factor = xsec['HT'+HT_bin] / tot_events
    hist.Scale(scale_factor)
    hist2.Scale(scale_factor)
    hist3.Scale(scale_factor)
    hist4.Scale(scale_factor)
    hist5.Scale(scale_factor)
    vals = []
    errs = []
    for i in range(0, hist.GetNbinsX() + 2):
        vals.append(hist.GetBinContent(i))
        errs.append(hist.GetBinError(i))
    print("vals = ", vals)
    print("errs = ", errs)

    file = ROOT.TFile(out_dir+"/histograms1"+'_'+HT_bin+'_'+id+".root", "RECREATE")
    hist.Write()
    file.Close()
    print("Written to file: ", out_dir+"/histograms1"+'_'+HT_bin+'_'+id+".root")

    file = ROOT.TFile(out_dir+"/histograms2"+'_'+HT_bin+'_'+id+".root", "RECREATE")
    hist2.Write()
    file.Close()
    print("Written to file: ", out_dir+"/histograms2"+'_'+HT_bin+'_'+id+".root")

    file = ROOT.TFile(out_dir+"/histograms3"+'_'+HT_bin+'_'+id+".root", "RECREATE")
    hist3.Write()
    file.Close()
    print("Written to file: ", out_dir+"/histograms3"+'_'+HT_bin+'_'+id+".root")

    file = ROOT.TFile(out_dir+"/histograms4"+'_'+HT_bin+'_'+id+".root", "RECREATE")
    hist4.Write()
    file.Close()
    print("Written to file: ", out_dir+"/histograms4"+'_'+HT_bin+'_'+id+".root")

    file = ROOT.TFile(out_dir+"/histograms5"+'_'+HT_bin+'_'+id+".root", "RECREATE")
    hist5.Write()
    file.Close()
    print("Written to file: ", out_dir+"/histograms5"+'_'+HT_bin+'_'+id+".root")
# def run_displacement(run_bins=None, out_dir='res'):
#     if run_bins is None:
#         run_bins = ["HT2000toInf"] 
#     hists1 = []
#     hists2 = []
#     hists3 = []

#     for sample in ['Py', 'Her']:
#         hist_tot1 = ROOT.TH1F('lambda'+'_'+sample, ';displacement cm;number of gen particles', len(bin_edges)-1, bin_edges_array.data())
#         hist_tot2 = ROOT.TH1F('lambda2'+'_'+sample, ';displacement cm;number of gen particles', 30, 0, 2.1)

#         if sample == 'Py':
#             inputfiles = inputfiles_Py
#             xsec = xsec_Py
#         elif sample == 'Her':
#             inputfiles = inputfiles_Her
#             xsec = xsec_Her

#         for HT_bin in run_bins: #inputfiles_Her: #
#             hist = ROOT.TH1F('lambda_tmp'+'_'+HT_bin+'_'+sample, ';displacement cm;number of gen particles', len(bin_edges)-1, bin_edges_array.data())
#             hist2 = ROOT.TH1F('lambda2_tmp'+'_'+HT_bin+'_'+sample, ';displacement cm;number of gen particles', 30, 0, 2.1)
#             hist3 = ROOT.TH2F('x_vs_R'+'_'+HT_bin+'_'+sample, 'B-hadron Displacement vs Jet Energy Response', len(bin_edges)-1, bin_edges_array.data(), 30, 0, 2)
#             tot_events = 0
#             for inputfile in inputfiles[HT_bin]:

#                 print("loading file: ", inputfile) 
#                 events = Events(inputfile)
#                 hist, hist2, hist3, num_events = get_displacement(events, handle, label, hist, hist2, hist3)
#                 tot_events += num_events

#             scale_factor = xsec[HT_bin] / tot_events
#             hist.Scale(scale_factor)
#             hist2.Scale(scale_factor)
#             hist3.Scale(scale_factor)

#             hist_tot1.Add(hist)
#             hist_tot2.Add(hist2)
#             hists1.append(hist)
#             hists2.append(hist2)
#             hists3.append(hist3)

#             vals = []
#             errs = []
#             for i in range(0, hist.GetNbinsX() + 2):
#                 vals.append(hist.GetBinContent(i))
#                 errs.append(hist.GetBinError(i))
#             print("vals = ", vals)
#             print("errs = ", errs)

#         hists1.append(hist_tot1)
#         hists2.append(hist_tot2)

#     vals = []
#     errs = []
#     for i in range(1, hist_tot1.GetNbinsX() + 1):
#         vals.append(hist_tot1.GetBinContent(i))
#         errs.append(hist_tot1.GetBinError(i))
#     print("vals = ", vals)
#     print("errs = ", errs)



#     file = ROOT.TFile(out_dir+"/histograms1"+'_'.join(run_bins)+".root", "RECREATE")
#     for hist in hists1:
#         hist.Write()
#     file.Close()

#     file = ROOT.TFile(out_dir+"/histograms2"+'_'.join(run_bins)+".root", "RECREATE")
#     for hist in hists2:
#         hist.Write()
#     file.Close()

#     file = ROOT.TFile(out_dir+"/histograms3"+'_'.join(run_bins)+".root", "RECREATE")
#     for hist in hists3:
#         hist.Write()
#     file.Close()

import optparse
def main():
    parser = optparse.OptionParser()
    parser.add_option('-b', '--bins', dest='bins', default="2000toInf", help='bins to run')
    parser.add_option('-o', '--out_dir', dest='out_dir', default='res', help='output directory')
    parser.add_option('-i', '--infile', dest='infile', default=None, help='input file')
    parser.add_option('-s', '--sample', dest='sample', default='Py', help='sample')
    parser.add_option('-d', '--id', dest='id', default=0, help='id')
    options, args = parser.parse_args()
    run_bins = options.bins
    out_dir = options.out_dir
    infile = options.infile
    sample = options.sample
    id = str(options.id)
    if run_bins is not None:
        run_bins = run_bins.split(',')

    if infile is None:
        infile = txt2filesls('QCD_{}_{}.txt'.format(sample, run_bins[0]), Nfiles=1, xrootdstr='')[0]
        # run_displacement(run_bins, out_dir)
    print("run_bins = ", run_bins)
    print("out_dir = ", out_dir)
    print("infile = ", infile)
    print("sample = ", sample)
    print("id = ", id)
    # run_displacement(run_bins, out_dir)

    run_displacement_file(infile, sample, run_bins[0], out_dir=out_dir, id=id)

if __name__ == "__main__":
    sys.exit(main())