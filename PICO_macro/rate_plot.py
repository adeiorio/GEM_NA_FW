import ROOT

outfile = ROOT.TFile.Open("/eos/home-a/acagnott/GEM_plot/Goliath/PICO2/dis_rate.root","RECREATE")
n_bins= 32
h_rate = ROOT.TH1F("h_rate", "discharge rate; run label; discharge rate(1/s)", n_bins, -0.5, 31.5)


f = open("dis_ratePICO2.txt", "r")


for i in range(n_bins):
    a = f.readline()
    a = a.split(",")
    
    if i <10: h_rate.GetXaxis().SetBinLabel(int(a[0]), "run0"+str(i))
    else: h_rate.GetXaxis().SetBinLabel(int(a[0]), "run"+str(i))
    h_rate.SetBinContent(int(a[0]), float(a[1]))

h_rate.Write()
