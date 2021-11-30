from scipy.signal import find_peaks
import ROOT
import optparse
from array import array
from utils import *
from time import ctime
import os
import datetime

usage = 'python makeplot.py'
parser = optparse.OptionParser(usage)
#parser.add_option('--merpart', dest='merpart', default = False, action='store_true', help='Default parts are not merged')
parser.add_option('-f', '--folder', dest='folder', type='string', default = '20191212', help='Default folder is 20191212')
parser.add_option('-i', '--input', dest='input', type='string', default = 'CERN_20191212_0000.root', help="Enter an input root file")
(opt, args) = parser.parse_args()

ROOT.gStyle.SetOptStat(0000)
ROOT.gStyle.SetOptFit(1111)
ROOT.gROOT.SetBatch()

startTime = datetime.datetime.now()
print("starting at "+str(startTime) )

folder = opt.folder
infile = ROOT.TFile.Open(folder + '/' + opt.input)
print("input file :", infile)
tree = infile.Get("t1")

entries = tree.GetEntries()


run_date = opt.input.strip('.root')
if not os.path.exists(run_date):
    os.makedirs(run_date)
print("directory " +run_date+" has been created")

frequency_data = (1./280.)*10**3 #ms 
# 280 Hz

#############
downscale = 50
############


#Entries = 10000
ig1t = array('f', entries*[0])
ig1b = array('f', entries*[0])
ig2t = array('f', entries*[0])
ig2b = array('f', entries*[0])
ig3t = array('f', entries*[0])
ig3b = array('f', entries*[0])
idrift = array('f', entries*[0])
vg1t = array('f', entries*[0])
vg1b = array('f', entries*[0])
vg2t = array('f', entries*[0])
vg2b = array('f', entries*[0])
vg3t = array('f', entries*[0])
vg3b = array('f', entries*[0])
vdrift = array('f', entries*[0])
time_current = array('f', entries*[0])
time_voltage = array('f', entries*[0])
human_time = array('f', entries*[0])
#offset
for i in range(entries):
    if i==0 : continue
    tree.GetEntry(i)
    ig1t[i] = -tree.I_G1T
    ig1b[i] = -tree.I_G1B
    ig2t[i] = tree.I_G2T
    ig2b[i] = tree.I_G2B
    ig3t[i] = -tree.I_G3T
    ig3b[i] = -tree.I_G3B
    idrift[i] = tree.I_drift
    time_current[i] = i*frequency_data*downscale 

    if tree.V_G1T<10000:
        vg1t[i] = tree.V_G1T
        vg1b[i] = tree.V_G1B
    	vg2t[i] = tree.V_G2T
    	vg2b[i] = tree.V_G2B
    	vg3t[i] = tree.V_G3T
    	vg3b[i] = tree.V_G3B
    	vdrift[i] = tree.V_drift
    	time_voltage[i] = i*frequency_data*downscale

    #print type(timestamp[i]), timestamp[i]
    #human_time[i] = ctime(timestamp[i])
#print timestamp
#print ctime(timestamp[0])
### Produzione graph di default
#make_graph(entries, x_array, y_array, name, title, x_title, y_title, color, style = 20)
gr_ig1t = make_graph(entries, time_current, ig1t, "Current_G1T", "Current G1T", "Time (ms)", "Current (nA)", colors[1], 4)
gr_ig1b = make_graph(entries, time_current, ig1b, "Current_G1B", "Current G1B", "Time (ms)", "Current (nA)", colors[2],5)
gr_ig2t = make_graph(entries, time_current, ig2t, "Current_G2T", "Current G2T", "Time (ms)", "Current (nA)", colors[3],6)
gr_ig2b = make_graph(entries, time_current, ig2b, "Current_G2B", "Current G2B", "Time (ms)", "Current (nA)", colors[4],7)
gr_ig3t = make_graph(entries, time_current, ig3t, "Current_G3T", "Current G3T", "Time (ms)", "Current (nA)", colors[5],8)
gr_ig3b = make_graph(entries, time_current, ig3b, "Current_G3B", "Current G3B", "Time (ms)", "Current (nA)", colors[6],9)
gr_idrift = make_graph(entries, time_current, idrift, "Current_Drift", "Current Drift", "Time (ms)", "Current (nA)", colors[0],3)

gr_vg1t = make_graph(entries, time_voltage, vg1t, "Voltage_G1T", "Voltage G1T", "Time (ms)", "Voltage (V)", colors[1],4)
gr_vg1b = make_graph(entries, time_voltage, vg1b, "Voltage_G1B", "Voltage G1B", "Time (ms)", "Voltage (V)", colors[2],5)
gr_vg2t = make_graph(entries, time_voltage, vg2t, "Voltage_G2T", "Voltage G2T", "Time (ms)", "Voltage (V)", colors[3],6)
gr_vg2b = make_graph(entries, time_voltage, vg2b, "Voltage_G2B", "Voltage G2B", "Time (ms)", "Voltage (V)", colors[4],7)
gr_vg3t = make_graph(entries, time_voltage, vg3t, "Voltage_G3T", "Voltage G3T", "Time (ms)", "Voltage (V)", colors[5],8)
gr_vg3b = make_graph(entries, time_voltage, vg3b, "Voltage_G3B", "Voltage G3B", "Time (ms)", "Voltage (V)", colors[6],9)
gr_vdrift = make_graph(entries, time_voltage, vdrift, "Voltage_Drift", "Voltage Drift", "Time (ms)", "Voltage (V)", colors[0],3)

time = datetime.datetime.now()
print("printing graphs at"+str(time))

### Stampa graph di default
print_hist(run_date, gr_ig1t, "Current_G1T", "A*")
print_hist(run_date, gr_ig1b, "Current_G1B", "A*")
print_hist(run_date, gr_ig2t, "Current_G2T", "A*")
print_hist(run_date, gr_ig2b, "Current_G2B", "A*")
print_hist(run_date, gr_ig3t, "Current_G3T", "A*")
print_hist(run_date, gr_ig3b, "Current_G3B", "A*")
print_hist(run_date, gr_idrift, "Current_Drift", "A*")

print_hist(run_date, gr_vg1t, "Voltage_G1T", "A*")
print_hist(run_date, gr_vg1b, "Voltage_G1B", "A*")
print_hist(run_date, gr_vg2t, "Voltage_G2T", "A*")
print_hist(run_date, gr_vg2b, "Voltage_G2B", "A*")
print_hist(run_date, gr_vg3t, "Voltage_G3T", "A*")
print_hist(run_date, gr_vg3b, "Voltage_G3B", "A*")
print_hist(run_date, gr_vdrift, "Voltage_Drift", "A*")

### Produzione histo di default
h_ig1t = make_hist(tree, 'I_G1T', 'Current distribution in G1T; Current (nA); Events', 1000, int(min(ig1t))-1, int(max(ig1t))+1)
h_ig1b = make_hist(tree, 'I_G1B', 'Current distribution in G1B; Current (nA); Events', 1000, int(min(ig1b))+1, int(max(ig1b))+1)
h_ig2t = make_hist(tree, 'I_G2T', 'Current distribution in G2T; Current (nA); Events', 1000, int(min(ig2t))-1, int(max(ig2t))+1)
h_ig2b = make_hist(tree, 'I_G2B', 'Current distribution in G2B; Current (nA); Events', 1000, int(min(ig2b))+1, int(max(ig2b))+1)
h_ig3t = make_hist(tree, 'I_G3T', 'Current distribution in G3T; Current (nA); Events', 1000, int(min(ig3t))-1, int(max(ig3t))+1)
h_ig3b = make_hist(tree, 'I_G3B', 'Current distribution in G3B; Current (nA); Events', 1000, int(min(ig3b))+1, int(max(ig3b))+1)
h_idrift = make_hist(tree, 'I_drift', 'Current distribution in drift; Current (nA); Events', 1000, int(min(idrift))+1, int(max(idrift))+1)
h_vg1t = make_hist(tree, 'V_G1T', 'Voltage distribution in G1T; Voltage (V); Events', 1000, int(min(vg1t))-1, 0)
h_vg1b = make_hist(tree, 'V_G1B', 'Voltage distribution in G1B; Voltage (V); Events', 1000, int(min(vg1b))+1, 0) 
h_vg2t = make_hist(tree, 'V_G2T', 'Voltage distribution in G2T; Voltage (V); Events', 1000, int(min(vg2t))-1, 0) 
h_vg2b = make_hist(tree, 'V_G2B', 'Voltage distribution in G2B; Voltage (V); Events', 1000, int(min(vg2b))+1, 0) 
h_vg3t = make_hist(tree, 'V_G3T', 'Voltage distribution in G3T; Voltage (V); Events', 1000, int(min(vg3t))-1, 0) 
h_vg3b = make_hist(tree, 'V_G3B', 'Voltage distribution in G3B; Voltage (V); Events', 1000, int(min(vg3b))+1, 0) 
h_vdrift = make_hist(tree, 'V_drift', 'Voltage distribution in drift; Voltage (V); Events', 1000, int(min(vdrift))+1, 0)

time = datetime.datetime.now()
print("printing graphs at"+str(time))

### Produzione histo di default
print_hist(run_date, h_ig1t, "Current_Distribution_G1T", "HIST", True)
print_hist(run_date, h_ig1b, "Current_Distribution_G1B", "HIST", True)
print_hist(run_date, h_ig2t, "Current_Distribution_G2T", "HIST", True)
print_hist(run_date, h_ig2b, "Current_Distribution_G2B", "HIST", True)
print_hist(run_date, h_ig3t, "Current_Distribution_G3T", "HIST", True)
print_hist(run_date, h_ig3b, "Current_Distribution_G3B", "HIST", True)
print_hist(run_date, h_idrift, "Current_Distribution_drift", "HIST", True)
print_hist(run_date, h_vg1t, "Voltage_Distribution_G1T", "HIST", True)
print_hist(run_date, h_vg1b, "Voltage_Distribution_G1B", "HIST", True)
print_hist(run_date, h_vg2t, "Voltage_Distribution_G2T", "HIST", True)
print_hist(run_date, h_vg2b, "Voltage_Distribution_G2B", "HIST", True)
print_hist(run_date, h_vg3t, "Voltage_Distribution_G3T", "HIST", True)
print_hist(run_date, h_vg3b, "Voltage_Distribution_G3B", "HIST", True)
print_hist(run_date, h_vdrift, "Voltage_Distribution_drift", "HIST", True)

#find_peaks(x, height=None, threshold=None, distance=None, prominence=None, width=None, wlen=None, rel_height=0.5, plateau_size=None)
peak_high = 10
threshold_peak = .8
prominence_peak = 1
peaks_ig1t, properties_ig1t = find_peaks(ig1t, height = peak_high, threshold = threshold_peak, prominence = prominence_peak)
peaks_ig1b, properties_ig1b = find_peaks(ig1b, height = peak_high, threshold = threshold_peak, prominence = prominence_peak)
peaks_ig2t, properties_ig2t = find_peaks(ig2t, height = peak_high, threshold = threshold_peak, prominence = prominence_peak)
peaks_ig2b, properties_ig2b = find_peaks(ig2b, height = peak_high, threshold = threshold_peak, prominence = prominence_peak)
peaks_ig3t, properties_ig3t = find_peaks(ig3t, height = peak_high, threshold = threshold_peak, prominence = prominence_peak)
peaks_ig3b, properties_ig3b = find_peaks(ig3b, height = peak_high, threshold = threshold_peak, prominence = prominence_peak)
peaks_idrift, properties_idrift = find_peaks(idrift, height = peak_high, threshold = threshold_peak, prominence = prominence_peak)
print("G1T ", peaks_ig1t, properties_ig1t)
print("G1B ", peaks_ig1b, properties_ig1b)
print("G2T ", peaks_ig2t, properties_ig2t)
print("G2B ", peaks_ig2b, properties_ig2b)
print("G3T ", peaks_ig3t, properties_ig3t)
print("G3B ", peaks_ig3b, properties_ig3b)
print("DRIFT ", peaks_idrift, properties_idrift)

if len(peaks_ig1t)>0:
    time_to_draw, peak_ig1t_to_draw = get_timepeak_arrays(peaks_ig1t, time_current, ig1t)
    gr_peak_ig1t = make_graph(len(peaks_ig1t), time_to_draw, peak_ig1t_to_draw, "CurrentPeaks_G1T", "Current Peaks G1T", "Time (ms)", "Current (nA)", ROOT.kRed)
    print_hist(run_date, [gr_ig1t.Clone(), gr_peak_ig1t.Clone()], "Current_peaks_G1T", "A*")

if len(peaks_ig1b)>0:
    time_to_draw, peak_ig1b_to_draw = get_timepeak_arrays(peaks_ig1b, time_current, ig1b)
    gr_peak_ig1b = make_graph(len(peaks_ig1b), time_to_draw, peak_ig1b_to_draw, "CurrentPeaks_G1B", "Current Peaks G1B", "Time (ms)", "Current (nA)", ROOT.kRed)
    print_hist(run_date, [gr_ig1b.Clone(), gr_peak_ig1b.Clone()], "Current_peaks_G1B", "A*")

if len(peaks_ig2t)>0:
    time_to_draw, peak_ig2t_to_draw = get_timepeak_arrays(peaks_ig2t, time_current, ig2t)
    gr_peak_ig2t = make_graph(len(peaks_ig2t), time_to_draw, peak_ig2t_to_draw, "CurrentPeaks_G2T", "Current Peaks G2T", "Time (ms)", "Current (nA)", ROOT.kRed)
    print_hist(run_date, [gr_ig2t.Clone(), gr_peak_ig2t.Clone()], "Current_peaks_G2T", "A*")

if len(peaks_ig2b)>0:
    time_to_draw, peak_ig2b_to_draw = get_timepeak_arrays(peaks_ig2b, time_current, ig2b)
    gr_peak_ig2b = make_graph(len(peaks_ig2b), time_to_draw, peak_ig2b_to_draw, "CurrentPeaks_G2B", "Current Peaks G2B", "Time (ms)", "Current (nA)", ROOT.kRed)
    print_hist(run_date, [gr_ig2b.Clone(), gr_peak_ig2b.Clone()], "Current_peaks_G2B", "A*")

if len(peaks_ig3t)>0:
    time_to_draw, peak_ig3t_to_draw = get_timepeak_arrays(peaks_ig3t, time_current, ig3t)
    gr_peak_ig3t = make_graph(len(peaks_ig3t), time_to_draw, peak_ig3t_to_draw, "CurrentPeaks_G3T", "Current Peaks G3T", "Time (ms)", "Current (nA)", ROOT.kRed)
    print_hist(run_date, [gr_ig3t.Clone(), gr_peak_ig3t.Clone()], "Current_peaks_G3T", "A*")

if len(peaks_ig3b)>0:
    time_to_draw, peak_ig3b_to_draw = get_timepeak_arrays(peaks_ig3b, time_current, ig3b)
    gr_peak_ig3b = make_graph(len(peaks_ig3b), time_to_draw, peak_ig3b_to_draw, "CurrentPeaks_G3B", "Current Peaks G3B", "Time (ms)", "Current (nA)", ROOT.kRed)
    print_hist(run_date, [gr_ig3b.Clone(), gr_peak_ig3b.Clone()], "Current_peaks_G3B", "A*")

if len(peaks_idrift)>0:
    time_to_draw, peak_idrift_to_draw = get_timepeak_arrays(peaks_idrift, time_current, idrift)
    gr_peak_drift = make_graph(len(peaks_idrift), time_to_draw, peak_idrift_to_draw, "CurrentPeaks_drift", "Current Peaks drift", "Time (ms)", "Current (nA)", ROOT.kRed)
    print_hist(run_date, [gr_idrift.Clone(), gr_peak_drift.Clone()], "Current_peaks_drift", "A*")


all_current = [gr_ig1t.Clone(), gr_ig1b.Clone(), gr_ig2t.Clone(), gr_ig2b.Clone(), gr_ig3t.Clone(), gr_ig3b.Clone(),gr_idrift.Clone()]
print_hist(run_date, all_current, 'All_currents', "A*")#,  "Current and Peak G1T; Time (ms); Current (nA)")
all_volt = [gr_vg1t.Clone(), gr_vg1b.Clone(), gr_vg2t.Clone(), gr_vg2b.Clone(), gr_vg3t.Clone(), gr_vg3b.Clone(),gr_vdrift.Clone()]
print_hist(run_date, all_volt, 'All_voltages', "A*")

#ROOT.gROOT.SetBatch(kFalse)

c1 = ROOT.TCanvas("c1_ch1","c1",50,50,700,600);
c1.SetFillColor(0);
c1.SetBorderMode(0);
c1.SetFrameFillStyle(0);
c1.SetFrameBorderMode(0);
c1.SetLeftMargin( 0.12 );
c1.SetRightMargin( 0.9 );
c1.SetTopMargin( 1 );
c1.SetBottomMargin(-1);
c1.SetTickx(1);
c1.SetTicky(1);
c1.Divide(4,2);
c1.cd(1);
gr_ig1t.Draw();
c1.cd(2);
gr_ig1b.Draw();
c1.cd(3);
gr_ig2t.Draw();
c1.cd(4);
gr_ig2b.Draw();
c1.cd(5);
gr_ig3t.Draw();
c1.cd(6);
gr_ig3b.Draw();
c1.cd(7);
gr_idrift.Draw();
#c1.cd(8);
c1.Draw();
