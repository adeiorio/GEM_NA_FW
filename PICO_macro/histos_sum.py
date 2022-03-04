import ROOT
import os
import optparse

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch()        # don't pop up canvases
ROOT.TH1.SetDefaultSumw2()
ROOT.TGaxis.SetMaxDigits(3)


def save_histo(folder, histo):
    c1 = ROOT.TCanvas()
    histo.Draw("colz")
    c1.Print(folder+histo.GetName()+".png")


usage = 'histos_sum.py.py' #-p PICO1
parser = optparse.OptionParser(usage)

parser.add_option('-p', '--pico', dest='pico', type='string', default = 'PICO1', help="Enter PICO number")
(opt, args) = parser.parse_args()

pico = opt.pico

final_h = ROOT.TH2F("integral_pulseheight","integral/pulse height VS pulse height ALL RUN; pulse height(nA); integral/pulse height",
                    10000, 0, 190000, 200, 0, 200)

h_chs = ROOT.TH1F("h_chs", "largest pulse height", 3, -0.5, 2.5)
h_chs.GetXaxis().SetBinLabel(1, "G1")
h_chs.GetXaxis().SetBinLabel(2, "G2")
h_chs.GetXaxis().SetBinLabel(3, "G3")

h_tau = ROOT.TH1F("tau", "tau; C(F)", 100, 0, 50*10**(-9))
h_pulseheight = ROOT.TH1F("pulseheight", "pulseheight; current(nA)", 100, 50, 180000)

h_drift_ph = ROOT.TH1F("h_drift_ph", "pulseheight drift; current(nA)", 120, -20*10**3, 20*10**3)

stack_pulseh = ROOT.THStack("stack_pulseh","pulse height; current(nA)")
stack_typ2_pulseh = ROOT.THStack("stack_type2_pulseh","pulse height type2 events; current(nA)")


h_type2_pulseheight_drift =  ROOT.TH1F("type2_pulseheight_drift", "Pulse height event type 2", 500, 50, 5000)
h_type2_pulseheight_drift.SetFillColor(ROOT.kBlack)
h_type2_pulseheight_g1t =  ROOT.TH1F("type2_pulseheight_g1t", "Pulse height event type 2", 500, 50, 5000)
h_type2_pulseheight_g1t.SetFillColor(ROOT.kGreen)
h_type2_pulseheight_g1b =  ROOT.TH1F("type2_pulseheight_g1b", "Pulse height event type 2", 500, 50, 5000)
h_type2_pulseheight_g1b.SetFillColor(ROOT.kGreen+3)
h_type2_pulseheight_g2t =  ROOT.TH1F("type2_pulseheight_g2t", "Pulse height event type 2", 500, 50, 5000)
h_type2_pulseheight_g2t.SetFillColor(ROOT.kCyan)
h_type2_pulseheight_g2b =  ROOT.TH1F("type2_pulseheight_g2b", "Pulse height event type 2", 500, 50, 5000)
h_type2_pulseheight_g2b.SetFillColor(ROOT.kCyan+3)
h_type2_pulseheight_g3t =  ROOT.TH1F("type2_pulseheight_g3t", "Pulse height event type 2", 500, 50, 5000)
h_type2_pulseheight_g3t.SetFillColor(ROOT.kRed)
h_type2_pulseheight_g3b =  ROOT.TH1F("type2_pulseheight_g3b", "Pulse height event type 2", 500, 50, 5000)
h_type2_pulseheight_g3b.SetFillColor(ROOT.kRed+3)
h_type2_ph = {"drift":h_type2_pulseheight_drift, "g1t":h_type2_pulseheight_g1t, "g1b":h_type2_pulseheight_g1b, "g2t":h_type2_pulseheight_g2t,
              "g2b":h_type2_pulseheight_g2b, "g3t":h_type2_pulseheight_g3t, "g3b":h_type2_pulseheight_g3b}

'''pulseh_nbins = 40
pulseh_min =1000
pulseh_max =40000

deltav_nbins = 10
deltav_min = 0
deltav_max = 5

deltamax_nbins = 10
deltamax_min = 0
deltamax_max = 10

h2_deltav_pulseh_drift = ROOT.TH2F("h2_deltav_pulseh_drift", "(V_max-V_mean) vs Pulse height; Pulse height(nA); (V_max-V_mean)(V)", 
                                   15, 0, 15000, deltav_nbins, deltav_min, deltav_max)
h2_deltav_pulseh_g1t = ROOT.TH2F("h2_deltav_pulseh_g1t", "(V_max-V_mean) vs Pulse height; Pulse height(nA); (V_max-V_mean)(V)", 
                                 pulseh_nbins,pulseh_min, pulseh_max, deltav_nbins, deltav_min, deltav_max)
h2_deltav_pulseh_g1b = ROOT.TH2F("h2_deltav_pulseh_g1b", "(V_max-V_mean) vs Pulse height; Pulse height(nA); (V_max-V_mean)(V)", 
                                 pulseh_nbins,pulseh_min, pulseh_max, deltav_nbins, deltav_min, deltav_max)
h2_deltav_pulseh_g2t = ROOT.TH2F("h2_deltav_pulseh_g2t", "(V_max-V_mean) vs Pulse height; Pulse height(nA); (V_max-V_mean)(V)", 
                                 pulseh_nbins,pulseh_min, pulseh_max, deltav_nbins, deltav_min, deltav_max)
h2_deltav_pulseh_g2b = ROOT.TH2F("h2_deltav_pulseh_g2b", "(V_max-V_mean) vs Pulse height; Pulse height(nA); (V_max-V_mean)(V)", 
                                 pulseh_nbins,pulseh_min, pulseh_max, deltav_nbins, deltav_min, deltav_max)
h2_deltav_pulseh_g3t = ROOT.TH2F("h2_deltav_pulseh_g3t", "(V_max-V_mean) vs Pulse height; Pulse height(nA); (V_max-V_mean)(V)", 
                                 pulseh_nbins,pulseh_min, pulseh_max, deltav_nbins, deltav_min, deltav_max)
h2_deltav_pulseh_g3b = ROOT.TH2F("h2_deltav_pulseh_g3b", "(V_max-V_mean) vs Pulse height; Pulse height(nA); (V_max-V_mean)(V)", 
                                 pulseh_nbins,pulseh_min, pulseh_max, deltav_nbins, deltav_min, deltav_max)

h2_deltamax_pulseh_drift = ROOT.TH2F("h2_deltamax_pulseh_drift", "(V_max-V_min) vs Pulse height; Pulse height(nA); (V_max-V_min)(V)", 
                                     15,pulseh_min, 15000, deltamax_nbins, deltamax_min, deltamax_max)
h2_deltamax_pulseh_g1t = ROOT.TH2F("h2_deltamax_pulseh_g1t", "(V_max-V_min) vs Pulse height; Pulse height(nA); (V_max-V_min)(V)", 
                                 pulseh_nbins,pulseh_min, pulseh_max, deltamax_nbins, deltamax_min, deltamax_max)
h2_deltamax_pulseh_g1b = ROOT.TH2F("h2_deltamax_pulseh_g1b", "(V_max-V_min) vs Pulse height; Pulse height(nA); (V_max-V_min)(V)", 
                                 pulseh_nbins,pulseh_min, pulseh_max, deltamax_nbins, deltamax_min, deltamax_max)
h2_deltamax_pulseh_g2t = ROOT.TH2F("h2_deltamax_pulseh_g2t", "(V_max-V_min) vs Pulse height; Pulse height(nA); (V_max-V_min)(V)", 
                                 pulseh_nbins,pulseh_min, pulseh_max, deltamax_nbins, deltamax_min, deltamax_max)
h2_deltamax_pulseh_g2b = ROOT.TH2F("h2_deltamax_pulseh_g2b", "(V_max-V_min) vs Pulse height; Pulse height(nA); (V_max-V_min)(V)", 
                                 pulseh_nbins,pulseh_min, pulseh_max, deltamax_nbins, deltamax_min, deltamax_max)
h2_deltamax_pulseh_g3t = ROOT.TH2F("h2_deltamax_pulseh_g3t", "(V_max-V_min) vs Pulse height; Pulse height(nA); (V_max-V_min)(V)", 
                                 pulseh_nbins,pulseh_min, pulseh_max, deltamax_nbins, deltamax_min, deltamax_max)
h2_deltamax_pulseh_g3b = ROOT.TH2F("h2_deltamax_pulseh_g3b", "(V_max-V_min) vs Pulse height; Pulse height(nA); (V_max-V_min)(V)", 
                                 pulseh_nbins,pulseh_min, pulseh_max, deltamax_nbins, deltamax_min, deltamax_max)

h2_V_max_pulseh_drift = ROOT.TH2F("h2_V_max_pulseh_drift", "V_max vs Pulse height; Pulse height(nA); V_max(V)", 
                                  15, 0, 15000, 50,  -3320, -3270) 
h2_V_max_pulseh_g1t = ROOT.TH2F("h2_V_max_pulseh_g1t", "V_max vs Pulse height; Pulse height(nA); V_max(V)", 
                                 pulseh_nbins,pulseh_min, pulseh_max, 50, -2530, -2480)
h2_V_max_pulseh_g1b = ROOT.TH2F("h2_V_max_pulseh_g1b", "V_max vs Pulse height; Pulse height(nA); V_max(V)", 
                                 pulseh_nbins,pulseh_min, pulseh_max, 50, -2130, -2080)
h2_V_max_pulseh_g2t = ROOT.TH2F("h2_V_max_pulseh_g2t", "V_max vs Pulse height; Pulse height(nA); V_max(V)", 
                                 pulseh_nbins,pulseh_min, pulseh_max, 50, -1820, -1770)
h2_V_max_pulseh_g2b = ROOT.TH2F("h2_V_max_pulseh_g2b", "V_max vs Pulse height; Pulse height(nA); V_max(V)", 
                                 pulseh_nbins,pulseh_min, pulseh_max, 50, -1435, -1385)
h2_V_max_pulseh_g3t = ROOT.TH2F("h2_V_max_pulseh_g3t", "V_max vs Pulse height; Pulse height(nA); V_max(V)", 
                                 pulseh_nbins,pulseh_min, pulseh_max, 50, -825, -795)
h2_V_max_pulseh_g3b = ROOT.TH2F("h2_V_max_pulseh_g3b", "V_max vs Pulse height; Pulse height(nA); V_max(V)", 
                                 pulseh_nbins,pulseh_min, pulseh_max, 50, -460, -410)

'''
pulseheight_g1 = ROOT.TH1F("pulseheight_g1", "pulseheight; current(nA)", 100, 50, 180000)
pulseheight_g1.SetFillColor(ROOT.kGreen)
pulseheight_g2 = ROOT.TH1F("pulseheight_g2", "pulseheight; current(nA)", 100, 50, 180000)
pulseheight_g2.SetFillColor(ROOT.kCyan)
pulseheight_g3 = ROOT.TH1F("pulseheight_g3", "pulseheight; current(nA)", 100, 50, 180000)
pulseheight_g3.SetFillColor(ROOT.kRed)


if '1' in pico : n_run = 34
else : n_run = 33

for i in range(1, n_run):
    if i<10:
        print i
        print "/eos/home-a/acagnott/GEM_plot/"+pico+"_run0000"+str(i)+"/discharges_count.root"
        if os.path.exists("/eos/home-a/acagnott/GEM_plot/"+pico+"_run000"+str(i)+"/discharges_count.root"):
            print "ok"
            infile = ROOT.TFile.Open("/eos/home-a/acagnott/GEM_plot/"+pico+"_run000"+str(i)+"/discharges_count.root")
            print infile
            histo = ROOT.TH2F(infile.Get("heig_int"))
            print histo.GetEntries()
            final_h.Add(histo)
            hist = ROOT.TH1F(infile.Get("h_chs"))
            h_chs.Add(hist)
            tau = ROOT.TH1F(infile.Get("tau"))
            h_tau.Add(tau)
            pulse = ROOT.TH1F(infile.Get("pulseheight"))
            h_pulseheight.Add(pulse)
            h = ROOT.TH1F(infile.Get("pulseheight_g1"))
            pulseheight_g1.Add(h)
            h = ROOT.TH1F(infile.Get("pulseheight_g2"))
            pulseheight_g2.Add(h)
            h = ROOT.TH1F(infile.Get("pulseheight_g3"))
            pulseheight_g3.Add(h)
            
            h = ROOT.TH1F(infile.Get("h_drift_ph"))
            h_drift_ph.Add(h)
            for ch in ["drift", "g1t", "g1b", "g2t", "g2b", "g3t", "g3b"]:
                h = ROOT.TH1F(infile.Get("type2_pulseheight_"+ch))
                h_type2_ph[ch].Add(h)
            
            '''h2d = ROOT.TH2F(infile.Get("h2_deltav_pulseh_drift"))
            h2_deltav_pulseh_drift.Add(h2d)
            h2d = ROOT.TH2F(infile.Get("h2_deltamax_pulseh_drift"))
            h2_deltamax_pulseh_drift.Add(h2d)
            h2d = ROOT.TH2F(infile.Get("h2_V_max_pulseh_drift")) #h2_V_max_pulseh_drift
            h2_V_max_pulseh_drift.Add(h2d)
            
            h2d = ROOT.TH2F(infile.Get("h2_deltav_pulseh_g1t"))
            h2_deltav_pulseh_g1t.Add(h2d)
            h2d = ROOT.TH2F(infile.Get("h2_deltamax_pulseh_g1t"))
            h2_deltamax_pulseh_g1t.Add(h2d)
            h2d = ROOT.TH2F(infile.Get("h2_V_max_pulseh_g1t"))
            h2_V_max_pulseh_g1t.Add(h2d)
            
            h2d = ROOT.TH2F(infile.Get("h2_deltav_pulseh_g1b"))
            h2_deltav_pulseh_g1b.Add(h2d)
            h2d = ROOT.TH2F(infile.Get("h2_deltamax_pulseh_g1b"))
            h2_deltamax_pulseh_g1b.Add(h2d)
            h2d = ROOT.TH2F(infile.Get("h2_V_max_pulseh_g1b"))
            h2_V_max_pulseh_g1b.Add(h2d)
            
            h2d = ROOT.TH2F(infile.Get("h2_deltav_pulseh_g2t"))
            h2_deltav_pulseh_g2t.Add(h2d)
            h2d = ROOT.TH2F(infile.Get("h2_deltamax_pulseh_g2t"))
            h2_deltamax_pulseh_g2t.Add(h2d)
            h2d = ROOT.TH2F(infile.Get("h2_V_max_pulseh_g2t"))
            h2_V_max_pulseh_g2t.Add(h2d)
            
            h2d = ROOT.TH2F(infile.Get("h2_deltav_pulseh_g2b"))
            h2_deltav_pulseh_g2b.Add(h2d)
            h2d = ROOT.TH2F(infile.Get("h2_deltamax_pulseh_g2b"))
            h2_deltamax_pulseh_g2b.Add(h2d)
            h2d = ROOT.TH2F(infile.Get("h2_V_max_pulseh_g2b"))
            h2_V_max_pulseh_g2b.Add(h2d)

            h2d = ROOT.TH2F(infile.Get("h2_deltav_pulseh_g3t"))
            h2_deltav_pulseh_g3t.Add(h2d)
            h2d = ROOT.TH2F(infile.Get("h2_deltamax_pulseh_g3t"))
            h2_deltamax_pulseh_g3t.Add(h2d)
            h2d = ROOT.TH2F(infile.Get("h2_V_max_pulseh_g3t"))
            h2_V_max_pulseh_g3t.Add(h2d)
            
            h2d = ROOT.TH2F(infile.Get("h2_deltav_pulseh_g3b"))
            h2_deltav_pulseh_g3b.Add(h2d)
            h2d = ROOT.TH2F(infile.Get("h2_deltamax_pulseh_g3b"))
            h2_deltamax_pulseh_g3b.Add(h2d)
            h2d = ROOT.TH2F(infile.Get("h2_V_max_pulseh_g3b"))
            h2_V_max_pulseh_g3b.Add(h2d)
            '''

    elif i<100:
        print i 
        if os.path.exists("/eos/home-a/acagnott/GEM_plot/"+pico+"_run00"+str(i)+"/discharges_count.root"):
            print "ok"
            infile = ROOT.TFile.Open("/eos/home-a/acagnott/GEM_plot/"+pico+"_run00"+str(i)+"/discharges_count.root")
            print infile
            histo = ROOT.TH2F(infile.Get("heig_int"))
            print histo.GetEntries()
            final_h.Add(histo)
            hist = ROOT.TH1F(infile.Get("h_chs"))
            h_chs.Add(hist)
            tau = ROOT.TH1F(infile.Get("tau"))
            h_tau.Add(tau)
            pulse = ROOT.TH1F(infile.Get("pulseheight"))
            h_pulseheight.Add(pulse)
            h = ROOT.TH1F(infile.Get("pulseheight_g1"))
            pulseheight_g1.Add(h)
            h = ROOT.TH1F(infile.Get("pulseheight_g2"))
            pulseheight_g2.Add(h)
            h = ROOT.TH1F(infile.Get("pulseheight_g3"))
            pulseheight_g3.Add(h)
            
            h = ROOT.TH1F(infile.Get("h_drift_ph"))
            h_drift_ph.Add(h)
            
            for ch in ["drift", "g1t", "g1b", "g2t", "g2b", "g3t", "g3b"]:
                h = ROOT.TH1F(infile.Get("type2_pulseheight_"+ch))
                h_type2_ph[ch].Add(h)
                
            '''h2d = ROOT.TH2F(infile.Get("h2_deltav_pulseh_drift"))
            h2_deltav_pulseh_drift.Add(h2d)
            h2d = ROOT.TH2F(infile.Get("h2_deltamax_pulseh_drift"))
            h2_deltamax_pulseh_drift.Add(h2d)
            h2d = ROOT.TH2F(infile.Get("h2_V_max_pulseh_drift"))
            h2_V_max_pulseh_drift.Add(h2d)
            
            h2d = ROOT.TH2F(infile.Get("h2_deltav_pulseh_g1t"))
            h2_deltav_pulseh_g1t.Add(h2d)
            h2d = ROOT.TH2F(infile.Get("h2_deltamax_pulseh_g1t"))
            h2_deltamax_pulseh_g1t.Add(h2d)
            h2d = ROOT.TH2F(infile.Get("h2_V_max_pulseh_g1t"))
            h2_V_max_pulseh_g1t.Add(h2d)
            
            h2d = ROOT.TH2F(infile.Get("h2_deltav_pulseh_g1b"))
            h2_deltav_pulseh_g1b.Add(h2d)
            h2d = ROOT.TH2F(infile.Get("h2_deltamax_pulseh_g1b"))
            h2_deltamax_pulseh_g1b.Add(h2d)
            h2d = ROOT.TH2F(infile.Get("h2_V_max_pulseh_g1b"))
            h2_V_max_pulseh_g1b.Add(h2d)
            
            h2d = ROOT.TH2F(infile.Get("h2_deltav_pulseh_g2t"))
            h2_deltav_pulseh_g2t.Add(h2d)
            h2d = ROOT.TH2F(infile.Get("h2_deltamax_pulseh_g2t"))
            h2_deltamax_pulseh_g2t.Add(h2d)
            h2d = ROOT.TH2F(infile.Get("h2_V_max_pulseh_g2t"))
            h2_V_max_pulseh_g2t.Add(h2d)
            
            h2d = ROOT.TH2F(infile.Get("h2_deltav_pulseh_g2b"))
            h2_deltav_pulseh_g2b.Add(h2d)
            h2d = ROOT.TH2F(infile.Get("h2_deltamax_pulseh_g2b"))
            h2_deltamax_pulseh_g2b.Add(h2d)
            h2d = ROOT.TH2F(infile.Get("h2_V_max_pulseh_g2b"))
            h2_V_max_pulseh_g2b.Add(h2d)

            h2d = ROOT.TH2F(infile.Get("h2_deltav_pulseh_g3t"))
            h2_deltav_pulseh_g3t.Add(h2d)
            h2d = ROOT.TH2F(infile.Get("h2_deltamax_pulseh_g3t"))
            h2_deltamax_pulseh_g3t.Add(h2d)
            h2d = ROOT.TH2F(infile.Get("h2_V_max_pulseh_g3t"))
            h2_V_max_pulseh_g3t.Add(h2d)
            
            h2d = ROOT.TH2F(infile.Get("h2_deltav_pulseh_g3b"))
            h2_deltav_pulseh_g3b.Add(h2d)
            h2d = ROOT.TH2F(infile.Get("h2_deltamax_pulseh_g3b"))
            h2_deltamax_pulseh_g3b.Add(h2d)
            h2d = ROOT.TH2F(infile.Get("h2_V_max_pulseh_g3b"))
            h2_V_max_pulseh_g3b.Add(h2d)
            '''
outfolder = "/eos/home-a/acagnott/GEM_plot/Goliath/"+pico+"/"
outfile = ROOT.TFile.Open("/eos/home-a/acagnott/GEM_plot/Goliath_"+pico+"integral_pulseheight.root","RECREATE")
outfile.cd()
h_chs.Write()
final_h.Write()
h_tau.Write()
h_pulseheight.Write()

stack_pulseh.Add(pulseheight_g1)
stack_pulseh.Add(pulseheight_g2)
stack_pulseh.Add(pulseheight_g3)
stack_pulseh.Write()

for ch in ["drift", "g1t", "g1b", "g2t", "g2b", "g3t", "g3b"]: stack_typ2_pulseh.Add(h_type2_ph[ch])
stack_typ2_pulseh.Write()
h_drift_ph.Write()

'''
h2_deltav_pulseh_drift.Write()
save_histo(outfolder, h2_deltav_pulseh_drift)
h2_deltamax_pulseh_drift.Write()
save_histo(outfolder, h2_deltamax_pulseh_drift)
h2_V_max_pulseh_drift.Write()
save_histo(outfolder, h2_V_max_pulseh_drift)
h2_deltav_pulseh_g1t.Write()
save_histo(outfolder, h2_deltav_pulseh_g1t)
h2_deltamax_pulseh_g1t.Write()
save_histo(outfolder, h2_deltamax_pulseh_g1t)
h2_V_max_pulseh_g1t.Write()
save_histo(outfolder, h2_V_max_pulseh_g1t)
h2_deltav_pulseh_g1b.Write()
save_histo(outfolder, h2_deltav_pulseh_g1b)
h2_deltamax_pulseh_g1b.Write()
save_histo(outfolder, h2_deltamax_pulseh_g1b)
h2_V_max_pulseh_g1b.Write()
save_histo(outfolder, h2_V_max_pulseh_g1b)
h2_deltav_pulseh_g2t.Write()
save_histo(outfolder, h2_deltav_pulseh_g2t)
h2_deltamax_pulseh_g2t.Write()
save_histo(outfolder, h2_deltamax_pulseh_g2t)
h2_V_max_pulseh_g2t.Write()
save_histo(outfolder, h2_V_max_pulseh_g2t)
h2_deltav_pulseh_g2b.Write()
save_histo(outfolder, h2_deltav_pulseh_g2b)
h2_deltamax_pulseh_g2b.Write()
save_histo(outfolder, h2_deltamax_pulseh_g2b)
h2_V_max_pulseh_g2b.Write()
save_histo(outfolder, h2_V_max_pulseh_g2b)
h2_deltav_pulseh_g3t.Write()
save_histo(outfolder, h2_deltav_pulseh_g3t)
h2_deltamax_pulseh_g3t.Write()
save_histo(outfolder, h2_deltamax_pulseh_g3t)
h2_V_max_pulseh_g3t.Write()
save_histo(outfolder, h2_V_max_pulseh_g3t)
h2_deltav_pulseh_g3b.Write()
save_histo(outfolder, h2_deltav_pulseh_g3b)
h2_deltamax_pulseh_g3b.Write()
save_histo(outfolder, h2_deltamax_pulseh_g3b)
h2_V_max_pulseh_g3b.Write()
save_histo(outfolder, h2_V_max_pulseh_g3b)
'''


outfile = ROOT.TFile.Open("/eos/home-a/acagnott/GEM_plot/Goliath/"+pico+"/dis_rate.root","RECREATE")
if pico=="PICO1":n_bins= 33
elif pico=="PICO2": n_bins = 32
h_rate = ROOT.TH1F("h_rate", "discharge rate; run label; discharge rate(1/s)", n_bins, -0.5, n_bins-0.5)


f = open("dis_rate"+pico+".txt", "r")


for i in range(1, n_bins+1):
    a = f.readline()
    a = a.split(",")
    
    if i <10: h_rate.GetXaxis().SetBinLabel(int(a[0]), "run0"+str(i))
    else: h_rate.GetXaxis().SetBinLabel(int(a[0]), "run"+str(i))
    h_rate.SetBinContent(int(a[0]), float(a[1]))
    print float(a[1])

outfile.cd()
h_rate.Write()

