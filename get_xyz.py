#! /usr/bin/env python

import ROOT
import sys
from os import path
from DataFormats.FWLite import Events, Handle
import numpy as np
import cmsstyle as CMS
import os


def Plot(square, iPos, hist1, hist2, outputPath="./pdfs"):
    # canv_name = f'example_{"square" if square else "rectangle"}_pos{iPos}'
    canv_name = 'lifetime'
    CMS.SetLumi("138")
    CMS.SetEnergy("13")
    # Write extra lines below the extra text (usuful to define regions/channels)
    CMS.ResetAdditionalInfo()
    CMS.AppendAdditionalInfo("Signal region")
    CMS.AppendAdditionalInfo("#mu-channel")

    canv = CMS.cmsCanvas(
        canv_name,
        0,
        90,
        1e-3,
        2,
        "X",
        "A.U.",
        square=square,
        extraSpace=0.01,
        iPos=iPos,
    )
    canv.SetLogy(True)
    leg = CMS.cmsLeg(0.60, 0.89 - 0.04 * 4, 0.89, 0.89, textSize=0.04)

    # Draw objects in one line
    CMS.cmsDraw(hist1, "hist", fcolor=ROOT.kAzure + 2, alpha=0.5)
    print(hist1)
    print(hist2)
    CMS.cmsDraw(hist2, "hist", fcolor=ROOT.kRed + 1, alpha=0.5)
    # CMS.cmsDraw(self.data, "P", mcolor=ROOT.kBlack)

    leg.AddEntry(hist1, "MG+Py8", "lp")
    leg.AddEntry(hist2, "MG+Her7", "f")
    # leg.AddEntry(self.signal, "Signal", "f")

    # Takes care of fixing overlay and closing object
    CMS.SaveCanvas(canv, os.path.join(outputPath, canv_name + ".pdf"))
    CMS.SaveCanvas(canv, os.path.join(outputPath, canv_name + ".png"))

    canv_name += "_ratio"
    dicanv = CMS.cmsDiCanvas(
        canv_name,
        10,
        90,
        0,
        0.2,
        0.0,
        2.0,
        "X",
        "A.U.",
        "Data/Pred.",
        square=square,
        extraSpace=0.1,
        iPos=iPos,
    )
    dicanv.cd(1)

    leg = CMS.cmsLeg(0.60, 0.89 - 0.05 * 5, 0.89, 0.89, textSize=0.05)
    leg.AddEntry(hist1, "MG+Py8", "lp")
    leg.AddEntry(hist2, "MG+Her7", "f")
    # leg.AddEntry(self.signal, "Signal", "f")

    CMS.cmsHeader(leg, "With title", textSize=0.05)

    CMS.cmsDraw(hist1, "hist", fcolor=ROOT.kRed + 1, alpha=0.5)
    CMS.cmsDraw(hist2, "hist", fcolor=ROOT.kAzure + 2, alpha=0.9)
    # CMS.cmsDraw(self.data, "P", mcolor=ROOT.kBlack)

    CMS.fixOverlay()

    dicanv.cd(2)
    leg_ratio = CMS.cmsLeg(
        0.17, 0.97 - 0.05 * 5, 0.35, 0.97, textSize=0.05, columns=2
    )
    # how alternative way to pass style options
    style = {"style": "hist", "lcolor": ROOT.kAzure + 2, "lwidth": 2, "fstyle": 0}

    ratio = hist1.Clone("ratio")
    ratio_nosignal = hist1.Clone("ratio_nosignal")

    # self.ratio.Divide(self.bkg_tot)
    # self.ratio_nosignal.Divide(self.bkg)

    CMS.cmsDraw(ratio_nosignal, **style)
    CMS.cmsDraw(ratio, "P", mcolor=ROOT.kBlack)

    leg_ratio.AddEntry(ratio, "Bkg", "lp")
    leg_ratio.AddEntry(ratio_nosignal, "Bkg+Signal", "l")

    ref_line = ROOT.TLine(10, 1, 90, 1)
    CMS.cmsDrawLine(ref_line, lcolor=ROOT.kBlack, lstyle=ROOT.kDotted)

    CMS.SaveCanvas(dicanv, os.path.join(outputPath, canv_name + ".pdf"))

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
handle = Handle('vector<reco::GenParticle>')
# handle = Handle('float')
# handle = Handle('vector<pat::Muon>')
label = 'prunedGenParticles'
# label = 'slimmedMuons'
# label = 'genParticles'

def get_lifetime(events, handle, label):
    hist = ROOT.TH1F('lambda', ';displacement cm;number of gen particles', 50, 3, 5)
    hist2 = ROOT.TH1F('lambda2', ';displacement cm;number of gen particles', 30, 0.1, 2.1)

    for event in events:
        # print("Event Nr = ", event.eventAuxiliary().event() )
        event.getByLabel(label, handle)
        genParts = handle.product()
        #import pdb; pdb.set_trace()
        
        

        for idx in range(genParts.size()):
            depths = [] # use depths.append(x) to add an item to the list
            
            genPart = genParts[idx]
            # genPart.Print()
            vertex = genPart.vertex()
            x = vertex.x()
            y = vertex.y()
            z = vertex.z()
            r = vertex.r()
            # r = dir(genParts)

            # if np.abs(genPart.pdgId())==5:
                # print("idx = ", idx, "pdgId = ", genPart.pdgId(), "status = ", genPart.status(), "x = ", np.round(x,6), "y = ", np.round(y,6), "z = ", np.round(z,6), "r = ", np.round(r,6), "isPromptDecayed", genPart.isPromptDecayed(), "isPromptFinalState", genPart.isPromptFinalState(), "isLastCopy = ", genPart.isLastCopy())
                # for daughter in genPart.daughterRefVector():
                #     print("daughter:     pdgId = ", daughter.pdgId(), "status = ", daughter.status(), "x = ", np.round(daughter.vertex().x(),6), "y = ", np.round(daughter.vertex().y(),6), "z = ", np.round(daughter.vertex().z(),6), "r = ", np.round(daughter.vertex().r(),6), "isPromptDecayed", daughter.isPromptDecayed(), "isPromptFinalState", daughter.isPromptFinalState(), "isLastCopy = ", daughter.isLastCopy())
                # for mother in genPart.motherRefVector():
                #     print("mother:       pdgId = ", mother.pdgId(), "status = ", mother.status(), "x = ", np.round(mother.vertex().x(),6), "y = ", np.round(mother.vertex().y(),6), "z = ", np.round(mother.vertex().z(),6), "r = ", np.round(mother.vertex().r(),6), "isPromptDecayed", mother.isPromptDecayed(), "isPromptFinalState", mother.isPromptFinalState(), "isLastCopy = ", mother.isLastCopy())

            if is_bhad(genPart.pdgId()) and genPart.isLastCopy():
                # print("idx = ", idx, "pdgId = ", genPart.pdgId(), "status = ", genPart.status(), "x = ", np.round(x,6), "y = ", np.round(y,6), "z = ", np.round(z,6), "r = ", np.round(r,6), "isPromptDecayed", genPart.isPromptDecayed(), "isPromptFinalState", genPart.isPromptFinalState(), "isLastCopy = ", genPart.isLastCopy())
                # for daughter in genPart.daughterRefVector():
                #     print("daughter:     pdgId = ", daughter.pdgId(), "status = ", daughter.status(), "x = ", np.round(daughter.vertex().x(),6), "y = ", np.round(daughter.vertex().y(),6), "z = ", np.round(daughter.vertex().z(),6), "r = ", np.round(daughter.vertex().r(),6), "isPromptDecayed", daughter.isPromptDecayed(), "isPromptFinalState", daughter.isPromptFinalState(), "isLastCopy = ", daughter.isLastCopy())
                # for mother in genPart.motherRefVector():
                #     print("mother:      pdgId = ", mother.pdgId(), "status = ", mother.status(), "x = ", np.round(mother.vertex().x(),6), "y = ", np.round(mother.vertex().y(),6), "z = ", np.round(mother.vertex().z(),6), "r = ", np.round(mother.vertex().r(),6), "isPromptDecayed", mother.isPromptDecayed(), "isPromptFinalState", mother.isPromptFinalState(), "isLastCopy = ", mother.isLastCopy())

                daughter = genPart.daughter(0)
                tof = np.abs(daughter.vertex().r()-r) /3 # in mus
                print("lifetime = ", tof)

            # print("r = ", r)
                hist.Fill(tof, 1)
                hist2.Fill(tof, 1)
    return hist, hist2

inputfile_Py = 'QCD_HT1000to1500_example.root'
inputfile_Her = 'QCD_HT1000to1500_Her_example.root'

hists1 = []
hists2 = []
for inputfile in [inputfile_Py, inputfile_Her]:

    if not path.exists(inputfile):
        print('No input file found!')

    print("loading file: ", inputfile) 
    events = Events(inputfile)
    hist, hist2 = get_lifetime(events, handle, label)
    hists1.append(hist)
    hists2.append(hist2)

Plot(square=CMS.kSquare, iPos=0, hist1=hists1[0], hist2=hists1[1], outputPath="./pdfs")

# ROOT.gStyle.SetOptFit(1)
# c = ROOT.TCanvas('c', 'c', 500, 450)
# c.cd()
# hists1[0].Draw()
# # hists1[0].Fit('expo')
# hists1[1].Draw('same')
# hists1[1].SetLineColor(2)
# # hists1[1].Fit('expo')
# # pdb.set_trace()
# # fit_function = hists1[1].GetFunction('expo')
# # fit_function.SetLineColor(ROOT.kBlue)

# # Create a legend
# legend = ROOT.TLegend(0.1, 0.7, 0.3, 0.9)
# legend.AddEntry(hists1[0], "Py8", "l")
# legend.AddEntry(hists1[1], "Her7", "l")
# legend.Draw()

# c.Print('lifetime.pdf')

# c = ROOT.TCanvas('c', 'c', 500, 450)
# c.cd()
# hists2[0].Draw()
# hists2[0].Fit('expo')
# hists2[1].Draw('same')
# hists2[1].SetLineColor(2)
# hists2[1].Fit('expo')
# fit_function = hists1[1].GetFunction('expo')
# fit_function.SetLineColor(ROOT.kBlue)
# c.Print('lifetime_zoom.pdf')