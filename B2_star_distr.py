#! /usr/bin/env python27
### Run within CMSSW environment

'''
Use AOD info
Get Bs^* distribution vs jet energy response in the jet
'''

import ROOT
import sys
from os import path
from DataFormats.FWLite import Events, Handle
from ROOT.Math import VectorUtil
import numpy as np
import math

# b_mes_in_Her = [511, 513, 515, 521, 523, 525, 531, 533, 535, 543]
# b_mes_in_Pu =  [511, 513, 521, 523, 531, 533, 541, 543, 553, 555]

b_meson_types = [511, 513, 515, 521, 523, 525, 531, 533, 535, 541, 543, 553, 555]

def is_B2_star(pdgId):
    if abs(pdgId)==525:
        return True
    else:
        return False

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

handle_genPart = Handle('vector<reco::GenParticle>')
label_genPart = 'genParticles'
handle_jets = Handle('vector<reco::PFJet>')
label_jets = 'ak4PFJetsCHS'
handle_genjets = Handle('vector<reco::GenJet>')
label_genjets = 'ak4GenJetsNoNu'
handle_gen_info = Handle('GenEventInfoProduct')
label_gen_info = 'generator'

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

def get_displacement(events, hist, debug_script=True, debug_jet_matching=False):
    ''' TODO:
    hists: dictionary of histograms
    hist{"B2_star_frac"}: pt fraction of the B2* hadron in the jet
    hist{"jet_response"}: jet energy response
    hist{"B2_star_pt2d"}: 2d histogram of B2* pt vs jet energy response
    '''
    num_events = events.size()
    print("Number of events: ", num_events)
    evtii = 0
    for event in events:
        # print("Event Nr = ", event.eventAuxiliary().event() )
        evtii+=1
        if evtii%1000==0:
            print("Event Nr = ", evtii )
        if evtii>100:
            break
        event.getByLabel(label_genPart, handle_genPart)
        genParts = handle_genPart.product()

        event.getByLabel(label_genjets, handle_genjets)
        gen_jets = handle_genjets.product()

        event.getByLabel(label_jets, handle_jets)
        jets = handle_jets.product()

        # import pdb; pdb.set_trace()
        event.getByLabel(label_gen_info, handle_gen_info)
        gen_info = handle_gen_info.product()
        event_weight = gen_info.weight()

        ### COMMENT
        # for jet in jets:
        #     import pdb; pdb.set_trace()
        #     if abs(jet.partonFlavour()) == 5: #and matched_gen.pt() > 750 and matched_gen.pt() < 1000: # not matched_gen == None and 
        #         good_jets.append(jet)

        # if len(good_jets)==0:
        #     print("No b jets found in the event ")
        #     continue

        ### Find all B2* hadrons and b hadrons in the event
        ### B hadrons are needed for finding b jets
        B2stars = []
        Bhads = []
        for idx in range(genParts.size()):            
            genPart = genParts[idx]
            if debug_script:
                if is_B2_star(genPart.pdgId()):
                    print("genPart phi = ", np.round(genPart.phi(),5), "genPart eta = ", np.round(genPart.eta(),5), "genPart pt = ", np.round(genPart.pt(),5), "genPart pdgId = ", genPart.pdgId())
                    for daughter in genPart.daughterRefVector():
                        print("daughter:     pdgId = ", daughter.pdgId(), "status = ", daughter.status(), "x = ", np.round(daughter.vertex().x(),6), "y = ", np.round(daughter.vertex().y(),6), "z = ", np.round(daughter.vertex().z(),6), "r = ", np.round(daughter.vertex().r(),6), "isPromptDecayed", daughter.isPromptDecayed(), "isPromptFinalState", daughter.isPromptFinalState(), "isLastCopy = ", daughter.isLastCopy())
                    for mother in genPart.motherRefVector():
                        print("mother:       pdgId = ", mother.pdgId(), "status = ", mother.status(), "x = ", np.round(mother.vertex().x(),6), "y = ", np.round(mother.vertex().y(),6), "z = ", np.round(mother.vertex().z(),6), "r = ", np.round(mother.vertex().r(),6), "isPromptDecayed", mother.isPromptDecayed(), "isPromptFinalState", mother.isPromptFinalState(), "isLastCopy = ", mother.isLastCopy())
                    print("  ")
            if is_B2_star(genPart.pdgId()) and genPart.isLastCopy():
                # print("Is last copy and is B2star")
                B2stars.append(genPart)
                Bhads.append(genPart)
            elif is_bhad(genPart.pdgId()) and genPart.isLastCopy():
                has_bhad_daughter = any(is_bhad(daughter.pdgId()) for daughter in genPart.daughterRefVector())
                if not has_bhad_daughter:
                    Bhads.append(genPart)

        ### Matching between the reco jets and gen jets
        matched_gens = []
        good_jets = []

        # b_had_matched_jet_idx = [0]*len(Bhads)
        for j, jet in enumerate(jets):
            bestDR = 999
            bestGen = None
            for gen in gen_jets:
                dr = np.sqrt(VectorUtil.DeltaR2(jet.p4(), gen.p4()))
                if dr < bestDR:
                    bestDR = dr
                    bestGen = gen

            if bestGen and bestDR < 0.1: #
                # import pdb; pdb.set_trace()
                if debug_script:
                    print(" PFJet {j}: pt={jetpt:.1f}, eta={jeteta:.2f}, phi={jetphi:.2f} ".format(j=j, jetpt=jet.pt(), jeteta=jet.eta(), jetphi=jet.phi()) +
                        "--> matched GenJet pt={bestGenpt:.1f}, dR={bestDR:.3f}".format(bestGenpt=bestGen.pt(), bestDR=bestDR))

            elif debug_script:
                print(" PFJet {j}: pt={jetpt:.1f}, eta={jeteta:.2f}, phi={jetphi:.2f} "
                    "--> no match".format(j=j, jetpt=jet.pt(), jeteta=jet.eta(), jetphi=jet.phi()))

            ### b flavour tagging: dr matching with b hadrons
            matched_with_bhad = False
            for ii, bhad in enumerate(Bhads):
                dr = np.sqrt(VectorUtil.DeltaR2(jet.p4(), bhad.p4()))
                if dr<0.2:
                    # print("is b jet")
                    # if (b_had_matched_jet_idx[ii])>0:
                    #     print("Warning! The b hadron already matched to a jet")
                    # b_had_matched_jet_idx[ii] = j
                    matched_with_bhad = True
                    break
            if matched_with_bhad and bestGen is not None:   
                matched_gens.append(bestGen)
                good_jets.append(jet)
        # print(len(B2stars), " B2* hadrons found in the event ")
        # print(len(Bhads), " B hadrons found in the event ")
        # print(len(good_jets), " b jets found in the event ")

        # goodbhads = []
        # B2_star_pts = []
        # B2_star_fracs = []
        Nmatched_hads = 0
        for jet, genJet in zip(good_jets, matched_gens):
            # print("jet pt = ", jet.pt(), "genJet pt = ", genJet.pt())
            B2_star_pt = 0
            # if len(B2stars)==0:
            #     # B2_star_pts.append(B2_star_pt)
            #     continue
            # for genPart in B2stars:
            had_pt_sums = {pdgid: 0 for pdgid in b_meson_types}
            for genPart in Bhads:
                # check if the b hadron comes from the high pt jet
                matches_with_jet = False
                if debug_script:
                    print("genPart phi = ", genPart.phi(), "genPart eta = ", genPart.eta(), "genPart pt = ", genPart.pt())
            
                ### we have to match all the b hadrons to the jet again to sum all all the b hadrons in the jet
                dr = np.sqrt(VectorUtil.DeltaR2(jet.p4(), genPart.p4()))
                if debug_script:
                    print("jet phi = ", jet.phi(), "jet eta = ", jet.eta(), "jet pt = ", jet.pt())
                    print("dr = ", dr  )
                if dr < 0.2:
                    matches_with_jet = True
                    pdgid = abs(genPart.pdgId())
                    if pdgid in had_pt_sums:
                        had_pt_sums[pdgid] += genPart.pt()
                    elif pdgid<600: 
                        print("Warning! pdgId ", pdgid, " not in the list of b mesons")
                    if is_B2_star(genPart.pdgId()):
                        B2_star_pt += genPart.pt()
                    if debug_jet_matching:
                        if abs(jet.partonFlavour()) == 5:
                            print("The given b hadron correctly matches with a high pt b jet")
                            Nmatched_hads += 1
                            # high_pt_jets.remove(jet)
                        else:
                            print("The given b hadron matches to a jet that is not a b jet")
                    # matched_jet = jet
            # B2_star_pts.append(B2_star_pt)
            B2_star_pt_frac = B2_star_pt/genJet.pt()
            jet_energy_response = jet.pt() / genJet.pt()
            # print("pt_sums: ", had_pt_sums)
            # print("B2_star_pt:", B2_star_pt)
            for pdgid, pt_sum in had_pt_sums.items():
                pt_frac = pt_sum / genJet.pt()
                hist["pt_frac_"+str(pdgid)].Fill(pt_frac)
                hist["pt_frac_"+str(pdgid)+'_2d'].Fill(pt_frac, jet_energy_response)

            # B2_star_fracs.append(B2_star_pt/matched_jet.genJet().pt())
            # print("B2_star_pt_frac:", B2_star_pt_frac)
            hist["B2_star_frac"].Fill(B2_star_pt_frac)
            hist["jet_response"].Fill(jet_energy_response)
            # hist["B2_star_pt2d"].Fill(B2_star_pt_frac, jet_energy_response)

    return hist, num_events

inputfiles_Py = {"HT1000to1500": txt2filesls('QCD_Py_1000to1500.txt', Nfiles=-1),
                 "HT1500to2000": txt2filesls('QCD_Py_1500to2000.txt', Nfiles=-1),
                 "HT2000toInf":  txt2filesls('QCD_Py_2000toInf.txt', Nfiles=-1)
                  }

inputfiles_Her = {"HT1000to1500": txt2filesls('QCD_Her_1000to1500.txt', Nfiles=-1),
                  "HT1500to2000": txt2filesls('QCD_Her_1500to2000.txt', Nfiles=-1),
                  "HT2000toInf":  txt2filesls('QCD_Her_2000toInf.txt', Nfiles=-1)
                  }
xsec_Py = {"HT1000to1500": 1118.0,
            "HT1500to2000": 109.8,
            "HT2000toInf": 21.93}

xsec_Her = {"HT1000to1500": 1118.0*1.1,
            "HT1500to2000": 109.8*1.15,
            "HT2000toInf": 21.93*1.2}


def run_B2_star_distr(inputfile, sample, HT_bin, out_dir='res_B2_star', id='0'):
    #    hist{"B2_star_frac"}: pt fraction of the B2* hadron in the jet
    #hist{"jet response"}: jet energy response
    #hist{"B2_star_pt2d"}: 2d histogram of B2* pt vs jet energy response
    hist = {}
    hist['B2_star_frac'] = ROOT.TH1F('B2_star_frac'+'_'+HT_bin+'_'+sample, ';pt fraction of B_2^* hadron;number of gen particles', 25, 0, 1)
    hist['jet_response'] = ROOT.TH1F('jet_response'+'_'+HT_bin+'_'+sample, ';jet response; number of gen particles', 30, 0, 2.1)
    hist['B2_star_pt2d'] = ROOT.TH2F('B2_star_pt2d'+'_'+HT_bin+'_'+sample, 'B2* pt vs Jet Energy Response', 25, 0, 1, 30, 0, 2.1)

    for pdgid in b_meson_types:
        hist["pt_frac_"+str(pdgid)] = ROOT.TH1F("bhad_ptfrac_{}".format(pdgid), ";pt fraction for bhadron {};N".format(pdgid), 25, 0, 1)
        hist["pt_frac_"+str(pdgid)+'_2d'] = ROOT.TH2F("bhad_ptfrac_2d_{}".format(pdgid), ";pt fraction;jet energy response", 25, 0, 1, 30, 0, 2.1)

    xrootdstr='root://xrootd-cms.infn.it/'
    inputfile = xrootdstr + inputfile
    print("loading file: ", inputfile) 
    events = Events(inputfile)
    hist, num_events = get_displacement(events, hist, debug_script=False)
    tot_events = num_events

    if sample == 'Py':
        xsec = xsec_Py
    elif sample == 'Her':
        xsec = xsec_Her
    scale_factor = xsec['HT'+HT_bin] / tot_events
    for key in hist:
        hist[key].Scale(scale_factor)
    vals = []
    errs = []
    for i in range(0, hist['pt_frac_525'].GetNbinsX() + 2):
        vals.append(hist['pt_frac_525'].GetBinContent(i))
        errs.append(hist['pt_frac_525'].GetBinError(i))
    print("vals = ", vals)
    print("errs = ", errs)

    for key in hist:
        file = ROOT.TFile(out_dir+"/"+key+'_'+HT_bin+'_'+id+".root", "RECREATE")
        hii = hist[key]
        # if "_2d" in key:
        #     ### normalize the columns to 1 ### TODO: disable later when runing over condor
        #     for binx in range(1, hii.GetNbinsX()+1):
        #         column_sum = 0
        #         for biny in range(1, hii.GetNbinsY()+1):
        #             column_sum += hii.GetBinContent(binx, biny)
        #         if column_sum > 0:
        #             for biny in range(1, hii.GetNbinsY()+1):
        #                 hii.SetBinContent(binx, biny, hii.GetBinContent(binx, biny) / column_sum)
        # hist[key].Sumw2()
        hii.Write()
        file.Close()
        print("Written to file: ", out_dir+"/"+key+'_'+HT_bin+'_'+id+".root")


    # file = ROOT.TFile(out_dir+"/B2_star_frac"+'_'+HT_bin+'_'+id+".root", "RECREATE")
    # hist["B2_star_frac"].Write()
    # file.Close()
    # print("Written to file: ", out_dir+"/B2_star_frac"+'_'+HT_bin+'_'+id+".root")

    # file = ROOT.TFile(out_dir+"/B2_star_pt2d"+'_'+HT_bin+'_'+id+".root", "RECREATE")
    # hist["B2_star_pt2d"].Write()
    # file.Close()
    # print("Written to file: ", out_dir+"/B2_star_pt2d"+'_'+HT_bin+'_'+id+".root")

    # file = ROOT.TFile(out_dir+"/jet_response"+'_'+HT_bin+'_'+id+".root", "RECREATE")
    # hist["jet_response"].Write()
    # file.Close()
    # print("Written to file: ", out_dir+"/jet_response"+'_'+HT_bin+'_'+id+".root")



import optparse
def main():
    ### TODO: update all to AOD
    parser = optparse.OptionParser()
    parser.add_option('-b', '--bins', dest='bins', default="2000toInf", help='bins to run')
    parser.add_option('-o', '--out_dir', dest='out_dir', default=None, help='output directory')
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
    if out_dir is None:
        out_dir = 'res_bhad_frac/'+sample 

    if infile is None:
        infile = txt2filesls('QCD_{}_{}_AOD.txt'.format(sample, run_bins[0]), Nfiles=1, xrootdstr='')[0]

    # infile = '/store/mc/RunIISummer20UL18RECO/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v2/2520000/0184321F-08CA-3740-9700-89D3C169F771.root'
    # sample = 'Py'

    # infile = '/store/mc/RunIISummer20UL18RECO/QCD_HT2000toInf_TuneCH3_13TeV-madgraphMLM-herwig7/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v2/2520000/05F67E83-EEF6-7345-9C0C-1C3F39F71840.root'
    # sample = 'Her'
        # run_displacement(run_bins, out_dir)
    print("run_bins = ", run_bins)
    print("out_dir = ", out_dir)
    print("infile = ", infile)
    print("sample = ", sample)
    print("id = ", id)
    # run_displacement(run_bins, out_dir)

    run_B2_star_distr(infile, sample, run_bins[0], out_dir=out_dir, id=id)

if __name__ == "__main__":
    sys.exit(main())