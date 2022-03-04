import ROOT
from array import array
from datetime import datetime
import optparse
from utils import *
import os
from scipy.signal import find_peaks
import numpy as np
from peak import *

def simultaneous_analysis(peaksG3B, ig3t, ig2b, ig2t, ig1t, ig1b, vg3t, vg2b, vg2t, vg1b, vg1t, outfile, delta_t = 10000):  #delta_t=10000s
    # starting from peaksG3B -> max prob discharges
    i = 0
    prev_t_peak = 0
    for p in peaksG3B:
        
        entry_pg3b = p.entry
        time_pg3b = p.time
        times = p.t_array
        pnt_to_eof = len(ig3t) - entry_pg3b
        outfile.cd()
        
        if p.t_peak==prev_t_peak : i+=1
        elif p.t_peak != prev_t_peak : i = 0
        
        outfile.mkdir("peak_"+str(p.t_peak)+"_"+str(i))
        if entry_pg3b<250:
            entry_start = 0
            entry_stop = entry_pg3b*2
            gr_curr_g3b = p.graph_peak(pnt_to_plot = entry_pg3b*2)
            gr_volt_g3b = p.graph_voltage(pnt_to_plot = entry_pg3b*2)
        elif pnt_to_eof < 250:
            entry_start = entry_pg3b - pnt_to_eof
            entry_stop = len(ig3t)
            gr_curr_g3b = p.graph_peak(pnt_to_plot = pnt_to_eof*2)
            gr_volt_g3b = p.graph_voltage(pnt_to_plot = pnt_to_eof*2)
        else:
            entry_start = entry_pg3b - 250
            entry_stop = entry_pg3b + 250
            gr_curr_g3b = p.graph_peak(pnt_to_plot = 500)
            gr_volt_g3b = p.graph_voltage(pnt_to_plot = 500)
        
        if entry_stop > len(vg3t): entry_stop_volt = len(vg3t)
        else: entry_stop_volt = entry_stop
        gr_curr_g3b.SetTitle("G3B current")
        gr_volt_g3b.SetTitle("G3B voltage")
        gr_curr_g3b.SetName("G3B_current")
        gr_volt_g3b.SetName("G3B_voltage")

        gr_curr_g3t = ROOT.TGraph(entry_stop-entry_start, times[entry_start: entry_stop], ig3t[entry_start:entry_stop])
        gr_curr_g3t.SetName("G3T_current")
        gr_curr_g3t.SetTitle("G3T current")
        gr_curr_g3t.SetMarkerStyle(20)
        gr_curr_g3t.GetXaxis().SetTitle("time (s)")
        gr_curr_g3t.GetYaxis().SetTitle("current (nA)")
        gr_volt_g3t = ROOT.TGraph(entry_stop-entry_start, times[entry_start: entry_stop], vg3t[entry_start:entry_stop_volt])
        gr_volt_g3t.SetName("G3T_voltage")
        gr_volt_g3t.SetTitle("G3T voltage")
        gr_volt_g3t.SetMarkerStyle(20)
        gr_volt_g3t.GetXaxis().SetTitle("time (s)")
        gr_volt_g3t.GetYaxis().SetTitle("voltage (V)")

        gr_curr_g2b = ROOT.TGraph(entry_stop-entry_start, times[entry_start: entry_stop], ig2b[entry_start:entry_stop])
        gr_curr_g2b.SetName("G2B_current")
        gr_curr_g2b.SetTitle("G2B current")
        gr_curr_g2b.SetMarkerStyle(20)
        gr_curr_g2b.GetXaxis().SetTitle("time (s)")
        gr_curr_g2b.GetYaxis().SetTitle("current (nA)")
        gr_volt_g2b = ROOT.TGraph(entry_stop-entry_start, times[entry_start: entry_stop], vg2b[entry_start:entry_stop_volt])
        gr_volt_g2b.SetName("G2B_voltage")
        gr_volt_g2b.SetTitle("G2B voltage")
        gr_volt_g2b.GetXaxis().SetTitle("time (s)")
        gr_volt_g2b.GetYaxis().SetTitle("voltage (V)")
        
        gr_curr_g2t = ROOT.TGraph(entry_stop-entry_start, times[entry_start: entry_stop], ig2t[entry_start:entry_stop])
        gr_curr_g2t.SetName("G2T_current")
        gr_curr_g2t.SetTitle("G2T current")
        gr_curr_g2t.SetMarkerStyle(20)
        gr_curr_g2t.GetXaxis().SetTitle("time (s)")
        gr_curr_g2t.GetYaxis().SetTitle("current (n A)")
        gr_volt_g2t = ROOT.TGraph(entry_stop-entry_start, times[entry_start: entry_stop], vg2t[entry_start:entry_stop_volt])
        gr_volt_g2t.SetName("G2T_voltage")
        gr_volt_g2t.SetTitle("G2T voltage")
        gr_volt_g2t.GetXaxis().SetTitle("time (s)")
        gr_volt_g2t.GetYaxis().SetTitle("voltage (V)")

        gr_curr_g1b = ROOT.TGraph(entry_stop-entry_start, times[entry_start: entry_stop], ig1b[entry_start:entry_stop])
        gr_curr_g1b.SetName("G1B_current")
        gr_curr_g1b.SetTitle("G1B current")
        gr_curr_g1b.SetMarkerStyle(20)
        gr_curr_g1b.GetXaxis().SetTitle("time (s)")
        gr_curr_g1b.GetYaxis().SetTitle("current (nA)")
        gr_volt_g1b = ROOT.TGraph(entry_stop-entry_start, times[entry_start: entry_stop], vg1b[entry_start:entry_stop_volt])
        gr_volt_g1b.SetName("G1B_voltage") 
        gr_volt_g1b.SetTitle("G1B voltage")
        gr_volt_g1b.SetMarkerStyle(20)
        gr_volt_g1b.GetXaxis().SetTitle("time (s)")
        gr_volt_g1b.GetYaxis().SetTitle("voltage (V)")

        gr_curr_g1t = ROOT.TGraph(entry_stop-entry_start, times[entry_start: entry_stop], ig1t[entry_start:entry_stop])
        gr_curr_g1t.SetName("G1T_current")
        gr_curr_g1t.SetTitle("G1T current")
        gr_curr_g1t.SetMarkerStyle(20)
        gr_curr_g1t.GetXaxis().SetTitle("time (s)")
        gr_curr_g1t.GetYaxis().SetTitle("current (nA)")
        gr_volt_g1t = ROOT.TGraph(entry_stop-entry_start, times[entry_start: entry_stop], vg1t[entry_start:entry_stop_volt])
        gr_volt_g1t.SetName("G1T_voltage") 
        gr_volt_g1t.SetTitle("G1T voltage")
        gr_volt_g1t.SetMarkerStyle(20)
        gr_volt_g1t.GetXaxis().SetTitle("time (s)")
        gr_volt_g1t.GetYaxis().SetTitle("voltage (V)")
        
        gr_curr_drift = ROOT.TGraph(entry_stop-entry_start, times[entry_start: entry_stop], idrift[entry_start:entry_stop])
        gr_curr_drift.SetName("DRIFT_current")
        gr_curr_drift.SetTitle("DRIFT current")
        gr_curr_drift.SetMarkerStyle(20)
        gr_curr_drift.GetXaxis().SetTitle("time (s)")
        gr_curr_drift.GetYaxis().SetTitle("current (nA)")
        gr_volt_drift = ROOT.TGraph(entry_stop-entry_start, times[entry_start: entry_stop], vdrift[entry_start:entry_stop_volt])
        gr_volt_drift.SetName("DRIFT_voltage") 
        gr_volt_drift.SetTitle("DRIFT voltage")
        gr_volt_drift.SetMarkerStyle(20)
        gr_volt_drift.GetXaxis().SetTitle("time (s)")
        gr_volt_drift.GetYaxis().SetTitle("voltage (V)")
        
        outfile.cd("peak_"+str(p.t_peak)+"_"+str(i))
        gr_curr_drift.Write()
        gr_volt_drift.Write()
        gr_curr_g3b.Write()
        gr_volt_g3b.Write()
        gr_curr_g3t.Write()
        gr_volt_g3t.Write()
        gr_curr_g2b.Write()
        gr_volt_g2b.Write()
        gr_curr_g2t.Write()
        gr_volt_g2t.Write()
        gr_curr_g1b.Write()
        gr_volt_g1b.Write()
        gr_curr_g1t.Write()
        gr_volt_g1t.Write()

        prev_t_peak=p.t_peak


def fit_hist(hist):
    print("fitting "+ hist.GetName())
    hist_to_fit = hist.Clone()
    xmin = hist_to_fit.GetXaxis().GetXmin()
    xmax = hist_to_fit.GetXaxis().GetXmax()
    g = ROOT.TF1("g", "gaus", xmin, xmax)
    hist_to_fit.Fit(g)
    mean, sigma = g.GetParameter(1), g.GetParameter(2)
    return mean, sigma

def peak_counter(hist, heights, n_bin, outfile, folder):
    for h in heights:
        if h < 50000: 
            hist.AddBinContent(hist.FindBin(h), 1)
        else: 
            hist.AddBinContent(n_bin, 1)
        
    outfile.cd()
    hist.Write()
    c1 = ROOT.TCanvas(hist.GetName(), "c1")
    hist.Draw()
    c1.SetLogy()
    c1.SetLogx()
    c1.Print(folder+"/"+hist.GetName()+".png")
    c1.Print(folder+"/"+hist.GetName()+".root")

def event_to_write(idrift, ig1t, ig1b, ig2t, ig2b, ig3t, ig3b, tresholds):
    #tresholds = [uptres_idrift, dwtres_idrift, uptres_ig1t, dwtres_ig1t, uptres_ig1b, dwtres_ig1b, uptres_ig2t, dwtres_ig2t, uptres_ig2b, 
    #         dwtres_ig2b, uptres_ig3t, dwtres_ig3t, uptres_ig3b, dwtres_ig3b]
    
    currs = [idrift, ig1t, ig1b, ig2t, ig2b, ig3t, ig3b]
    flag1, flag2, flag3, flag4, flag5, flag6, flag7 = True, True, True, True, True, True, True
    index = 0
    for curr_val in idrift:
        flag1 *= (curr_val>tresholds[index*2] or curr_val<tresholds[index*2+1])
    index+=1
    for curr_val in ig1t:
        flag2 *= (curr_val>tresholds[index*2] or curr_val<tresholds[index*2+1])
    index+=1
    for curr_val in ig1b:
        flag3 *= (curr_val>tresholds[index*2] or curr_val<tresholds[index*2+1])
    index+=1
    for curr_val in ig2t:
        flag4 *= (curr_val>tresholds[index*2] or curr_val<tresholds[index*2+1])
    index+=1
    for curr_val in ig2b:
        flag5 *= (curr_val>tresholds[index*2] or curr_val<tresholds[index*2+1])
    index+=1
    for curr_val in ig3t:
        flag6 *= (curr_val>tresholds[index*2] or curr_val<tresholds[index*2+1])
    index+=1
    for curr_val in ig3b:
        flag7 *= (curr_val>tresholds[index*2] or curr_val<tresholds[index*2+1])
    boolean = flag1 or flag2 or flag3 or flag4 or flag5 or flag6 or flag7
    return boolean





ROOT.gStyle.SetOptStat("emr")
ROOT.gROOT.SetBatch()

usage = 'python peak_analysis.py' #-i PICO*_run_00**
parser = optparse.OptionParser(usage)
parser.add_option('-f', '--folder', dest='folder', type='string', default = '/eos/home-a/adeiorio/GEM/Goliath/', help='Default folder is /eos/home-a/adeiorio/GEM/Goliath')
parser.add_option('-i', '--input', dest='input', type='string', default = 'PICO1_run0001', help="Enter an input root file")
parser.add_option('-p', '--peakfinder', dest='findpeak', default = False, action='store_true', help = "Default do not use find peaks")
parser.add_option('-d', '--distributions', dest='dist', default = False, action='store_true', help = "Default do not save distributions")
parser.add_option('-a', '--all', dest='all', default = False, action='store_true', help = "Default save_all is False")
(opt, args) = parser.parse_args()

#/eos/home-a/adeiorio/GEM/Goliath
#/eos/home-a/adeiorio/GEM/LABNA_scariche/10_01_22
folder = opt.folder
infile = ROOT.TFile.Open(folder + '/' + opt.input+'.root')
print("input file :", infile)
tree = infile.Get("t1")
entries = tree.GetEntries()
run_label = opt.input

outfolder = folder.replace('/eos/home-a/adeiorio/GEM/', '/eos/home-a/acagnott/GEM_plot/')
outfolder = outfolder+"/"+run_label
print outfolder
start_time = datetime.now()

if 'Goliath' in folder : 
    time_from_data = False
    
    #outfolder = "/eos/user/a/acagnott/GEM_plot/"+ run_label

else: 
    time_from_data = True
    #outfolder = "/eos/user/a/acagnott/GEM_plot/LABNA/10_11_22/"+ run_label

#time_from_data = False

print("entries:"+str(entries))

if (opt.all) : save_all= True
else : save_all = False

#save_all = False

print('save all:',  save_all)

curr_ig3t_distr, curr_ig2t_distr, curr_ig1t_distr, curr_ig3b_distr, curr_ig2b_distr, curr_ig1b_distr, curr_idrift_distr, volt_g3b_distr, volt_g3t_distr, volt_g2b_distr, volt_g2t_distr, volt_g1b_distr, volt_g1t_distr, volt_drift_distr= h_init(nbins_current = 100, xmin_current = -50, xmax_current = 50, nbins_voltage= 4000, xmin_voltage= -3500, xmax_voltage= 0)

acquisition_rate = 380.
downscale = 1
acquisition_time = (1./acquisition_rate)*downscale #s

if opt.dist:
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
    outfile = ROOT.TFile.Open(outfolder+"/"+ run_label+".root", "RECREATE")

    outfolder_distr = outfolder+"/distributions"
    if not os.path.exists(outfolder_distr):
        os.makedirs(outfolder_distr)
    print("saving distributions...")
    
    for i in range(1, entries):
        tree.GetEntry(i)
        curr_ig3t_distr.Fill(tree.I_G3T)
        curr_ig3b_distr.Fill(tree.I_G3B)
        curr_ig2t_distr.Fill(tree.I_G2T)
        curr_ig2b_distr.Fill(tree.I_G2B)
        curr_ig1t_distr.Fill(tree.I_G1T)
        curr_ig1b_distr.Fill(tree.I_G1B)
        curr_idrift_distr.Fill(tree.I_drift)

        '''curr_m_ig3t_distr.Fill(-tree.I_G3T)
        curr_m_ig3b_distr.Fill(-tree.I_G3B)
        curr_m_ig2t_distr.Fill(-tree.I_G2T)
        curr_m_ig2b_distr.Fill(-tree.I_G2B)
        curr_m_ig1t_distr.Fill(-tree.I_G1T)
        curr_m_ig1b_distr.Fill(-tree.I_G1B)
        curr_m_idrift_distr.Fill(-tree.I_drift)
        '''
        volt_g3t_distr.Fill(tree.I_G3T)
        volt_g3b_distr.Fill(tree.I_G3B)
        volt_g2t_distr.Fill(tree.I_G2T)
        volt_g2b_distr.Fill(tree.I_G2B)
        volt_g1t_distr.Fill(tree.V_G1T)
        volt_g1b_distr.Fill(tree.V_G1B)
        volt_drift_distr.Fill(tree.V_drift)
    print("HISTOS filled")
    print_hist(outfolder_distr, curr_ig3t_distr.Clone(), "IG3T_current_distribution", "HIST")    
    curr_ig3t_distr.Write()
    print_hist(outfolder_distr, curr_ig3b_distr.Clone(), "IG3B_current_distribution", "HIST")    
    curr_ig3b_distr.Write()
    print_hist(outfolder_distr, curr_ig2t_distr.Clone(), "IG2T_current_distribution", "HIST")
    curr_ig2t_distr.Write()
    print_hist(outfolder_distr, curr_ig2b_distr.Clone(), "IG2B_current_distribution", "HIST")    
    curr_ig2b_distr.Write()
    print_hist(outfolder_distr, curr_ig1t_distr.Clone(), "IG1T_current_distribution", "HIST")    
    curr_ig1t_distr.Write()
    print_hist(outfolder_distr, curr_ig1b_distr.Clone(), "IG1B_current_distribution", "HIST")    
    curr_ig1b_distr.Write()
    print_hist(outfolder_distr, curr_idrift_distr.Clone(), "IDRIFT_current_distribution", "HIST")
    curr_idrift_distr.Write()
    '''
    print_hist(outfolder_distr, curr_m_ig3t_distr.Clone(), "mIG3T_current_distribution", "HIST")    
    curr_m_ig3t_distr.Write()
    print_hist(outfolder_distr, curr_m_ig3b_distr.Clone(), "mIG3B_current_distribution", "HIST")    
    curr_m_ig3b_distr.Write()
    print_hist(outfolder_distr, curr_m_ig2t_distr.Clone(), "mIG2T_current_distribution", "HIST")
    curr_m_ig2t_distr.Write()
    print_hist(outfolder_distr, curr_m_ig2b_distr.Clone(), "mIG2B_current_distribution", "HIST")    
    curr_m_ig2b_distr.Write()
    print_hist(outfolder_distr, curr_m_ig1t_distr.Clone(), "mIG1T_current_distribution", "HIST")    
    curr_m_ig1t_distr.Write()
    print_hist(outfolder_distr, curr_m_ig1b_distr.Clone(), "mIG1B_current_distribution", "HIST")    
    curr_m_ig1b_distr.Write()
    print_hist(outfolder_distr, curr_m_idrift_distr.Clone(), "mIDRIFT_current_distribution", "HIST")
    curr_m_idrift_distr.Write()
    '''
    volt_g3t_distr.Write()
    print_hist(outfolder_distr, volt_g3t_distr.Clone(), "G3T_voltage_distribution", "HIST")
    volt_g3b_distr.Write()
    print_hist(outfolder_distr, volt_g3b_distr.Clone(), "G3B_voltage_distribution", "HIST")
    volt_g2t_distr.Write()
    print_hist(outfolder_distr, volt_g2t_distr.Clone(), "G2T_voltage_distribution", "HIST")
    volt_g2b_distr.Write()
    print_hist(outfolder_distr, volt_g2b_distr.Clone(), "G2B_voltage_distribution", "HIST")
    volt_g1t_distr.Write()
    print_hist(outfolder_distr, volt_g1t_distr.Clone(), "G1T_voltage_distribution", "HIST")
    volt_g1b_distr.Write()
    print_hist(outfolder_distr, volt_g1b_distr.Clone(), "G1B_voltage_distribution", "HIST")
    volt_drift_distr.Write()
    print_hist(outfolder_distr, volt_drift_distr.Clone(), "DRIFT_voltage_distribution", "HIST")
    
    print("HISTOS: saved")

    hist_names = [curr_ig3t_distr, curr_ig2t_distr, curr_ig1t_distr, curr_ig3b_distr, curr_ig2b_distr, curr_ig1b_distr, 
                  curr_idrift_distr]#, curr_m_ig3t_distr, curr_m_ig2t_distr, curr_m_ig1t_distr, curr_m_ig3b_distr, 
                  #curr_m_ig2b_distr, curr_m_ig1b_distr, curr_m_idrift_distr]
                  #, volt_g3b_distr, volt_g3t_distr, volt_g2b_distr, volt_g2t_distr, volt_g1b_distr, volt_g1t_distr, volt_drift_distr ]
    means, sigmas = [], []
    for hist_name in hist_names:
        mean, sigma = fit_hist(hist_name)
        means.append(mean)
        sigmas.append(sigma)

else:
    outfile = ROOT.TFile.Open(outfolder+"/"+ run_label+".root")
    hist_names = ['curr_ig3t_distr', 'curr_ig2t_distr', 'curr_ig1t_distr', 'curr_ig3b_distr', 'curr_ig2b_distr', 'curr_ig1b_distr', 
                  'curr_idrift_distr']#, 'curr_m_ig3t_distr', 'curr_m_ig2t_distr', 'curr_m_ig1t_distr', 'curr_m_ig3b_distr', 
                  #'curr_m_ig2b_distr', 'curr_m_ig1b_distr', 'curr_m_idrift_distr']
                  #, 'volt_g3b_distr', 'volt_g3t_distr', 'volt_g2b_distr', 'volt_g2t_distr', 'volt_g1b_distr', 'volt_g1t_distr', 'volt_drift_distr']
    means, sigmas = [], []
    for hist_name in hist_names:
        histo = outfile.Get(hist_name).Clone()
        mean, sigma = fit_hist(histo)
        means.append(mean)
        sigmas.append(sigma)

    outfile = ROOT.TFile.Open(outfolder+"/"+ run_label+".root", "UPDATE")

print means
print sigmas

uptres_ig3t = means[0]+5*sigmas[0]
uptres_ig2t = means[1]+5*sigmas[1]
uptres_ig1t = means[2]+5*sigmas[2]
uptres_ig3b = means[3]+5*sigmas[3]
uptres_ig2b = means[4]+5*sigmas[4]
uptres_ig1b = means[5]+5*sigmas[5]
uptres_idrift = means[6]+5*sigmas[6]
dwtres_ig3t = means[0]-5*sigmas[0]
dwtres_ig2t = means[1]-5*sigmas[1]
dwtres_ig1t = means[2]-5*sigmas[2]
dwtres_ig3b = means[3]-5*sigmas[3]
dwtres_ig2b = means[4]-5*sigmas[4]
dwtres_ig1b = means[5]-5*sigmas[5]
dwtres_idrift = means[6]-5*sigmas[6]
tresholds = [uptres_idrift, dwtres_idrift, uptres_ig1t, dwtres_ig1t, uptres_ig1b, dwtres_ig1b, uptres_ig2t, dwtres_ig2t, uptres_ig2b, 
             dwtres_ig2b, uptres_ig3t, dwtres_ig3t, uptres_ig3b, dwtres_ig3b]

print("Idrift:"+str(dwtres_idrift)+" to "+str(uptres_idrift))
print("Ig1t:"+str(dwtres_ig1t)+" to "+str(uptres_ig1t))
print("Ig1b:"+str(dwtres_ig1b)+" to "+str(uptres_ig1b))
print("Ig2t:"+str(dwtres_ig2t)+" to "+str(uptres_ig2t))
print("Ig2t:"+str(dwtres_ig2b)+" to "+str(uptres_ig2b))
print("Ig3t:"+str(dwtres_ig3t)+" to "+str(uptres_ig3t))
print("Ig3b:"+str(dwtres_ig3b)+" to "+str(uptres_ig3b))


#Variables to save peak
m_peak_check = 3 # numero di misure che deve restare fuori dai 5 sigam per salvare il picco 
delay = 1520 #measures between two peaks (every peak in this interval will be reject): 1520->4s
n_meas = 950 #measures saved around one peak, n_meas before and n_meas after (950->2.5s so in totale we will have 5s)



if save_all:   
    ig1t = array('d')
    ig1b = array('d')
    ig2t = array('d')
    ig2b = array('d')
    ig3t = array('d')
    ig3b = array('d')
    idrift = array('d')
    m_ig1t = array('d')
    m_ig1b = array('d')
    m_ig2t = array('d')
    m_ig2b = array('d')
    m_ig3t = array('d')
    m_ig3b = array('d')
    m_idrift = array('d')
    vg1t = array('d')
    vg1b = array('d')
    vg2t = array('d')
    vg2b = array('d')
    vg3t_ = array('d')
    vg3t = array('d')
    vg3b = array('d')
    vdrift = array('d')
    time_current = array('d')
    time_voltage = array('d')
    deltav_drg1t = array('d')
    deltav_g1tg1b = array('d')
    deltav_g1bg2t = array('d')
    deltav_g2tg2b = array('d')
    deltav_g2bg3t = array('d')
    deltav_g3tg3b = array('d')

else:
    ig1t = []
    ig1b = []
    ig2t = []
    ig2b = []
    ig3t = []
    ig3b = []
    idrift = []
    m_ig1t = []
    m_ig1b = []
    m_ig2t = []
    m_ig2b = []
    m_ig3t = []
    m_ig3b = []
    m_idrift = []
    vg1t = []
    vg1b = []
    vg2t = []
    vg2b = []
    vg3t_ = []
    vg3t = []
    vg3b = []
    vdrift = []
    deltav_drg1t = []
    deltav_g1tg1b = []
    deltav_g1bg2t = []
    deltav_g2tg2b = []
    deltav_g2bg3t = []
    deltav_g3tg3b = []
    time_current = []
    time_voltage = []


last_event_saved = 0

for i in range(1, entries):
    if(i%1000000==1):print('Event #', i, 'out of', entries)
    tree.GetEntry(i)
    if (time_from_data and i==1):
        var = tree.Time
        temp1 = datetime.fromtimestamp(var)#.strftime('%a, %d %b %Y %H:%M:%S.%f')
        
        
    if save_all:
        ig3b.append(tree.I_G3B)
        ig3t.append(tree.I_G3T)
        ig2t.append(tree.I_G2T)
        ig2b.append(tree.I_G2B)
        ig1t.append(tree.I_G1T)
        ig1b.append(tree.I_G1B)
        idrift.append(tree.I_drift)

        m_ig3b.append(-tree.I_G3B)
        m_ig3t.append(-tree.I_G3T)
        m_ig2t.append(-tree.I_G2T)
        m_ig2b.append(-tree.I_G2B)
        m_ig1t.append(-tree.I_G1T)
        m_ig1b.append(-tree.I_G1B)
        m_idrift.append(-tree.I_drift)

        if time_from_data:
            temp = datetime.fromtimestamp(tree.Time)
            time = temp-temp1
            if (i<100):
                print temp1
                print temp
                print time
                print time.microseconds* 10**(-6) + time.seconds
            time_current.append(time.microseconds*10**(-6) + time.seconds)
            
        else:
            time_current.append(i* acquisition_time) 
        
        if (tree.V_G3T<10000 and i >10):
            vdrift.append(tree.V_drift)
            vg1t.append(tree.V_G1T)
            vg1b.append(tree.V_G1B)
            vg2t.append(tree.V_G2T)
            vg2b.append(tree.V_G2B)
            vg3t.append(tree.V_G3T)
            vg3b.append(tree.V_G3B)
            if time_from_data:
                time = datetime.fromtimestamp(tree.Time)
                time = temp-temp1
            
                time_voltage.append(time.microseconds*10**(-6) + time.seconds)
                
            else:
                time_voltage.append(i* acquisition_time)
            
            deltav_drg1t.append(-tree.V_drift+tree.V_G1T)
            deltav_g1tg1b.append(-tree.V_G1T+tree.V_G1B)
            deltav_g1bg2t.append(-tree.V_G1B+tree.V_G2T)
            deltav_g2tg2b.append(-tree.V_G2T+tree.V_G2B)
            deltav_g2bg3t.append(-tree.V_G2B+tree.V_G3T)
            deltav_g3tg3b.append(-tree.V_G3T+tree.V_G3B)
    else:
        to_write = False
        if(tree.I_drift>tresholds[0] or tree.I_drift<tresholds[1] or tree.I_G1T>tresholds[2] or tree.I_G1T<tresholds[3] or  tree.I_G1B>tresholds[4] or tree.I_G1B<tresholds[5] or 
           tree.I_G2T>tresholds[6] or tree.I_G2T<tresholds[7] or  tree.I_G2B>tresholds[8] or tree.I_G2B<tresholds[9] or  tree.I_G3T>tresholds[10] or tree.I_G3T<tresholds[11] or
           tree.I_G3B>tresholds[12] or tree.I_G3B<tresholds[13]):
        
            ig1t_ = array('d')
            ig1b_ = array('d')
            ig2t_ = array('d')
            ig2b_ = array('d')
            ig3t_ = array('d')
            ig3b_ = array('d')
            idrift_ = array('d')
            for j in range(i, i+ m_peak_check):
                tree.GetEntry(j)
                ig1t_.append(tree.I_G1T)
                ig1b_.append(tree.I_G1B)
                ig2t_.append(tree.I_G2T)
                ig2b_.append(tree.I_G2B)
                ig3t_.append(tree.I_G3T)
                ig3b_.append(tree.I_G3B)
                idrift_.append(tree.I_drift)
            to_write = event_to_write(idrift_, ig1t_, ig1b_, ig2t_, ig2b_, ig3t_, ig3b_, tresholds)
        if(to_write):
            if(last_event_saved == 0 or i-last_event_saved>delay):
                k=0
                last_event_saved = i
                print('adding an anomalies: event #', i)
                
                ig1t_ = array('d')
                ig1b_ = array('d')
                ig2t_ = array('d')
                ig2b_ = array('d')
                ig3t_ = array('d')
                ig3b_ = array('d')
                idrift_ = array('d')
                mig1t_ = array('d')
                mig1b_ = array('d')
                mig2t_ = array('d')
                mig2b_ = array('d')
                mig3t_ = array('d')
                mig3b_ = array('d')
                midrift_ = array('d')
                vg1t_ = array('d')
                vg1b_ = array('d')
                vg2t_ = array('d')
                vg2b_ = array('d')
                vg3t_ = array('d')
                vg3b_ = array('d')
                vdrift_ = array('d')
                deltav_drg1t_ = array('d') 
                deltav_g1tg1b_ = array('d')
                deltav_g1bg2t_ = array('d')
                deltav_g2tg2b_ = array('d')
                deltav_g2bg3t_ = array('d')
                deltav_g3tg3b_ = array('d')       
                time_current_ = array('d')
                time_voltage_ = array('d')
                
                start = i- n_meas
                stop= i + n_meas
                if i< n_meas: start = 0
                if i+n_meas > entries: stop = entries
                for j in range(start, stop): 
                    tree.GetEntry(j)                    
                    
                    ig1t_.append(tree.I_G1T)
                    ig1b_.append(tree.I_G1B)
                    ig2t_.append(tree.I_G2T)
                    ig2b_.append(tree.I_G2B)
                    ig3t_.append(tree.I_G3T)
                    ig3b_.append(tree.I_G3B)
                    idrift_.append(tree.I_drift)
                    mig1t_.append(-tree.I_G1T)
                    mig1b_.append(-tree.I_G1B)
                    mig2t_.append(-tree.I_G2T)
                    mig2b_.append(-tree.I_G2B)
                    mig3t_.append(-tree.I_G3T)
                    mig3b_.append(-tree.I_G3B)
                    midrift_.append(-tree.I_drift)
                    if time_from_data:
                        time_current.append(tree.Time)
                    else:
                        time_current.append(i* acquisition_time)

                    
                    if (tree.V_G3T<10000 and i >10):
                        vg1t_.append(tree.V_G1T)
                        vg1b_.append(tree.V_G1B)
                        vg2t_.append(tree.V_G2T)
                        vg2b_.append(tree.V_G2B)
                        vg3t_.append(tree.V_G3T)
                        vg3b_.append(tree.V_G3B)
                        vdrift_.append(tree.V_drift)
                        deltav_drg1t_.append(-tree.V_drift+tree.V_G1T) 
                        deltav_g1tg1b_.append(-tree.V_G1T+tree.V_G1B)
                        deltav_g1bg2t_.append(-tree.V_G1B+tree.V_G2T)
                        deltav_g2tg2b_.append(-tree.V_G2T+tree.V_G2B)
                        deltav_g2bg3t_.append(-tree.V_G2B+tree.V_G3T)
                        deltav_g3tg3b_.append(-tree.V_G3T+tree.V_G3B)
                        if time_from_data:
                            time_voltage.append(tree.Time)
                        else:
                            time_voltage.append(i* acquisition_time)
                        
                
                time_current.append(time_current_)
                time_voltage.append(time_voltage_)
                ig1t.append(ig1t_)
                ig1b.append(ig1b_)
                ig2t.append(ig2t_)
                ig2b.append(ig2b_)
                ig3t.append(ig3t_)
                ig3b.append(ig3b_)
                idrift.append(idrift_)
                m_ig1t.append(mig1t_)
                m_ig1b.append(mig1b_)
                m_ig2t.append(mig2t_)
                m_ig2b.append(mig2b_)
                m_ig3t.append(mig3t_)
                m_ig3b.append(mig3b_)
                m_idrift.append(midrift_)
                vg1t.append(vg1t_)
                vg1b.append(vg1b_)
                vg2t.append(vg2t_)
                vg2b.append(vg2b_)
                vg3t.append(vg3t_)
                vg3b.append(vg3b_)
                vdrift.append(vdrift_)
                deltav_drg1t.append(deltav_drg1t_) 
                deltav_g1tg1b.append(deltav_g1tg1b_)
                deltav_g1bg2t.append(deltav_g1bg2t_)
                deltav_g2tg2b.append(deltav_g2tg2b_)
                deltav_g2bg3t.append(deltav_g2bg3t_)
                deltav_g3tg3b.append(deltav_g3tg3b_)
                
                

print("Ending loop on event")

if save_all:
    
    make_plots(outfolder, outfile, time_current, time_voltage, ig1t, ig1b, ig2t, ig2b, ig3t, ig3b, idrift, 
               m_ig1t, m_ig1b, m_ig2t, m_ig2b, m_ig3t, m_ig3b, m_idrift, 
               vg1t, vg1b, vg2t, vg2b, vg3t, vg3b, vdrift, deltav_drg1t, deltav_g1tg1b, deltav_g1bg2t, deltav_g2tg2b, deltav_g2bg3t, deltav_g3tg3b, 0)
else:
    
    for n in range(len(ig1t)):
        if n<10: 
            outfolder_peak = outfolder+"/peak_0"+str(n)
        else:
            outfolder_peak = outfolder+"/peak_"+str(n)
        if not os.path.exists(outfolder_peak):
            os.makedirs(outfolder_peak)
            
        make_plots(outfolder_peak, outfile, time_current[n], time_voltage[n], ig1t[n], ig1b[n], ig2t[n], ig2b[n], ig3t[n], ig3b[n], idrift[n], 
                   m_ig1t[n], m_ig1b[n], m_ig2t[n], m_ig2b[n], m_ig3t[n], m_ig3b[n], m_idrift[n],
                   vg1t[n], vg1b[n], vg2t[n], vg2b[n], vg3t[n], vg3b[n], vdrift[n], deltav_drg1t[n], deltav_g1tg1b[n], deltav_g1bg2t[n], deltav_g2tg2b[n], deltav_g2bg3t[n], deltav_g3tg3b[n], n) 
   


#Nei run senza accensione o spegnimento delle gem

if opt.findpeak :
    distance = 1  # 1 secondi 
    height = 3000
    mean_ig1t, sigma_ig1t = fit_hist(curr_ig1t_distr, ig1t)
    mean_ig1b, sigma_ig1b = fit_hist(curr_ig1b_distr, ig1b)
    mean_ig2t, sigma_ig2t = fit_hist(curr_ig2t_distr, ig2t)
    mean_ig2b, sigma_ig2b = fit_hist(curr_ig2b_distr, ig2b)
    mean_ig3t, sigma_ig3t = fit_hist(curr_ig3t_distr, ig3t)
    mean_ig3b, sigma_ig3b = fit_hist(curr_ig3b_distr, ig3b)
    mean_idrift, sigma_idrift = fit_hist(curr_idrift_distr, idrift)
    mean_m_ig1t, sigma_m_ig1t = fit_hist(curr_m_ig1t_distr, m_ig1t)
    mean_m_ig1b, sigma_m_ig1b = fit_hist(curr_m_ig1b_distr, m_ig1b)
    mean_m_ig2t, sigma_m_ig2t = fit_hist(curr_m_ig2t_distr, m_ig2t)
    mean_m_ig2b, sigma_m_ig2b = fit_hist(curr_m_ig2b_distr, m_ig2b)
    mean_m_ig3t, sigma_m_ig3t = fit_hist(curr_m_ig3t_distr, m_ig3t)
    mean_m_ig3b, sigma_m_ig3b = fit_hist(curr_m_ig3b_distr, m_ig3b)
    mean_m_idrift, sigma_m_idrift = fit_hist(curr_m_idrift_distr, m_idrift)

    '''
    peaks_ig1t, properties_ig1t = find_peaks(ig1t, height = height, distance = distance)
    peaks_ig1b, properties_ig1b = find_peaks(ig1b, height = height, distance = distance)
    peaks_ig2t, properties_ig2t = find_peaks(ig2t, height = height, distance = distance)
    peaks_ig2b, properties_ig2b = find_peaks(ig2b, height = height, distance = distance)
    peaks_ig3t, properties_ig3t = find_peaks(ig3t, height = height, distance= distance)
    peaks_ig3b, properties_ig3b = find_peaks(ig3b, height = height, distance = distance)
    peaks_idrift, properties_idrift = find_peaks(idrift, height = height, distance = distance)
    peaks_m_ig1t, properties_m_ig1t = find_peaks(m_ig1t, height = height, distance = distance)
    peaks_m_ig1b, properties_m_ig1b = find_peaks(m_ig1b, height = height, distance = distance)
    peaks_m_ig2t, properties_m_ig2t = find_peaks(m_ig2t, height = height, distance = distance)
    peaks_m_ig2b, properties_m_ig2b = find_peaks(m_ig2b, height = height, distance = distance)
    peaks_m_ig3t, properties_m_ig3t = find_peaks(m_ig3t, height = height, distance= distance)
    peaks_m_ig3b, properties_m_ig3b = find_peaks(m_ig3b, height = height, distance = distance)
    peaks_m_idrift, properties_m_idrift = find_peaks(idrift, height = height, distance = distance)
    '''
    f = open(outfolder+"/"+run_label+"_peakproperties.txt", "w")
    peaks_ig1t, properties_ig1t = find_peaks(ig1t, height = mean_ig1t+3*sigma_ig1t, distance = distance)
    peaks_ig1b, properties_ig1b = find_peaks(ig1b, height = mean_ig1b+3*sigma_ig1b, distance = distance)
    peaks_ig2t, properties_ig2t = find_peaks(ig2t, height = mean_ig2t+3*sigma_ig2t, distance = distance)
    peaks_ig2b, properties_ig2b = find_peaks(ig2b, height = mean_ig2b+3*sigma_ig2b, distance = distance)
    peaks_ig3t, properties_ig3t = find_peaks(ig3t, height = mean_ig3t+3*sigma_ig3t, distance= distance)
    peaks_ig3b, properties_ig3b = find_peaks(ig3b, height = mean_ig3b+3*sigma_ig3b, distance = distance)
    peaks_idrift, properties_idrift = find_peaks(idrift, height = mean_idrift+3*sigma_idrift, distance = distance)
    peaks_m_ig1t, properties_m_ig1t = find_peaks(m_ig1t, height = mean_m_ig1t+3*sigma_m_ig1t, distance = distance)
    peaks_m_ig1b, properties_m_ig1b = find_peaks(m_ig1b, height = mean_m_ig1b+3*sigma_m_ig1b, distance = distance)
    peaks_m_ig2t, properties_m_ig2t = find_peaks(m_ig2t, height = mean_m_ig2t+3*sigma_m_ig2t, distance = distance)
    peaks_m_ig2b, properties_m_ig2b = find_peaks(m_ig2b, height = mean_m_ig2b+3*sigma_m_ig2b, distance = distance)
    peaks_m_ig3t, properties_m_ig3t = find_peaks(m_ig3t, height = mean_m_ig3t+3*sigma_m_ig3t, distance= distance)
    peaks_m_ig3b, properties_m_ig3b = find_peaks(m_ig3b, height = mean_m_ig3b+3*sigma_m_ig3b, distance = distance)
    peaks_m_idrift, properties_m_idrift = find_peaks(m_idrift, height = mean_m_idrift+3*sigma_m_idrift, distance = distance)
        
    f.write("DRIFT : " + str(peaks_idrift) + ' ' + str(properties_idrift))
    f.write("G1T : "+ str(peaks_ig1t) + ' ' + str( properties_ig1t))
    f.write("G1B : "+ str(peaks_ig1b) + ' ' + str( properties_ig1b))
    f.write("-G1T : "+ str(peaks_m_ig1t) + ' ' + str( properties_m_ig1t))
    f.write("-G1B : "+ str(peaks_m_ig1b) + ' ' + str( properties_m_ig1b))
    f.write("G2T : "+ str(peaks_ig2t) + ' ' + str( properties_ig2t))
    f.write("G2B : "+ str(peaks_ig2b) + ' ' + str( properties_ig2b))
    f.write("-G2T : "+ str(peaks_m_ig2t) + ' ' + str( properties_m_ig2t))
    f.write("-G2B : "+ str(peaks_m_ig2b) + ' ' + str( properties_m_ig2b))
    f.write("G3T : "+ str(peaks_ig3t) + ' ' + str( properties_ig3t))
    f.write("G3B : "+ str(peaks_ig3b) + ' ' + str( properties_ig3b))
    f.write("-G3T : "+ str(peaks_m_ig3t) + ' ' + str( properties_m_ig3t))
    f.write("-G3B : "+ str(peaks_m_ig3b) + ' ' + str( properties_m_ig3b))
    
    #peaksG3B = []
    #peak_m_G3B = []
    #for p in peaks_ig3b: peaksG3B.append(peak(entry = p, t_array = time_current, height = ig3b[p], i_array = ig3b, v_array = vg3b))
    #for p in peaks_m_ig3b: peaks_m_G3B.append(peak(entry = p, t_array = time_current, height = m_ig3b[p], i_array = m_ig3b, v_array = vg3b))

    

    '''peaksG3B = []
    peaksG2T = []
    peaksG2B = []
    peaksG1T = []
    peaksG1B = []
    peaksDRIFT = []

    for p in peaks_ig3t: peaksG3T.append(peak(entry = p, t_array = time_current, height = ig3t[p], i_array = ig3t, v_array = vg3t))
    for p in peaks_ig3b: peaksG3B.append(peak(entry = p, t_array = time_current, height = ig3b[p], i_array = ig3b, v_array = vg3b))
    for p in peaks_ig2t: peaksG2T.append(peak(entry = p, t_array = time_current, height = ig2t[p], i_array = ig2t, v_array = vg2t))
    for p in peaks_ig2b: peaksG2B.append(peak(entry = p, t_array = time_current, height = ig2b[p], i_array = ig2b, v_array = vg2b))
    for p in peaks_ig1t: peaksG1T.append(peak(entry = p, t_array = time_current, height = ig1t[p], i_array = ig1t, v_array = vg1t))
    for p in peaks_ig1b: peaksG1B.append(peak(entry = p, t_array = time_current, height = ig1b[p], i_array = ig1b, v_array = vg1b))
    for p in peaks_idrift: peaksDRIFT.append(peak(entry = p, t_array = time_current, height = idrift[p], i_array = idrift, v_array = vdrift))
    '''
    #outfile.Close()

    #outfile = ROOT.TFile.Open(outfolder+"/peaks_overview.root", "RECREATE")
        
    #simultaneous_analysis(peaksG3B, ig3t, ig2b, ig2t, ig1t, ig1b, vg3t, vg2b, vg2t, vg1b, vg1t, outfile, delta_t = 10000)
    #simultaneous_analysis(peaks_m_G3B, ig3t, ig2b, ig2t, ig1t, ig1b, vg3t, vg2b, vg2t, vg1b, vg1t, outfile, delta_t = 10000)

    #outfile.Close()

    #-TH1F  con binnaggio che riporta altezza di picco
    binning = array('f', [0, 6, 8, 10, 12, 14, 16, 18, 20, 25, 30, 35, 40, 50, 100, 1000, 5000, 10000, 50000])
    hist_heights1T = ROOT.TH1F("ndis_vs_peak_1T", "peak amplitude G1T; Peak heights [nA]; Number of discharges",len(binning)-1,  binning)
    hist_heights1B = ROOT.TH1F("ndis_vs_peak_1B", "peak amplitude G1B; Peak heights [nA]; Number of discharges",len(binning)-1, binning)
    hist_heights2T = ROOT.TH1F("ndis_vs_peak_2T", "peak amplitude G2T; Peak heights [nA]; Number of discharges",len(binning)-1, binning)
    hist_heights2B = ROOT.TH1F("ndis_vs_peak_2B", "peak amplitude G2B; Peak heights [nA]; Number of discharges",len(binning)-1, binning)
    hist_heights3T = ROOT.TH1F("ndis_vs_peak_3T", "peak amplitude G3T; Peak heights [nA]; Number of discharges",len(binning)-1, binning)
    hist_heights3B = ROOT.TH1F("ndis_vs_peak_3B", "peak amplitude G3B; Peak heights [nA]; Number of discharges",len(binning)-1, binning)
    hist_heightsDRIFT = ROOT.TH1F("ndis_vs_peak_DRIFT", "peak amplitude DRIFT; Peak heights [nA]; Number of discharges",len(binning)-1, binning)
    hist_heightsm1T = ROOT.TH1F("ndis_vs_m_peak_1T", "peak amplitude -G1T; Peak heights [nA]; Number of discharges",len(binning)-1,  binning)
    hist_heightsm1B = ROOT.TH1F("ndis_vs_m_peak_1B", "peak amplitude -G1B; Peak heights [nA]; Number of discharges",len(binning)-1, binning)
    hist_heightsm2T = ROOT.TH1F("ndis_vs_m_peak_2T", "peak amplitude -G2T; Peak heights [nA]; Number of discharges",len(binning)-1, binning)
    hist_heightsm2B = ROOT.TH1F("ndis_vs_m_peak_2B", "peak amplitude -G2B; Peak heights [nA]; Number of discharges",len(binning)-1, binning)
    hist_heightsm3T = ROOT.TH1F("ndis_vs_m_peak_3T", "peak amplitude -G3T; Peak heights [nA]; Number of discharges",len(binning)-1, binning)
    hist_heightsm3B = ROOT.TH1F("ndis_vs_m_peak_3B", "peak amplitude -G3B; Peak heights [nA]; Number of discharges",len(binning)-1, binning)
    hist_heightsmDRIFT = ROOT.TH1F("ndis_vs_m_peak_DRIFT", "peak amplitude DRIFT; Peak heights [nA]; Number of discharges",len(binning)-1, binning)
    peak_counter(hist_heights1T, properties_ig1t["peak_heights"],  len(binning)-1, outfile, outfolder)
    peak_counter(hist_heights1B, properties_ig1b["peak_heights"],  len(binning)-1, outfile, outfolder)
    peak_counter(hist_heights2T, properties_ig2t["peak_heights"],  len(binning)-1, outfile, outfolder)
    peak_counter(hist_heights2B, properties_ig2b["peak_heights"],  len(binning)-1, outfile, outfolder)
    peak_counter(hist_heights3T, properties_ig3t["peak_heights"],  len(binning)-1, outfile, outfolder)
    peak_counter(hist_heights3B, properties_ig3b["peak_heights"],  len(binning)-1, outfile, outfolder)
    peak_counter(hist_heightsDRIFT, properties_idrift["peak_heights"],  len(binning)-1, outfile, outfolder)

    peak_counter(hist_heightsm1T, properties_m_ig1t["peak_heights"],  len(binning)-1, outfile, outfolder)
    peak_counter(hist_heightsm1B, properties_m_ig1b["peak_heights"],  len(binning)-1, outfile, outfolder)
    peak_counter(hist_heightsm2T, properties_m_ig2t["peak_heights"],  len(binning)-1, outfile, outfolder)
    peak_counter(hist_heightsm2B, properties_m_ig2b["peak_heights"],  len(binning)-1, outfile, outfolder)
    peak_counter(hist_heightsm3T, properties_m_ig3t["peak_heights"],  len(binning)-1, outfile, outfolder)
    peak_counter(hist_heightsm3B, properties_m_ig3b["peak_heights"],  len(binning)-1, outfile, outfolder)
    peak_counter(hist_heightsmDRIFT, properties_m_idrift["peak_heights"],  len(binning)-1, outfile, outfolder)


    outfile.Close()


else : outfile.Close()


'''
for peak in peaks_ig1b: hist_heights1T.Fill(hist_heights1T.FindBin(peak, 1)
for peak in peaks_ig2t: hist_heights1T.Fill(hist_heights1T.FindBin(peak, 1)
for peak in peaks_ig2b: hist_heights1T.Fill(hist_heights1T.FindBin(peak, 1)
for peak in peaks_ig3t: hist_heights1T.Fill(hist_heights1T.FindBin(peak, 1)
for peak in peaks_ig3b: hist_heights1T.Fill(hist_heights1T.FindBin(peak, 1)
for peak in peaks_idrift: hist_heights1T.Fill(hist_heights1T.FindBin(peak, 1)
'''
    
end_time = datetime.now()
deltatime = end_time-start_time
print("Finished in "+ str(deltatime))
