#! /usr/bin/env python
#-------------------------------------------------------------
# File: roofit_ttbar.py
# Created: 16 March 2016 Kelly Tsai
#-------------------------------------------------------------  

import os,sys
from time import sleep
from math import *
from ROOT import *

def main():
    # make a workspace
    wspace = RooWorkspace('wspace')

    # The observable is x and lies in the range [0, 300]
    x     = RooRealVar(  'x',     'x',                0, 300 )
    f1 = TFile("Merged_TT_TuneCUETP8M1_13TeV-powheg-pythia8-runallAnalysis.root")
    h_Mjj = f1.Get("histfacFatJet_ZLight/h_Mjj0")
    h_data  = RooDataHist("Mjj","Mjj dataset",RooArgList(x), h_Mjj);

    # Create two Gaussian PDF
    mean1   = RooRealVar(  'mean1',  'mean of gaussian',90 ,80 ,110)
    mean2   = RooRealVar(  'mean2',  'mean of gaussian',170 ,150 ,220)
    sigma1 = RooRealVar(  'sigma1', 'width of gaussian', 17)
    sigma2 = RooRealVar(  'sigma2', 'width of gaussian', 14)
    gauss1 = RooGaussian( 'gauss1', 'gaussian PDF', x, mean1, sigma1)
    gauss2 = RooGaussian( 'gauss2', 'gaussian PDF', x, mean2, sigma2)
    frac   = RooRealVar("frac","fraction",0.5,0.,1.)
    model  = RooAddPdf("model","g1+g2",RooArgList(gauss1,gauss2),RooArgList(frac))

    #----------------------------------------------------
    # do a binned fit to h_data
    #----------------------------------------------------
    # import h_data and model into workspace
    getattr(wspace,'import')(h_data)
    getattr(wspace,'import')(model)

    #time module
    swatch = TStopwatch()
    swatch.Start()

    #the simpler interface "fitTo"
    model.fitTo(h_data,
                RooFit.Save(),
                RooFit.Extended(False))

    # plot
    c1 = TCanvas('fig_binnedFit', 'fit', 10, 10, 500, 500)
    xframe = wspace.var('x').frame()
    h_data.plotOn(xframe)
    model.plotOn(xframe)
    model.paramOn(xframe)
    xframe.Draw()

    print "real time: %10.3f s" % swatch.RealTime()
    
    fout = TFile("output.root","recreate")
    c1.Write()
    fout.Close()

try:
    main()
except KeyboardInterrupt:
    print
    print "python program"
    print