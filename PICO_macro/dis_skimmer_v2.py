from array import array
import ROOT
from datetime import datetime
import optparse
from utils import *
import os
from scipy.signal import find_peaks
import numpy as np
from peak import *
import copy

usage = 'python peak_analysis.py' #-i PICO*_run_00**
parser = optparse.OptionParser(usage)
parser.add_option('-f', '--folder', dest='folder', type='string', default = '/eos/home-a/adeiorio/GEM/Goliath/', help='Default folder is /eos/home-a/adeiorio/GEM/Goliath')
parser.add_option('-i', '--input', dest='input', type='string', default = 'PICO1_run0001', help="Enter an input root file")
#parser.add_option('-p', '--peakfinder', dest='findpeak', default = False, action='store_true', help = "Default do not use find peaks")
#parser.add_option('-d', '--distributions', dest='dist', default = False, action='store_true', help = "Default do not save distributions")
#parser.add_option('-a', '--all', dest='all', default = False, action='store_true', help = "Default save_all is False")
(opt, args) = parser.parse_args()

#/eos/home-a/adeiorio/GEM/Goliath

def event_to_write(idrift, ig1t, ig1b, ig2t, ig2b, ig3t, ig3b, up, down):
    currs = [idrift, ig1t, ig1b, ig2t, ig2b, ig3t, ig3b]
    flag1, flag2, flag3, flag4, flag5, flag6, flag7 = True, True, True, True, True, True, True
    index = 0
    for curr_val in idrift:
        flag1 *= (curr_val > up['I_drift'] or curr_val < down['I_drift'])
    index+=1
    for curr_val in ig1t:
        flag2 *= (curr_val > up['I_G1T'] or curr_val < down['I_G1T']) 
    index+=1
    for curr_val in ig1b:
        flag3 *= (curr_val > up['I_G1B'] or curr_val < down['I_G1B'])
    index+=1
    for curr_val in ig2t:
        flag4 *= (curr_val > up['I_G2T'] or curr_val < down['I_G2T'])
    index+=1
    for curr_val in ig2b:
        flag5 *= (curr_val > up['I_G2B'] or curr_val < down['I_G2B'])
    index+=1
    for curr_val in ig3t:
        flag6 *= (curr_val > up['I_G3T'] or curr_val < down['I_G3T'])
    index+=1
    for curr_val in ig3b:
        flag7 *= (curr_val > up['I_G3B'] or curr_val < down['I_G3B'])
    boolean = flag1 or flag2 or flag3 or flag4 or flag5 or flag6 or flag7
    return boolean

ROOT.gStyle.SetOptStat("emr")
ROOT.gROOT.SetBatch()
run_label = opt.input

start_time = datetime.now()

folder = opt.folder
infile = ROOT.TFile.Open(folder + '/' + opt.input+'.root')
print("input file :", infile)
tree = infile.Get("t1")
entries = tree.GetEntries()
outfolder = "/eos/user/a/acagnott/GEM_plot/"+ run_label

acquisition_rate = 380.
downscale = 1
acquisition_time = (1./acquisition_rate)*downscale #s

print("entries:"+str(entries))

#Variables to save peak
m_peak_check = 3 # numero di misure che deve restare fuori dai 5 sigam per salvare il picco
delay = 1520 #measures between two peaks (every peak in this interval will be reject): 1520->4s
n_meas = 950 #measures saved around one peak, n_meas before and n_meas after (950->2.5ms so in total we will have 5s)

ig3t_distr, ig2t_distr, ig1t_distr, ig3b_distr, ig2b_distr, ig1b_distr, idrift_distr, vg3b_distr, vg3t_distr, vg2b_distr, vg2t_distr, vg1b_distr, vg1t_distr, vdrift_distr =  h_init(nbins_current = 100, xmin_current = -50, xmax_current = 50, nbins_voltage= 4000, xmin_voltage= -3500, xmax_voltage= 0)

print(type(ig3t_distr))
print(ig3t_distr) 
curr_volt_dict = {'I_G3T': ig3t_distr, 'I_G3B': ig3b_distr, 'I_G2T': ig2t_distr, 'I_G2B': ig2b_distr, 'I_G1T': ig1t_distr, 'I_G1B': ig1b_distr, 'I_drift': idrift_distr, 'V_G3T': vg3t_distr, 'V_G3B': vg3b_distr, 'V_G2T': vg2t_distr, 'V_G2B': vg2b_distr, 'V_G1T': vg1t_distr, 'V_G1B': vg1b_distr, 'V_drift': vdrift_distr}

print(type(ig3t_distr))
print(ig3t_distr) 

skimfile = ROOT.TFile.Open(folder + '/' + opt.input+'_skim.root', "RECREATE")

down, up = {},{}
nsigmas = 5

for nt in curr_volt_dict.keys():
    print(nt, curr_volt_dict[nt].GetName())
    infile.cd()
    infile.Get("t1").Project(curr_volt_dict[nt].GetName(), nt)
    print(curr_volt_dict[nt].GetMean())
    if(nt.startswith('I')):
        mean, sigma = fit_hist(curr_volt_dict[nt].Clone())
        up[nt] = mean + nsigmas*sigma
        down[nt] = mean - nsigmas*sigma
        print(nt, up[nt], down[nt])
    skimfile.cd()
    curr_volt_dict[nt].Clone().Write()
    
skimfile.cd()
skimtree = ROOT.TTree("t1", "Skimmed tree")
ig1t = array('f', [0]*2*n_meas)
ig1b = array('f', [0]*2*n_meas)
ig2t = array('f', [0]*2*n_meas)
ig2b = array('f', [0]*2*n_meas)
ig3t = array('f', [0]*2*n_meas)
ig3b = array('f', [0]*2*n_meas)
idrift = array('f', [0]*2*n_meas)
trg1t = array('i', [0])
trg1b = array('i', [0])
trg2t = array('i', [0])
trg2b = array('i', [0])
trg3t = array('i', [0])
trg3b = array('i', [0])
trdrift = array('i', [0])
vg1t = array('f', [0]*2*n_meas)
vg1b = array('f', [0]*2*n_meas)
vg2t = array('f', [0]*2*n_meas)
vg2b = array('f', [0]*2*n_meas)
vg3t = array('f', [0]*2*n_meas)
vg3b = array('f', [0]*2*n_meas)
vdrift = array('f', [0]*2*n_meas)
deltav_drg1t = array('f', [0]*2*n_meas) 
deltav_g1tg1b = array('f', [0]*2*n_meas)
deltav_g1bg2t = array('f', [0]*2*n_meas)
deltav_g2tg2b = array('f', [0]*2*n_meas)
deltav_g2bg3t = array('f', [0]*2*n_meas)
deltav_g3tg3b = array('f', [0]*2*n_meas)
timestamp_current = array('f', [0]*2*n_meas)
timestamp_voltage = array('f', [0]*2*n_meas)
deltatime_current = array('f', [0]*2*n_meas)
deltatime_voltage = array('f', [0]*2*n_meas)

#Branching the output tree
skimtree.Branch("IG1T", ig1t, "IG1T[1900]/F")
skimtree.Branch("IG1B", ig1b, "IG1B[1900]/F")
skimtree.Branch("IG2T", ig2t, "IG2T[1900]/F")
skimtree.Branch("IG2B", ig2b, "IG2B[1900]/F")
skimtree.Branch("IG3T", ig3t, "IG3T[1900]/F")
skimtree.Branch("IG3B", ig3b, "IG3B[1900]/F")
skimtree.Branch("IDRIFT", idrift, "IDRIFT[1900]/F")
skimtree.Branch("TRG1T", trg1t, "TRG1T/I")
skimtree.Branch("TRG1B", trg1b, "TRG1B/I")
skimtree.Branch("TRG2T", trg2t, "TRG2T/I")
skimtree.Branch("TRG2B", trg2b, "TRG2B/I")
skimtree.Branch("TRG3T", trg3t, "TRG3T/I")
skimtree.Branch("TRG3B", trg3b, "TRG3B/I")
skimtree.Branch("TRDRIFT", trdrift, "TRDRIFT/I")
skimtree.Branch("VG1T", vg1t, "VG1T[1900]/F")
skimtree.Branch("VG1B", vg1b, "VG1B[1900]/F")
skimtree.Branch("VG2T", vg2t, "VG2T[1900]/F")
skimtree.Branch("VG2B", vg2b, "VG2B[1900]/F")
skimtree.Branch("VG3T", vg3t, "VG3T[1900]/F")
skimtree.Branch("VG3B", vg3b, "VG3B[1900]/F")
skimtree.Branch("VDRIFT", vdrift, "VDRIFT[1900]/F")
skimtree.Branch("DeltaV_drg1t", deltav_drg1t, "DeltaV_drg1t[1900]/F")
skimtree.Branch("DeltaV_g1tg1b", deltav_g1tg1b, "DeltaV_g1tg1b[1900]/F")
skimtree.Branch("DeltaV_g1bg2t", deltav_g1bg2t, "DeltaV_g1bg2t[1900]/F")
skimtree.Branch("DeltaV_g2tg2b", deltav_g2tg2b, "DeltaV_g2tg2b[1900]/F")
skimtree.Branch("DeltaV_g2bg3t", deltav_g2bg3t, "DeltaV_g2bg3t[1900]/F")
skimtree.Branch("DeltaV_g3tg3b", deltav_g3tg3b, "DeltaV_g3tg3b[1900]/F")
skimtree.Branch("timestamp_current", timestamp_current, "timestamp_current[1900]/F")
skimtree.Branch("timestamp_voltage", timestamp_voltage, "timestamp_voltage[1900]/F")
skimtree.Branch("deltatime_current", deltatime_current, "deltatime_current[1900]/F")
skimtree.Branch("deltatime_voltage", deltatime_voltage, "deltatime_voltage[1900]/F")

last_event_saved = 0

tree.GetEntry(1)
start_run = datetime.fromtimestamp(tree.Time)
print("start run: " + start_run.strftime('%a, %d %b %Y %H:%M:%S.%f'))

tree.GetEntry(entries-1)
stop_run = datetime.fromtimestamp(tree.Time)
print("stop run: " + stop_run.strftime('%a, %d %b %Y %H:%M:%S.%f'))

print("run lenght: " + str(stop_run-start_run))

for i in range(1, entries):
    if(i%1000000==1):print('Event #', i, 'out of', entries)
    tree.GetEntry(i)
    
    to_write = False
    trdrift[0], trg1t[0], trg1b[0], trg2t[0], trg2b[0], trg3t[0], trg3b[0] = 0, 0, 0, 0, 0, 0, 0
    if(tree.I_drift > up['I_drift'] or tree.I_drift < down['I_drift']):
        trdrift[0] = 1
    if(tree.I_G1T > up['I_G1T'] or tree.I_G1T < down['I_G1T']):
        trg1t[0] = 1
    if(tree.I_G1B > up['I_G1B'] or tree.I_G1B < down['I_G1B']):
        trg1b[0] = 1
    if(tree.I_G2T > up['I_G2T'] or tree.I_G2T < down['I_G2T']):
        trg2t[0] = 1
    if(tree.I_G2B > up['I_G2B'] or tree.I_G2B < down['I_G2B']):
        trg2b[0] = 1
    if(tree.I_G3T > up['I_G3T'] or tree.I_G3T < down['I_G3T']):
        trg3t[0] = 1
    if(tree.I_G3B > up['I_G3B'] or tree.I_G3B < down['I_G3B']):
        trg3b[0] = 1

    if(trdrift[0] + trg1t[0] + trg1b[0] + trg2t[0] + trg2b[0] + trg3t[0] + trg3b[0] > 0):
        ig1t_ = array('f')
        ig1b_ = array('f')
        ig2t_ = array('f')
        ig2b_ = array('f')
        ig3t_ = array('f')
        ig3b_ = array('f')
        idrift_ = array('f')
        for j in range(i, i+ m_peak_check):
            tree.GetEntry(j)
            ig1t_.append(tree.I_G1T)
            ig1b_.append(tree.I_G1B)
            ig2t_.append(tree.I_G2T)
            ig2b_.append(tree.I_G2B)
            ig3t_.append(tree.I_G3T)
            ig3b_.append(tree.I_G3B)
            idrift_.append(tree.I_drift)
        to_write = event_to_write(idrift_, ig1t_, ig1b_, ig2t_, ig2b_, ig3t_, ig3b_, up, down)
        if((last_event_saved == 0 or i-last_event_saved>delay) and to_write):
            k = 0
            last_event_saved = i
            print('adding an anomalies: event #', i)
    
            start = i - n_meas
            stop = i + n_meas
            if i < n_meas: start = 1
            if i+n_meas > entries: stop = entries
            l = 0
            m = 0
            for j in range(start, stop): 
                tree.GetEntry(j)                    
                ig1t[l] = copy.deepcopy(tree.I_G1T)
                ig1b[l] = copy.deepcopy(tree.I_G1B)
                ig2t[l] = copy.deepcopy(tree.I_G2T)
                ig2b[l] = copy.deepcopy(tree.I_G2B)
                ig3t[l] = copy.deepcopy(tree.I_G3T)
                ig3b[l] = copy.deepcopy(tree.I_G3B)
                idrift[l] = copy.deepcopy(tree.I_drift)
                timestamp_current[l] = copy.deepcopy(tree.Time)
                deltatime = datetime.fromtimestamp(tree.Time)-start_run
                deltatime_current[l] = copy.deepcopy( deltatime.microseconds*10**(-6) + deltatime.seconds )
                
                if (tree.V_G3T<10000):
                    vg1t[m] = copy.deepcopy(tree.V_G1T)
                    vg1b[m] = copy.deepcopy(tree.V_G1B)
                    vg2t[m] = copy.deepcopy(tree.V_G2T)
                    vg2b[m] = copy.deepcopy(tree.V_G2B)
                    vg3t[m] = copy.deepcopy(tree.V_G3T)
                    vg3b[m] = copy.deepcopy(tree.V_G3B)
                    vdrift[m] = copy.deepcopy(tree.V_drift)
                    deltav_drg1t[m] = copy.deepcopy(-tree.V_drift+tree.V_G1T)
                    deltav_g1tg1b[m] = copy.deepcopy(-tree.V_G1T+tree.V_G1B)
                    deltav_g1bg2t[m] = copy.deepcopy(-tree.V_G1B+tree.V_G2T)
                    deltav_g2tg2b[m] = copy.deepcopy(-tree.V_G2T+tree.V_G2B)
                    deltav_g2bg3t[m] = copy.deepcopy(-tree.V_G2B+tree.V_G3T)
                    deltav_g3tg3b[m] = copy.deepcopy(-tree.V_G3T+tree.V_G3B)
                    timestamp_voltage[m] = copy.deepcopy(tree.Time)
                    deltatime = datetime.fromtimestamp(tree.Time)-start_run
                    deltatime_voltage[m] = copy.deepcopy( deltatime.microseconds*10**(-6) + deltatime.seconds )
                    
                    m += 1
                l += 1
            skimtree.Fill()    
                
print("Ending loop on event")
skimfile.Write()
skimfile.Close()
end_time = datetime.now()
deltatime = end_time-start_time
print("Finished in "+ str(deltatime))
