# cmsstyle requires centos7 with lch centos7, not cmssw
import ROOT
# import sys
# from os import path
import cmsstyle as CMS
import os

CMS.SetLumi("")
CMS.SetEnergy("13")
CMS.SetExtraText("Simulation Private Work")


def Plot(square, iPos, hist1, hist2, outputPath="./pdfs"):
    # canv_name = f'example_{"square" if square else "rectangle"}_pos{iPos}'
    canv_name = 'x_T'
    # Write extra lines below the extra text (usuful to define regions/channels)
    # CMS.ResetAdditionalInfo()
    # CMS.AppendAdditionalInfo("Signal region")
    # CMS.AppendAdditionalInfo("#mu-channel")

    # Add overflow to the last bin
    nbins = hist1.GetNbinsX()
    for ii in range(0, nbins + 2):
        print("bin content: ", hist1.GetBinContent(ii))

    # Add overflow to the last bin
    nbins = hist2.GetNbinsX()
    for ii in range(0, nbins + 2):
        print("bin content: ", hist2.GetBinContent(ii))
    # Calculate the bin width. This assumes all bins have the same width.
    # bin_width = hist1.GetXaxis().GetBinWidth(1)
    # hist2.Scale(0.9)
    # Scale the histograms by the bin width.
    for i in range(1, hist1.GetNbinsX() + 1):
        bin_content = hist1.GetBinContent(i)
        bin_width = hist1.GetBinWidth(i)
        hist1.SetBinContent(i, bin_content / bin_width)

    for i in range(1, hist2.GetNbinsX() + 1):
        bin_content = hist2.GetBinContent(i)
        bin_width = hist2.GetBinWidth(i)
        hist2.SetBinContent(i, bin_content / bin_width)


    # Get the minimum and maximum y values
    y_min = min(hist1.GetMinimum(), hist2.GetMinimum())*0.85
    y_max = max(hist1.GetMaximum(), hist2.GetMaximum())*1.1

    # Get the minimum and maximum x values
    x_min = min(hist1.GetXaxis().GetXmin(), hist2.GetXaxis().GetXmin())
    x_max = max(hist1.GetXaxis().GetXmax(), hist2.GetXaxis().GetXmax())

    canv = CMS.cmsCanvas(
        canv_name,
        x_min,
        x_max,
        y_min,
        y_max,
        "transverse displacement, x_{T} [cm]",
        "dN/dx_{T}",
        square=square,
        extraSpace=0.01,
        iPos=iPos,
    )
    canv.SetLogy(True)
    leg = CMS.cmsLeg(0.60, 0.89 - 0.04 * 4, 0.89, 0.89, textSize=0.04)

    # Draw objects in one line
    CMS.cmsDraw(hist1, "histE", lcolor=ROOT.kAzure + 2, alpha=0.5, lwidth=2, fstyle=0)
    # CMS.cmsDraw(hist1, "P", fcolor=ROOT.kAzure + 2, alpha=0.5)
    # print(hist1)
    # print(hist2)
    CMS.cmsDraw(hist2, "histE", lcolor=ROOT.kRed + 1, alpha=0.5, lwidth=2, fstyle=0)
    # CMS.cmsDraw(hist2, "P", fcolor=ROOT.kRed + 1, alpha=0.5)

    # CMS.cmsDraw(hist1, "P", mcolor=ROOT.kBlack)

    leg.AddEntry(hist1, "MG+Py8", "f")
    leg.AddEntry(hist2, "MG+Her7", "f")
    # leg.AddEntry(self.signal, "Signal", "f")

    # Takes care of fixing overlay and closing object
    canv.SaveAs(outputPath+'/'+canv_name + ".png")
    CMS.SaveCanvas(canv, os.path.join(outputPath, canv_name + ".pdf"))
    # CMS.SaveCanvas(canv, os.path.join(outputPath, canv_name + ".png"))

    canv_name += "_ratio"
    dicanv = CMS.cmsDiCanvas(
        canv_name,
        x_min,
        x_max,
        y_min,
        y_max,
        0.75,
        1.25,
        "transverse displacement, x_{T} [cm]",
        "dN/dx",
        "#frac{MG+Py8}{MG+Her7}",
        square=square,
        extraSpace=0.09,
        extraLeftMult=1.09,
        iPos=iPos,
    )
    # import pdb; pdb.set_trace()
    # print("LeftMargin = ", dicanv.GetLeftMargin())
    dicanv.cd(1)

    leg = CMS.cmsLeg(0.60, 0.89 - 0.05 * 5, 0.89, 0.89, textSize=0.05)
    leg.AddEntry(hist1, "MG+Py8", "f")
    leg.AddEntry(hist2, "MG+Her7", "f")
    # leg.AddEntry(self.signal, "Signal", "f")

    # CMS.cmsHeader(leg, "With title", textSize=0.05)

    # Draw objects in one line
    CMS.cmsDraw(hist1, "histE", lcolor=ROOT.kAzure + 2, alpha=0.5, lwidth=2, fstyle=0)
    # CMS.cmsDraw(hist1, "P", fcolor=ROOT.kAzure + 2, alpha=0.5)
    CMS.cmsDraw(hist2, "histE", lcolor=ROOT.kRed + 1, alpha=0.5, lwidth=2, fstyle=0)
    # CMS.cmsDraw(hist2, "P", fcolor=ROOT.kRed + 1, alpha=0.5)
    CMS.fixOverlay()

    dicanv.cd(2)
    # leg_ratio = CMS.cmsLeg(
        # 0.17, 0.97 - 0.05 * 5, 0.35, 0.97, textSize=0.05, columns=2
    # )
    # how alternative way to pass style options
    # style = {"style": "hist", "lcolor": ROOT.kAzure + 2, "lwidth": 2, "fstyle": 0, "alpha":0.5}

    ratio = hist1.Clone("ratio")
    ratio_nosignal = hist2.Clone("ratio_nosignal")

    ratio.Divide(ratio_nosignal)
    ratio_nosignal.Divide(ratio_nosignal)

    # # Add overflow to the last bin
    # nbins = ratio.GetNbinsX()
    # ratio.SetBinContent(nbins, ratio.GetBinContent(nbins) + ratio.GetBinContent(nbins + 1))

    # nbins = ratio_nosignal.GetNbinsX()
    # ratio_nosignal.SetBinContent(nbins, ratio_nosignal.GetBinContent(nbins) + ratio_nosignal.GetBinContent(nbins + 1))

    # self.ratio_nosignal.Divide(self.bkg)
    # CMS.cmsDraw(ratio_nosignal, "hist", fcolor=ROOT.kRed + 1, alpha=0.5)
    # CMS.cmsDraw(ratio, "hist", mcolor=ROOT.kAzure+2, alpha=0.5)
    # CMS.cmsDraw(ratio_nosignal, "P", fcolor=ROOT.kRed + 1, alpha=0.5)
    # CMS.cmsDraw(ratio, "P", mcolor=ROOT.kAzure+2, alpha=0.5)
    # CMS.cmsDraw(ratio_nosignal, "histE", fcolor=ROOT.kAzure + 2, alpha=0.5, lwidth=2, fstyle=0)
    CMS.cmsDraw(ratio_nosignal, "histE", lcolor=ROOT.kRed + 1, alpha=0.5, lwidth=2, fstyle=0)
    CMS.cmsDraw(ratio, "histE", lcolor=ROOT.kAzure + 2, alpha=0.5, lwidth=2, fstyle=0)
    # CMS.cmsDraw(ratio, "P")
    # # Store the color attributes
    # lcolor1 = hist1.GetLineColor()
    # lcolor2 = hist2.GetLineColor()
    # lcolor3 = ratio.GetLineColor()
    # lcolor4 = ratio_nosignal.GetLineColor()
    # # Reapply the color attributes
    # # ratio.SetLineColor(lcolor1)
    # # ratio_nosignal.SetLineColor(lcolor2)
    # print("lcolor1 = ", lcolor1, " lcolor2 = ", lcolor2, " lcolor3 = ", lcolor3, " lcolor4 = ", lcolor4)

    # leg_ratio.AddEntry(ratio, "MG+Py8", "f")
    # leg_ratio.AddEntry(ratio_nosignal, "MG+Her7", "f")

    ref_line = ROOT.TLine(x_min, 1, x_max, 1)
    CMS.cmsDrawLine(ref_line, lcolor=ROOT.kBlack, lstyle=ROOT.kDotted)

    dicanv.SaveAs(outputPath+'/'+canv_name + ".png")
    CMS.SaveCanvas(dicanv, os.path.join(outputPath, canv_name + ".pdf"))

def Plot2D(square, iPos, hist, samp, outputPath="./pdfs"):
    # canv_name = f'example_2D_{"square" if square else "rectangle"}_pos{iPos}'
    canv_name = 'x_T_response_2D'+'_'+samp
    # Allow to reduce the size of the lumi info 
    hist.QuantilesY()
    scaleLumi = 0.80 if square else None
    canv = CMS.cmsCanvas(
        canv_name,
        0,
        20,
        0,
        2,
        "transverse displacement, x_{T} [cm]",
        "response, R, of the matched jet", # = #frac{#p_{T, ptcl}}{#p_{T,gen}}",
        square=square,
        extraSpace=0.02,
        iPos=iPos,
        with_z_axis=True,
        scaleLumi=scaleLumi,
    )
    for binx in range(1, hist.GetNbinsX()+1):
        column_sum = 0
        for biny in range(1, hist.GetNbinsY()+1):
            column_sum += hist.GetBinContent(binx, biny)
        if column_sum > 0:
            for biny in range(1, hist.GetNbinsY()+1):
                hist.SetBinContent(binx, biny, hist.GetBinContent(binx, biny) / column_sum)

    hist.GetZaxis().SetTitle("Events normalised per column")
    hist.GetZaxis().SetTitleOffset(1.4 if square else 1.2)
    hist.Draw("same colz")
    CMS.ResetAdditionalInfo()
    add_text = "MG+Py8" if samp == "Py" else "MG+Her7"
    CMS.AppendAdditionalInfo(add_text)
    CMS.AppendAdditionalInfo("blah")
    # Set a new palette
    CMS.SetAlternative2DColor(hist, CMS.cmsStyle)

    # Allow to adjust palette position
    CMS.UpdatePalettePosition(hist, canv)

    canv.SaveAs(outputPath+'/'+canv_name + ".png")
    CMS.SaveCanvas(canv, os.path.join(outputPath, canv_name + ".pdf"))

def Plot_median_respponse(square, iPos, hist1, hist2, median1, median2, outputPath="./pdfs"):
    # canv_name = f'example_{"square" if square else "rectangle"}_pos{iPos}'
    canv_name = 'response_vs_xT'

    nbins = hist1.GetNbinsX()
    for ii in range(0, nbins + 2):
        print("bin content: ", hist1.GetBinContent(ii))

    # Add overflow to the last bin
    nbins = hist2.GetNbinsX()
    for ii in range(0, nbins + 2):
        print("bin content: ", hist2.GetBinContent(ii))



    # Get the minimum and maximum y values
    y_min = min(hist1.GetMinimum(), hist2.GetMinimum())*0.983
    y_max = max(hist1.GetMaximum(), hist2.GetMaximum())*1.036

    # Get the minimum and maximum x values
    x_min = min(hist1.GetXaxis().GetXmin(), hist2.GetXaxis().GetXmin())
    x_max = max(hist1.GetXaxis().GetXmax(), hist2.GetXaxis().GetXmax())

    canv_name += "_ratio"
    dicanv = CMS.cmsDiCanvas(
        canv_name,
        x_min,
        x_max,
        y_min,
        y_max,
        0.9,
        1.1,
        "transverse displacement, x_{T} [cm]",
        "median response",
        "#frac{MG+Py8}{MG+Her7}",
        square=square,
        extraSpace=0.17,
        extraLeftMult=1.23,
        iPos=iPos,
    )
    dicanv.cd(1)

    leg = CMS.cmsLeg(0.34, 0.82 - 0.05 * 2, 0.59, 0.82, textSize=0.05)
    leg.AddEntry(hist1, "MG+Py8", "pE")
    leg.AddEntry(hist2, "MG+Her7", "pE")

    # Draw objects in one line
    CMS.cmsDraw(hist1, "P", mcolor=ROOT.kAzure + 2)
    CMS.cmsDraw(hist2, "P", mcolor=ROOT.kRed + 1)

    line1 = ROOT.TLine(hist1.GetXaxis().GetXmin(), median1, hist1.GetXaxis().GetXmax(), median1)
    CMS.cmsDrawLine(line1, lcolor=ROOT.kAzure + 2, lstyle=2)

    # line1.SetLineColor(ROOT.kAzure + 2)
    # line1.Draw()

    line2 = ROOT.TLine(hist2.GetXaxis().GetXmin(), median2, hist2.GetXaxis().GetXmax(), median2)
    CMS.cmsDrawLine(line2, lcolor=ROOT.kRed + 1, lstyle=2)
    # line2.Draw()

    # Draw a gray, dashed line at y=1
    line3 = ROOT.TLine(hist1.GetXaxis().GetXmin(), 1, hist1.GetXaxis().GetXmax(), 1)
    CMS.cmsDrawLine(line3, lcolor=ROOT.kBlack, lstyle=ROOT.kDotted)
    # line3.SetLineColor(ROOT.kGray)
    # line3.SetLineStyle(2)  # 2 is the style for dashed lines
    # line3.Draw()

    # New legend for the median lines
    leg2 = CMS.cmsLeg(0.60, 0.82 - 0.05 * 2, 0.99, 0.82, textSize=0.05)
    leg2.AddEntry(line1, "Median all bins", "l")
    leg2.AddEntry(line2, "Median all bins", "l")

    leg3 = CMS.cmsLeg(0.20, 0.84, 0.29, 0.89, textSize=0.05)
    leg3.AddEntry(None, "750 < p_{T, reco} < 1000 GeV, b jets", "")
    CMS.fixOverlay()

    dicanv.cd(2)

    ratio = hist1.Clone("ratio")
    ratio_nosignal = hist2.Clone("ratio_nosignal")

    ratio.Divide(ratio_nosignal)
    ratio_nosignal.Divide(ratio_nosignal)

    CMS.cmsDraw(ratio_nosignal, "P", mcolor=ROOT.kRed + 1)
    CMS.cmsDraw(ratio, "P", mcolor=ROOT.kAzure + 2)

    ref_line = ROOT.TLine(x_min, 1, x_max, 1)
    CMS.cmsDrawLine(ref_line, lcolor=ROOT.kBlack, lstyle=ROOT.kDotted)

    dicanv.SaveAs(outputPath+'/'+canv_name + ".png")
    CMS.SaveCanvas(dicanv, os.path.join(outputPath, canv_name + ".pdf"))

# # file = ROOT.TFile("res/histograms1HT2000toInf.root")
# HT_bin = '2000toInf'
# import glob
# filesPy = glob.glob("res/Py/{}/histograms1_{}_*.root".format(HT_bin, HT_bin))
# NfilesPy = len(filesPy)
# filesHer = glob.glob("res/Her/{}/histograms1_{}_*.root".format(HT_bin, HT_bin))
# NfilesHer = len(filesHer)
# print("NfilesPy = ", NfilesPy, " NfilesHer = ", NfilesHer)

# file = ROOT.TFile("res/Her/{}/histograms1_{}.root".format(HT_bin, HT_bin))
# hists_Her = file.Get("lambda_tmp_{}_Her".format(HT_bin))
# # import pdb; pdb.set_trace()
# hists_Her.Scale(0.96/NfilesHer)


# file2 = ROOT.TFile("res/Py/{}/histograms1_{}.root".format(HT_bin, HT_bin))
# hists_Py = file2.Get("lambda_tmp_{}_Py".format(HT_bin))
# hists_Py.Scale(1./NfilesPy)

# file3 = ROOT.TFile("res/Py/{}/histograms3_{}.root".format(HT_bin, HT_bin))
# hists3_Py = file3.Get("x_vs_R_{}_Py".format(HT_bin))
# # hists3_Py.Scale(1./NfilesPy)
# file4 = ROOT.TFile("res/Her/{}/histograms3_{}.root".format(HT_bin, HT_bin))
# hists3_Her = file4.Get("x_vs_R_{}_Her".format(HT_bin))

HT_bin = '2000toInf'
import glob
filesPy = glob.glob("res/Py/{}/histograms4_{}_*.root".format(HT_bin, HT_bin))
NfilesPy = len(filesPy)
filesHer = glob.glob("res/Her/{}/histograms4_{}_*.root".format(HT_bin, HT_bin))
NfilesHer = len(filesHer)
print("NfilesPy = ", NfilesPy, " NfilesHer = ", NfilesHer)

file = ROOT.TFile("res/Her/{}/histograms4_{}.root".format(HT_bin, HT_bin))
hists_Her = file.Get("xT_tmp_{}_Her".format(HT_bin))
# import pdb; pdb.set_trace()
hists_Her.Scale(1./hists_Her.Integral())
# hists_Her.Scale(0.96/NfilesHer)


file2 = ROOT.TFile("res/Py/{}/histograms4_{}.root".format(HT_bin, HT_bin))
hists_Py = file2.Get("xT_tmp_{}_Py".format(HT_bin))
# hists_Py.Scale(1./NfilesPy)
hists_Py.Scale(1./hists_Py.Integral())

file3 = ROOT.TFile("res/Py/{}/histograms5_{}.root".format(HT_bin, HT_bin))
hists3_Py = file3.Get("xT_vs_R_{}_Py".format(HT_bin))
# hists3_Py.Scale(1./NfilesPy)
file4 = ROOT.TFile("res/Her/{}/histograms5_{}.root".format(HT_bin, HT_bin))
hists3_Her = file4.Get("xT_vs_R_{}_Her".format(HT_bin))
# hists3_Her.Scale(1./NfilesHer)
# print("Read histos")

# import pdb ; pdb.set_trace()
median_Py = hists3_Py.QuantilesX()
median_Her = hists3_Her.QuantilesX()

hists3_Py_1D = hists3_Py.ProjectionY()
hists3_Her_1D = hists3_Her.ProjectionY()

import numpy as np
# nq = 1  # Number of quantiles to calculate
xq = np.array([0.5])  # The quantile to calculate (0.5 for the median)
median_Py_tot = np.zeros(1)  # Array to store the calculated quantiles
median_Her_tot = np.zeros(1)  # Array to store the calculated quantiles

hists3_Py_1D.GetQuantiles(1, median_Py_tot, xq)
hists3_Her_1D.GetQuantiles(1, median_Her_tot, xq)

median_Py_tot = median_Py_tot[0]
median_Her_tot = median_Her_tot[0]

print("median_Py_tot = ", median_Py_tot)
print("median_Her_tot = ", median_Her_tot)


Plot(square=CMS.kSquare, iPos=0, hist1=hists_Py, hist2=hists_Her, outputPath="./pdfs")
Plot2D(square=CMS.kSquare, iPos=0, hist=hists3_Py, samp='Py', outputPath="./pdfs")
Plot2D(square=CMS.kSquare, iPos=0, hist=hists3_Her, samp='Her', outputPath="./pdfs")
Plot_median_respponse(square=CMS.kSquare, iPos=0, hist1=median_Py, hist2=median_Her, median1=median_Py_tot, median2=median_Her_tot, outputPath="./pdfs")