import ROOT
from array import array
import numpy as np

ROOT.gStyle.SetOptStat(0)
ROOT.TH1.SetDefaultSumw2()
ROOT.TGaxis.SetMaxDigits(3)

colors = [ROOT.kBlue,
          ROOT.kBlack,
          ROOT.kRed,
          ROOT.kGreen+2,
          ROOT.kMagenta+2,
          ROOT.kAzure,
	  ROOT.kCyan]

def print_hist(plotpath, hist, name, option = "HIST", log = False, stack = False, title = ""):
    #ROOT.gROOT.SetBatch()        # don't pop up canvases
    if not(isinstance(hist, list)):
        c1 = ROOT.TCanvas(name, "c1", 50,50,700,600)
        hist.Draw(option)            
        if log:
            c1.SetLogy(1)
        c1.Print(plotpath + "/" + name + ".png")
        c1.Print(plotpath + "/" + name + ".root")
    elif isinstance(hist, list):
        c1 = ROOT.TCanvas(name, "c1", 50,50,700,600)
        if isinstance(hist[0], ROOT.TGraph) or isinstance(hist[0], ROOT.TGraphAsymmErrors):
            i = 0
            mg = ROOT.TMultiGraph('mg', hist[0].GetTitle()+';'+hist[0].GetXaxis().GetTitle()+';'+hist[0].GetYaxis().GetTitle())
            minima = []
            for h in hist:
                #h.SetLineColor(colors[i])
                mg.Add(h)
                minima.append(h.GetMinimum())
                i += 1
            mg.SetMinimum(min(minima))
            mg.Draw(option)
            #mg.Draw("AP")
            Low = hist[0].GetXaxis().GetBinLowEdge(1)
            Nbin = hist[0].GetXaxis().GetNbins()
            High = hist[0].GetXaxis().GetBinUpEdge(Nbin)
            mg.GetXaxis().Set(Nbin, Low, High)
            '''
            for i in range(hist[0].GetXaxis().GetNbins()):
                u = i + 1
                mg.GetXaxis().SetBinLabel(u, hist[0].GetXaxis().GetBinLabel(u))
            '''
        elif isinstance(hist[0], ROOT.TEfficiency):
            i = 0
            mg = ROOT.TMultiGraph('mg', hist[0].GetTitle()+';'+hist[0].CreateGraph().GetXaxis().GetTitle()+';'+hist[0].CreateGraph().GetYaxis().GetTitle())

            for h in hist:
                print( h)
                h.SetLineColor(colors[i])
                mg.Add(h.CreateGraph())
                i += 1
            mg.SetMaximum(1.1)
            mg.SetMinimum(0.001)
            mg.Draw(option)
            
        elif isinstance(hist[0], ROOT.TH1F):
            mg = ROOT.THStack()
            i = 0
            print(hist[0].GetTitle(), hist[0].GetXaxis().GetTitle(), hist[0].GetYaxis().GetTitle())
            for h in hist:
                #h.SetLineColor(colors[i])
                if stack:
                    #h.SetFillColor(colors[i])
                    mg.Add(h)
                    i += 1
                else:
                  for h in hist:
                    h.Draw(option+'SAME')
            mg.Draw(option)
            mg.GetXaxis().SetTitle(hist[0].GetXaxis().GetTitle())
            mg.GetYaxis().SetTitle(hist[0].GetYaxis().GetTitle())
            if title == "":
                mg.SetTitle(hist[0].GetTitle()) 
            else:
                mg.SetTitle(title)
        if log:
            c1.SetLogy(1)
        c1.Pad().Modified()
        c1.Pad().Update()
        c1.BuildLegend(0.7, 0.65, 0.95, 0.9)
        c1.Pad().Modified()
        c1.Pad().Update()
        
        c1.Print(plotpath + "/" + str(name) + '.png')
        c1.Print(plotpath + "/" + str(name) + '.root')

def save_hist(infile, plotpath, hist, option = "HIST"):
    fout = ROOT.TFile.Open(plotpath + "/" + infile +".root", "UPDATE")
    fout.cd()
    hist.Write()
    fout.Close()

def make_graph(entries, x_array, y_array, name, title, x_title, y_title, color, style = 20):
    graph = ROOT.TGraph(entries, x_array, y_array)
    graph.SetNameTitle(name, title)
    graph.GetXaxis().SetTitle(x_title)
    graph.GetYaxis().SetTitle(y_title)
    graph.SetMarkerColor(color)
    graph.SetMarkerStyle(style)
    return graph

def make_hist(tree, variable, title, nbins, xmin, xmax):
    histoname = variable
    th1f = ROOT.TH1F(histoname, title, nbins, xmin, xmax)
    tree.Project(histoname, variable)
    return th1f

def get_timepeak_arrays(peak_array, time_array, full_array):
    peak_to_draw = array('f', len(peak_array)*[0])
    time_to_draw = array('f', len(peak_array)*[0])
    for i in range(len(peak_array)):
        peak_to_draw[i] = full_array[peak_array[i]]
        time_to_draw[i] = time_array[peak_array[i]]
    return time_to_draw, peak_to_draw

def FFT(histo):
    #Compute the transform and look at the magnitude of the output
    hm = None #ROOT.TH1F("hm", "Magnitude of the 1st transform", histo.GetNbinsX()*2, 0, histo.GetNbinsX()*2-1)
    ROOT.TVirtualFFT.SetTransform(0)
    hm = histo.FFT(hm, "MAG M")
    hm.SetNameTitle("hm", "Magnitude of the 1st transform")
    hm.Scale(1/histo.GetNbinsX())

    #Look at the phase of the output
    hp = None #ROOT.TH1F("hp", "Phase of the 1st transform", histo.GetNbinsX()*2, 0, histo.GetNbinsX()*2-1)
    #ROOT.TVirtualFFT.SetTransform(0)
    hp = histo.FFT(hp, "PH M")
    hp.SetNameTitle("hp", "Phase of the 1st transform")

    #Look at the real part of the output
    hre = None #ROOT.TH1F("hre", "Real part of the 1st transform", histo.GetNbinsX()*2, 0, histo.GetNbinsX()*2-1)
    #ROOT.TVirtualFFT.SetTransform(0)
    hre = histo.FFT(hre, "RE M")
    hre.SetNameTitle("hre", "Real part of the 1st transform")

    #Look at the imaginary part of the output
    him = None #ROOT.TH1F("him", "Imaginary part of the 1st transform", histo.GetNbinsX()*2, 0, histo.GetNbinsX()*2-1)
    #ROOT.TVirtualFFT.SetTransform(0)
    him = histo.FFT(him, "IM M")
    him.SetNameTitle("him", "Imaginary part of the 1st transform")

    #Look at the DC component and the Nyquist harmonic:
    #re = array('f', [0])
    #im = array('f', [0])
    re = ROOT.Double(0)
    im = ROOT.Double(0)
    #That's the way to get the current transform object:
    fft = ROOT.TVirtualFFT.GetCurrentTransform()
    #Use the following method to get just one point of the output
    fft.GetPointComplex(0, re, im)
    print("1st transform: DC component: %f\n", re)
    fft.GetPointComplex(histo.GetNbinsX()/2+1, re, im)
    print("1st transform: Nyquist harmonic: %f\n", re)
    #Use the following method to get the full output:
    #re_full = []
    #im_full = []
    #fft.GetPointsComplex(re_full, im_full)
    return hm, hp, hre, him

def graphFFT(in_array):
    size = array('i', [0])
    size[0] = len(in_array)
    n = len(in_array)
    print n
    range_sec = float(n*4E-9) # in seconds
    points = []
    ps = []  #// until Nyquist
    m = 0
    m2 = 0
     
    #//double phase[n/2 + 1];  // until Nyquist
    for i in range(n):
        points.append(in_array[i])
        m += points[-1]
        m2 += points[-1]*points[-1]
     
    s2 = m2/n - m*m/n/n
     
    fft = ROOT.TVirtualFFT.FFT(1, size, "R2C")
    fft.SetPoints(in_array)
    fft.Transform()

    real = array('d', [0])
    imag = array('d', [0])
    g_ps = ROOT.TGraph()
    #g_ps = ROOT.TH1F('h', "Power Spectrum; Frequency [Hz]; Spectral Power", n/2 + 1, 0, n/2)
    for i in range(n/2 + 1):
        re = ROOT.Double(0)
        im = ROOT.Double(0)
        fft.GetPointComplex(i, re, im)
        real.append(re)
        imag.append(im)
        ps.append(re*re + im*im/n/s2) #// Delta chi2, as in Lomb Scargle
        g_ps.SetPoint(i, i/range_sec, ps[-1])
        #g_ps.Fill(int(i/range_sec), ps[-1])
        #print(i, i/range_sec, ps[-1])       
       #//phase[i] = atan2(Im, Re);
        #print real, imag
    g_ps.SetTitle("Power Spectrum; Frequency [Hz]; Spectral Power")
    g_ps.SetLineColor(ROOT.kGreen+2)
    g_ps.SetMarkerColor(ROOT.kGreen+2)
    g_ps.SetLineWidth(2)

    #let's make the anti transform
    #re_full = array('d', [0]*(n/2-1))
    #im_full = array('d', [0]*(n/2-1))
    re_full = array('d', [0]*(n))
    im_full = array('d', [0]*(n))
    fft.GetPointsComplex(re_full, im_full)
    print(len(re_full), len(im_full))
    #real_clean = array('d', [0])
    #imag_clean = array('d', [0])
    fft_back = ROOT.TVirtualFFT.FFT(1, size, "C2R M K")
    fft_back.SetPointsComplex(re_full, im_full)
    fft_back.Transform()
    hb = None
    #//Let's look at the output
    hb = ROOT.TH1.TransformHisto(fft_back, hb, "Re")
    hb.SetTitle("The backward transform result")
    #return g_ps, hb
    return g_ps, real, imag, ps, hb

def clean_antiFFT(real, imag, ps):
    ps_clean = []
    trhd = 1e15
    real_clean = array('d', [0])
    imag_clean = array('d', [0])
    for i in range(len(real)):
        #if ps_value<trhd:
        real_clean.append(real[i])
        imag_clean.append(imag[i])
        #ps_clean.append(ps[i])
    size = array('i', [0])
    size[0] = (len(real_clean)-1)*2
    print len(real_clean), len(imag_clean)
    print size
    #print real_clean, imag_clean
    fft_back = ROOT.TVirtualFFT.FFT(1, size, "C2R M K")
    #fft_back.SetPointsComplex(real_clean, imag_clean)
    fft_back.SetPointsComplex(real, imag)
    fft_back.Transform()
    hb = None
    #//Let's look at the output
    hb = ROOT.TH1.TransformHisto(fft_back, hb, "Re")
    hb.SetTitle("The backward transform result")
    return hb


def treshold(ig, time):     #ig e time sono due array.array
    list_ig = []
    for i in len(time):
        if(time[i]>400000): 
            list_ig.append(ig[i])
    
    np_ig = np.array(list_ig)
    basel = 5* np.var(np_ig)

    return basel 
