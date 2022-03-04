import ROOT
from array import array
from utils import *
import os
import optparse

usage = 'draw_event.py' #-i PICO*_run_00**
parser = optparse.OptionParser(usage)
parser.add_option('-i', '--input', dest='input', type='string', default = 'PICO1_0001', help="Enter an input root file")
parser.add_option('-f', '--folder', dest='folder', type='string', default = '/eos/home-a/adeiorio/GEM/Goliath/', help='Default folder is /eos/home-a/adeiorio/GEM/Goliath')
parser.add_option('-e', '--entry', dest='entry', type='int', default = 0, help="Enter the event entry")
(opt, args) = parser.parse_args()

folder = opt.folder
outfolder = folder.replace("adeiorio/GEM/","acagnott/GEM_plot/")
outfolder = outfolder + "/"+opt.input+"/graph_"+str(opt.entry)
print outfolder
#outfolder = "/eos/home-a/acagnott/GEM_plot/LABGEM_scariche/"+opt.input+"/graph_"+str(opt.entry)
if not os.path.exists(outfolder):
    os.makedirs(outfolder)


if not "000" in opt.input :
    
    infile = ROOT.TFile.Open(folder+"/"+opt.input+"_skim.root")
    print infile
    outfile = ROOT.TFile.Open(outfolder+"/graphs.root","RECREATE")
else:

    infile = ROOT.TFile.Open(folder+"/"+opt.input+"_skim.root")
    print infile
    outfile = ROOT.TFile.Open(outfolder+"/graphs.root","RECREATE")

tree = infile.Get("t1")


tree.GetEntry(opt.entry)

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
time = tree.time_current#tree.deltatime_current

graph_dr = make_graph(1900, time, idrift, "graph_idrift", "idrift", "time(s)", "current(nA)", ROOT.kBlack)
graph_g1t = make_graph(1900, time, ig1t, "graph_ig1t", "ig1t", "time(s)", "current(nA)", ROOT.kGreen)
graph_g1b = make_graph(1900, time, ig1b, "graph_ig1b", "ig1b", "time(s)", "current(nA)", ROOT.kGreen+3)
graph_g2t = make_graph(1900, time, ig2t, "graph_ig2t", "ig2t", "time(s)", "current(nA)", ROOT.kCyan)
graph_g2b = make_graph(1900, time, ig2b, "graph_ig2b", "ig2b", "time(s)", "current(nA)", ROOT.kCyan+3)    
graph_g3t = make_graph(1900, time, ig3t, "graph_ig3t", "ig3t", "time(s)", "current(nA)", ROOT.kRed)
graph_g3b = make_graph(1900, time, ig3b, "graph_ig3b", "ig3b", "time(s)", "current(nA)", ROOT.kRed+3)

all_current = [graph_dr.Clone(), graph_g1t.Clone(), graph_g1b.Clone(), graph_g2t.Clone(), graph_g2b.Clone(), graph_g3t.Clone(), graph_g3b.Clone()]
print_hist(outfolder, all_current, opt.input+'_'+ str(opt.entry)+'_all_currents', "AP")

graph_delta1 = make_graph(1900, time, delta1, "graph_delta1", "#Delta(G1T-Drift)", "time(s)", "Voltage(V)", ROOT.kBlack)
graph_delta2 = make_graph(1900, time, delta2, "graph_delta2", "#Delta(G1B-G1T)", "time(s)", "Voltage(V)", ROOT.kGreen)
graph_delta3 = make_graph(1900, time, delta3, "graph_delta3", "#Delta(G2T-G1B)", "time(s)", "Voltage(V)", ROOT.kGreen+3)
graph_delta4 = make_graph(1900, time, delta4, "graph_delta4", "#Delta(G2B-G2T)", "time(s)", "Voltage(V)", ROOT.kCyan)
graph_delta5 = make_graph(1900, time, delta5, "graph_delta5", "#Delta(G3T-G2B)", "time(s)", "Voltage(V)", ROOT.kCyan+3)
graph_delta6 = make_graph(1900, time, delta6, "graph_delta6", "#Delta(G3B-G3T)", "time(s)", "Voltage(V)", ROOT.kRed)

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
