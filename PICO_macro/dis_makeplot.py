import ROOT
from array import array
from utils import *
from datetime import datetime
import optparse
from dict_run import *
import pandas as pd
import root_pandas

ROOT.gStyle.SetOptStat("emr")
ROOT.gROOT.SetBatch()

usage = 'dis_makeplot.py.py' #-i PICO*_run_00**
parser = optparse.OptionParser(usage)
parser.add_option('-f', '--folder', dest='folder', type='string', default = '/eos/home-a/adeiorio/GEM/Goliath/', help='Default folder is /eos/home-a/adeiorio/GEM/Goliath')
parser.add_option('-i', '--input', dest='input', type='string', default = 'PICO1_run0001', help="Enter an input root file")
parser.add_option('-w', '--write_file', dest='write_file', default = False, action = 'store_true', help = "Default do not write txt files")
parser.add_option('-a', '--append_file', dest='append_file', default = False, action = 'store_true', help = "Default create a new txt files")
parser.add_option('-t', '--fit_fun', dest='fit', default = False, action = 'store_true', help = "Default do not expo fit on currents")
(opt, args) = parser.parse_args()

fit = opt.fit

folder = opt.folder
infile = ROOT.TFile.Open(folder+'/'+opt.input+'_skim.root')
tree = infile.Get("t1")
entries = tree.GetEntries()

data_folder = folder.split("/")[5]
if data_folder == 'LABGEM_scariche':
    data_folder = data_folder+'/'+folder.split("/")[6]

#outfolder = "/eos/home-a/acagnott/GEM_plot/"+data_folder+"/"+opt.input+"/"


write_file = opt.write_file

csv_created = opt.append_file

pico = opt.input.split('_')[0]

'''hist_dis = ROOT.TH1F("hist_dis", "", 7, -0.5, 6.5)
hist_dis.SetBinContent(0, entries)

# G3 : All electrodes, tr2: all electrodes-G3B,  G2: G2+G1, tr1: dr+g1t+g1b+g2t, G1: drift +g1, dr: drift.
hist_dis.GetXaxis().SetBinLabel(1, "DRIFT")
hist_dis.GetXaxis().SetBinLabel(2, "G1T")
hist_dis.GetXaxis().SetBinLabel(3, "G1B")
hist_dis.GetXaxis().SetBinLabel(4, "G2T")
hist_dis.GetXaxis().SetBinLabel(5, "G2B")
hist_dis.GetXaxis().SetBinLabel(6, "G3T")
hist_dis.GetXaxis().SetBinLabel(7, "G3B")

#hist_dis.GetXaxis().SetBinLabel(7, "induction")
'''
drift = array('f')
g1t = array('f')
g1b = array('f')
g2t = array('f')
g2b = array('f')
g3t = array('f')
g3b = array('f')


n_ind = 0
maxval = array('f')
electrode_maxval = array('i')
int_M5k = array('f')
int_m5k = array('f')
integrals = array('f')
heights = array('f')
heights_ = array('f')

#tres_height = 5000
#tres_int = 50000
flag_g1t = False
flag_g1b = False
flag_g2t = False
flag_g2b = False
flag_g3t = False
flag_g3b = False
dis_count = 0

volt_pulsh_ratio = []
taus = []
phs = []
typ2_pulseheight = []
ph_drift = []
 
pulseh_drift = [] 
pulseh_g1t = [] 
pulseh_g1b = []
pulseh_g2t = [] 
pulseh_g2b = []
pulseh_g3t = []
pulseh_g3b = []
volt_drift_wrt_mean = []
volt_drift_deltamax = []
volt_drift_center = []
volt_g1t_wrt_mean = []
volt_g1t_deltamax = []
volt_g1t_center = []
volt_g1b_wrt_mean = []
volt_g1b_deltamax = []
volt_g1b_center = []
volt_g2t_wrt_mean = []
volt_g2t_deltamax = []
volt_g2t_center = []
volt_g2b_wrt_mean = []
volt_g2b_deltamax = []
volt_g2b_center = []
volt_g3t_wrt_mean = []
volt_g3t_deltamax = []
volt_g3t_center = []
volt_g3b_wrt_mean = []
volt_g3b_deltamax = []
volt_g3b_center = []


h_chs = ROOT.TH1F("h_chs", "largest pulse height", 3, -0.5, 2.5)

h_chs.GetXaxis().SetBinLabel(1, "G1")
h_chs.GetXaxis().SetBinLabel(2, "G2")
h_chs.GetXaxis().SetBinLabel(3, "G3")


ch_name = ["DRIFT", "G1T", "G1B", "G2T", "G2B", "G3T", "G3B"]

disdrift = 0
disg1t = 0
disg2t = 0
disg3t = 0
disg1b = 0
disg2b = 0
disg3b = 0

for j in range(entries):
    tree.GetEntry(j)
    
    #if(opt.input+"_"+str(j) in events_to_jump or opt.input in events_to_jump): continue
    
    flag_list = {"G1T": False, "G1B": False, "G2T": False, "G2B": False, "G3T": False, "G3B": False}
    #print("event ", i)
    
    #if (tree.TRDRIFT): plot_drift(opt.input, j)
    
    if((tree.TRDRIFT and not tree.TRG1T and not tree.TRG1B and not tree.TRG2T and not tree.TRG2B and not tree.TRG3T and not tree.TRG3B)): 
        disdrift +=1
        #print 'event'+str(j)
    if((not tree.TRDRIFT and tree.TRG1T and not tree.TRG1B and not tree.TRG2T and not tree.TRG2B and not tree.TRG3T and not tree.TRG3B)):
        print 'event g1t' +str(j)
        disg1t +=1
    if((not tree.TRDRIFT and not tree.TRG1T and not tree.TRG1B and tree.TRG2T and not tree.TRG2B and not tree.TRG3T and not tree.TRG3B)): 
        print 'event g2t' +str(j)
        disg2t +=1
    if((not tree.TRDRIFT and not tree.TRG1T and not tree.TRG1B and not tree.TRG2T and not tree.TRG2B and tree.TRG3T and not tree.TRG3B)): 
        print 'event g3t' +str(j)
        disg3t +=1
    if((not tree.TRDRIFT and not tree.TRG1T and tree.TRG1B and not tree.TRG2T and not tree.TRG2B and not tree.TRG3T and not tree.TRG3B)):
        print 'event g1b' +str(j)
        disg1b +=1
    if((not tree.TRDRIFT and not tree.TRG1T and not tree.TRG1B and not tree.TRG2T and tree.TRG2B and not tree.TRG3T and not tree.TRG3B)): 
        print 'event g2b' +str(j)
        disg2b +=1
    if((not tree.TRDRIFT and not tree.TRG1T and not tree.TRG1B and not tree.TRG2T and not tree.TRG2B and not tree.TRG3T and tree.TRG3B)): 
        print 'event g3b' +str(j)
        disg3b +=1

    TR_list = {"DRIFT":tree.TRDRIFT, "G1T":tree.TRG1T, "G1B":tree.TRG1B, "G2T":tree.TRG2T, "G2B":tree.TRG2B, 
               "G3T":tree.TRG3T, "G3B":tree.TRG3B}

    integral_list = {"DRIFT":tree.INTEGRAL_IDRIFT, "G1T":tree.INTEGRAL_IG1T, "G1B":tree.INTEGRAL_IG1B, "G2T":tree.INTEGRAL_IG2T, "G2B":tree.INTEGRAL_IG2B, 
                     "G3T":tree.INTEGRAL_IG3T, "G3B":tree.INTEGRAL_IG3B}

    pulseheight_list = {"DRIFT":tree.PULSEHEIGHT_IDRIFT, "G1T":tree.PULSEHEIGHT_IG1T, "G1B":tree.PULSEHEIGHT_IG1B, 
                        "G2T":tree.PULSEHEIGHT_IG2T, "G2B":tree.PULSEHEIGHT_IG2B, 
                        "G3T":tree.PULSEHEIGHT_IG3T, "G3B":tree.PULSEHEIGHT_IG3B}

    pulseheight_typ1_list = {"G1T": min(tree.IG1T), "G1B": max(tree.IG1B), 
                             "G2T":min(tree.IG2T), "G2B":max(tree.IG2B), 
                             "G3T":min(tree.IG3T), "G3B":max(tree.IG3B)}

    for i,ch in enumerate(ch_name):
        if TR_list[ch]:
            #hist_dis.AddBinContent(i+1, 1)
            if pulseheight_list[ch]!=0:
                integrals.append(integral_list[ch])
                heights.append(pulseheight_list[ch])
            if (ch!="DRIFT"):
                if(abs(pulseheight_typ1_list[ch])>50 and abs(integral_list[ch]/pulseheight_list[ch])>10 and abs(integral_list[ch])>100000):
                    print("flag True "+ch, j)
                    flag_list[ch] = True
                    
                    
    g1_flag = (flag_list["G1T"]*flag_list["G1B"])
    g2_flag = (flag_list["G2T"]*flag_list["G2B"])
    g3_flag = (flag_list["G3T"]*flag_list["G3B"])
    
    tot_flag = g1_flag + g2_flag + g3_flag
    
    #if j==5 : print g1_flag, g2_flag, g3_flag 

    if(tot_flag):# and abs(tree.PULSEHEIGHT_IG3T)>5000):
        deltaIg1 = abs(tree.PULSEHEIGHT_IG1B-tree.PULSEHEIGHT_IG1T)
        deltaIg2 = abs(tree.PULSEHEIGHT_IG2B-tree.PULSEHEIGHT_IG2T)
        deltaIg3 = abs(tree.PULSEHEIGHT_IG3B-tree.PULSEHEIGHT_IG3T)
        h = [deltaIg1, deltaIg2, deltaIg3]
        
        maxdelta = max(h)
        taus.append([])
        phs.append([])
     
        taus[-1], phs[-1], a = plot_allch(opt.input, j, draw_volt = False, data = data_folder, fit = fit)
        
        if write_file and not csv_created:
            write_csv(data_folder, opt.input, j, 'w')# da cambiare 'w' con 'a' quando deve fare l'append --> capire come far cambiare questa cosa
            csv_created = True
        elif write_file and csv_created:
            write_csv(data_folder, opt.input, j, 'a')# da cambiare 'w' con 'a' quando deve fare l'append --> capire come far cambiare questa cosa

        ph_drift.append(a)
        
        #d1,d2,d3 = volt_pulseh_ratio(opt.input, j)

        #volt_pulsh_ratio.append(d1)
        #volt_pulsh_ratio.append(d2)
        #volt_pulsh_ratio.append(d3)
        

        if maxdelta == h[0] : 
            electrode = 1
            h_chs.AddBinContent(1,1)
        if maxdelta == h[1] : 
            electrode = 2
            h_chs.AddBinContent(2,1)
        if maxdelta == h[2] : 
            electrode = 3
            h_chs.AddBinContent(3,1)
        maxval.append(maxdelta)
        electrode_maxval.append(electrode)
        dis_count+=1
    cond1 = 0
    cond2 = True#tree.PULSEHEIGHT_IDRIFT<0 and tree.PULSEHEIGHT_IG1T<0 and tree.PULSEHEIGHT_IG1B<0 and tree.PULSEHEIGHT_IG2T<0 and tree.PULSEHEIGHT_IG2B<0 and  tree.PULSEHEIGHT_IG3T<0 and tree.PULSEHEIGHT_IG3B<0
    
    for ch in ch_name: 
        cond1 += TR_list[ch]
        if ch !='G3B': cond2 *= (pulseheight_list[ch]<0)

    if(cond1> 6 and cond2):
        n_ind += 1
        graph_event(folder, opt.input, j, write_file)
        dict = {"drift": abs(tree.PULSEHEIGHT_IDRIFT), "g1t":abs(tree.PULSEHEIGHT_IG1T), "g1b":abs(tree.PULSEHEIGHT_IG1B),
                "g2t":abs(tree.PULSEHEIGHT_IG2T) , "g2b":abs(tree.PULSEHEIGHT_IG2B) ,"g3t":abs(tree.PULSEHEIGHT_IG3T) , 
                "g3b":abs(tree.PULSEHEIGHT_IG3B) }
        typ2_pulseheight.append(dict)
        

print("number of inducted signals: ",n_ind)
print("number of only drift: ",disdrift)
print("number of onlyg1t: ",disg1t)
print("number of onlyg2t: ",disg2t)
print("number of onlyg3t: ",disg3t)
print("number of onlyg1b: ",disg1b)
print("number of onlyg2b: ",disg2b)
print("number of onlyg3b: ",disg3b)

'''outfile = ROOT.TFile.Open(outfolder+"discharges_count.root", "RECREATE")    
pulseheight = array('f')
for val in drift: pulseheight.append(val)
for val in g1t: pulseheight.append(val)
for val in g1b: pulseheight.append(val)
for val in g2t: pulseheight.append(val)
for val in g2b: pulseheight.append(val)
for val in g3t: pulseheight.append(val)
for val in g3b: pulseheight.append(val)

#print(min(pulseheight), max(pulseheight))
if len(pulseheight)!=0:
    h_heights = ROOT.TH2F("pulse_height", "pulse_height", 7, -0.5, 6.5, 50, min(pulseheight)-50, max(pulseheight)+50)
    h_heights.GetXaxis().SetBinLabel(1,"drift")
    h_heights.GetXaxis().SetBinLabel(2, "G1T")
    h_heights.GetXaxis().SetBinLabel(3, "G1B")
    h_heights.GetXaxis().SetBinLabel(4, "G2T")
    h_heights.GetXaxis().SetBinLabel(5, "G2B")
    h_heights.GetXaxis().SetBinLabel(6, "G3T")
    h_heights.GetXaxis().SetBinLabel(7, "G3B")

    for val in drift: h_heights.Fill(0, val)
    for val in g1t: h_heights.Fill(1, val)
    for val in g1b: h_heights.Fill(2, val)
    for val in g2t: h_heights.Fill(3, val)
    for val in g2b: h_heights.Fill(4, val)
    for val in g3t: h_heights.Fill(5, val)
    for val in g3b: h_heights.Fill(6, val)

    h_heights.Write()
print (opt.input+ " #discharges :", dis_count)
print maxval
print electrode_maxval


h_heig_int = ROOT.TH2F("heig_int", "pulse height integral; pulse height; integral/pulse height", 10000, 0, 190000, 200, 0, 200)

h_integral_height = ROOT.TH2F("h_integral_height","integral VS pulse height; pulse height(nA); integral", 10000, 0, 190000, 1000, 100000,20000000)

if len(heights)!=0:
    for i in range(len(integrals)):
        h_integral_height.Fill(abs(heights[i]), abs(integrals[i]))


    int_d_heights = array('f')
    for i in range(len(integrals)): int_d_heights.append(abs(integrals[i]/heights[i]))
    
    for i in range(len(integrals)):
        h_heig_int.Fill(abs(heights[i]), int_d_heights[i])
        

print('ok')
tau = ROOT.TH1F("tau", "Discharges fit;C(F)", 100, 0, 5*10**(-8))
pulseheight = ROOT.TH1F("pulseheight", "pulse height;current(nA)", 100, 50, 180000)

pulseheight_g1 = ROOT.TH1F("pulseheight_g1", "pulse height;current(nA)", 100, 50, 180000)
pulseheight_g2 = ROOT.TH1F("pulseheight_g2", "pulse height;current(nA)", 100, 50, 180000)
pulseheight_g3 = ROOT.TH1F("pulseheight_g3", "pulse height;current(nA)", 100, 50, 180000)

for t in taus:
    
    for val in t: 
        tau.Fill(-val/10000000)
for val in volt_pulsh_ratio : print val

for p in phs:
    for val in p:
        pulseheight.Fill(abs(val))
for p in phs:
    pulseheight_g1.Fill(abs(p[0]))
    pulseheight_g1.Fill(abs(p[1]))
    pulseheight_g2.Fill(abs(p[2]))
    pulseheight_g2.Fill(abs(p[3]))
    pulseheight_g3.Fill(abs(p[4]))
    pulseheight_g3.Fill(abs(p[5]))

pulseheight_g1.SetFillColor(ROOT.kGreen)
pulseheight_g2.SetFillColor(ROOT.kCyan)
pulseheight_g3.SetFillColor(ROOT.kRed)

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

for h in typ2_pulseheight:
    h_type2_pulseheight_drift.Fill(h["drift"])
    h_type2_pulseheight_g1t.Fill(h["g1t"])
    h_type2_pulseheight_g1b.Fill(h["g1b"])
    h_type2_pulseheight_g2t.Fill(h["g2t"])
    h_type2_pulseheight_g2b.Fill(h["g2b"])
    h_type2_pulseheight_g3t.Fill(h["g3t"])
    h_type2_pulseheight_g3b.Fill(h["g3b"])

h_drift_ph = ROOT.TH1F("h_drift_ph", "pulse height drift", 120, -20*10**3, 20*10**3)

for val in ph_drift: h_drift_ph.Fill(val)

pulseh_nbins = 40
pulseh_min =1000
pulseh_max =40000

deltav_nbins = 10
deltav_min = 0
deltav_max = 5

deltamax_nbins = 10
deltamax_min = 0
deltamax_max = 10


outfile.cd()
h_type2_pulseheight_drift.Write()
h_type2_pulseheight_g1t.Write()
h_type2_pulseheight_g1b.Write()
h_type2_pulseheight_g2t.Write()
h_type2_pulseheight_g2b.Write()
h_type2_pulseheight_g3t.Write()
h_type2_pulseheight_g3b.Write()
tau.Write()
h_heig_int.Write()    
hist_dis.Write()
h_chs.Write()
h_integral_height.Write()
pulseheight.Write()
pulseheight_g1.Write()
pulseheight_g2.Write()
pulseheight_g3.Write()
h_drift_ph.Write()
'''


if data_folder == 'Goliath':
    pico = (opt.input).split("_")[0]
    run =  (opt.input).split("_")[1]
    n_run = int(run.split("00")[1])
    time = dict_run[pico][run]["tot_time"]
    dis_rate = dis_count/time

#if not opt.write_file: write_rate(pico, run, dis_rate)

'''print dis_rate
if '0001' in opt.input:
    f = open("dis_rate"+pico+".txt", "w")
else:
    f = open("dis_rate"+pico+".txt", "a")
f.write(str(n_run)+", "+ str(dis_rate)+"\n")
'''
if data_folder != 'Goliath':
    pico = opt.input
'''    
outfolder = "/eos/home-a/acagnott/GEM_plot/"+data_folder
df = pd.read_csv(outfolder+"/"+ pico+'discharges_event.csv')
df.to_root(outfolder+"/"+ pico+'discharges_event.root', key='t1')
'''
