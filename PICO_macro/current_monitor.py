import ROOT
import os
from datetime import datetime
from array import array
from math import sqrt

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch()        # don't pop up canvases
ROOT.TH1.SetDefaultSumw2()
ROOT.TGaxis.SetMaxDigits(3)

path = '/eos/home-a/acagnott/GEMData/CERN_P5/'

#start = 90
n_run = 98

color = {'idrift': ROOT.kBlack,
         'ig1t': ROOT.kGreen,
         'ig1b':ROOT.kGreen+3,
         'ig2t': ROOT.kCyan,
         'ig2b':ROOT.kCyan+3,
         'ig3t': ROOT.kRed,
         'ig3b':ROOT.kRed+3,
}

def take_mean(run, y, x, ch):
    file = ROOT.TFile.Open(path+"PICO1_run"+run+"_skim.root", "READ")
    
    print "curr_"+ch+"_distr"
    tmp = file.Get("curr_"+ch+"_distr") #ch = ig1t
    print tmp
    tfitresult = tmp.Fit("gaus", "S")
    #print tfitresult.IsValid()
    if ((int(run)<8) and (ch=='ig1t')):
        print run, ch
        y.append(0)
        x.append(0)
    else:
        print('integral', tmp.Integral())
        y.append(tfitresult.Parameter(1))
        x.append(tfitresult.Parameter(2)/sqrt(tmp.Integral()))
    
    return

chs = ['idrift', 'ig1t', 'ig1b', 'ig2t', 'ig2b', 'ig3t', 'ig3b']
means = {ch: [] for ch in chs}
sigmas = {ch: [] for ch in chs}
graphs = {ch: ROOT.TGraphErrors() for ch in chs}

run_plotted = []
run_absent = []

for i in range(19, 31):
    #print int(str(i).zfill(4))
    if i == 86 or i ==87: continue
    for ch in chs:
        if os.path.exists(path+"PICO1_run"+str(i).zfill(4)+"_skim.root"):
            take_mean(str(i).zfill(4), means[ch], sigmas[ch], ch)
            run_plotted.append(i)
        else : 
            run_absent.append(i)

run_absent.append(86)
run_absent.append(87)
outfile = ROOT.TFile.Open("/eos/home-a/acagnott/GEM_plot/CERN_P5/means_graph.root", "RECREATE")


xpoints = [x for x in xrange(n_run+1) if x not in run_absent]#[x for x in xrange(100) if x != 50]]
xpoints = [x for x in xrange(n_run+1) if x in run_plotted]#[x for x in xrange(100) if x != 50]]
print xpoints

for ch in chs:
    graphs[ch] = ROOT.TGraphErrors(len(xpoints), array('f',xpoints),
                                   array('f',means[ch]),
                                   array('f', [0]*len(xpoints)),
                                   array('f',sigmas[ch]))
    graphs[ch].SetMarkerColor(color[ch])
    graphs[ch].SetMarkerStyle(20)
    graphs[ch].SetTitle(ch.upper()+" mean")
    graphs[ch].SetName(ch)
    graphs[ch].GetXaxis().SetTitle("#run")
    
    #n_bin = graphs[ch].GetXaxis().GetNbins()
    
    #r = int((graphs[ch].GetXaxis().GetXmax())/n_bin)
    
    
    '''j=0
    r = 0.5*(3)*0.7
    while j*r <= graphs[ch].GetXaxis().GetXmax():
        bin_index = graphs[ch].GetXaxis().FindBin(j*r)
        graphs[ch].GetXaxis().SetBinLabel(bin_index,"run"+str(j))
        j+=1
    '''
    #for i in range(1, n_run+1):
    #    graphs[ch].GetXaxis().SetBinLabel((i*2*r)-1, "run"+str(i)+":start and stop")

    #graphs[ch].GetXaxis().SetBinLabel(2, "run1:start and stop")
    graphs[ch].GetYaxis().SetTitle("current_{mean} (nA)")
    graphs[ch].GetXaxis().SetRangeUser(-0.5, n_run+1.5)
    graphs[ch].GetYaxis().SetRangeUser(-25, 25)
    graphs[ch].Write()

c1 = ROOT.TCanvas("all_graphs")
c1.Divide(2,4)
c1.cd(1)
graphs["idrift"].Draw()
c1.cd(3)
graphs["ig1t"].Draw()
c1.cd(4)
graphs["ig1b"].Draw()
c1.cd(5)
graphs["ig2t"].Draw()
c1.cd(6)
graphs["ig2b"].Draw()
c1.cd(7)
graphs["ig3t"].Draw()
c1.cd(8)
graphs["ig3b"].Draw()
c1.Write()
