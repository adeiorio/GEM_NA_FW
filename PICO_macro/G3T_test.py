
#Specifica per run 0008 del 20191213

import ROOT
from array import array
import optparse
from utils import *
import os
from scipy.signal import find_peaks
import numpy as np
from peak import *


ROOT.gStyle.SetOptStat(0000)
ROOT.gROOT.SetBatch()

# python G3T_test.py -f 20191212 -i CERN_20191212_0000.root
usage = 'python G3T_test.py'
parser = optparse.OptionParser(usage)
#parser.add_option('--merpart', dest='merpart', default = False, action='store_true', help='Default parts are not merged')   
parser.add_option('-f', '--folder', dest='folder', type='string', default = '20191212', help='Default folder is 20191212')
parser.add_option('-i', '--input', dest='input', type='string', default = 'CERN_20191212_0000.root', help="Enter an input root file")
(opt, args) = parser.parse_args()

folder = '/eos/home-a/adeiorio/GEM/' + opt.folder
infile = ROOT.TFile.Open(folder + '/' + opt.input)
print("input file :", infile)
tree = infile.Get("t1")



'''
def baseline_voltage(v_array):
    values = []
    for i in range(1, 1001):
        values.append(v_array[-i])
    values = np.array(values)
    mean = np.mean(values) 
    mean = (int)(mean)+1
    return mean
                                 
def rise_time(mean, v_array, t_array):
    rise_time_value = 0 
    for i in range(len(v_array)):
        if(rise_time_value==0 and  abs(v_array[i])>abs(mean)): 
            rise_time_value = t_array[i]
            entry = i
    return rise_time_value, entry
'''

def make_canvas(title, mean_tot, mean_tot_dev, means, means_dev, step, n_peak):
    #if n_peak==0 :outfile = ROOT.TFile.Open(run_date+"/"+title+"_canvases_means.root", "RECREATE")
    #else: outfile = ROOT.TFile.Open(run_date+"/"+title+"_canvases_means.root", "UPDATE")
    
    histo = ROOT.TH1F("runtime_mean", "means before peak "+ str(step), len(means), -0.5, len(means)-0.5)
    for i in range(len(means)) : 
        histo.SetBinContent(i+1, means[i])
        histo.SetBinError(i+1, means_dev[i])
    line = ROOT.TLine(-0.5, mean_tot, (len(means)-0.5), mean_tot)
    line_dev1 = ROOT.TLine(-0.5, mean_tot+mean_tot_dev, (len(means)-0.5), mean_tot+mean_tot_dev)
    line_dev1.SetLineColor(ROOT.kRed)
    line_dev2 = ROOT.TLine(-0.5, mean_tot-mean_tot_dev, (len(means)-0.5), mean_tot-mean_tot_dev)
    line_dev2.SetLineColor(ROOT.kRed)
    c1 = ROOT.TCanvas(title+str(n_peak), title+str(n_peak))
    histo.Draw()
    line.Draw("same")
    line_dev1.Draw("same")
    line_dev2.Draw("same")
    #c1.Write()
    c1Clone = c1.Clone()
    return c1Clone

def simultaneous_analysis(peaksG3B, ig3t, ig2b, ig2t, ig1t, ig1b, vg3t, vg2b, vg2t, vg1b, vg1t, outfile, delta_t = 10000):  #delta_t=10000s
    # starting from peaksG3B -> max prob discharges
    for p in peaksG3B:
        entry_pg3b = p.entry
        time_pg3b = p.time
        times = p.t_array
        pnt_to_eof = len(ig3t) - entry_pg3b
        outfile.cd()
        outfile.mkdir("peak_"+str(p.t_peak))
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
        gr_curr_g3t.GetYaxis().SetTitle("current (#mu A)")
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
        gr_curr_g2b.GetYaxis().SetTitle("current (#mu A)")
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
        gr_curr_g2t.GetYaxis().SetTitle("current (#mu A)")
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
        gr_curr_g1b.GetYaxis().SetTitle("current (#mu A)")
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
        gr_curr_g1t.GetYaxis().SetTitle("current (#mu A)")
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
        gr_curr_drift.GetYaxis().SetTitle("current (#mu A)")
        gr_volt_drift = ROOT.TGraph(entry_stop-entry_start, times[entry_start: entry_stop], vdrift[entry_start:entry_stop_volt])
        gr_volt_drift.SetName("DRIFT_voltage") 
        gr_volt_drift.SetTitle("DRIFT voltage")
        gr_volt_drift.SetMarkerStyle(20)
        gr_volt_drift.GetXaxis().SetTitle("time (s)")
        gr_volt_drift.GetYaxis().SetTitle("voltage (V)")
        
        outfile.cd("peak_"+str(p.t_peak))
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


def peaks_analysis(channel, ofile, peaks, step):
    #print channel
    #tau_ = []
    outfile.mkdir(channel)
    for index, peak in enumerate(peaks):
        #print("ch:"+channel+" peak #"+str(index))
        if peak.entry == peaks[-1].entry :
            gr_peak = peak.graph_peak(pnt_to_plot = 10)
            gr_volt = peak.graph_voltage(pnt_to_plot = 100)
        elif peak.entry == peaks[0].entry : 
            gr_peak = peak.graph_peak(pnt_to_plot = peak.entry)
            gr_volt = peak.graph_voltage(pnt_to_plot = peak.entry)
        elif peak.entry < 250 :  
            gr_peak = peak.graph_peak(pnt_to_plot = peak.entry)
            gr_volt = peak.graph_voltage(pnt_to_plot = peak.entry)
        else : 
            gr_peak = peak.graph_peak()
            gr_volt = peak.graph_voltage()
        #print("tau peak "+str(index)+" "+channel+": "+ str(tau))
        #tau_.append(tau)
        #print peak.t_peak
        gr_peak.SetName("discharge_"+channel+"peak_"+str(peak.t_peak))
        gr_volt.SetName("voltage_"+channel+"peak"+str(peak.t_peak))
        gr_peak.SetTitle(channel)
        gr_volt.SetTitle(channel)
        ofile.cd(channel)
        gr_peak.Write()
        ofile.cd(channel)
        gr_volt.Write()
        if index == 0:
            if peak.entry < 10000:
                 mean_tot, mean_tot_dev, means, means_dev, rms, rms_dev, rms_step, rms_step_dev = peak.runtime_mean(pnt_tot = peak.entry - 10, step = (int)(peak.entry/5)  , to_drop = 10) # da controllare step
                 step_ = (int)(peak.entry/5)
            else:
                mean_tot, mean_tot_dev, means, means_dev, rms, rms_dev, rms_step, rms_step_dev = peak.runtime_mean(step = step)
                step_ = step
        elif peak.entry==peaks[-1].entry:
            mean_tot, mean_tot_dev, means, means_dev, rms, rms_dev, rms_step, rms_step_dev = peak.runtime_mean(pnt_tot = peak.entry - 10, step = (int)(peak.entry/5)  , to_drop = 10)
            step_ = (int)(peak.entry/5)
        elif (peak.entry-peaks[index-1].entry<500) : continue
        else:
            if peak.entry-peaks[index-1].entry<10000 : 
                mean_tot, mean_tot_dev, means, means_dev, rms, rms_dev, rms_step, rms_step_dev = peak.runtime_mean(pnt_tot =  (peak.entry-peaks[index-1].entry) -200 , step = 100, to_drop = 50)
                step_ = 100
            else:
                
                mean_tot, mean_tot_dev, means, means_dev, rms, rms_dev, rms_step, rms_step_dev = peak.runtime_mean(step = step)
                step_ = step
        canvas_rms = make_canvas(channel+"rms_peak", rms, rms_dev, rms_step, rms_step_dev, step_, peak.t_peak)
        canvas_mean = make_canvas(channel+"mean_peak", mean_tot, mean_tot_dev, means, means_dev, step_, peak.t_peak)
        ofile.cd(channel)
        canvas_rms.Write()
        canvas_mean.Write()
        #gr_peak, tau = peak.tau()
        
    #return tau_


entries = tree.GetEntries()
run_date = opt.input.strip('.root')
outfolder = "/eos/user/a/acagnott/GEM_plot/"+ run_date
if not os.path.exists(outfolder):
    os.makedirs(outfolder)
outfile = ROOT.TFile.Open(outfolder+"/"+ run_date+"_allGraph.root", "RECREATE")
print("output file :", outfile)

print("entries:"+str(entries))



frequency_data = (1./380.) #s 
# 280 Hz
#390 Hz
downscale = 1
if ("0000" in run_date): downscale = 1
if("0008" in run_date): downscale = 50


# per cancellare i primi punti scommentare:
if("0008" in run_date): trig_entry_current = 0 
elif("0000" in run_date): trig_entry_current = (int)(0.3*10**6/ frequency_data)  #punti iniziali saltati --> 0.3*10**6 s 
else: trig_entry_current = 0


ig1t = array('f')
ig1b = array('f')
ig2t = array('f')
ig2b = array('f')
ig3t = array('f')
ig3b = array('f')
idrift = array('f')
vg1t = array('f')
vg1b = array('f')
vg2t = array('f')
vg2b = array('f')
vg3t_ = array('f')
vg3t = array('f')
vg3b = array('f')
vdrift = array('f')
time_c = array('f')
time_v = array('f')
time_current = array('f')
time_voltage = array('f')
n_entry = array('i')

tree.GetEntry(0)
offset_t = tree.Time        

curr_ig3t_distr = ROOT.TH1F("curr_ig3t_distr", "G3T current distribution", 100, -20,20)
curr_ig2t_distr = ROOT.TH1F("curr_ig2t_distr", "G2T current distribution", 100, -20,20)
curr_ig1t_distr = ROOT.TH1F("curr_ig1t_distr", "G1T current distribution", 100, -20,20)
curr_ig3b_distr = ROOT.TH1F("curr_ig3b_distr", "G3B current distribution", 100, -20,20)
curr_ig2b_distr = ROOT.TH1F("curr_ig2b_distr", "G2B current distribution", 100, -20,20)
curr_ig1b_distr = ROOT.TH1F("curr_ig1b_distr", "G1B current distribution", 100, -20,20)
curr_idrift_distr = ROOT.TH1F("curr_idrift_distr", "DRIFT current distribution", 100, -20,20)

for i in range(1, entries):
    tree.GetEntry(i)
    n_entry.append(i)
    ig3b.append(-tree.I_G3B)
    ig3t.append(-tree.I_G3T)
    ig2t.append(-tree.I_G2T)
    ig2b.append(tree.I_G2B)
    ig1t.append(-tree.I_G1T)
    ig1b.append(tree.I_G1B)
    #idrift.append(-tree.I_drift)
    idrift.append(tree.I_drift)
    time_current.append(i* frequency_data*downscale) 
    time_c.append(tree.Time-offset_t)
    curr_ig3t_distr.Fill(tree.I_G3T)
    curr_ig3b_distr.Fill(tree.I_G3B)
    curr_ig2t_distr.Fill(tree.I_G2T)
    curr_ig2b_distr.Fill(tree.I_G2B)
    curr_ig1t_distr.Fill(tree.I_G1T)
    curr_ig1b_distr.Fill(tree.I_G1B)
    curr_idrift_distr.Fill(tree.I_drift)
    
    if tree.V_G3T<10000 :
        #if(tree.V_drift==0 or tree.V_G1T==0 or tree.V_G1B==0 or tree.V_G2T==0 or tree.V_G2B==0 or tree.V_G3T==0 or tree.V_G3B==0):
        vdrift.append(tree.V_drift)
        vg1t.append(tree.V_G1T)
        vg1b.append(tree.V_G1B)
        vg2t.append(tree.V_G2T)
        vg2b.append(tree.V_G2B)
        vg3t.append(tree.V_G3T)
        vg3b.append(tree.V_G3B)
        time_voltage.append(i* frequency_data*downscale)
        time_v.append(tree.Time-offset_t)
        
        if (vdrift[-1] > 0) : print vdrift[-1]

#print time_current
print("end loop on tree")
#tot_time = entries*frequency_data
#print tot_time

curr_ig3t_distr.Write()
curr_ig3b_distr.Write()
curr_ig2t_distr.Write()
curr_ig2b_distr.Write()
curr_ig1t_distr.Write()
curr_ig1b_distr.Write()
curr_idrift_distr.Write()


'''
stable_vg3t_value = baseline_voltage(vg3t)
rise_time, trig_entry = rise_time(stable_vg3t_value, vg3t, time_voltage)

print("baseline voltage value "+str(stable_vg3t_value))
print("rise time "+str(rise_time)+" entry #"+str(trig_entry))

vg3t_chargeup = array('f', trig_entry*[0])
time_chargeup = array('f', trig_entry*[0])

for i in range(trig_entry):
    time_chargeup[i] = time_voltage[i]
    vg3t_chargeup[i] = vg3t[i]
''' 
          
gr_tv = ROOT.TGraph(len(time_voltage), time_voltage, vg3t)
gr_tv.SetMarkerStyle(20)
gr_tv.SetName("Voltage_G3T")
gr_tv.Write()

gr_tv = ROOT.TGraph(len(time_voltage), time_voltage, vdrift)
gr_tv.SetMarkerStyle(20)
gr_tv.SetName("Voltage_DRIFT")
gr_tv.Write()

gr_tv = ROOT.TGraph(len(time_voltage), time_voltage, vg3b)
gr_tv.SetMarkerStyle(20)
gr_tv.SetName("Voltage_G3B")
gr_tv.Write()

gr_tv = ROOT.TGraph(len(time_voltage), time_voltage, vg1t)
gr_tv.SetMarkerStyle(20)
gr_tv.SetName("Voltage_G1T")
gr_tv.Write()

gr_tv = ROOT.TGraph(len(time_voltage), time_voltage, vg1b)
gr_tv.SetMarkerStyle(20)
gr_tv.SetName("Voltage_G1B")
gr_tv.Write()

gr_tv = ROOT.TGraph(len(time_voltage), time_voltage, vg2t)
gr_tv.SetMarkerStyle(20)
gr_tv.SetName("Voltage_G2T")
gr_tv.Write()

gr_tv = ROOT.TGraph(len(time_voltage), time_voltage, vg2b)
gr_tv.SetMarkerStyle(20)
gr_tv.SetName("Voltage_G2B")
gr_tv.Write()

hist_t = ROOT.TH1F("h_time", "time", 24667, min(time_c), max(time_c))

for i in range(len(time_c)): 
    #print type(time[i])
    hist_t.Fill(time_c[i])
#print hist_t
hist_t.Write()
 
#vg3t = vg3t[trig_entry:]

#per ig3t ho bisogno di trovare un punto piu avanti




print("first point considered: " +str(trig_entry_current))

ig3t = ig3t[trig_entry_current:]
ig3b = ig3b[trig_entry_current:]
ig2t = ig2t[trig_entry_current:]
ig2b = ig2b[trig_entry_current:]
ig1t = ig1t[trig_entry_current:]
ig1b = ig1b[trig_entry_current:]
idrift = idrift[trig_entry_current:]
time_current = time_current[trig_entry_current:]  


print entries-trig_entry_current-1
print len(time_current)
print len(ig3t)

#time_c for run10 -> instead of time_current

gr_ig3t = ROOT.TGraph(entries-trig_entry_current-1, time_current, ig3t)
gr_ig3t.SetMarkerStyle(20)
gr_ig3t.SetName("ig3t")
gr_ig3t.Write()

gr_ig3b = ROOT.TGraph(entries-trig_entry_current-1, time_current, ig3b)
gr_ig3b.SetMarkerStyle(20)
gr_ig3b.SetName("ig3b")
gr_ig3b.Write()


gr_ig2t = ROOT.TGraph(entries-trig_entry_current-1, time_current, ig2t)
gr_ig2t.SetMarkerStyle(20)
gr_ig2t.SetName("ig2t")
gr_ig2t.Write()

gr_ig2b = ROOT.TGraph(entries-trig_entry_current-1, time_current, ig2b)
gr_ig2b.SetMarkerStyle(20)
gr_ig2b.SetName("ig2b")
gr_ig2b.Write()


gr_ig1t = ROOT.TGraph(entries-trig_entry_current-1, time_current, ig1t)
gr_ig1t.SetMarkerStyle(20)
gr_ig1t.SetName("ig1t")
gr_ig1t.Write()

gr_ig1b = ROOT.TGraph(entries-trig_entry_current-1, time_current, ig1b)
gr_ig1b.SetMarkerStyle(20)
gr_ig1b.SetName("ig1b")
gr_ig1b.Write()

gr_idrift = ROOT.TGraph(entries-trig_entry_current-1, time_current, idrift)
gr_idrift.SetMarkerStyle(20)
gr_idrift.SetName("idrift")
gr_idrift.Write()

outfile.Close()

outfile = ROOT.TFile.Open(outfolder+"/"+ run_date+"_discharges.root", "RECREATE")


#Find_peaks(x, height=None, threshold=None, distance=None, prominence=None, width=None, wlen=None, rel_height=0.5, plateau_size=None)             
peak_high = 30 #10
threshold_peak = .5
prominence_peak = None#.01
distance = 5 #15s
#2000 #50s

peaks_ig1t, properties_ig1t = find_peaks(ig1t, height = peak_high, distance = distance)
peaks_ig1b, properties_ig1b = find_peaks(ig1b, height = peak_high, distance = distance)
peaks_ig2t, properties_ig2t = find_peaks(ig2t, height = peak_high, distance = distance)
peaks_ig2b, properties_ig2b = find_peaks(ig2b, height = peak_high, distance = distance)
peaks_ig3t, properties_ig3t = find_peaks(ig3t, height = peak_high, distance= distance)
peaks_ig3b, properties_ig3b = find_peaks(ig3b, height = peak_high, distance = distance)
peaks_idrift, properties_idrift = find_peaks(idrift, height = peak_high, distance = distance)
print("DRIFT ", peaks_idrift, properties_idrift)
print("G1T ", peaks_ig1t, properties_ig1t)
print("G1B ", peaks_ig1b, properties_ig1b)
print("G2T ", peaks_ig2t, properties_ig2t)
print("G2B ", peaks_ig2b, properties_ig2b)
print("G3T ", peaks_ig3t, properties_ig3t)
print("G3B ", peaks_ig3b, properties_ig3b)


# creo un array per ogni picco individuato da find_peak con : entry, time, height
# ed ogni picco avra anche un secondo array con i valori di ig3t precedenti (10000 punti) che saranno poi mediati ogni 100 comparato con la media totale di quei punti 
# dato che il picco ha solitamente un paio di punti precedenti che si trovano ad altezza simile, prendo i punti a partire da 10 prima 


step = 1000


peaksG3T = []
peaksG3B = []
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

#ofile = ROOT.TFile.Open(run_date+"/"+ run_date+"_discharges.root", "RECREATE")


#tau_3T = peaks_analysis("G3T", ofile, peaksG3T, step)
#tau_3B = peaks_analysis("G3B", ofile, peaksG3B, step)
#tau_2T = peaks_analysis("G2T", ofile, peaksG2T, step)
#tau_2B = peaks_analysis("G2B", ofile, peaksG2B, step)
#tau_1T = peaks_analysis("G1T", ofile, peaksG1T, step)
#tau_1B = peaks_analysis("G1B", ofile, peaksG1B, step)
#tau_drift = peaks_analysis("DRIFT", ofile, peaksDRIFT, step)

'''
#print("ch :G3T")
peaks_analysis("G3T", outfile, peaksG3T, step)
#print("ch :G3B")
peaks_analysis("G3B", outfile, peaksG3B, step)
#print("ch :G2T")
peaks_analysis("G2T", outfile, peaksG2T, step)
#print("ch :G2B")
peaks_analysis("G2B", outfile, peaksG2B, step)
#print("ch :G1T")
peaks_analysis("G1T", outfile, peaksG1T, step)
#print("ch :G1B")
peaks_analysis("G1B", outfile, peaksG1B, step)
#print("ch :GDrift")
peaks_analysis("DRIFT", outfile, peaksDRIFT, step)
'''
outfile.Close()

outfile = ROOT.TFile.Open(outfolder+"/peaks_overview.root", "RECREATE")
        
simultaneous_analysis(peaksG3B, ig3t, ig2b, ig2t, ig1t, ig1b, vg3t, vg2b, vg2t, vg1b, vg1t, outfile, delta_t = 10000)





'''
#mean_tot_1, means_1, rms_1, rms_dev1, rms__1, rms__dev1 = peaksG3T[0].runtime_mean(step)
#gr_peak1, tau1 = peaksG3T[0].tau()


#i_array1 = ig3t[peaks_ig3t[0]-n_points-50: peaks_ig3t[0]-50]
peak1 = peak(entry = peaks_ig3t[0], t_array = time_current, height = ig3t[peaks_ig3t[0]], i_array = ig3t)
mean_tot_1, means_1, rms_1, rms_dev1, rms__1, rms__dev1 = peak1.runtime_mean(step)
#i_array1 = ig3t[peak1.entry: peak1.entry +10000]


# per picco 2 prendo 50 punti prima perche ci sono due picchi
#i_array2 = ig3t[peaks_ig3t[1]-n_points-50: peaks_ig3t[1]-50]
peak2 = peak(entry = peaks_ig3t[1], t_array = time_current, height = ig3t[peaks_ig3t[1]], i_array = ig3t)
mean_tot_2, means_2, rms_2, rms_dev2, rms__2, rms__dev2 = peak2.runtime_mean(step)
#i_array2 = ig3t[peak2.entry: peak2.entry +10000]


i_array3 = ig3t[peaks_ig3t[2]-n_points-50: peaks_ig3t[2]-50]
peak3 = peak(entry = peaks_ig3t[2], t_array = time_current, height = ig3t[peaks_ig3t[2]], i_array = ig3t)
mean_tot_3, means_3, rms_3, rms_dev3, rms__3, rms__dev3 = peak3.runtime_mean(step)
#i_array3 = ig3t[peak3.entry: peak3.entry +10000]


# da aggiustare con le std_dev ma per adesso commentate in quanto rms piu indicativa
#make_canvas("means_peak", mean_tot_1, means_1, step, 1)
#make_canvas("means_peak", mean_tot_2, means_2, step, 2)
#make_canvas("means_peak", mean_tot_3, means_3, step, 3)

make_canvas("rms_peak", rms_1, rms_dev1, rms__1, rms__dev1, step, 1)
#make_canvas("rms_peak", rms_2, rms_dev2, rms__2, rms__dev2, step, 2)
#make_canvas("rms_peak", rms_3, rms_dev3, rms__3, rms__dev3, step, 3)



gr_peak1.SetName("discharge_peak1_IG3T")
cv_peak1 = ROOT.TCanvas()
cv_peak1.cd()
gr_peak1.Draw()

outfile.cd()
cv_peak1.Write()
outfile.Close()

peak1 = array("f", 3*[0])
peak2 = array("f", 3*[0])
peak3 = array("f", 3*[0])

peak1[0] = peaks_ig3t[0]
peak1[1] = time_current[peaks_ig3t[0]]
peak1[2] = ig3t[peaks_ig3t[0]]
peak2[0] = peaks_ig3t[1]
peak2[1] = time_current[peaks_ig3t[1]]
peak2[2] = ig3t[peaks_ig3t[1]]
peak3[0] = peaks_ig3t[2]
peak3[1] = time_current[peaks_ig3t[2]]
peak3[2] = ig3t[peaks_ig3t[2]]




mean_tot_2, means_2 = runtime_mean(ig3t, peak2, n_points, step)
mean_tot_3, means_3 = runtime_mean(ig3t, peak3, n_points, step)
print(means_1)
print(mean_tot_1)
#histo1 = make_canvas(title, mean_tot_1, means_1, step, n_peak)

make_canvas(mean_tot_1, means_1, step, 1)
make_canvas(mean_tot_2, means_2, step, 2)
make_canvas(mean_tot_3, means_3, step, 3)



C1  = ROOT.TCanvas()

n_peaks = len(peaks_ig3t)

print("G3T ", peaks_ig3t, properties_ig3t)
time = array("f", n_peaks*[.0])
for i in range(n_peaks):time[i] = time_current[peaks_ig3t[i]]
print time

points= 10000
step = 100

peak1 = array("f", points*[.0])
peak2 = array("f", points*[.0])
peak3 = array("f", points*[.0])

peak1 = ig3t[peaks_ig3t[0]-points-9:peaks_ig3t[0]-10]
peak2 = ig3t[peaks_ig3t[1]-points-1:peaks_ig3t[1]]
peak3 = ig3t[peaks_ig3t[2]-points-1:peaks_ig3t[2]]

mean_peak1 = runtime_mean(peak1, step)
mean_peak1_tot = ROOT.TLine(-0.5, mean(peak1), 9.5, mean(peak1)) 
means_peak1 = ROOT.TH1F("means_peak1", "runtime means peak 1", 10, -0.5, 9.5)
mean_peak2_tot = mean(peak2)
mean_peak2 = runtime_mean(peak2, step)
means_peak2 = ROOT.TH1F("means_peak2", "runtime means peak 2", 10, -0.5, 9.5)
mean_peak3_tot = mean(peak3)
mean_peak3 = runtime_mean(peak3, step)
means_peak3 = ROOT.TH1F("means_peak3", "runtime means peak 3", 10, -0.5, 9.5)



print(mean_peak1_tot)
print(mean_peak2_tot)
print(mean_peak3_tot)

#means_peak1.SetBinContent(0, mean_peak1_tot)
means_peak2.SetBinContent(0, mean_peak2_tot)
means_peak3.SetBinContent(0, mean_peak3_tot)
for i in range(1, step): 
    means_peak1.SetBinContent(i, mean_peak1[i-1])
    means_peak2.SetBinContent(i, mean_peak2[i-1])
    means_peak3.SetBinContent(i, mean_peak3[i-1])
  
c1.cd()
means_peak1.Draw()
mean_peak1_tot.Draw("same")
c1.Write()
means_peak1.Write()
means_peak2.Write()
means_peak3.Write()
'''

    
# Da FARE: 
#   studio della carica di V nei primi istanti solo per il file 0000
#   calcolo della entry a cui si stabilizza e iniziare la successiva ricerca dopo questa entry
 
#   graph con iVStime VoltVStime
#   histos i e V
#   find_peaks
#   histos intorno ai picchi come sul foglio
#   medie dei valori in corrente prima dei picchi
#   DOPO AVER COMPLETATO QUESTO PER UN SINGOLO CANALE: graph con i canali sulle x e la entry dei picchi sulle y 
