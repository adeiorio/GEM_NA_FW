import ROOT
from array import array
import os
from dict_run import *

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch()        # don't pop up canvases
ROOT.TH1.SetDefaultSumw2()
ROOT.TGaxis.SetMaxDigits(3)

variables_to_write = {"pico": 1, "run": 0, "event": 0,
                      "drift_pulseheight": 0,"drift_mean": 0,"drift_time": 0,"drift_voltage": 0,"driftvolt_mean": 0,
                      "drift_deltamaxvolt": 0,"drift_integral": 0, 
                      "G1T_pulseheight": 0,"G1T_mean": 0,"G1T_time": 0,"G1T_voltage": 0,"G1Tvolt_mean": 0,"G1T_deltamaxvolt": 0,"G1T_integral": 0,
                      "G1B_pulseheight": 0,"G1B_mean": 0,"G1B_time": 0,"G1B_voltage": 0,"G1Bvolt_mean": 0,"G1B_deltamaxvolt": 0,"G1B_integral": 0,
                      "G2T_pulseheight": 0,"G2T_mean": 0,"G2T_time": 0,"G2T_voltage": 0,"G2Tvolt_mean": 0,"G2T_deltamaxvolt": 0,"G2T_integral": 0, 
                      "G2B_pulseheight": 0,"G2B_mean": 0,"G2B_time": 0,"G2B_voltage": 0,"G2Bvolt_mean": 0,"G2B_deltamaxvolt": 0,"G2B_integral": 0,
                      "G3T_pulseheight": 0,"G3T_mean": 0,"G3T_time": 0,"G3T_voltage": 0,"G3Tvolt_mean": 0,"G3T_deltamaxvolt": 0,"G3T_integral": 0,
                      "G3B_pulseheight": 0,"G3B_mean": 0,"G3B_time": 0,"G3B_voltage": 0,"G3Bvolt_mean": 0,"G3B_deltamaxvolt": 0,"G3B_integral": 0,
                      "deltav_g1t_dr": 0,"deltav_g1b_g1t": 0,"deltav_g2t_g1b": 0,"deltav_g2b_g2t": 0,"deltav_g3t_g2b": 0,"deltav_g3b_g3t": 0,
                      "mean_deltav_g1t_dr": 0,"mean_deltav_g1b_g1t": 0,"mean_deltav_g2t_g1b": 0,"mean_deltav_g2b_g2t": 0,"mean_deltav_g3t_g2b": 0,"mean_deltav_g3b_g3t": 0}


colors = [ROOT.kBlue,
          ROOT.kBlack,
          ROOT.kRed,
          ROOT.kGreen+2,
          ROOT.kMagenta+2,
          ROOT.kAzure+6]
def mean(array):
    sum = 0 
    for val in array:
        sum+= val
    mean = sum / len(array)
    return mean
     

def fit_hist(hist):
    print("fitting "+ hist.GetName())
    hist_to_fit = hist.Clone()
    xmin = hist_to_fit.GetXaxis().GetXmin()
    xmax = hist_to_fit.GetXaxis().GetXmax()
    g = ROOT.TF1("g", "gaus", xmin, xmax)
    hist_to_fit.Fit(g)
    mean, sigma = g.GetParameter(1), g.GetParameter(2)
    return mean, sigma

def print_hist(plotpath, hist, name, option = "HIST", log = False, stack = False, title = ""):
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
     hist.Write("", ROOT.TObject.kOverwrite)
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

def h_init( nbins_current = 100, xmin_current = -50, xmax_current = 50, nbins_voltage= 4000, xmin_voltage= -3500, xmax_voltage= 0): 
    curr_ig3t_distr = ROOT.TH1F("curr_ig3t_distr", "G3T current distribution; Current (nA); #events", nbins_current, xmin_current, xmax_current)
    curr_ig2t_distr = ROOT.TH1F("curr_ig2t_distr", "G2T current distribution; Current (nA); #events", nbins_current, xmin_current, xmax_current)
    curr_ig1t_distr = ROOT.TH1F("curr_ig1t_distr", "G1T current distribution; Current (nA); #events", nbins_current, xmin_current, xmax_current)
    curr_ig3b_distr = ROOT.TH1F("curr_ig3b_distr", "G3B current distribution; Current (nA); #events", nbins_current, xmin_current, xmax_current)
    curr_ig2b_distr = ROOT.TH1F("curr_ig2b_distr", "G2B current distribution; Current (nA); #events", nbins_current, xmin_current, xmax_current)
    curr_ig1b_distr = ROOT.TH1F("curr_ig1b_distr", "G1B current distribution; Current (nA); #events", nbins_current, xmin_current, xmax_current)
    curr_idrift_distr = ROOT.TH1F("curr_idrift_distr", "DRIFT current distribution; Current (nA); #events", nbins_current, xmin_current, xmax_current)

    volt_g3b_distr = ROOT.TH1F("volt_g3b_distr", "G3B voltage distribution; Voltage (V); #events", nbins_voltage, xmin_voltage, xmax_voltage)
    volt_g3t_distr = ROOT.TH1F("volt_g3t_distr", "G3T voltage distribution; Voltage (V); #events", nbins_voltage, xmin_voltage, xmax_voltage)
    volt_g2b_distr = ROOT.TH1F("volt_g2b_distr", "G2B voltage distribution; Voltage (V); #events", nbins_voltage, xmin_voltage, xmax_voltage)
    volt_g2t_distr = ROOT.TH1F("volt_g2t_distr", "G2T voltage distribution; Voltage (V); #events", nbins_voltage, xmin_voltage, xmax_voltage)
    volt_g1b_distr = ROOT.TH1F("volt_g1b_distr", "G1B voltage distribution; Voltage (V); #events", nbins_voltage, xmin_voltage, xmax_voltage)
    volt_g1t_distr = ROOT.TH1F("volt_g1t_distr", "G1T voltage distribution; Voltage (V); #events", nbins_voltage, xmin_voltage, xmax_voltage)
    volt_drift_distr = ROOT.TH1F("volt_drift_distr", "DRIFT voltage distribution; Voltage (V); #events", nbins_voltage, xmin_voltage, xmax_voltage)

    return curr_ig3t_distr.Clone(), curr_ig2t_distr.Clone(), curr_ig1t_distr.Clone(), curr_ig3b_distr.Clone(), curr_ig2b_distr.Clone(), curr_ig1b_distr.Clone(), curr_idrift_distr.Clone(), volt_g3b_distr.Clone(), volt_g3t_distr.Clone(), volt_g2b_distr.Clone(), volt_g2t_distr.Clone(), volt_g1b_distr.Clone(), volt_g1t_distr.Clone(), volt_drift_distr.Clone()

def make_plots(outfolder, ofile, time_current, time_voltage, ig1t, ig1b, ig2t, ig2b, ig3t, ig3b, idrift, 
               m_ig1t, m_ig1b, m_ig2t, m_ig2b, m_ig3t, m_ig3b, m_idrift,
               vg1t, vg1b, vg2t, vg2b, vg3t, vg3b, vdrift, deltav_drg1t, deltav_g1tg1b, deltav_g1bg2t, deltav_g2tg2b, deltav_g2bg3t, deltav_g3tg3b, k):
    ofile.cd()
    gr_idrift = ROOT.TGraph(len(time_current), time_current, idrift)
    gr_idrift.SetName("gr_idrift_"+str(k))
    gr_idrift.SetTitle("I drift")
    gr_idrift.GetXaxis().SetTitle("time (s)")
    gr_idrift.GetYaxis().SetTitle("current (nA)")
    gr_idrift.SetMarkerColor(ROOT.kBlack)
    gr_idrift.SetMarkerStyle(20)
    gr_ig1t = ROOT.TGraph(len(time_current), time_current, ig1t) 
    gr_ig1t.SetName("gr_ig1t_"+str(k))
    gr_ig1t.SetTitle("I g1t")
    gr_ig1t.GetXaxis().SetTitle("time (s)")
    gr_ig1t.GetYaxis().SetTitle("current (nA)")
    gr_ig1t.SetMarkerColor(ROOT.kGreen)
    gr_ig1t.SetMarkerStyle(20)
    gr_ig1b = ROOT.TGraph(len(time_current), time_current, ig1b) 
    gr_ig1b.SetName("gr_ig1b_"+str(k))
    gr_ig1b.SetTitle("I g1b")
    gr_ig1b.GetXaxis().SetTitle("time (s)")
    gr_ig1b.GetYaxis().SetTitle("current (nA)")
    gr_ig1b.SetMarkerColor(ROOT.kGreen+3)
    gr_ig1b.SetMarkerStyle(20)
    gr_ig2t = ROOT.TGraph(len(time_current), time_current, ig2t) 
    gr_ig2t.SetName("gr_ig2t_"+str(k))
    gr_ig2t.SetTitle("I g2t")
    gr_ig2t.GetXaxis().SetTitle("time (s)")
    gr_ig2t.GetYaxis().SetTitle("current (nA)")
    gr_ig2t.SetMarkerColor(ROOT.kCyan)
    gr_ig2t.SetMarkerStyle(20)
    gr_ig2b = ROOT.TGraph(len(time_current), time_current, ig2b) 
    gr_ig2b.SetName("gr_ig2b_"+str(k))
    gr_ig2b.SetTitle("I g2b")
    gr_ig2b.GetXaxis().SetTitle("time (s)")
    gr_ig2b.GetYaxis().SetTitle("current (nA)")
    gr_ig2b.SetMarkerColor(ROOT.kCyan+3)
    gr_ig2b.SetMarkerStyle(20)
    gr_ig3t = ROOT.TGraph(len(time_current), time_current, ig3t) 
    gr_ig3t.SetName("gr_ig3t_"+str(k))
    gr_ig3t.SetTitle("I g3t")
    gr_ig3t.GetXaxis().SetTitle("time (s)")
    gr_ig3t.GetYaxis().SetTitle("current (nA)")
    gr_ig3t.SetMarkerColor(ROOT.kRed)
    gr_ig3t.SetMarkerStyle(20)
    gr_ig3b = ROOT.TGraph(len(time_current), time_current, ig3b) 
    gr_ig3b.SetName("gr_ig3b_"+str(k))
    gr_ig3b.SetTitle("I g3b")
    gr_ig3b.GetXaxis().SetTitle("time (s)")
    gr_ig3b.GetYaxis().SetTitle("current (nA)")
    gr_ig3b.SetMarkerColor(ROOT.kRed+3)
    gr_ig3b.SetMarkerStyle(20)

    gr_idrift.Write() 
    print_hist(outfolder, gr_idrift.Clone(), "Idrift_time_"+str(k), "AL*")    
    gr_ig1t.Write() 
    print_hist(outfolder, gr_ig1t.Clone(), "Ig1t_time_"+str(k), "AL*")
    gr_ig1b.Write() 
    print_hist(outfolder, gr_ig1b.Clone(), "Ig1b_time_"+str(k), "AL*")
    gr_ig2t.Write() 
    print_hist(outfolder, gr_ig2t.Clone(), "Ig2t_time_"+str(k), "AL*")
    gr_ig2b.Write() 
    print_hist(outfolder, gr_ig2b.Clone(), "Ig2b_time_"+str(k), "AL*")
    gr_ig3t.Write() 
    print_hist(outfolder, gr_ig3t.Clone(), "Ig3t_time_"+str(k), "AL*")
    gr_ig3b.Write()
    print_hist(outfolder, gr_ig3b.Clone(), "Ig3b_time_"+str(k), "AL*")

    all_current = [gr_idrift.Clone(), gr_ig1t.Clone(), gr_ig1b.Clone(), gr_ig2t.Clone(), gr_ig2b.Clone(), gr_ig3t.Clone(), gr_ig3b.Clone()]
    print_hist(outfolder, all_current, 'All_currents_'+str(k), "AL*")

    gr_m_idrift = ROOT.TGraph(len(time_current), time_current, m_idrift) 
    gr_m_idrift.SetName("gr_m_idrift_"+str(k))
    gr_m_idrift.SetTitle("-I drift")
    gr_m_idrift.GetXaxis().SetTitle("time (s)")
    gr_m_idrift.GetYaxis().SetTitle("current (nA)")
    gr_m_idrift.SetMarkerStyle(20)
    gr_m_idrift.SetMarkerColor(ROOT.kBlack)
    gr_m_ig1t = ROOT.TGraph(len(time_current), time_current, m_ig1t) 
    gr_m_ig1t.SetName("gr_m_ig1t_"+str(k))
    gr_m_ig1t.SetTitle("-I g1t")
    gr_m_ig1t.GetXaxis().SetTitle("time (s)")
    gr_m_ig1t.GetYaxis().SetTitle("current (nA)")
    gr_m_ig1t.SetMarkerStyle(20)
    gr_m_ig1t.SetMarkerColor(ROOT.kGreen)
    gr_m_ig1b = ROOT.TGraph(len(time_current), time_current, m_ig1b) 
    gr_m_ig1b.SetName("gr_m_ig1b_"+str(k))
    gr_m_ig1b.SetTitle("-I g1b")
    gr_m_ig1b.GetXaxis().SetTitle("time (s)")
    gr_m_ig1b.GetYaxis().SetTitle("current (nA)")
    gr_m_ig1b.SetMarkerStyle(20)
    gr_m_ig1b.SetMarkerColor(ROOT.kGreen+3)
    gr_m_ig2t = ROOT.TGraph(len(time_current), time_current, m_ig2t) 
    gr_m_ig2t.SetName("gr_m_ig2t_"+str(k))
    gr_m_ig2t.SetTitle("-I g2t")
    gr_m_ig2t.GetXaxis().SetTitle("time (s)")
    gr_m_ig2t.GetYaxis().SetTitle("current (nA)")
    gr_m_ig2t.SetMarkerStyle(20)
    gr_m_ig2t.SetMarkerColor(ROOT.kCyan)
    gr_m_ig2b = ROOT.TGraph(len(time_current), time_current, m_ig2b) 
    gr_m_ig2b.SetName("gr_m_ig2b_"+str(k))
    gr_m_ig2b.SetTitle("-I g2b")
    gr_m_ig2b.GetXaxis().SetTitle("time (s)")
    gr_m_ig2b.GetYaxis().SetTitle("current (nA)")
    gr_m_ig2b.SetMarkerStyle(20)
    gr_m_ig2b.SetMarkerColor(ROOT.kCyan+3)
    gr_m_ig3t = ROOT.TGraph(len(time_current), time_current, m_ig3t) 
    gr_m_ig3t.SetName("gr_m_ig3t_"+str(k))
    gr_m_ig3t.SetTitle("-I g3t")
    gr_m_ig3t.GetXaxis().SetTitle("time (s)")
    gr_m_ig3t.GetYaxis().SetTitle("current (nA)")
    gr_m_ig3t.SetMarkerStyle(20)
    gr_m_ig3t.SetMarkerColor(ROOT.kRed)
    gr_m_ig3b = ROOT.TGraph(len(time_current), time_current, m_ig3b) 
    gr_m_ig3b.SetName("gr_m_ig3b_"+str(k))
    gr_m_ig3b.SetTitle("-I g3b")
    gr_m_ig3b.GetXaxis().SetTitle("time (s)")
    gr_m_ig3b.GetYaxis().SetTitle("current (nA)")
    gr_m_ig3b.SetMarkerStyle(20)
    gr_m_ig3b.SetMarkerColor(ROOT.kRed+3)

    gr_m_idrift.Write() 
    print_hist(outfolder, gr_m_idrift, "m_Idrift_time_"+str(k), "AL*")    
    gr_m_ig1t.Write() 
    print_hist(outfolder, gr_m_ig1t, "m_Ig1t_time_"+str(k), "AL*")
    gr_m_ig1b.Write() 
    print_hist(outfolder, gr_m_ig1b, "m_Ig1b_time_"+str(k), "AL*")
    gr_m_ig2t.Write() 
    print_hist(outfolder, gr_m_ig2t, "m_Ig2t_time_"+str(k), "AL*")
    gr_m_ig2b.Write() 
    print_hist(outfolder, gr_m_ig2b, "m_Ig2b_time_"+str(k), "AL*")
    gr_m_ig3t.Write() 
    print_hist(outfolder, gr_m_ig3t, "m_Ig3t_time_"+str(k), "AL*")
    gr_m_ig3b.Write()
    print_hist(outfolder, gr_m_ig3b, "m_Ig3b_time_"+str(k), "AL*")

    gr_vdrift = ROOT.TGraph(len(time_voltage), time_voltage, vdrift)
    gr_vdrift.SetName("gr_vdrift_"+str(k))
    gr_vdrift.SetMarkerStyle(20)
    gr_vdrift.SetTitle("V drift")
    gr_vdrift.GetXaxis().SetTitle("time (s)")
    gr_vdrift.GetYaxis().SetTitle("voltage (V)")
    gr_vdrift.SetMarkerColor(ROOT.kBlack)    
    gr_vg1t = ROOT.TGraph(len(time_voltage), time_voltage, vg1t) 
    gr_vg1t.SetName("gr_vg1t_"+str(k))
    gr_vg1t.SetMarkerStyle(20)
    gr_vg1t.SetTitle("V G1T")
    gr_vg1t.GetXaxis().SetTitle("time (s)")
    gr_vg1t.GetYaxis().SetTitle("voltage (V)")
    gr_vg1t.SetMarkerColor(ROOT.kGreen)
    gr_vg1b = ROOT.TGraph(len(time_voltage), time_voltage, vg1b) 
    gr_vg1b.SetName("gr_vg1b_"+str(k))
    gr_vg1b.SetMarkerStyle(20)
    gr_vg1b.SetTitle("V G1B")
    gr_vg1b.GetXaxis().SetTitle("time (s)")
    gr_vg1b.GetYaxis().SetTitle("voltage (V)")
    gr_vg1b.SetMarkerColor(ROOT.kGreen+3)
    gr_vg2t = ROOT.TGraph(len(time_voltage), time_voltage, vg2t) 
    gr_vg2t.SetName("gr_vg2t_"+str(k))
    gr_vg2t.SetMarkerStyle(20)
    gr_vg2t.SetTitle("V G2T")
    gr_vg2t.GetXaxis().SetTitle("time (s)")
    gr_vg2t.GetYaxis().SetTitle("voltage (V)")
    gr_vg2t.SetMarkerColor(ROOT.kCyan)
    gr_vg2b = ROOT.TGraph(len(time_voltage), time_voltage, vg2b) 
    gr_vg2b.SetName("gr_vg2b_"+str(k))
    gr_vg2b.SetMarkerStyle(20)
    gr_vg2b.SetTitle("V G2B")
    gr_vg2b.GetXaxis().SetTitle("time (s)")
    gr_vg2b.GetYaxis().SetTitle("voltage (V)")
    gr_vg2b.SetMarkerColor(ROOT.kCyan+3)
    gr_vg3t = ROOT.TGraph(len(time_voltage), time_voltage, vg3t) 
    gr_vg3t.SetName("gr_vg3t_"+str(k))
    gr_vg3t.SetMarkerStyle(20)
    gr_vg3t.SetTitle("V G3T")
    gr_vg3t.GetXaxis().SetTitle("time (s)")
    gr_vg3t.GetYaxis().SetTitle("voltage (V)")
    gr_vg3t.SetMarkerColor(ROOT.kRed)
    gr_vg3b = ROOT.TGraph(len(time_voltage), time_voltage, vg3b) 
    gr_vg3b.SetName("gr_vg3b_"+str(k))
    gr_vg3b.SetMarkerStyle(20)
    gr_vg3b.SetTitle("V G3B")
    gr_vg3b.GetXaxis().SetTitle("time (s)")
    gr_vg3b.GetYaxis().SetTitle("voltage (V)")
    gr_vg3b.SetMarkerColor(ROOT.kRed+3)


    gr_vdrift.Write() 
    print_hist(outfolder, gr_vdrift, "Vdrift_time_"+str(k), "AL*")    
    gr_vg1t.Write() 
    print_hist(outfolder, gr_vg1t, "VG1t_time_"+str(k), "AL*")
    gr_vg1b.Write() 
    print_hist(outfolder, gr_vg1b, "Vg1b_time_"+str(k), "AL*")
    gr_vg2t.Write() 
    print_hist(outfolder, gr_vg2t, "Vg2t_time_"+str(k), "AL*")
    gr_vg2b.Write() 
    print_hist(outfolder, gr_vg2b, "Vg2b_time_"+str(k), "AL*")
    gr_vg3t.Write() 
    print_hist(outfolder, gr_vg3t, "Vg3t_time_"+str(k), "AL*")
    gr_vg3b.Write()
    print_hist(outfolder, gr_vg3b, "Vg3b_time_"+str(k), "AL*")

    all_voltages = [gr_vdrift.Clone(), gr_vg1t.Clone(), gr_vg1b.Clone(), gr_vg2t.Clone(), gr_vg2b.Clone(), gr_vg3t.Clone(), gr_vg3b.Clone()]
    print_hist(outfolder, all_voltages, 'All_voltages_'+str(k), "AL*")

    gr_deltav_drg1t = ROOT.TGraph(len(time_voltage), time_voltage, deltav_drg1t)
    gr_deltav_drg1t.SetName("gr_deltav_grg1t_"+str(k))
    gr_deltav_drg1t.SetMarkerStyle(20)
    gr_deltav_drg1t.SetTitle("#Delta V (-drift+G1T)")
    gr_deltav_drg1t.GetXaxis().SetTitle("time (s)")
    gr_deltav_drg1t.GetYaxis().SetTitle("voltage (V)")
    gr_deltav_drg1t.SetMarkerColor(ROOT.kBlack)
    gr_deltav_g1tg1b = ROOT.TGraph(len(time_voltage), time_voltage, deltav_g1tg1b) 
    gr_deltav_g1tg1b.SetName("gr_deltav_g1tg1b_"+str(k))
    gr_deltav_g1tg1b.SetMarkerStyle(20)
    gr_deltav_g1tg1b.SetTitle("#Delta V (-G1T+G1B)")
    gr_deltav_g1tg1b.GetXaxis().SetTitle("time (s)")
    gr_deltav_g1tg1b.GetYaxis().SetTitle("voltage (V)")
    gr_deltav_g1tg1b.SetMarkerColor(ROOT.kGreen)
    gr_deltav_g1bg2t = ROOT.TGraph(len(time_voltage), time_voltage, deltav_g1bg2t) 
    gr_deltav_g1bg2t.SetName("gr_deltav_g1bg2t_"+str(k))
    gr_deltav_g1bg2t.SetMarkerStyle(20)
    gr_deltav_g1bg2t.SetTitle("#Delta V (-G1B+G2T)")
    gr_deltav_g1bg2t.GetXaxis().SetTitle("time (s)")
    gr_deltav_g1bg2t.GetYaxis().SetTitle("voltage (V)")
    gr_deltav_g1bg2t.SetMarkerColor(ROOT.kGreen+3)
    gr_deltav_g2tg2b = ROOT.TGraph(len(time_voltage), time_voltage, deltav_g2tg2b) 
    gr_deltav_g2tg2b.SetName("gr_deltav_g2tg2b_"+str(k))
    gr_deltav_g2tg2b.SetMarkerStyle(20)
    gr_deltav_g2tg2b.SetTitle("#Delta V (-G2T+G2B)")
    gr_deltav_g2tg2b.GetXaxis().SetTitle("time (s)")
    gr_deltav_g2tg2b.GetYaxis().SetTitle("voltage (V)")
    gr_deltav_g2tg2b.SetMarkerColor(ROOT.kBlue)
    gr_deltav_g2bg3t = ROOT.TGraph(len(time_voltage), time_voltage, deltav_g2bg3t) 
    gr_deltav_g2bg3t.SetName("gr_deltav_g2bg3t_"+str(k))
    gr_deltav_g2bg3t.SetMarkerStyle(20)
    gr_deltav_g2bg3t.SetTitle("#Delta V (-G2B+G3T)")
    gr_deltav_g2bg3t.GetXaxis().SetTitle("time (s)")
    gr_deltav_g2bg3t.GetYaxis().SetTitle("voltage (V)")
    gr_deltav_g2bg3t.SetMarkerColor(ROOT.kCyan)
    gr_deltav_g3tg3b = ROOT.TGraph(len(time_voltage), time_voltage, deltav_g3tg3b) 
    gr_deltav_g3tg3b.SetName("gr_deltav_g3tg3b_"+str(k))
    gr_deltav_g3tg3b.SetMarkerStyle(20)
    gr_deltav_g3tg3b.SetTitle("#Delta V (-G3T+G3B)")
    gr_deltav_g3tg3b.GetXaxis().SetTitle("time (s)")
    gr_deltav_g3tg3b.GetYaxis().SetTitle("voltage (V)")
    gr_deltav_g3tg3b.SetMarkerColor(ROOT.kRed)

    gr_deltav_drg1t.Write() 
    print_hist(outfolder, gr_deltav_drg1t, "deltaV_drg1t_time_"+str(k), "AL*")    
    gr_deltav_g1tg1b.Write() 
    print_hist(outfolder, gr_deltav_g1tg1b, "deltaV_g1tg1b_time_"+str(k), "AL*")
    gr_deltav_g1bg2t.Write() 
    print_hist(outfolder, gr_deltav_g1bg2t, "deltaV_g1bg2t_time_"+str(k), "AL*")
    gr_deltav_g2tg2b.Write() 
    print_hist(outfolder, gr_deltav_g2tg2b, "deltaV_g2tg2b_time_"+str(k), "AL*")
    gr_deltav_g2bg3t.Write() 
    print_hist(outfolder, gr_deltav_g2bg3t, "deltaV_g2bg3t_time_"+str(k), "AL*")
    gr_deltav_g3tg3b.Write() 
    print_hist(outfolder, gr_deltav_g3tg3b, "deltaV_g3tg3b_time_"+str(k), "AL*")
    
    all_deltaV = [gr_deltav_drg1t.Clone(), gr_deltav_g1tg1b.Clone(), gr_deltav_g1bg2t.Clone(), gr_deltav_g2tg2b.Clone(), gr_deltav_g2bg3t.Clone(), gr_deltav_g3tg3b.Clone()]
    print_hist(outfolder, all_deltaV, 'All_deltaV_'+str(k), "AL*")

def integral(i_array, t_array, i):
    # i_array 950*2 entries
    #i_to_mean = i_array[0:900]
    #baseline = mean(i_to_mean)
    '''hist_current = ROOT.TH1F("","", 300, min(i_array[:950]), )
    #print i_array[:900]
    for i in range(900):
        hist_current.Fill(i_array[i])
    baseline = hist_current.GetMean()
    '''
    if i <950: n=i
    else: n = 950
    baseline = mean(i_array[:(n-50)])
    #print ("baseline = ",baseline)
    start = t_array[n-50]
    stop = t_array[n-50+700] # +380 ~ +1s (faccio un po di meno
    
    h_to_int = ROOT.TH1F("hist", "hist", 700, start, stop)
    for i in range(700):
        h_to_int.SetBinContent(i, i_array[i+n-50]-baseline)
    integral = h_to_int.Integral()
    #print ("int= ",integral)
    return integral

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++   dis_makeplot functions +++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def plot_drift( run, entry):
    outfolder = "/eos/home-a/acagnott/GEM_plot/cathode_graphs/"
    if not os.path.exists(outfolder):
        os.mkdir(outfolder)
    if not "000" in run :
        
        infile = ROOT.TFile.Open("/eos/home-a/adeiorio/GEM/Goliath/"+run+"_skim.root")
        print infile
        outfile = ROOT.TFile.Open("/eos/home-a/acagnott/GEM_plot/cathode_graphs/"+run+ "_"+str(entry)+".root","RECREATE")
    else:
        
        infile = ROOT.TFile.Open("/eos/home-a/adeiorio/GEM/Goliath/"+run+"_skim.root")
        print infile
        outfile = ROOT.TFile.Open("/eos/home-a/acagnott/GEM_plot/cathode_graphs/"+run+ "_"+str(entry)+".root","RECREATE")       

    pico = run.split("_")[0]
    tree = infile.Get("t1")

    tree.GetEntry(entry)
    
    i_array = tree.IDRIFT
    v_array = tree.VDRIFT
    delta1 = tree.DeltaV_drg1t
    time_current = tree.time_current
    if abs(max(i_array))>abs(min(i_array)): maxdrift = max(i_array)
    else: maxdrift = min(i_array)
    
    in_drift = Get_index(i_array, maxdrift)

    graph = ROOT.TGraph(1900,tree.time_current, i_array)
    graph.SetMarkerStyle(20)
    outfile.cd()
    graph.Write()
    graph_idrift = make_graph(1900, tree.time_current, i_array, "graph_vdrift", "I Drift", "time(s)", "Current(nA)", ROOT.kBlack)
    print_hist(outfolder, graph_idrift, run+'_'+str(entry)+'_idrift', 'APL')
    graph_vdrift = make_graph(20, tree.time_current, v_array, "graph_vdrift", "V Drift", "time(s)", "Voltage(V)", ROOT.kBlack)
    print_hist(outfolder, graph_vdrift, run+'_'+str(entry)+'_vdrift', 'APL')

    f1 = open("/eos/home-a/acagnott/GEM_plot/"+pico+"_drift.csv", "a")
    f1.write("\n")
    f1.write(run+","+str(entry)+", drift (ph), time, deltaV(g1t-dr), V drift")
    f1.write(",,"+str(maxdrift)+","+str(time_current[in_drift])+","+str(delta1[in_drift])+","+ str(v_array[in_drift])+"\n")
    
def plot_allch(run, entry, draw_volt = False, data = 'Goliath', fit = False):#, write_file = False):
    
    infile = ROOT.TFile.Open("/eos/home-a/adeiorio/GEM/"+data+"/"+run+"_skim.root")
    print infile

    outfolder_csv = "/eos/home-a/acagnott/GEM_plot/"+data+"/"
    outfolder = outfolder_csv+"graphsdischarges/"
    
    if not os.path.exists(outfolder_csv):
        os.mkdir(outfolder_csv)
    if not os.path.exists(outfolder):
        os.mkdir(outfolder)

    outfolder = outfolder_csv+"graphsdischarges/"+run+"_"+str(entry)
        
    if not os.path.exists(outfolder):
        os.mkdir(outfolder)

    outfile = ROOT.TFile.Open(outfolder+"/graphs.root","RECREATE")
    pico = run.split("_")[0]
    run_label = run.split("_")[1]
    run_label = run_label.split('00')[1]
    tree = infile.Get("t1")

    tree.GetEntry(entry)
    idrift = tree.IDRIFT
    ig1t = tree.IG1T
    ig1b = tree.IG1B
    ig2t = tree.IG2T
    ig2b = tree.IG2B
    ig3t = tree.IG3T
    ig3b = tree.IG3B
    vdrift = tree.VDRIFT
    vg1t = tree.VG1T
    vg1b = tree.VG1B
    vg2t = tree.VG2T
    vg2b = tree.VG2B
    vg3t = tree.VG3T
    vg3b = tree.VG3B
    delta1 = tree.DeltaV_drg1t
    delta2 = tree.DeltaV_g1tg1b
    delta3 = tree.DeltaV_g1bg2t
    delta4 = tree.DeltaV_g2tg2b
    delta5 = tree.DeltaV_g2bg3t
    delta6 = tree.DeltaV_g3tg3b
    
    delta1_var = tree.DeltaV_drg1t_var
    delta2_var = tree.DeltaV_g1tg1b_var
    delta3_var = tree.DeltaV_g1bg2t_var
    delta4_var = tree.DeltaV_g2tg2b_var
    delta5_var = tree.DeltaV_g2bg3t_var
    delta6_var = tree.DeltaV_g3tg3b_var
    
    integral_idrift = tree.INTEGRAL_IDRIFT
    integral_ig1t = tree.INTEGRAL_IG1T
    integral_ig1b = tree.INTEGRAL_IG1B
    integral_ig2t = tree.INTEGRAL_IG2T
    integral_ig2b = tree.INTEGRAL_IG2B
    integral_ig3t = tree.INTEGRAL_IG3T
    integral_ig3b = tree.INTEGRAL_IG3B

    if data == 'Goliath':
        time_current = tree.time_current
        time_voltage = tree.time_voltage
    else:
        time_current = tree.deltatime_current
        time_voltage = tree.deltatime_voltage
        timestamp_current = tree.timestamp_current
        timestamp_voltage = tree.timestamp_voltage

    taus = []
    
    if max(idrift)>abs(min(idrift)): max_drift = max(idrift)
    else: max_drift = min(idrift)
    
    in_drift = Get_index(idrift, max_drift)
    in_g1t = Get_index(ig1t, min(ig1t))
    in_g1b = Get_index(ig1b, max(ig1b))
    in_g2t = Get_index(ig2t, min(ig2t))
    in_g2b = Get_index(ig2b, max(ig2b))
    in_g3t = Get_index(ig3t, min(ig3t))
    in_g3b = Get_index(ig3b, max(ig3b))

    in_vdr = Get_index(delta1_var,max(delta1_var))
    in_vg1 = Get_index(delta2_var, max(delta2_var))
    in_delta3 = Get_index(delta3_var, max(delta3_var))
    in_vg2 = Get_index(delta4_var, max(delta4_var))
    in_delta5 = Get_index(delta5_var, max(delta5_var))
    in_vg3 = Get_index(delta6_var, max(delta6_var))
    
    #print in_drift,in_g1t,in_g1b,in_g2t,in_g2b,in_g3t,in_g3b,in_vdr,in_vg1,in_delta3,in_vg2,in_delta5,in_vg3

    '''time_ref_current = time_current[in_g3t]
    time_ref_voltage = 0
    for t in time_voltage:
        if t< time_ref_current: continue
        elif t> time_ref_current and time_ref_voltage==0: time_ref_voltage = t
        else : break
        
    voltage_index = Get_index(time_voltage, time_ref_voltage)
    '''
    ph = [min(ig1t), max(ig1b), min(ig2t), max(ig2b), min(ig3t), max(ig3b)]
    
    n_1 = 5
    n_2 = 200
    
    if len(ig3t)<200: n_2 = 50
    
    '''if "PICO1_run0029" in run : n_2 = 100
    #elif "PICO1_run0008" in run : n_2 = 10
    elif "PICO2_run0028" in run : n_2 = 100
    '''
    if data == 'Goliath' :
        tot_time = ''
    else:
        #print timestamp_current[0]
        start = datetime.fromtimestamp(timestamp_current[0])
        #print start
        tot_time = 'start:' + start.strftime('%a,%d %b %Y %H:%M:%S.%f') 
        
    

    graph_dr = make_graph(1900, time_current, idrift, "graph_idrift", "idrift "+tot_time, "time(s)", "current(nA)", ROOT.kBlack)
    graph_g1t = make_graph(1900, time_current, ig1t, "graph_ig1t", "ig1t "+tot_time, "time(s)", "current(nA)", ROOT.kGreen)
    graph_g1b = make_graph(1900, time_current, ig1b, "graph_ig1b", "ig1b "+tot_time, "time(s)", "current(nA)", ROOT.kGreen+3)
    graph_g2t = make_graph(1900, time_current, ig2t, "graph_ig2t", "ig2t "+tot_time, "time(s)", "current(nA)", ROOT.kCyan)
    graph_g2b = make_graph(1900, time_current, ig2b, "graph_ig2b", "ig2b "+tot_time, "time(s)", "current(nA)", ROOT.kCyan+3)
    graph_g3t = make_graph(1900, time_current, ig3t, "graph_ig3t", "ig3t "+tot_time, "time(s)", "current(nA)", ROOT.kRed)
    graph_g3b = make_graph(1900, time_current, ig3b, "graph_ig3b", "ig3b "+tot_time, "time(s)", "current(nA)", ROOT.kRed+3)
    
    if (not ('PICO1_run0008' in run or 'PICO1_run0009' in run ) and fit and not draw_volt):
        taus.append(1./fit_exp(graph_g1t.Clone(), time_current[in_g1t+ n_1], time_current[in_g1t+n_2], True))
        taus.append(1./fit_exp(graph_g1b.Clone(), time_current[in_g1b+ n_1], time_current[in_g1b+n_2], False))
        taus.append(1./fit_exp(graph_g2t.Clone(), time_current[in_g2t+ n_1], time_current[in_g2t+n_2], True))
        taus.append(1./fit_exp(graph_g2b.Clone(), time_current[in_g2b+ n_1], time_current[in_g2b+n_2], False))
        taus.append(1./fit_exp(graph_g3t.Clone(), time_current[in_g3t+ n_1], time_current[in_g3t+n_2], True))
        taus.append(1./fit_exp(graph_g3b.Clone(), time_current[in_g3b+ n_1], time_current[in_g3b+n_2], False))

    
    mean_volt_drift = mean(vdrift)
    mean_volt_g1t = mean(vg1t)
    mean_volt_g1b = mean(vg1b)
    mean_volt_g2t = mean(vg2t)
    mean_volt_g2b = mean(vg2b)
    mean_volt_g3t = mean(vg3t)
    mean_volt_g3b = mean(vg3b)


    max_volt_drift = vdrift[in_vdr]
    max_volt_g1t = vg1t[in_vg1]
    max_volt_g1b = vg1b[in_vg1]
    max_volt_g2t = vg2t[in_vg2]
    max_volt_g2b = vg2b[in_vg2]
    max_volt_g3t = vg3t[in_vg3]
    max_volt_g3b = vg3b[in_vg3]
    
    volt_drift_wrt_mean = max_volt_drift - mean_volt_drift
    volt_drift_deltamax = abs(max(vdrift) - min(vdrift))
    volt_drift_center = vdrift[in_vdr]
    volt_g1t_wrt_mean = max_volt_g1t - mean_volt_g1t
    volt_g1t_deltamax = abs(max(vg1t) - min(vg1t))
    volt_g1t_center = vg1t[in_vg1]
    volt_g1b_wrt_mean = max_volt_g1b - mean_volt_g1b
    volt_g1b_deltamax = abs(max(vg1b) - min(vg1b))
    volt_g1b_center = vg1b[in_vg1]
    volt_g2t_wrt_mean = max_volt_g2t - mean_volt_g2t
    volt_g2t_deltamax = abs(max(vg2t) - min(vg2t))
    volt_g2t_center = vg2t[in_vg2]
    volt_g2b_wrt_mean = max_volt_g2b - mean_volt_g2b
    volt_g2b_deltamax = abs(max(vg2b) - min(vg2b))
    volt_g2b_center = vg2b[in_vg2]
    volt_g3t_wrt_mean = max_volt_g3t - mean_volt_g3t
    volt_g3t_deltamax = abs(max(vg3t) - min(vg3t))
    volt_g3t_center = vg3t[in_vg2]
    volt_g3b_wrt_mean = max_volt_g3b - mean_volt_g3b
    volt_g3b_deltamax = abs(max(vg3b) - min(vg3b))
    volt_g3b_center = vg3b[in_vg2]
    
    mean_delta_g1t_dr = mean(delta1)
    mean_delta_g1b_g1t = mean(delta2)
    mean_delta_g2t_g1b = mean(delta3)
    mean_delta_g2b_g2t = mean(delta4)
    mean_delta_g3t_g3b = mean(delta5)
    mean_delta_g3b_g3t = mean(delta6)
    '''
    if write_file:
        if data =='Goliath':
            f_rate = open("dis_rate"+pico+".txt", "r")
            line = f_rate.readlines()[int(run_label)-1]
            rate = line.split(',')[1]
        
            print run_label
            print "run rate", rate
            f_rate.close()
        
        if data=='Goliath':
            if ('0002' in run) :

                f = open(outfolder_csv+pico+"discharges_event.csv" ,"w")
                f.write("\n")
                f.write("pico,run,event,drift_pulseheight,drift_mean,drift_time,drift_voltage,driftvolt_mean,drift_deltamaxvolt, drift_integral"+ 
                        "G1T_pulseheight,G1T_mean,G1T_tau,G1T_time,G1T_voltage,G1Tvolt_mean,G1T_deltamaxvolt,G1T_integral,"+
                        "G1B_pulseheight,G1B_mean,G1B_tau,G1B_time,G1B_voltage,G1Bvolt_mean,G1B_deltamaxvolt,G1B_integral,"+
                        "G2T_pulseheight,G2T_mean,G2T_tau,G2T_time,G2T_voltage,G2Tvolt_mean,G2T_deltamaxvolt,G2T_integral,"+ 
                        "G2B_pulseheight,G2B_mean,G2B_tau,G2B_time,G2B_voltage,G2Bvolt_mean,G2B_deltamaxvolt,G2B_integral,"+
                        "G3T_pulseheight,G3T_mean,G3T_tau,G3T_time,G3T_voltage,G3Tvolt_mean,G3T_deltamaxvolt,G3T_integral,"+
                        "G3B_pulseheight,G3B_mean,G3B_tau,G3B_time,G3B_voltage,G3Bvolt_mean,G3B_deltamaxvolt,G3B_integral,"+
                        "deltav_g1t_dr,delta_g1b_g1t,delta_g2t_g1b,delta_g2b_g2t,delta_g3t_g2b,delta_g3b_g3t,"+
                        "mean_delta_g1t_dr,mean_delta_g1b_g1t,mean_delta_g2t_g1b,mean_delta_g2b_g2t,mean_delta_g3t_g3b,mean_delta_g3b_g3t,discharge_rate\n")
                
            else:
                f = open(outfolder_csv+pico+"discharges_event.csv" ,"a")
        
            f.write(pico.split('O')[1]+","+run_label+","+str(entry)+","+ 
                    str(max_drift) + "," +str(mean(idrift))+","+ str(time_current[in_drift]) + "," + str(vdrift[in_vdr]) + "," + str(volt_drift_wrt_mean) + "," + str(volt_drift_deltamax)+","+str(integral_idrift)+","+      
                    str(min(ig1t)) + "," +str(mean(ig1t))+","+ str(taus[0]) + "," + str(time_current[in_g1t])+ "," + str(vg1t[in_vg1])+","+str(volt_g1t_wrt_mean)+","+str(volt_g1t_deltamax)+","+str(integral_ig1t)+","+   
                    str(max(ig1b)) + "," +str(mean(ig1b))+","+ str(taus[1]) + "," + str(time_current[in_g1b])+ "," + str(vg1b[in_vg1])+","+str(volt_g1b_wrt_mean)+","+str(volt_g1b_deltamax)+","+str(integral_ig1b)+","+   
                    str(min(ig2t)) + "," +str(mean(ig2t))+","+ str(taus[2]) + "," + str(time_current[in_g2t])+ "," + str(vg2t[in_vg2])+","+str(volt_g2t_wrt_mean)+","+str(volt_g2t_deltamax)+","+str(integral_ig2t)+","+      
                    str(max(ig2b)) + "," +str(mean(ig2b))+","+ str(taus[3]) + "," + str(time_current[in_g2b])+ "," + str(vg2b[in_vg2])+","+str(volt_g2b_wrt_mean)+","+str(volt_g2b_deltamax)+","+str(integral_ig2b)+","+         
                    str(min(ig3t)) + "," +str(mean(ig3t))+","+ str(taus[4]) + "," + str(time_current[in_g3t])+ "," + str(vg3t[in_vg2])+","+str(volt_g3t_wrt_mean)+","+str(volt_g3t_deltamax)+","+str(integral_ig3t)+","+         
                    str(max(ig3b)) + "," +str(mean(ig3b))+","+ str(taus[5]) + "," + str(time_current[in_g3b])+ "," + str(vg3t[in_vg2])+","+str(volt_g3b_wrt_mean)+","+str(volt_g3b_deltamax)+","+str(integral_ig3b)+","+         
                    str(delta1[in_vdr])+","+str(delta2[in_vg1])+","+str(delta3[in_delta3])+","+str(delta4[in_vg2])+","+str(delta5[in_delta5])+","+str(delta6[in_vg3])+
                    ","+str(mean_delta_g1t_dr)+","+str(mean_delta_g1b_g1t)+","+str(mean_delta_g2t_g1b)+","+str(mean_delta_g2b_g2t)+","+
                    str(mean_delta_g3t_g3b)+","+str(mean_delta_g3b_g3t)+","+str(rate)+"\n")
        else:
            
            if os.path.exists(outfolder_csv+pico+"_"+run+"discharges_event.csv"):
                f = open(outfolder_csv+pico+"_"+run+"discharges_event.csv" ,"a")
                
            else:
                f = open(outfolder_csv+"/"+run+"_discharges_event.csv" ,"w")
                f.write("\n")
                f.write("pico,run,event,drift_pulseheight,drift_mean,drift_time,drift_voltage,driftvolt_mean,drift_deltamaxvolt, drift_integral"+ 
                        "G1T_pulseheight,G1T_mean,G1T_time,G1T_voltage,G1Tvolt_mean,G1T_deltamaxvolt,G1T_integral,"+
                        "G1B_pulseheight,G1B_mean,G1B_time,G1B_voltage,G1Bvolt_mean,G1B_deltamaxvolt,G1B_integral,"+
                        "G2T_pulseheight,G2T_mean,G2T_time,G2T_voltage,G2Tvolt_mean,G2T_deltamaxvolt,G2T_integral,"+ 
                        "G2B_pulseheight,G2B_mean,G2B_time,G2B_voltage,G2Bvolt_mean,G2B_deltamaxvolt,G2B_integral,"+
                        "G3T_pulseheight,G3T_mean,G3T_time,G3T_voltage,G3Tvolt_mean,G3T_deltamaxvolt,G3T_integral,"+
                        "G3B_pulseheight,G3B_mean,G3B_time,G3B_voltage,G3Bvolt_mean,G3B_deltamaxvolt,G3B_integral,"+
                        "deltav_g1t_dr,delta_g1b_g1t,delta_g2t_g1b,delta_g2b_g2t,delta_g3t_g2b,delta_g3b_g3t,"+
                        "mean_delta_g1t_dr,mean_delta_g1b_g1t,mean_delta_g2t_g1b,mean_delta_g2b_g2t,mean_delta_g3t_g3b,mean_delta_g3b_g3t\n")

            f.write(pico.split('O')[1]+","+run_label+","+str(entry)+","+ 
                    str(max_drift) + "," +str(mean(idrift))+","+ str(timestamp_current[in_drift]) + "," + str(vdrift[in_vdr]) + "," + str(volt_drift_wrt_mean) + "," + str(volt_drift_deltamax)+","+str(integral_idrift)+","+      
                    str(min(ig1t)) + "," +str(mean(ig1t))+"," + str(timestamp_current[in_g1t])+ "," + str(vg1t[in_vg1])+","+str(volt_g1t_wrt_mean)+","+str(volt_g1t_deltamax)+","+str(integral_ig1t)+","+   
                    str(max(ig1b)) + "," +str(mean(ig1b))+"," +  str(timestamp_current[in_g1b])+ "," + str(vg1b[in_vg1])+","+str(volt_g1b_wrt_mean)+","+str(volt_g1b_deltamax)+","+str(integral_ig1b)+","+   
                    str(min(ig2t)) + "," +str(mean(ig2t))+"," +  str(timestamp_current[in_g2t])+ "," + str(vg2t[in_vg2])+","+str(volt_g2t_wrt_mean)+","+str(volt_g2t_deltamax)+","+str(integral_ig2t)+","+      
                    str(max(ig2b)) + "," +str(mean(ig2b))+"," +  str(timestamp_current[in_g2b])+ "," + str(vg2b[in_vg2])+","+str(volt_g2b_wrt_mean)+","+str(volt_g2b_deltamax)+","+str(integral_ig2b)+","+         
                    str(min(ig3t)) + "," +str(mean(ig3t))+"," +  str(timestamp_current[in_g3t])+ "," + str(vg3t[in_vg2])+","+str(volt_g3t_wrt_mean)+","+str(volt_g3t_deltamax)+","+str(integral_ig3t)+","+         
                    str(max(ig3b)) + "," +str(mean(ig3b))+"," +  str(timestamp_current[in_g3b])+ "," + str(vg3t[in_vg2])+","+str(volt_g3b_wrt_mean)+","+str(volt_g3b_deltamax)+","+str(integral_ig3b)+","+         
                    str(delta1[in_vdr])+","+str(delta2[in_vg1])+","+str(delta3[in_delta3])+","+str(delta4[in_vg2])+","+str(delta5[in_delta5])+","+str(delta6[in_vg3])+
                    ","+str(mean_delta_g1t_dr)+","+str(mean_delta_g1b_g1t)+","+str(mean_delta_g2t_g1b)+","+str(mean_delta_g2b_g2t)+","+
                    str(mean_delta_g3t_g3b)+","+str(mean_delta_g3b_g3t)+"\n")
    '''

        
    graph_dr.Write()
    graph_g1t.Write()
    graph_g1b.Write()
    graph_g2t.Write()
    graph_g2b.Write()
    graph_g3t.Write()
    graph_g3b.Write()
    
    all_current = [graph_dr.Clone(), graph_g1t.Clone(), graph_g1b.Clone(), graph_g2t.Clone(), graph_g2b.Clone(), graph_g3t.Clone(), graph_g3b.Clone()]
    print_hist(outfolder, all_current, run+'_'+ str(entry)+'_all_currents', "APL")
    print_hist(outfolder, graph_dr.Clone(), run+'_'+str(entry)+'_drift',"APL")

    gr_vdrift = make_graph(20, time_voltage, vdrift, "graph_vdrift", "vdrift", "time(s)", "voltage(V)", ROOT.kBlack)
    gr_vg1t = make_graph(20, time_voltage, vg1t, "graph_vg1t", "vg1t", "time(s)", "voltage(V)", ROOT.kGreen)
    gr_vg1b = make_graph(20, time_voltage, vg1b, "graph_vg1b", "vg1b", "time(s)", "voltage(V)", ROOT.kGreen+3)
    gr_vg2t = make_graph(20, time_voltage, vg2t, "graph_vg2t", "vg2t", "time(s)", "voltage(V)", ROOT.kCyan)
    gr_vg2b = make_graph(20, time_voltage, vg2b, "graph_vg2b", "vg2b", "time(s)", "voltage(V)", ROOT.kCyan+3)
    gr_vg3t = make_graph(20, time_voltage, vg3t, "graph_vg3t", "vg3t", "time(s)", "voltage(V)", ROOT.kRed)
    gr_vg3b = make_graph(20, time_voltage, vg3b, "graph_vg3b", "vg3b", "time(s)", "voltage(V)", ROOT.kRed+3)
    
    gr_vg1t.Write() 
    gr_vg1b.Write() 
    gr_vg2t.Write() 
    gr_vg2b.Write() 
    gr_vg3t.Write() 
    gr_vg3b.Write()

    all_voltages = [gr_vdrift.Clone(), gr_vg1t.Clone(), gr_vg1b.Clone(), gr_vg2t.Clone(), gr_vg2b.Clone(), gr_vg3t.Clone(), gr_vg3b.Clone()]
    print_hist(outfolder, all_voltages, run+'_'+str(entry)+'_all_voltages', "APL")

    graph_delta1 = make_graph(20, time_voltage, delta1, "graph_delta1", "#Delta(G1T-Drift) "+tot_time, "time(s)", "Voltage(V)", ROOT.kBlack)
    graph_delta2 = make_graph(20, time_voltage, delta2, "graph_delta2", "#Delta(G1B-G1T) "+tot_time, "time(s)", "Voltage(V)", ROOT.kGreen)
    graph_delta3 = make_graph(20, time_voltage, delta3, "graph_delta3", "#Delta(G2T-G1B) "+tot_time, "time(s)", "Voltage(V)", ROOT.kGreen+3)
    graph_delta4 = make_graph(20, time_voltage, delta4, "graph_delta4", "#Delta(G2B-G2T) "+tot_time, "time(s)", "Voltage(V)", ROOT.kCyan)
    graph_delta5 = make_graph(20, time_voltage, delta5, "graph_delta5", "#Delta(G3T-G2B) "+tot_time, "time(s)", "Voltage(V)", ROOT.kCyan+3)
    graph_delta6 = make_graph(20, time_voltage, delta6, "graph_delta6", "#Delta(G3B-G3T) "+tot_time, "time(s)", "Voltage(V)", ROOT.kRed)
    
    graph_vdrift = make_graph(20, time_voltage, vdrift, "graph_vdrift", "V Drift "+tot_time, "time(s)", "Voltage(V)", ROOT.kBlack)
    print_hist(outfolder, graph_vdrift, run+'_'+str(entry)+'_vdrift', 'APL')
    
    if draw_volt:
        outf = '/eos/home-a/acagnott/www/GEM/graph_deltp10_p20/'+run+"_"+str(entry)
    
        print_hist(outf, graph_dr, run+'_'+str(entry)+'_graphIdrift', 'APL')
        print_hist(outf, graph_g1t, run+'_'+str(entry)+'_graphIg1t', 'APL')
        print_hist(outf, graph_g1b, run+'_'+str(entry)+'_graphIg1b', 'APL')
        print_hist(outf, graph_g2t, run+'_'+str(entry)+'_graphIg2t', 'APL')
        print_hist(outf, graph_g2b, run+'_'+str(entry)+'_graphIg2b', 'APL')
        print_hist(outf, graph_g3t, run+'_'+str(entry)+'_graphIg3t', 'APL')
        print_hist(outf, graph_g3b, run+'_'+str(entry)+'_graphIg3b', 'APL')
        print_hist(outf, gr_vdrift, run+'_'+str(entry)+'_graphVdrift', 'APL')
        print_hist(outf, gr_vg1t, run+'_'+str(entry)+'_graphVg1t', 'APL')
        print_hist(outf, gr_vg1b, run+'_'+str(entry)+'_graphVg1b', 'APL')
        print_hist(outf, gr_vg2t, run+'_'+str(entry)+'_graphVg2t', 'APL')
        print_hist(outf, gr_vg2b, run+'_'+str(entry)+'_graphVg2b', 'APL')
        print_hist(outf, gr_vg3t, run+'_'+str(entry)+'_graphVg3t', 'APL')
        print_hist(outf, gr_vg3b, run+'_'+str(entry)+'_graphVg3b', 'APL')
        print_hist(outf, graph_delta1, run+'_'+str(entry)+'_graphDeltaV_g1t_dr', 'APL')    
        print_hist(outf, graph_delta2, run+'_'+str(entry)+'_graphDeltaV_g1b_g1t', 'APL')    
        print_hist(outf, graph_delta3, run+'_'+str(entry)+'_graphDeltaV_g2t_g1b', 'APL')    
        print_hist(outf, graph_delta4, run+'_'+str(entry)+'_graphDeltaV_g2b_g2t', 'APL')    
        print_hist(outf, graph_delta5, run+'_'+str(entry)+'_graphDeltaV_g3t_g2b', 'APL')    
        print_hist(outf, graph_delta6, run+'_'+str(entry)+'_graphDeltaV_g3b_g3t', 'APL')    

    graph_delta1.Write()
    graph_delta2.Write()
    graph_delta3.Write()
    graph_delta4.Write()
    graph_delta5.Write()
    graph_delta6.Write()
    
    all_deltaV = [graph_delta1.Clone(), graph_delta2.Clone(), graph_delta3.Clone(), graph_delta4.Clone(), graph_delta5.Clone(), graph_delta6.Clone()]
    print_hist(outfolder, all_deltaV, run+'_'+ str(entry)+'_all_deltaV', "APL")
             
    return taus, ph, max_drift

def write_csv(data, run, entry, optwrite = 'w'):
    # data = 'Goliath' or 'LABGEM_scariche/12_01_22'
    # run = 'PICO1_run00XX'
    # entry = (int)
    
    #data-->
    
    infile = ROOT.TFile.Open("/eos/home-a/adeiorio/GEM/"+data+"/"+run+"_skim.root")
    tree = infile.Get('t1')
    tree.GetEntry(entry)
    
    pico = run.split("_")[0] #PICOX
    run_label = run.split("_")[1] #run00XX
    
    #saving values to write--> to save as string to write on csv file
    
    chs = ['drift', 'G1T', 'G1B', 'G2T', 'G2B', 'G3T', 'G3B'] #to capitalize
    deltas = ['g1t_dr', 'g1b_g1t', 'g2t_g1b', 'g2b_g2t', 'g3t_g2b', 'g3b_g3t']
    curr = {'drift': tree.IDRIFT, 'G1T': tree.IG1T, 'G1B': tree.IG1B, 'G2T': tree.IG2T, 'G2B': tree.IG2B, 'G3T': tree.IG3T, 'G3B': tree.IG3B}
    
    if max(tree.IDRIFT)>abs(min(tree.IDRIFT)): max_drift = max(tree.IDRIFT)
    else: max_drift = min(tree.IDRIFT)
    
    curr_max = {'drift': max_drift, 'G1T': min(tree.IG1T), 'G1B': max(tree.IG1B), 'G2T': min(tree.IG2T), 'G2B': min(tree.IG2B),'G3T': min(tree.IG3T), 'G3B': max(tree.IG3B)}
    index_curr =  {'drift': Get_index(curr['drift'], max_drift), 'G1T': Get_index(curr['G1T'], min(tree.IG1T)), 'G1B': Get_index(curr['G1B'], max(tree.IG1B)), 
                   'G2T': Get_index(curr['G2T'], min(tree.IG2T)), 'G2B': Get_index(curr['G2B'], min(tree.IG2B)), 
                   'G3T': Get_index(curr['G3T'], min(tree.IG3T)), 'G3B': Get_index(curr['G3B'], max(tree.IG3B)) }

    integral = {'drift': tree.INTEGRAL_IDRIFT, 'G1T': tree.INTEGRAL_IG1T, 'G1B': tree.INTEGRAL_IG1B, 'G2T': tree.INTEGRAL_IG2T,'G2B': tree.INTEGRAL_IG2B, 'G3T': tree.INTEGRAL_IG3T, 'G3B': tree.INTEGRAL_IG3B}
    
    volt = {'drift': tree.VDRIFT, 'G1T': tree.VG1T, 'G1B': tree.VG1B, 'G2T': tree.VG2T, 'G2B': tree.VG2B,'G3T': tree.VG3T, 'G3B': tree.VG3B}
    deltav = {'g1t_dr': tree.DeltaV_drg1t, 'g1b_g1t':tree.DeltaV_g1tg1b, 'g2t_g1b':tree.DeltaV_g1bg2t, 'g2b_g2t':tree.DeltaV_g2tg2b, 'g3t_g2b':tree.DeltaV_g2bg3t, 'g3b_g3t':tree.DeltaV_g3tg3b}
    deltav_var = {'g1t_dr': tree.DeltaV_drg1t_var, 'g1b_g1t':tree.DeltaV_g1tg1b_var, 'g2t_g1b':tree.DeltaV_g1bg2t_var, 'g2b_g2t':tree.DeltaV_g2tg2b_var, 'g3t_g2b':tree.DeltaV_g2bg3t_var, 'g3b_g3t':tree.DeltaV_g3tg3b_var}

    index_deltas = {'g1t_dr': Get_index(deltav_var['g1t_dr'],max(deltav_var['g1t_dr'])), 'g1b_g1t': Get_index(deltav_var['g1b_g1t'], max(deltav_var['g1b_g1t'])), 
                    'g2t_g1b': Get_index(deltav_var['g2t_g1b'], max(deltav_var['g2t_g1b'])), 'g2b_g2t': Get_index(deltav_var['g2b_g2t'], max(deltav_var['g2b_g2t'])), 
                    'g3t_g2b': Get_index(deltav_var['g3t_g2b'], max(deltav_var['g3t_g2b'])), 'g3b_g3t': Get_index(deltav_var['g3b_g3t'], max(deltav_var['g3b_g3t']))}
    index_volt = {'drift': index_deltas['g1t_dr'], 'G1T': index_deltas['g1b_g1t'], 'G1B': index_deltas['g1b_g1t'], 
                  'G2T': index_deltas['g2t_g1b'], 'G2B': index_deltas['g2t_g1b'], 'G3T': index_deltas['g3b_g3t'], 'G3B': index_deltas['g3b_g3t']}

    if hasattr(tree, 'timestamp_current'):
        time_current = tree.timestamp_current
        time_voltage = tree.timestamp_voltage
    else:
        time_current = tree.time_current
        time_voltage = tree.time_voltage
        
    variables_to_write['pico'] = int(pico.split('O')[1])
    variables_to_write['run'] = int(run_label.replace("run",""))
    variables_to_write['event'] = (entry)

    for ch in chs:
        variables_to_write[ch+'_pulseheight'] = (curr_max[ch])
        variables_to_write[ch+'_mean'] = (mean(curr[ch]))
        variables_to_write[ch+'_time'] = (time_current[index_curr[ch]])
        variables_to_write[ch+'_voltage'] = (volt[ch][index_volt[ch]])

        volt_wrt_mean = volt[ch][index_volt[ch]] - mean(volt[ch])
        volt_deltamax = abs(max(volt[ch]) - min(volt[ch]))

    
        variables_to_write[ch+'volt_mean'] = (volt_wrt_mean)
        variables_to_write[ch+'_deltamaxvolt'] = (volt_deltamax)
        variables_to_write[ch+'_integral'] = (integral[ch])
    

    for delt in deltas :
        variables_to_write['deltav_'+delt] = (deltav[delt][index_deltas[delt]])
        variables_to_write['mean_deltav_'+delt] = (mean(deltav[delt]))
    
    # writing csv 
    outfolder_csv = "/eos/home-a/acagnott/GEM_plot/"+data+"/"
    
    f = open(outfolder_csv+pico+'discharges_event.csv', optwrite)
    
    list_variables = variables_to_write.keys()
    
    if optwrite =='w':
        # without tau --> to add (?)
        for var in list_variables: f.write(var+",")
        f.write("\n")
    

    for var in list_variables:
        if var != variables_to_write.keys()[-1]:
            f.write(str(variables_to_write[var])+",")
            #print var , variables_to_write[var]
        else:
            f.write(str(variables_to_write[var])+"\n")
    


def graph_event(run, entry, write_file=False):
    infile = ROOT.TFile.Open("/eos/home-a/adeiorio/GEM/Goliath/"+run+"_skim.root")
    print infile
    outfolder = "/eos/home-a/acagnott/GEM_plot/graphsIndSignals/"+run+"_"+str(entry)
    if not os.path.exists(outfolder):
        os.mkdir(outfolder)
    outfile = ROOT.TFile.Open(outfolder+"/graphs.root","RECREATE")
    pico = run.split("_")[0]
    tree = infile.Get("t1")

    tree.GetEntry(entry)
    idrift = tree.IDRIFT
    ig1t = tree.IG1T
    ig1b = tree.IG1B
    ig2t = tree.IG2T
    ig2b = tree.IG2B
    ig3t = tree.IG3T
    ig3b = tree.IG3B
    delta1 = tree.DeltaV_drg1t
    delta2 = tree.DeltaV_g1tg1b
    delta3 = tree.DeltaV_g1bg2t
    delta4 = tree.DeltaV_g2tg2b
    delta5 = tree.DeltaV_g2bg3t
    delta6 = tree.DeltaV_g3tg3b
    time_current = tree.time_current
    
    

    graph_dr = make_graph(1900, tree.time_current, idrift, "graph_idrift", "idrift", "time(s)", "current(nA)", ROOT.kBlack)
    graph_g1t = make_graph(1900, tree.time_current, ig1t, "graph_ig1t", "ig1t", "time(s)", "current(nA)", ROOT.kGreen)
    graph_g1b = make_graph(1900, tree.time_current, ig1b, "graph_ig1b", "ig1b", "time(s)", "current(nA)", ROOT.kGreen+3)
    graph_g2t = make_graph(1900, tree.time_current, ig2t, "graph_ig2t", "ig2t", "time(s)", "current(nA)", ROOT.kCyan)
    graph_g2b = make_graph(1900, tree.time_current, ig2b, "graph_ig2b", "ig2b", "time(s)", "current(nA)", ROOT.kCyan+3)    
    graph_g3t = make_graph(1900, tree.time_current, ig3t, "graph_ig3t", "ig3t", "time(s)", "current(nA)", ROOT.kRed)
    graph_g3b = make_graph(1900, tree.time_current, ig3b, "graph_ig3b", "ig3b", "time(s)", "current(nA)", ROOT.kRed+3)
 
    graph_dr.Write()
    graph_g1t.Write()
    graph_g1b.Write()
    graph_g2t.Write()
    graph_g2b.Write()
    graph_g3t.Write()
    graph_g3b.Write()
    
    all_current = [graph_dr.Clone(), graph_g1t.Clone(), graph_g1b.Clone(), graph_g2t.Clone(), graph_g2b.Clone(), graph_g3t.Clone(), graph_g3b.Clone()]
    print_hist(outfolder, all_current, run+'_'+ str(entry)+'_all_currents', "APL")
    
    graph_delta1 = make_graph(20, tree.time_voltage, delta1, "graph_delta1", "#Delta(G1T-Drift)", "time(s)", "Voltage(V)", ROOT.kBlack)
    graph_delta2 = make_graph(20, tree.time_voltage, delta2, "graph_delta2", "#Delta(G1B-G1T)", "time(s)", "Voltage(V)", ROOT.kGreen)
    graph_delta3 = make_graph(20, tree.time_voltage, delta3, "graph_delta3", "#Delta(G2T-G1B)", "time(s)", "Voltage(V)", ROOT.kGreen+3)
    graph_delta4 = make_graph(20, tree.time_voltage, delta4, "graph_delta4", "#Delta(G2B-G2T)", "time(s)", "Voltage(V)", ROOT.kCyan)
    graph_delta5 = make_graph(20, tree.time_voltage, delta5, "graph_delta5", "#Delta(G3T-G2B)", "time(s)", "Voltage(V)", ROOT.kCyan+3)
    graph_delta6 = make_graph(20, tree.time_voltage, delta6, "graph_delta6", "#Delta(G3B-G3T)", "time(s)", "Voltage(V)", ROOT.kRed)
    
    graph_delta1.Write()
    graph_delta2.Write()
    graph_delta3.Write()
    graph_delta4.Write()
    graph_delta5.Write()
    graph_delta6.Write()
    
    all_deltaV = [graph_delta1.Clone(), graph_delta2.Clone(), graph_delta3.Clone(), graph_delta4.Clone(), graph_delta5.Clone(), graph_delta6.Clone()]
    print_hist(outfolder, all_deltaV, run+'_'+ str(entry)+'_all_deltaV', "APL")
    
    in_drift = Get_index(idrift, min(idrift))
    in_g1t = Get_index(ig1t, min(ig1t))
    in_g1b = Get_index(ig1b, min(ig1b))
    in_g2t = Get_index(ig2t, min(ig2t))
    in_g2b = Get_index(ig2b, min(ig2b))
    in_g3t = Get_index(ig3t, min(ig3t))
    in_g3b = Get_index(ig3b, min(ig3b))
    
    ph = [min(ig1t), min(ig1b), min(ig2t), min(ig2b), min(ig3t), min(ig3b)]
    

    '''if write_file:
        if '0001' in run:
            f = open("/eos/home-a/acagnott/GEM_plot/"+pico+"_indsignals_fit.csv" ,"w")
        else:
            f = open("/eos/home-a/acagnott/GEM_plot/"+pico+"_indsignals_fit.csv" ,"a")
        f.write("\n")
        f.write(run+","+str(entry)+",drift(ph),G1T(ph),G1B(ph),G2T(ph),G2B(ph),G3T(ph),G3B(ph) \n")
    
        f.write(" , ,"+str(min(idrift))+","+str(min(ig1t))+","+str(min(ig1b))+"," +str(min(ig2t))+","+str(min(ig2b))+","+str(min(ig3t))+","+str(min(ig3b))+"\n")
    
        f.write("time, ,"+str(time_current[in_drift])+","+str(time_current[in_g1t])+","+str(time_current[in_g1b])+","+str(time_current[in_g2t])+","+str(time_current[in_g2b])+","+str(time_current[in_g3t])+","+str(time_current[in_g3b])+"\n")
        f.write("delta V, in corrispondenza di time:, delta(g1t-dr),(g1b-g1t),(g2t-g1b),(g2b-g2t),(g3t-g2b),(g3b-g3t) \n")
        f.write(" , ,"+str(delta1[in_g1t])+","+str(delta2[in_g1b])+","+str(delta3[in_g2t])+","+str(delta4[in_g2b])+","+str(delta5[in_g3t])+","+str(delta6[in_g3b])+"\n")
    
    '''

def fit_exp(graph, start, stop, top= True):
    if top:
        fitf = ROOT.TF1("fitf", "-expo", start, stop)
    else:
        fitf = ROOT.TF1("fitf", "expo", start, stop)

    print("fitting graph in [", start," and ", stop, "]")
    #fitf.SetParameter(1, -0.1)
    graph.Fit(fitf,"R")
    return fitf.GetParameter(1)


def Get_index(array, value, b=False):
    for i, val in enumerate(array):     
        if b :
            if abs(val) == value : 
                index = i 
        else :
            if val == value : 
                index = i 
    return index


def write_volt_pulseh_ratio(run, entry):

    infile = ROOT.TFile.Open("/eos/home-a/adeiorio/GEM/Goliath/"+run+"_skim.root")
    #print infile
    outfolder = "/eos/home-a/acagnott/GEM_plot/graphsdischarges/"+run+"_"+str(entry)
    if not os.path.exists(outfolder):
        os.mkdir(outfolder)
    
    pico = run.split("_")[0]
    tree = infile.Get("t1")    
    
    tree.GetEntry(entry)

    #idrift = tree.IDRIFT
    ig1t = tree.IG1T
    ig1b = tree.IG1B
    ig2t = tree.IG2T
    ig2b = tree.IG2B
    ig3t = tree.IG3T
    ig3b = tree.IG3B
    #delta1 = tree.DeltaV_drg1t
    deltag1 = tree.DeltaV_g1tg1b
    #delta3 = tree.DeltaV_g1bg2t
    deltag2 = tree.DeltaV_g2tg2b
    #delta5 = tree.DeltaV_g2bg3t
    deltag3 = tree.DeltaV_g3tg3b

    mean_volt_g1 = mean(deltag1)
    mean_volt_g2 = mean(deltag2)
    mean_volt_g3 = mean(deltag3)
    
    if abs(max(deltag1)-mean_volt_g1)>abs(min(deltag1)-mean_volt_g1): max_volt_g1 = max(deltag1)
    else : max_volt_g1 = min(deltag1)
    if abs(max(deltag2)-mean_volt_g2)>abs(min(deltag2)-mean_volt_g2): max_volt_g2 = max(deltag2)
    else : max_volt_g2 = min(deltag2)
    if abs(max(deltag3)-mean_volt_g3)>abs(min(deltag3)-mean_volt_g3): max_volt_g3 = max(deltag3)
    else : max_volt_g3 = min(deltag3)

    pulseh_g1 = max([abs(min(ig1t)), abs(max(ig1b))])
    pulseh_g2 = max([abs(min(ig2t)), abs(max(ig2b))])
    pulseh_g3 = max([abs(min(ig3t)), abs(max(ig3b))])
                    
    volt_g1_wrt_mean = max_volt_g1 - mean_volt_g1
    volt_g1_deltamax =abs(max(deltag1) - min(deltag1))
    volt_g2_wrt_mean = max_volt_g2 - mean_volt_g2
    volt_g1_deltamax =abs(max(deltag2) - min(deltag2))
    volt_g3_wrt_mean = max_volt_g3 - mean_volt_g3
    volt_g1_deltamax =abs(max(deltag3) - min(deltag3))

    ratio1 = abs(volt_g1/pulseh_g1)
    ratio2 = abs(volt_g2/pulseh_g2)
    ratio3 = abs(volt_g3/pulseh_g3)
    
    f = open("volt_pulseh_ratio.txt", "a")
    f.write("\n " + run +"  "+ str(entry) +"\n")
    f.write("G1T voltage(V): "+str(volt_g1)+";  deltaG1_mean(V) ="+str(mean_volt_g1)+" \n") 
    f.write("    pulse height(nA): "+str(pulseh_g1)+"\n")
    f.write("    ratio (V/nA): "+ str(ratio1) +" -> "+str(ratio1*10**9)+" (Ohm) \n")
    f.write("G2T voltage(V): "+str(volt_g2)+";  deltaG2_mean(V) ="+str(mean_volt_g2)+" \n") 
    f.write("    pulse height(nA): "+str(pulseh_g2)+"\n")
    f.write("    ratio (V/nA): "+ str(ratio2) +" -> "+str(ratio2*10**9)+" (Ohm) \n")
    f.write("G3T voltage(V): "+str(volt_g3)+";  deltaG3_mean(V) ="+str(mean_volt_g3)+" \n") 
    f.write("    pulse height(nA): "+str(pulseh_g3)+"\n")
    f.write("    ratio (V/nA): "+ str(ratio3) +" -> "+str(ratio3*10**9)+" (Ohm) \n")
    
    return ratio1, ratio2, ratio3

def get_max_voltage(run, entry):
    
    infile = ROOT.TFile.Open("/eos/home-a/adeiorio/GEM/Goliath/"+run+"_skim.root")
    #print infile
    outfolder = "/eos/home-a/acagnott/GEM_plot/graphsdischarges/"+run+"_"+str(entry)
    if not os.path.exists(outfolder):
        os.mkdir(outfolder)
    
    pico = run.split("_")[0]
    tree = infile.Get("t1")    
    
    tree.GetEntry(entry)

    idrift = tree.IDRIFT
    ig1t = tree.IG1T
    ig1b = tree.IG1B
    ig2t = tree.IG2T
    ig2b = tree.IG2B
    ig3t = tree.IG3T
    ig3b = tree.IG3B
    vdrift = tree.VDRIFT
    vg1t = tree.VG1T
    vg1b = tree.VG1B
    vg2t = tree.VG2T
    vg2b = tree.VG2B
    vg3t = tree.VG3T
    vg3b = tree.VG3B
    #delta1 = tree.DeltaV_drg1t
    deltag1 = tree.DeltaV_g1tg1b
    #delta3 = tree.DeltaV_g1bg2t
    deltag2 = tree.DeltaV_g2tg2b
    #delta5 = tree.DeltaV_g2bg3t
    deltag3 = tree.DeltaV_g3tg3b

    pulseh_drift = max([abs(min(idrift)), abs(max(idrift))])
    pulseh_g1t = abs(min(ig1t)) 
    pulseh_g1b = abs(max(ig1b))
    pulseh_g2t = abs(min(ig2t)) 
    pulseh_g2b = abs(max(ig2b))
    pulseh_g3t = abs(min(ig3t)) 
    pulseh_g3b = abs(max(ig3b))

    in_drift = Get_index(idrift, pulseh_drift, b = True)
    in_g1t = Get_index(ig1t, min(ig1t))
    in_g1b = Get_index(ig1b, max(ig1b))
    in_g2t = Get_index(ig2t, min(ig2t))
    in_g2b = Get_index(ig2b, max(ig2b))
    in_g3t = Get_index(ig3t, min(ig3t))
    in_g3b = Get_index(ig3b, max(ig3b))
    
    mean_volt_drift = mean(vdrift)
    mean_volt_g1t = mean(vg1t)
    mean_volt_g1b = mean(vg1b)
    mean_volt_g2t = mean(vg2t)
    mean_volt_g2b = mean(vg2b)
    mean_volt_g3t = mean(vg3t)
    mean_volt_g3b = mean(vg3b)
    
    if abs(max(vdrift)-mean_volt_drift)>abs(min(vdrift)-mean_volt_drift): max_volt_drift = max(vdrift)
    else : max_volt_drift = min(vdrift)
    if abs(max(vg1t)-mean_volt_g1t)>abs(min(vg1t)-mean_volt_g1t): max_volt_g1t = max(vg1t)
    else : max_volt_g1t = min(vg1t)
    if abs(max(vg1b)-mean_volt_g1t)>abs(min(vg1b)-mean_volt_g1t): max_volt_g1b = max(vg1b)
    else : max_volt_g1b = min(vg1b)
    if abs(max(vg2t)-mean_volt_g2t)>abs(min(vg2t)-mean_volt_g2t): max_volt_g2t = max(vg2t)
    else : max_volt_g2t = min(vg2t)
    if abs(max(vg2b)-mean_volt_g2b)>abs(min(vg2b)-mean_volt_g2b): max_volt_g2b = max(vg2b)
    else : max_volt_g2b = min(vg2b)
    if abs(max(vg3t)-mean_volt_g3t)>abs(min(vg3t)-mean_volt_g3t): max_volt_g3t = max(vg3t)
    else : max_volt_g3t = min(vg3t)
    if abs(max(vg3b)-mean_volt_g3b)>abs(min(vg3b)-mean_volt_g3b): max_volt_g3b = max(vg3b)
    else : max_volt_g3b = min(vg3b)

    volt_drift_wrt_mean = max_volt_drift - mean_volt_drift
    volt_drift_deltamax = abs(max(vdrift) - min(vdrift))
    volt_drift_center = vdrift[in_drift]
    volt_g1t_wrt_mean = max_volt_g1t - mean_volt_g1t
    volt_g1t_deltamax = abs(max(vg1t) - min(vg1t))
    volt_g1t_center = vg1t[in_g1t]
    volt_g1b_wrt_mean = max_volt_g1b - mean_volt_g1b
    volt_g1b_deltamax = abs(max(vg1b) - min(vg1b))
    volt_g1b_center = vg1b[in_g1b]
    volt_g2t_wrt_mean = max_volt_g2t - mean_volt_g2t
    volt_g2t_deltamax = abs(max(vg2t) - min(vg2t))
    volt_g2t_center = vg2t[in_g2t]
    volt_g2b_wrt_mean = max_volt_g2b - mean_volt_g2b
    volt_g2b_deltamax = abs(max(vg2b) - min(vg2b))
    volt_g2b_center = vg2b[in_g2b]
    volt_g3t_wrt_mean = max_volt_g3t - mean_volt_g3t
    volt_g3t_deltamax = abs(max(vg3t) - min(vg3t))
    volt_g3t_center = vg3t[in_g3t]
    volt_g3b_wrt_mean = max_volt_g3b - mean_volt_g3b
    volt_g3b_deltamax = abs(max(vg3b) - min(vg3b))
    volt_g3b_center = vg3b[in_g3b]
    
    values = { "volt_drift_wrt_mean": volt_drift_wrt_mean, "volt_drift_deltamax": volt_drift_deltamax, "volt_drift_center":volt_drift_center, 
               "pulseheight_drift": pulseh_drift,
               "volt_g1t_wrt_mean": volt_g1t_wrt_mean, "volt_g1t_deltamax": volt_g1t_deltamax, "volt_g1t_center":volt_g1t_center, 
               "pulseheight_g1t": pulseh_g1t,
               "volt_g1b_wrt_mean": volt_g1b_wrt_mean, "volt_g1b_deltamax": volt_g1b_deltamax, "volt_g1b_center":volt_g1b_center,
               "pulseheight_g1b": pulseh_g1b,
               "volt_g2t_wrt_mean": volt_g2t_wrt_mean, "volt_g2t_deltamax": volt_g2t_deltamax, "volt_g2t_center":volt_g2t_center,
               "pulseheight_g2t": pulseh_g2t,
               "volt_g2b_wrt_mean": volt_g2b_wrt_mean, "volt_g2b_deltamax": volt_g2b_deltamax, "volt_g2b_center":volt_g2b_center,
               "pulseheight_g2b": pulseh_g2b,
               "volt_g3t_wrt_mean": volt_g3t_wrt_mean, "volt_g3t_deltamax": volt_g3t_deltamax, "volt_g3t_center":volt_g3t_center,
               "pulseheight_g3t": pulseh_g3t,
               "volt_g3b_wrt_mean": volt_g3b_wrt_mean, "volt_g3b_deltamax": volt_g3b_deltamax, "volt_g3b_center":volt_g3b_center,
               "pulseheight_g3b": pulseh_g3b
           }

    return values


def save_histo(folder, histo):
    c1 = ROOT.TCanvas()
    histo.Draw("colz")
    c1.Print(folder+histo.GetName()+".png")

def write_rate(pio, run, dis_rate):
    n_run = int(run.split("00")[1])
    time = dict_run[pico][run]["tot_time"]
    dis_rate = dis_count/time
    print dis_rate
    if '0001' in opt.input:
        f = open("dis_rate"+pico+".txt", "w")
    else:
        f = open("dis_rate"+pico+".txt", "a")
    f.write(str(n_run)+", "+ str(dis_rate)+"\n")


