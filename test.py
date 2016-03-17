#! /usr/bin/env python

import os,sys
from ROOT import RooRealVar, RooArgSet, RooLinkedList,RooFit
from ROOT import TCanvas, TAxis, TH1F, TFile, gPad
from ROOT import RooGaussian
from ROOT import *

def main():
    # Mjj0 of TT MC Bkg
    f1 = TFile("Merged_TT_TuneCUETP8M1_13TeV-powheg-pythia8-runallAnalysis.root")
    h_Mjj = f1.Get("histfacFatJet_ZLight/h_Mjj0")
    h_Mjj.GetXaxis().SetRangeUser(0,300)
    var_mean = h_Mjj.GetMean()

    # Build Gaussian PDF
    x     = RooRealVar(  'x',     'x',                0, 300 )
    mean  = RooRealVar(  'mean',  'mean of gaussian', var_mean )
    sigma = RooRealVar(  'sigma', 'width of gaussian', 5)
    gauss = RooGaussian( 'gauss', 'gaussian PDF', x, mean, sigma)
    data  = RooDataHist("data","Mjj dataset",RooArgList(x), h_Mjj);
    
    # Plot PDF
    xframe = x.frame(RooFit.Title("Gaussian p.d.f."))
    gauss.plotOn( xframe )
    gauss.plotOn(xframe,RooFit.LineColor(2)) 
    
    # Generate a toy MC set
    # data = gauss.generate( RooArgSet(x), 10000 )
    # Plot PDF and toy data overlaid
    xframe2 = x.frame(RooFit.Title("Gaussian p.d.f. with Mjj"))
    # data.plotOn( xframe2, RooLinkedList() )
    # data.plotOn( xframe2 )
    data.plotOn( xframe2 )
    gauss.plotOn( xframe2)
    # Fit PDF to toy
    mean.setConstant( kFALSE )
    sigma.setConstant( kFALSE )
    gauss.fitTo(data)
    
    c1 = TCanvas("c1","Example",800,400)
    c1.Divide(3)
    c1.cd(1)
    gPad.SetLeftMargin(0.15)
    xframe.GetYaxis().SetTitleOffset(1.6)
    xframe.Draw()
    
    c1.cd(2)
    gPad.SetLeftMargin(0.15)
    xframe2.GetYaxis().SetTitleOffset(1.6)
    xframe2.Draw() 

    c1.SaveAs('testMjj0.png')
    
    # # Print final value of parameters
    fout = TFile("output.root","recreate")
    c1.Write()
    fout.Close()

try:
    main()
except KeyboardInterrupt:
    print
    print "ciao!"
    print    
    