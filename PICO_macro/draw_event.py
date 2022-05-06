import ROOT
from array import array
from utils import *
import os
import optparse
from datetime import datetime

usage = 'draw_event.py' #-i PICO*_run_00**
parser = optparse.OptionParser(usage)
parser.add_option('-i', '--input', dest='input', type='string', default = 'PICO1_0001', help="Enter an input root file")
parser.add_option('-f', '--folder', dest='folder', type='string', default = '/eos/home-a/adeiorio/GEM/Goliath/', help='Default folder is /eos/home-a/adeiorio/GEM/Goliath')
parser.add_option('-e', '--entry', dest='entry', type='int', default = 0, help="Enter the event entry")
(opt, args) = parser.parse_args()

folder = opt.folder
if 'adeiorio' in folder: outfolder = folder.replace("adeiorio/GEM/","acagnott/GEM_plot/")
elif 'acagnott' in folder: outfolder = folder.replace("GEMData","GEM_plot")
outfolder = outfolder + "/"+opt.input+"/graph_"+str(opt.entry)
print outfolder
#outfolder = "/eos/home-a/acagnott/GEM_plot/LABGEM_scariche/"+opt.input+"/graph_"+str(opt.entry)
if not os.path.exists(outfolder):
    os.makedirs(outfolder)


if not "000" in opt.input :
    
    infile = ROOT.TFile.Open(folder+"/"+opt.input+"_skim.root")
    #infile = ROOT.TFile.Open(folder+"/"+opt.input+".root")
    print infile
    outfile = ROOT.TFile.Open(outfolder+"/graphs.root","RECREATE")
else:

    infile = ROOT.TFile.Open(folder+"/"+opt.input+"_skim.root")
    #infile = ROOT.TFile.Open(folder+"/"+opt.input+".root")
    print infile
    outfile = ROOT.TFile.Open(outfolder+"/graphs.root","RECREATE")

vdrift = []
vg1t = []
vg1b = []
vg2t =[]
vg2b =[]
vg3t =[]
vg3b =[] 
time_volt =[]
delta1 = []
delta2 = []
delta3 = []
delta4 = []
delta5 = []
delta6 = []


tree = infile.Get("t1")

tree.GetEntry(opt.entry)

idrift = tree.IDRIFT
ig1t = tree.IG1T
ig1b = tree.IG1B
ig2t = tree.IG2T
ig2b = tree.IG2B
ig3t = tree.IG3T
ig3b = tree.IG3B
vdrift = (tree.VDRIFT)
vg1t = (tree.VG1T)
vg1b = (tree.VG1B)
vg2t = (tree.VG2T)
vg2b = (tree.VG2B)
vg3t = (tree.VG3T)
vg3b = (tree.VG3B)
dtime = tree.deltatime_voltage[len(tree.deltatime_voltage)-1]/len(vg3t)
time_volt = [i*dtime  for i in range(len(vg3t))]
time_volt = array('f', time_volt)
#time_volt = (tree.deltatime_voltage)#tree.time_current#tree.deltatime_current
delta1 = (tree.DeltaV_drg1t)
delta2 = (tree.DeltaV_g1tg1b)
delta3 = (tree.DeltaV_g1bg2t)
delta4 = (tree.DeltaV_g2tg2b)
delta5 = (tree.DeltaV_g2bg3t)
delta6 = (tree.DeltaV_g3tg3b)
dtime = tree.deltatime_current[len(tree.deltatime_current)-1]/len(ig3t)
time =  [i*dtime  for i in range(len(ig3t))]
time = array('f', time)
#time = tree.deltatime_current
timestamp_current = tree.timestamp_current
timestamp_voltage = tree.timestamp_voltage

dtime = datetime.fromtimestamp(timestamp_current[len(idrift)-1])-datetime.fromtimestamp(timestamp_current[0])
dtime_curr = (dtime.seconds+dtime.microseconds*10**-6)/len(idrift)
dtime_volt = (dtime.seconds+dtime.microseconds*10**-6)/len(vdrift)
time_current = array('f',[dtime_curr *j  for j in range(len(idrift))])
time_voltage = array('f',[dtime_volt *j  for j in range(len(vdrift))])

print 'time_volt '+ str(len(time_volt))
print 'time '+ str(len(time))
print 'idrift ' + str(len(idrift))
print 'vdridt ' + str(len(idrift))

start_time = datetime.fromtimestamp(tree.timestamp_current[0])
start_time = start_time.strftime('%a,%d %b %Y %H:%M:%S')

graph_dr = make_graph(1900, time_current, idrift, "graph_idrift", "idrift "+start_time, "time(s)", "current(nA)", ROOT.kBlack)
graph_g1t = make_graph(1900, time_current, ig1t, "graph_ig1t", "ig1t "+start_time, "time(s)", "current(nA)", ROOT.kGreen)
graph_g1b = make_graph(1900, time_current, ig1b, "graph_ig1b", "ig1b "+start_time, "time(s)", "current(nA)", ROOT.kGreen+3)
graph_g2t = make_graph(1900, time_current, ig2t, "graph_ig2t", "ig2t "+start_time, "time(s)", "current(nA)", ROOT.kCyan)
graph_g2b = make_graph(1900, time_current, ig2b, "graph_ig2b", "ig2b "+start_time, "time(s)", "current(nA)", ROOT.kCyan+3)    
graph_g3t = make_graph(1900, time_current, ig3t, "graph_ig3t", "ig3t "+start_time, "time(s)", "current(nA)", ROOT.kRed)
graph_g3b = make_graph(1900, time_current, ig3b, "graph_ig3b", "ig3b "+start_time, "time(s)", "current(nA)", ROOT.kRed+3)

all_current = [graph_dr.Clone(), graph_g1t.Clone(), graph_g1b.Clone(), graph_g2t.Clone(), graph_g2b.Clone(), graph_g3t.Clone(), graph_g3b.Clone()]
print_hist(outfolder, all_current, opt.input+'_'+ str(opt.entry)+'_all_currents', "AP")

#print delta1

graph_delta1 = make_graph(len(delta1), time_voltage, delta1, "graph_delta1", "#Delta(G1T-Drift) "+start_time, "time(s)", "Voltage(V)", ROOT.kBlack)
graph_delta2 = make_graph(len(delta1), time_voltage, delta2, "graph_delta2", "#Delta(G1B-G1T) "+start_time , "time(s)", "Voltage(V)", ROOT.kGreen)
graph_delta3 = make_graph(len(delta1), time_voltage, delta3, "graph_delta3", "#Delta(G2T-G11B) "+start_time, "time(s)", "Voltage(V)", ROOT.kGreen+3)
graph_delta4 = make_graph(len(delta1), time_voltage, delta4, "graph_delta4", "#Delta(G2B-G2T) "+start_time , "time(s)", "Voltage(V)", ROOT.kCyan)
graph_delta5 = make_graph(len(delta1), time_voltage, delta5, "graph_delta5", "#Delta(G3T-G21B) "+start_time, "time(s)", "Voltage(V)", ROOT.kCyan+3)
graph_delta6 = make_graph(len(delta1), time_voltage, delta6, "graph_delta6", "#Delta(G3B-G3T) "+start_time , "time(s)", "Voltage(V)", ROOT.kRed)

graph_dr.Write()
graph_g1t.Write()
graph_g1b.Write()
graph_g2t.Write()
graph_g2b.Write()
graph_g3t.Write()
graph_g3b.Write()
    
graph_delta1.Write()
graph_delta2.Write()
graph_delta3.Write()
graph_delta4.Write()
graph_delta5.Write()
graph_delta6.Write()
    
all_deltaV = [graph_delta1.Clone(), graph_delta2.Clone(), graph_delta3.Clone(), graph_delta4.Clone(), graph_delta5.Clone(), graph_delta6.Clone()]
print_hist(outfolder, all_deltaV, opt.input+'_'+ str(opt.entry)+'_all_deltaV', "AP")

graph_vdr = make_graph(len(vdrift), time_voltage, vdrift, "graph_vdrift", "vdrift "+start_time, "time(s)", "voltage(V)", ROOT.kBlack)
graph_vg1t = make_graph(len(vdrift), time_voltage, vg1t, "graph_vg1t", "vg1t "+start_time, "time(s)", "voltage(V)", ROOT.kGreen)
graph_vg1b = make_graph(len(vdrift), time_voltage, vg1b, "graph_vg1b", "vg1b "+start_time, "time(s)", "voltage(V)", ROOT.kGreen+3)
graph_vg2t = make_graph(len(vdrift), time_voltage, vg2t, "graph_vg2t", "vg2t "+start_time, "time(s)", "voltage(V)", ROOT.kCyan)
graph_vg2b = make_graph(len(vdrift), time_voltage, vg2b, "graph_vg2b", "vg2b "+start_time, "time(s)", "voltage(V)", ROOT.kCyan+3)    
graph_vg3t = make_graph(len(vdrift), time_voltage, vg3t, "graph_vg3t", "vg3t "+start_time, "time(s)", "voltage(V)", ROOT.kRed)
graph_vg3b = make_graph(len(vdrift), time_voltage, vg3b, "graph_vg3b", "vg3b "+start_time, "time(s)", "voltage(V)", ROOT.kRed+3)

all_volt = [graph_vdr.Clone(), graph_vg1t.Clone(), graph_vg1b.Clone(), graph_vg2t.Clone(), graph_vg2b.Clone(), graph_vg3t.Clone(), graph_vg3b.Clone()]
print_hist(outfolder, all_volt, opt.input+'_'+ str(opt.entry)+'_all_voltages', "AP")


graph_vdr.Write()
graph_vg1t.Write()
graph_vg1b.Write()
graph_vg2t.Write()
graph_vg2b.Write()
graph_vg3t.Write()
graph_vg3b.Write()
