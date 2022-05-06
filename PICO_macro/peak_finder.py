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
parser.add_option('-i', '--input', dest='input', type='string', default = 'CERN_20191212_0000', help="Enter an input root file")
(opt, args) = parser.parse_args()

ROOT.gStyle.SetOptStat(0000)
ROOT.gStyle.SetOptFit(1111)
ROOT.gROOT.SetBatch()

startTime = datetime.datetime.now()
print("starting at "+str(startTime) )

folder = opt.folder
infile = ROOT.TFile.Open(folder + '/' + opt.input+'.root')
print("input file :", infile)
tree = infile.Get("t1")
n_jump = 100
entries = tree.GetEntries()-n_jump


#subfold = opt.input.strip('.root')
#run_date = opt.folder.replace('GEMData', 'GEM_plot')+'/' #/eos/home-a/acagnott/GEM_plot/CERNdata_dischargesfiltertest/
run_date = '/eos/home-a/acagnott/www/GEM/P5data/'
if not os.path.exists(run_date):
    os.makedirs(run_date)
run_date = run_date + opt.input#.strip('.root')
if not os.path.exists(run_date):
    os.makedirs(run_date)
print("directory " +run_date+" has been created")


os.system('cp /eos/home-a/acagnott/www/GEM/filtertests/PICO1_run0000/.htaccess '+run_date)

frequency_data = (1./280.)*10**3 #ms 
# 280 Hz

#############
downscale = 50
############


#Entries = 10000
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
vg3t = array('f')
vg3b = array('f')
vdrift = array('f')
time_current = array('f')
time_voltage = array('f')
human_time = array('f')

#offset

m=0
tree.GetEntry(0)
start_run = datetime.datetime.fromtimestamp(tree.Time)
tree.GetEntry(tree.GetEntries()-1)
stop_run = datetime.datetime.fromtimestamp(tree.Time)

deltatime = (stop_run-start_run)
deltatime = deltatime.seconds +deltatime.microseconds*10**(-6)

deltatime = deltatime / tree.GetEntries()

last_value = 1000000
for i in range(entries):
    if i<n_jump : 
        continue
    tree.GetEntry(i)
    ig1t.append(tree.I_G1T)
    ig1b.append(tree.I_G1B)
    ig2t.append(tree.I_G2T)
    ig2b.append(tree.I_G2B)
    ig3t.append(tree.I_G3T)
    ig3b.append(tree.I_G3B)
    idrift.append(tree.I_drift)
    #delta = datetime.datetime.fromtimestamp(tree.Time)-start_run#i*frequency_data*downscale
    time_current.append(deltatime*i) #delta.seconds + delta.microseconds*10**6

    if tree.V_G1T<10000 and tree.V_G2T!=last_value:
        m +=1
        vg1t.append(tree.V_G1T)
        vg1b.append(tree.V_G1B)
    	vg2t.append(tree.V_G2T)
    	vg2b.append(tree.V_G2B)
    	vg3t.append(tree.V_G3T)
    	vg3b.append(tree.V_G3B)
    	vdrift.append(tree.V_drift)
        #delta = datetime.datetime.fromtimestamp(tree.Time)-start_run#i*frequency_data*downscale
        time_voltage.append(deltatime * i) #delta.seconds + delta.microseconds*10**6
    	#time_voltage[i] = i*frequency_data*downscale
        last_value = tree.V_G2T
    #print type(timestamp[i]), timestamp[i]
    #human_time[i] = ctime(timestamp[i])
#print timestamp
#print ctime(timestamp[0])
### Produzione graph di default
#make_graph(entries, x_array, y_array, name, title, x_title, y_title, color, style = 20)
#print 'entries:', entries
#print 'ig3b lenght', len(ig3b)
#print 'time_current lenght', len(time_current)

#print m
#print len(vg2t)
#print vg2t
#print len(time_voltage)


gr_ig1t = make_graph(len(ig1t), time_current, ig1t, "Current_G1T", "Current G1T "+start_run.strftime('%a,%d %b %Y %H:%M:%S.%f'), "Time (s)", "Current (nA)", colors[1])
gr_ig1b = make_graph(len(ig1b), time_current, ig1b, "Current_G1B", "Current G1B"+start_run.strftime('%a,%d %b %Y %H:%M:%S.%f'), "Time (s)", "Current (nA)", colors[2])
gr_ig2t = make_graph(len(ig2t), time_current, ig2t, "Current_G2T", "Current G2T"+start_run.strftime('%a,%d %b %Y %H:%M:%S.%f'), "Time (s)", "Current (nA)", colors[3])
gr_ig2b = make_graph(len(ig2b), time_current, ig2b, "Current_G2B", "Current G2B"+start_run.strftime('%a,%d %b %Y %H:%M:%S.%f'), "Time (s)", "Current (nA)", colors[4])
gr_ig3t = make_graph(len(ig3t), time_current, ig3t, "Current_G3T", "Current G3T"+start_run.strftime('%a,%d %b %Y %H:%M:%S.%f'), "Time (s)", "Current (nA)", colors[5])
gr_ig3b = make_graph(len(ig3b), time_current, ig3b, "Current_G3B", "Current G3B"+start_run.strftime('%a,%d %b %Y %H:%M:%S.%f'), "Time (s)", "Current (nA)", colors[6])
gr_idrift = make_graph(len(idrift), time_current, idrift, "Current_Drift", "Current Drift"+start_run.strftime('%a,%d %b %Y %H:%M:%S.%f'), "Time (s)", "Current (nA)", colors[0])

gr_vg1t = make_graph(m, time_voltage, vg1t, "Voltage_G1T", "Voltage G1T"+start_run.strftime('%a,%d %b %Y %H:%M:%S.%f'), "Time (s)", "Voltage (V)", colors[1])
gr_vg1b = make_graph(m, time_voltage, vg1b, "Voltage_G1B", "Voltage G1B"+start_run.strftime('%a,%d %b %Y %H:%M:%S.%f'), "Time (s)", "Voltage (V)", colors[2])
gr_vg2t = make_graph(m, time_voltage, vg2t, "Voltage_G2T", "Voltage G2T"+start_run.strftime('%a,%d %b %Y %H:%M:%S.%f'), "Time (s)", "Voltage (V)", colors[3])
gr_vg2b = make_graph(m, time_voltage, vg2b, "Voltage_G2B", "Voltage G2B"+start_run.strftime('%a,%d %b %Y %H:%M:%S.%f'), "Time (s)", "Voltage (V)", colors[4])
gr_vg3t = make_graph(m, time_voltage, vg3t, "Voltage_G3T", "Voltage G3T"+start_run.strftime('%a,%d %b %Y %H:%M:%S.%f'), "Time (s)", "Voltage (V)", colors[5])
gr_vg3b = make_graph(m, time_voltage, vg3b, "Voltage_G3B", "Voltage G3B"+start_run.strftime('%a,%d %b %Y %H:%M:%S.%f'), "Time (s)", "Voltage (V)", colors[6])
gr_vdrift = make_graph(m, time_voltage, vdrift, "Voltage_Drift", "Voltage Drift"+start_run.strftime('%a,%d %b %Y %H:%M:%S.%f'), "Time (s)", "Voltage (V)", colors[0])

time = datetime.datetime.now()
print("printing graphs at"+str(time))


### Stampa graph di default
print_hist(run_date, gr_ig1t, "Current_G1T", "AL*")
print_hist(run_date, gr_ig1b, "Current_G1B", "AL*")
print_hist(run_date, gr_ig2t, "Current_G2T", "AL*")
print_hist(run_date, gr_ig2b, "Current_G2B", "AL*")
print_hist(run_date, gr_ig3t, "Current_G3T", "AL*")
print_hist(run_date, gr_ig3b, "Current_G3B", "AL*")
print_hist(run_date, gr_idrift, "Current_Drift", "AL*")

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

h_vg1t = make_hist(tree, 'V_G1T', 'Voltage distribution in G1T; Voltage (V); Events', 100, int(min(vg1t))-1, int(max(vg1t))+1)
h_vg1b = make_hist(tree, 'V_G1B', 'Voltage distribution in G1B; Voltage (V); Events', 100, int(min(vg1b))-1, int(max(vg1b))+1) 
h_vg2t = make_hist(tree, 'V_G2T', 'Voltage distribution in G2T; Voltage (V); Events', 100, int(min(vg2t))-1, int(max(vg2t))+1) 
h_vg2b = make_hist(tree, 'V_G2B', 'Voltage distribution in G2B; Voltage (V); Events', 100, int(min(vg2b))-1, int(max(vg2b))+1) 
h_vg3t = make_hist(tree, 'V_G3T', 'Voltage distribution in G3T; Voltage (V); Events', 100, int(min(vg3t))-1, int(max(vg3t))+1) 
h_vg3b = make_hist(tree, 'V_G3B', 'Voltage distribution in G3B; Voltage (V); Events', 100, int(min(vg3b))-1, int(max(vg3b))+1) 
h_vdrift = make_hist(tree, 'V_drift', 'Voltage distribution in drift; Voltage (V); Events', 100, int(min(vdrift))-1, int(max(vdrift))+1)

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

all_current = [gr_ig1t.Clone(), gr_ig1b.Clone(), gr_ig2t.Clone(), gr_ig2b.Clone(), gr_ig3t.Clone(), gr_ig3b.Clone(),gr_idrift.Clone()]
print_hist(run_date, all_current, 'All_currents', "AL*")#,  "Current and Peak G1T; Time (ms); Current (nA)")
all_volt = [gr_vg1t.Clone(), gr_vg1b.Clone(), gr_vg2t.Clone(), gr_vg2b.Clone(), gr_vg3t.Clone(), gr_vg3b.Clone(),gr_vdrift.Clone()]
print_hist(run_date, all_volt, 'All_voltages', "A*")

