import ROOT
from utils import *
import os
import optparse

usage = 'dis_makeplot.py.py' #-i PICO*_run_00**
parser = optparse.OptionParser(usage)
parser.add_option('-d', '--data', dest='folder', type='string', default = 'Goliath/', help='Default folder is ../Goliath/')
parser.add_option('-i', '--input', dest='input', type='string', default = 'PICO1_run0000', help="Enter an input root file")
(opt, args) = parser.parse_args()

data_folder = opt.folder

save_volt = False

deltapulseh_max = 10000
#pulseh_max = 20000


def save_plot(plot, draw_opt):
    c1 = ROOT.TCanvas()
    plot.Draw(draw_opt)
    c1.Print(folder+p+"/"+plot.GetName()+".png")
    c1.Print(folder+p+"/"+plot.GetName()+".root")


folder = "/eos/home-a/acagnott/GEM_plot/"+data_folder
if 'Goliath' in data_folder:
    pico = ['PICO1', 'PICO2']
else: 
    pico = [opt.input]

for p in pico:
    tfile = p+"discharges_event.root"
    print tfile
    infile = ROOT.TFile.Open(folder+tfile)
    tree = infile.Get("t1")

    entries = tree.GetEntries()
    print entries
    pulseheightg1t = []
    pulseheightg1b = []
    pulseheightg2t = []
    pulseheightg2b = []
    pulseheightg3t = []
    pulseheightg3b = []
    deltapulseheight_g1 =[]
    deltapulseheight_g2 =[]
    deltapulseheight_g3 =[]
    var_deltapulseheight_g1 =[]
    var_deltapulseheight_g2 =[]
    var_deltapulseheight_g3 =[]
    n_run = []
    dis_rate = []
    v_mean_g1t = []
    v_mean_g1b = []
    v_mean_g2t = []
    v_mean_g2b = []
    v_mean_g3t = []
    v_mean_g3b = []
    deltav_g1 = []
    deltav_g2 = []
    deltav_g3 = []
    deltav_g1_var = []
    deltav_g2_var = []
    deltav_g3_var = []
    deltav_g1_mean = []
    deltav_g2_mean = []
    deltav_g3_mean = []
    integral_g1t = []
    integral_g1b =[]
    integral_g2t = []
    integral_g2b =[]
    integral_g3t = []
    integral_g3b =[]
    mean_g1t = []
    mean_g1b = []
    mean_g2t = []
    mean_g2b = []
    mean_g3t = []
    mean_g3b = []

    for i in range(entries):
        tree.GetEntry(i)
        n_run.append(int(tree.run))
        if hasattr(tree, 'discharge_rate'): dis_rate.append(tree.discharge_rate)
        pulseheightg1t.append(abs(tree.G1T_pulseheight))
        pulseheightg1b.append(abs(tree.G1B_pulseheight))
        pulseheightg2t.append(abs(tree.G2T_pulseheight))
        pulseheightg2b.append(abs(tree.G2B_pulseheight))
        pulseheightg3t.append(abs(tree.G3T_pulseheight))
        pulseheightg3b.append(abs(tree.G3B_pulseheight))
        
        integral_g1t.append(tree.G1T_integral)
        integral_g1b.append(tree.G1B_integral)
        integral_g2t.append(tree.G2T_integral)
        integral_g2b.append(tree.G2B_integral)
        integral_g3t.append(tree.G3T_integral)
        integral_g3b.append(tree.G3B_integral)
       
        deltapulseheight_g1.append(pulseheightg1t[i]- pulseheightg1b[i])
        deltapulseheight_g2.append(pulseheightg2t[i]- pulseheightg2b[i])
        deltapulseheight_g3.append(pulseheightg3t[i]- pulseheightg3b[i])    
        
        var_deltapulseheight_g1.append((pulseheightg1t[i]- pulseheightg1b[i])/(pulseheightg1t[i]+ pulseheightg1b[i]))
        var_deltapulseheight_g2.append((pulseheightg2t[i]- pulseheightg2b[i])/(pulseheightg2t[i]+ pulseheightg2b[i]))
        var_deltapulseheight_g3.append((pulseheightg3t[i]- pulseheightg3b[i])/(pulseheightg3t[i]+ pulseheightg3b[i]))    

        mean_g1t.append(abs(tree.G1T_mean))
        mean_g1b.append(abs(tree.G1B_mean))
        mean_g2t.append(abs(tree.G2T_mean))
        mean_g2b.append(abs(tree.G2B_mean))
        mean_g3t.append(abs(tree.G3T_mean))
        mean_g3b.append(abs(tree.G3B_mean))

        
        condg1 = abs(deltapulseheight_g1[i]) > deltapulseh_max #and pulseheightg1b[i]>pulseh_max
        condg2 = abs(deltapulseheight_g2[i]) > deltapulseh_max #and pulseheightg2b[i]>pulseh_max
        condg3 = abs(deltapulseheight_g3[i]) > deltapulseh_max #and pulseheightg3b[i]>pulseh_max

        if (save_volt and (condg1 or condg2 or condg3)): 
            if tree.run<10:
                plot_allch('PICO'+str(tree.pico)+'_run000'+str(tree.run), tree.event, draw_volt=True) 
                #print 'cp -r /eos/home-a/acagnott/GEM_plot/graphsdischarges/PICO'+str(tree.pico)+'_run000'+str(tree.run)+'_'+str(tree.event)+' /eos/home-a/acagnott/www/GEM/graph_deltp10_p20/'
                #os.system('cp -r /eos/home-a/acagnott/GEM_plot/graphsdischarges/PICO'+str(tree.pico)+'_run000'+str(tree.run)+'_'+str(tree.event)+' /eos/home-a/acagnott/www/GEM/graph_deltp10_p20/')
            elif tree.run<100: 
                plot_allch('PICO'+str(tree.pico)+'_run00'+str(tree.run), tree.event, draw_volt=True) 
                #os.system('cp -r /eos/home-a/acagnott/GEM_plot/graphsdischarges/PICO'+str(tree.pico)+'_run00'+str(tree.run)+'_'+str(tree.event)+' /eos/home-a/acagnott/www/GEM/graph_deltp10_p20/')
                #print 'cp -r /eos/home-a/acagnott/GEM_plot/graphsdischarges/PICO'+str(tree.pico)+'_run00'+str(tree.run)+'_'+str(tree.event)+' /eos/home-a/acagnott/www/GEM/graph_deltp10_p20/'

        v_mean_g1t.append(tree.G1Tvolt_mean)
        v_mean_g1b.append(tree.G1Bvolt_mean)
        v_mean_g2t.append(tree.G2Tvolt_mean)
        v_mean_g2b.append(tree.G2Bvolt_mean)
        v_mean_g3t.append(tree.G3Tvolt_mean)
        v_mean_g3b.append(tree.G3Bvolt_mean)
        deltav_g1_var.append(abs(tree.deltav_g1b_g1t-tree.mean_deltav_g1b_g1t))
        deltav_g2_var.append(abs(tree.deltav_g2b_g2t-tree.mean_deltav_g2b_g2t))
        deltav_g3_var.append(abs(tree.deltav_g3b_g3t-tree.mean_deltav_g3b_g3t))
        deltav_g1.append(tree.deltav_g1b_g1t)
        deltav_g2.append(tree.deltav_g2b_g2t)
        deltav_g3.append(tree.deltav_g3b_g3t)
        deltav_g1_mean.append(tree.mean_deltav_g1b_g1t)
        deltav_g2_mean.append(tree.mean_deltav_g2b_g2t)
        deltav_g3_mean.append(tree.mean_deltav_g3b_g3t)
        
        '''print "deltav_var events"
        if abs(deltav_g1_var[i])> 1: print "G1 ",tree.pico, tree.run, tree.event 
        if abs(deltav_g2_var[i])> 1: print "G2 ",tree.pico, tree.run, tree.event 
        if abs(deltav_g3_var[i])> 1: print "G3 ",tree.pico, tree.run, tree.event 
        '''
    
    #max_ph = [max(pulseheightg1t),max(pulseheightg1b),max(pulseheightg2t),max(pulseheightg2b),max(pulseheightg3t),max(pulseheightg3b)]
    #max_pulseh = max(max_ph)
    max_pulseh = 50000
    #min_ph = [min(pulseheightg1t),min(pulseheightg1b),min(pulseheightg2t),min(pulseheightg2b),min(pulseheightg3t),min(pulseheightg3b)]
    #min_pulseh = min(min_ph)
    min_pulseh = 1000
    
    n_bin_ph = 49#int((max_pulseh-min_pulseh)/(10**3))

    n_bin_volt = 50
    min_volt = 0
    max_volt = 5

    nbin_dis_rate = 10
    if hasattr(tree, 'dis_rate'):
        min_disrate = min(dis_rate)
        max_disrate = max(dis_rate)
    else:
        min_disrate = 0
        max_disrate = 1

    nbin_run = 33
    min_run = 0.5
    max_run = 33.5

    hist_pulseheight_g1 = ROOT.TH1F("h_pulseheight_g1", "Pulse Height G1", n_bin_ph, min_pulseh, max_pulseh)
    hist_pulseheight_g1.SetFillColor(ROOT.kGreen)
    hist_pulseheight_g2 = ROOT.TH1F("h_pulseheight_g2", "Pulse Height G2", n_bin_ph, min_pulseh, max_pulseh)
    hist_pulseheight_g2.SetFillColor(ROOT.kCyan)
    hist_pulseheight_g3 = ROOT.TH1F("h_pulseheight_g3", "Pulse Height G3", n_bin_ph, min_pulseh, max_pulseh)
    hist_pulseheight_g3.SetFillColor(ROOT.kRed)


    hist_vmean_allch = ROOT.TH2F("h_vmean_allch","(V_max -V_mean) Vs pulse height; pulseheight(nA); (V_max-V_mean)(V)", 
                                 n_bin_ph, min_pulseh, max_pulseh, n_bin_volt, min_volt, max_volt)
    hist_vmean_topch = ROOT.TH2F("h_vmean_topch","(V_max -V_mean) Vs pulse height; pulseheight(nA); (V_max-V_mean)(V)", 
                                 n_bin_ph, min_pulseh, max_pulseh, n_bin_volt, min_volt, max_volt)
    hist_vmean_botch = ROOT.TH2F("h_vmean_botch","(V_max -V_mean) Vs pulse height; pulseheight(nA); (V_max-V_mean)(V)", 
                                 n_bin_ph, min_pulseh, max_pulseh, n_bin_volt, min_volt, max_volt)
    hist_deltav_mean_bot = ROOT.TH2F("h_vdelta_mean_bot", "(#Delta V_max -#Delta V_mean) Vs pulse height;pulse height(nA);(#Delta V_max -#Delta V_mean)(V",
                                       n_bin_ph, min_pulseh, max_pulseh, n_bin_volt, min_volt, max_volt)
    hist_deltav_mean_botg1 = ROOT.TH2F("h_vdelta_mean_botg1", "(#Delta V_max -#Delta V_mean) Vs pulse height;pulse height(nA);(#Delta V_max -#Delta V_mean)(V",
                                       n_bin_ph, min_pulseh, max_pulseh, n_bin_volt, min_volt, max_volt)
    hist_deltav_mean_botg2 = ROOT.TH2F("h_vdelta_mean_botg2", "(#Delta V_max -#Delta V_mean) Vs pulse height;pulse height(nA);(#Delta V_max -#Delta V_mean)(V",
                                       n_bin_ph, min_pulseh, max_pulseh, n_bin_volt, min_volt, max_volt)
    hist_deltav_mean_botg3 = ROOT.TH2F("h_vdelta_mean_botg3", "(#Delta V_max -#Delta V_mean) Vs pulse height;pulse height(nA);(#Delta V_max -#Delta V_mean)(V",
                                       n_bin_ph, min_pulseh, max_pulseh, n_bin_volt, min_volt, max_volt)
    
    hist_deltav_mean_top = ROOT.TH2F("h_vdelta_mean_top", "(#Delta V_max -#Delta V_mean) Vs pulse height;pulse height(nA);(#Delta V_max -#Delta V_mean)(V",
                                       n_bin_ph, min_pulseh, max_pulseh, n_bin_volt, min_volt, max_volt)
    hist_deltav_mean_topg1 = ROOT.TH2F("h_vdelta_mean_topg1", "(#Delta V_max -#Delta V_mean) Vs pulse height;pulse height(nA);(#Delta V_max -#Delta V_mean)(V",
                                       n_bin_ph, min_pulseh, max_pulseh, n_bin_volt, min_volt, max_volt)
    hist_deltav_mean_topg2 = ROOT.TH2F("h_vdelta_mean_topg2", "(#Delta V_max -#Delta V_mean) Vs pulse height;pulse height(nA);(#Delta V_max -#Delta V_mean)(V",
                                       n_bin_ph, min_pulseh, max_pulseh, n_bin_volt, min_volt, max_volt)
    hist_deltav_mean_topg3 = ROOT.TH2F("h_vdelta_mean_topg3", "(#Delta V_max -#Delta V_mean) Vs pulse height;pulse height(nA);(#Delta V_max -#Delta V_mean)(V",
                                       n_bin_ph, min_pulseh, max_pulseh, n_bin_volt, min_volt, max_volt)
                                       
    hist_pulseheight_disrate = ROOT.TH2F("h_pulseheight_disrate_allch", "discharge rate Vs Pulse height; pulse height(nA); discharge rate(1/s)", n_bin_ph, min_pulseh, max_pulseh,
                                         nbin_dis_rate, min_disrate, max_disrate)
    hist_pulseheight_n_run = ROOT.TH2F("h_pulseheight_n_run_allch", "Pulse height Vs #run; #run;pulse height(nA)",
                                         nbin_run, min_run, max_run, n_bin_ph, min_pulseh, max_pulseh)

    hist_pulseheight_disrate_g1 = ROOT.TH2F("h_pulseheight_disrate_g1", "discharge rate Vs Pulse height; pulse height(nA); discharge rate(1/s)", n_bin_ph, min_pulseh, max_pulseh,
                                         nbin_dis_rate, min_disrate, max_disrate)
    hist_pulseheight_n_run_g1 = ROOT.TH2F("h_pulseheight_n_run_g1", "Pulse height Vs #run; #run;pulse height(nA)",
                                         nbin_run, min_run, max_run, n_bin_ph, min_pulseh, max_pulseh)
    
    hist_pulseheight_disrate_g2 = ROOT.TH2F("h_pulseheight_disrate_g2", "discharge rate Vs Pulse height; pulse height(nA); discharge rate(1/s)", n_bin_ph, min_pulseh, max_pulseh,
                                         nbin_dis_rate, min_disrate, max_disrate)
    hist_pulseheight_n_run_g2 = ROOT.TH2F("h_pulseheight_n_run_g2", "Pulse height Vs #run; #run;pulse height(nA)",
                                         nbin_run, min_run, max_run, n_bin_ph, min_pulseh, max_pulseh)
    
    hist_pulseheight_disrate_g3 = ROOT.TH2F("h_pulseheight_disrate_g3", "discharge rate Vs Pulse height; pulse height(nA); discharge rate(1/s)", n_bin_ph, min_pulseh, max_pulseh,
                                            nbin_dis_rate, min_disrate, max_disrate)
    hist_pulseheight_n_run_g3 = ROOT.TH2F("h_pulseheight_n_run_g3", "Pulse height Vs #run; #run;pulse height(nA)",
                                         nbin_run, min_run, max_run, n_bin_ph, min_pulseh, max_pulseh)


    #max_deltaph = max(deltapulseheight_g1+deltapulseheight_g2+deltapulseheight_g3)
    #min_deltaph = min(deltapulseheight_g1+deltapulseheight_g2+deltapulseheight_g3)
    #nbin_deltaph = int((max_deltaph-min_deltaph)/1000)
    
    hist_deltapulseheight_pulseheight = ROOT.TH2F("pulseheight_deltapulseheight","(PulseH_{top}-PulseH_{bot})Vs I_bot;pulseheight Bot(nA);(PulseH_{top}-PulseH_{bot})",
                                                  n_bin_ph, min_pulseh, max_pulseh, n_bin_ph*2, -max_pulseh , max_pulseh) 

    x_max_var_deltapulseh = max([max(var_deltapulseheight_g1), max(var_deltapulseheight_g2), max(var_deltapulseheight_g3)])
    x_min_var_deltapulseh = min([min(var_deltapulseheight_g1), min(var_deltapulseheight_g2), min(var_deltapulseheight_g3)])
    n_bin_var_deltapulseh = 50#int((x_max_var_deltapulseh+ x_min_var_deltapulseh)/100)
    
    x_max_integral = 2000000#max([max(integral_g1t), max(integral_g1b), max(integral_g2t), max(integral_g2b), max(integral_g3t), max(integral_g3b)])
    x_min_integral = -2000000#min([min(integral_g1t), min(integral_g1b), min(integral_g2t), min(integral_g2b), min(integral_g3t), min(integral_g3b)])
    n_bin_int = 100

    hist_vardeltapulseheight_pulseheight = ROOT.TH2F("pulseheight_vardeltapulseheight","(PulseH_{top}-PulseH_{bot})/(PulseH_{top}+PulseH_{bot}) Vs PulseH_{bot};pulseheight Bot(nA);(PulseH_{top}-PulseH_{bot})/(PulseH_{top}+PulseH_{bot})", n_bin_ph, min_pulseh, max_pulseh, n_bin_var_deltapulseh, x_min_var_deltapulseh, x_max_var_deltapulseh) 

    hist_vardeltapulseheight_integral = ROOT.TH2F("integral_vardeltapulseheight","(PulseH_{top}-PulseH_{bot})/(PulseH_{top}+PulseH_{bot}) Vs integral;integral bottom;(PulseH_{top}-PulseH_{bot})/(PulseH_{top}+PulseH_{bot})", n_bin_int, x_min_integral, x_max_integral, n_bin_var_deltapulseh, x_min_var_deltapulseh, x_max_var_deltapulseh) 

    histos_n_run = {"g1":hist_pulseheight_n_run_g1 ,"g2":hist_pulseheight_n_run_g2,"g3":hist_pulseheight_n_run_g3}
    histos_disrate = {"g1":hist_pulseheight_disrate_g1 ,"g2":hist_pulseheight_disrate_g2 ,"g3":hist_pulseheight_disrate_g3}
    

    pulse_height_topch = {"g1":pulseheightg1t, "g2":pulseheightg2t, "g3":pulseheightg3t}
    pulse_height_botch = {"g1":pulseheightg1b, "g2":pulseheightg2b, "g3":pulseheightg3b}

    gem = ["g1","g2","g3"]

    h_deltav_mean_deltav_g1 = ROOT.TH2F("h_deltav_mean_deltav_g1", "#Delta V _{discharge} Vs #Delta V _{mean} GEM1; #Delta V _{discharge} (V); #Delta V _{mean}(V)", 
                                        100, min(deltav_g1), max(deltav_g1),
                                        100, min(deltav_g1_mean), max(deltav_g1_mean))
    h_deltav_mean_deltav_g2 = ROOT.TH2F("h_deltav_mean_deltav_g2", "#Delta V #_{discharge} Vs #Delta V #_{mean} GEM2; #Delta V _{discharge} (V); #Delta V _{mean}(V)", 
                                        100, min(deltav_g2), max(deltav_g2),
                                        100, min(deltav_g2_mean), max(deltav_g2_mean))
    h_deltav_mean_deltav_g3 = ROOT.TH2F("h_deltav_mean_deltav_g3", "#Delta V #_{discharge} Vs #Delta V #_{mean} GEM3; #Delta V _{discharge} (V); #Delta V _{mean}(V)", 
                                        100, min(deltav_g3), max(deltav_g3),
                                        100, min(deltav_g3_mean), max(deltav_g3_mean))

    deltav_mean_deltav = {"g1":h_deltav_mean_deltav_g1,"g2":h_deltav_mean_deltav_g2,"g3":h_deltav_mean_deltav_g3}

    h_curr_mean_g1t = ROOT.TH1F("h_curr_mean_g1t","G1T mean current",100, 0, 10000)
    h_curr_mean_g1b = ROOT.TH1F("h_curr_mean_g1b","G1B mean current",100, 0, 10000)
    h_curr_mean_g2t = ROOT.TH1F("h_curr_mean_g2t","G2T mean current",100, 0, 10000)
    h_curr_mean_g2b = ROOT.TH1F("h_curr_mean_g2b","G2B mean current",100, 0, 10000)
    h_curr_mean_g3t = ROOT.TH1F("h_curr_mean_g3t","G3T mean current",100, 0, 10000)
    h_curr_mean_g3b = ROOT.TH1F("h_curr_mean_g3b","G3B mean current",100, 0, 10000)

    for i in range(entries):
        
        h_curr_mean_g1t.Fill(mean_g1t[i])
        h_curr_mean_g1b.Fill(mean_g1b[i])
        h_curr_mean_g2t.Fill(mean_g2t[i])
        h_curr_mean_g2b.Fill(mean_g2b[i])
        h_curr_mean_g3t.Fill(mean_g3t[i])
        h_curr_mean_g3b.Fill(mean_g3b[i])        


        deltav_mean_deltav["g1"].Fill(deltav_g1[i], deltav_g1_mean[i])
        deltav_mean_deltav["g2"].Fill(deltav_g2[i], deltav_g2_mean[i])
        deltav_mean_deltav["g3"].Fill(deltav_g3[i], deltav_g3_mean[i])
        
        

        if pulseheightg1t[i]>max_pulseh : hist_pulseheight_g1.AddBinContent(n_bin_ph, 1)
        else : hist_pulseheight_g1.Fill(pulseheightg1t[i])
        if pulseheightg1b[i]>max_pulseh : hist_pulseheight_g1.AddBinContent(n_bin_ph, 1)
        else : hist_pulseheight_g1.Fill(pulseheightg1b[i])
        if pulseheightg2t[i]>max_pulseh : hist_pulseheight_g2.AddBinContent(n_bin_ph, 1)
        else : hist_pulseheight_g2.Fill(pulseheightg2t[i])
        if pulseheightg2b[i]>max_pulseh : hist_pulseheight_g2.AddBinContent(n_bin_ph, 1)
        else : hist_pulseheight_g2.Fill(pulseheightg2b[i])
        if pulseheightg3t[i]>max_pulseh : hist_pulseheight_g3.AddBinContent(n_bin_ph, 1)
        else : hist_pulseheight_g3.Fill(pulseheightg3t[i])
        if pulseheightg3b[i]>max_pulseh : hist_pulseheight_g3.AddBinContent(n_bin_ph, 1)
        else : hist_pulseheight_g3.Fill(pulseheightg3b[i])
        
        hist_deltapulseheight_pulseheight.Fill(pulseheightg1b[i], deltapulseheight_g1[i])
        hist_deltapulseheight_pulseheight.Fill(pulseheightg2b[i], deltapulseheight_g2[i])
        hist_deltapulseheight_pulseheight.Fill(pulseheightg3b[i], deltapulseheight_g3[i])
        
        bin_vardeltapulseh_g1_max = hist_vardeltapulseheight_pulseheight.FindBin(max_pulseh, var_deltapulseheight_g1[i])
        bin_vardeltapulseh_g1_min = hist_vardeltapulseheight_pulseheight.FindBin(min_pulseh, var_deltapulseheight_g1[i])
        bin_vardeltapulseh_g2_max = hist_vardeltapulseheight_pulseheight.FindBin(max_pulseh, var_deltapulseheight_g2[i])
        bin_vardeltapulseh_g2_min = hist_vardeltapulseheight_pulseheight.FindBin(min_pulseh, var_deltapulseheight_g2[i])
        bin_vardeltapulseh_g3_max = hist_vardeltapulseheight_pulseheight.FindBin(max_pulseh, var_deltapulseheight_g3[i])
        bin_vardeltapulseh_g3_min = hist_vardeltapulseheight_pulseheight.FindBin(min_pulseh, var_deltapulseheight_g3[i])
        
        if pulseheightg1b[i]>max_pulseh :hist_vardeltapulseheight_pulseheight.AddBinContent(bin_vardeltapulseh_g1_max) 
        elif pulseheightg1b[i]<min_pulseh :hist_vardeltapulseheight_pulseheight.AddBinContent(bin_vardeltapulseh_g1_min)
        else: hist_vardeltapulseheight_pulseheight.Fill(pulseheightg1b[i], var_deltapulseheight_g1[i])
        if pulseheightg2b[i]>max_pulseh : hist_vardeltapulseheight_pulseheight.AddBinContent(bin_vardeltapulseh_g2_max)
        elif pulseheightg2b[i]<min_pulseh : hist_vardeltapulseheight_pulseheight.AddBinContent(bin_vardeltapulseh_g2_min)
        else:hist_vardeltapulseheight_pulseheight.Fill(pulseheightg2b[i], var_deltapulseheight_g2[i])
        if pulseheightg3b[i]>max_pulseh : hist_vardeltapulseheight_pulseheight.AddBinContent(bin_vardeltapulseh_g3_max)
        elif pulseheightg3b[i]>max_pulseh : hist_vardeltapulseheight_pulseheight.AddBinContent(bin_vardeltapulseh_g3_min)
        else:hist_vardeltapulseheight_pulseheight.Fill(pulseheightg3b[i], var_deltapulseheight_g3[i])
        
        bin_g1_max = hist_vardeltapulseheight_integral.FindBin(x_max_integral,var_deltapulseheight_g1[i])
        bin_g1_min = hist_vardeltapulseheight_integral.FindBin(x_min_integral,var_deltapulseheight_g1[i])
        bin_g2_max = hist_vardeltapulseheight_integral.FindBin(x_max_integral,var_deltapulseheight_g2[i])
        bin_g2_min = hist_vardeltapulseheight_integral.FindBin(x_min_integral,var_deltapulseheight_g2[i])
        bin_g3_max = hist_vardeltapulseheight_integral.FindBin(x_max_integral,var_deltapulseheight_g3[i])
        bin_g3_min = hist_vardeltapulseheight_integral.FindBin(x_min_integral,var_deltapulseheight_g3[i])
        if integral_g1b[i]>x_max_integral: hist_vardeltapulseheight_integral.AddBinContent(bin_g1_max)
        elif integral_g1b[i]<x_min_integral: hist_vardeltapulseheight_integral.AddBinContent(bin_g1_min)
        else: hist_vardeltapulseheight_integral.Fill(integral_g1b[i], var_deltapulseheight_g1[i])
        if integral_g2b[i]>x_max_integral: hist_vardeltapulseheight_integral.AddBinContent(bin_g2_max)
        elif integral_g2b[i]<x_min_integral: hist_vardeltapulseheight_integral.AddBinContent(bin_g2_min)
        else: hist_vardeltapulseheight_integral.Fill(integral_g2b[i], var_deltapulseheight_g2[i])
        if integral_g3b[i]>x_max_integral: hist_vardeltapulseheight_integral.AddBinContent(bin_g3_max)
        elif integral_g3b[i]<x_min_integral: hist_vardeltapulseheight_integral.AddBinContent(bin_g3_min)
        else: hist_vardeltapulseheight_integral.Fill(integral_g3b[i], var_deltapulseheight_g3[i])

        hist_vmean_allch.Fill(pulseheightg1t[i], v_mean_g1t[i])
        hist_vmean_allch.Fill(pulseheightg1b[i], v_mean_g1b[i])
        hist_vmean_allch.Fill(pulseheightg2t[i], v_mean_g2t[i])
        hist_vmean_allch.Fill(pulseheightg2b[i], v_mean_g2b[i])
        hist_vmean_allch.Fill(pulseheightg3t[i], v_mean_g3t[i])
        hist_vmean_allch.Fill(pulseheightg3b[i], v_mean_g3b[i])
        
        hist_vmean_topch.Fill(pulseheightg1t[i], v_mean_g1t[i])
        hist_vmean_topch.Fill(pulseheightg2t[i], v_mean_g2t[i])
        hist_vmean_topch.Fill(pulseheightg3t[i], v_mean_g3t[i])
        
        hist_vmean_botch.Fill(pulseheightg1b[i], v_mean_g1b[i])
        hist_vmean_botch.Fill(pulseheightg2b[i], v_mean_g2b[i])
        hist_vmean_botch.Fill(pulseheightg3b[i], v_mean_g3b[i])

        hist_deltav_mean_top.Fill(pulseheightg1t[i], deltav_g1_var[i])
        hist_deltav_mean_top.Fill(pulseheightg2t[i], deltav_g2[i])
        hist_deltav_mean_top.Fill(pulseheightg3t[i], deltav_g3[i])
        
        hist_deltav_mean_topg1.Fill(pulseheightg1t[i], deltav_g1_var[i])
        hist_deltav_mean_topg2.Fill(pulseheightg2t[i], deltav_g2_var[i])
        hist_deltav_mean_topg3.Fill(pulseheightg3t[i], deltav_g3_var[i])

        hist_deltav_mean_bot.Fill(pulseheightg1b[i], deltav_g1_var[i])
        hist_deltav_mean_bot.Fill(pulseheightg2b[i], deltav_g2_var[i])
        hist_deltav_mean_bot.Fill(pulseheightg3b[i], deltav_g3_var[i])
        
        hist_deltav_mean_botg1.Fill(pulseheightg1b[i], deltav_g1_var[i])
        hist_deltav_mean_botg2.Fill(pulseheightg2b[i], deltav_g2_var[i])
        hist_deltav_mean_botg3.Fill(pulseheightg3b[i], deltav_g3_var[i])
        
        if hasattr(tree, 'discharge_rate'):
            hist_pulseheight_disrate.Fill(pulseheightg1t[i], dis_rate[i])
            hist_pulseheight_disrate.Fill(pulseheightg1b[i], dis_rate[i])
            hist_pulseheight_disrate.Fill(pulseheightg2t[i], dis_rate[i])
            hist_pulseheight_disrate.Fill(pulseheightg2b[i], dis_rate[i])
            hist_pulseheight_disrate.Fill(pulseheightg3t[i], dis_rate[i])
            hist_pulseheight_disrate.Fill(pulseheightg3b[i], dis_rate[i])
        
        hist_pulseheight_n_run.Fill(n_run[i], pulseheightg1t[i])
        hist_pulseheight_n_run.Fill(n_run[i], pulseheightg1b[i])
        hist_pulseheight_n_run.Fill(n_run[i], pulseheightg2t[i])
        hist_pulseheight_n_run.Fill(n_run[i], pulseheightg2b[i])
        hist_pulseheight_n_run.Fill(n_run[i], pulseheightg3t[i])
        hist_pulseheight_n_run.Fill(n_run[i], pulseheightg3b[i])
        
        for g in gem :
            histos_n_run[g].Fill(n_run[i], pulse_height_topch[g][i])
            histos_n_run[g].Fill(n_run[i], pulse_height_botch[g][i])
            if hasattr(tree, 'discharge_rate'):
                histos_disrate[g].Fill(pulse_height_topch[g][i], dis_rate[i])
                histos_disrate[g].Fill(pulse_height_botch[g][i], dis_rate[i])

    stack_pulseh = ROOT.THStack("h_pulseheight_g0_stack","pulse height; current(nA)")
    stack_pulseh.Add(hist_pulseheight_g1)
    stack_pulseh.Add(hist_pulseheight_g2)
    stack_pulseh.Add(hist_pulseheight_g3)


    save_plot(h_curr_mean_g1t,"HIST")
    save_plot(h_curr_mean_g1b,"HIST")
    save_plot(h_curr_mean_g2t,"HIST")
    save_plot(h_curr_mean_g2b,"HIST")
    save_plot(h_curr_mean_g3t,"HIST")
    save_plot(h_curr_mean_g3b,"HIST")
    save_plot(hist_vardeltapulseheight_integral, "colz")
    save_plot(hist_vardeltapulseheight_pulseheight, "colz")
    save_plot(stack_pulseh, "HIST")
    save_plot(hist_pulseheight_g1, "HIST")
    save_plot(hist_pulseheight_g2, "HIST")
    save_plot(hist_pulseheight_g3, "HIST")
    save_plot(hist_vmean_allch, "colz")
    save_plot(hist_deltav_mean_top, "colz")
    save_plot(hist_deltav_mean_topg1, "colz")
    save_plot(hist_deltav_mean_topg2, "colz")
    save_plot(hist_deltav_mean_topg3, "colz")
    save_plot(hist_deltav_mean_bot, "colz")
    save_plot(hist_deltav_mean_botg1, "colz")
    save_plot(hist_deltav_mean_botg2, "colz")
    save_plot(hist_deltav_mean_botg3, "colz")
    save_plot(hist_vmean_topch, "colz")
    save_plot(hist_vmean_botch, "colz")
    save_plot(hist_pulseheight_disrate, "colz")
    save_plot(hist_pulseheight_n_run, "colz")
    save_plot(hist_deltapulseheight_pulseheight, "colz")

    for g in gem : 
        save_plot(histos_n_run[g], "colz")
        save_plot(histos_disrate[g], "colz")
        save_plot(deltav_mean_deltav[g], "colz")

