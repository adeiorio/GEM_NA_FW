import ROOT
from array import array

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch()        # don't pop up canvases
ROOT.TH1.SetDefaultSumw2()
ROOT.TGaxis.SetMaxDigits(3)

colors = [ROOT.kBlue,
          ROOT.kBlack,
          ROOT.kRed,
          ROOT.kGreen+2,
          ROOT.kMagenta+2,
          ROOT.kAzure+6]

def print_hist(plotpath, hist, name, option = "HIST", log = False, stack = False, title = ""):
    if not(isinstance(hist, list)):
        c1 = ROOT.TCanvas(name, "c1", 50,50,700,600)
        hist.Draw(option)            
        if log:
            c1.SetLogy(1)
        c1.Print(plotpath + "/" + name + ".png")
        c1.Print(plotpath + "/" + name + ".root")
    elif isinstance(hist, list):
        c1 = ROOT.TCanvas(name, "c1", 50,50,700,600)
        if isinstance(hist[0], ROOT.TGraph) or isinstance(hist[0], ROOT.TGraphAsymmErrors):
            i = 0
            mg = ROOT.TMultiGraph('mg', hist[0].GetTitle()+';'+hist[0].GetXaxis().GetTitle()+';'+hist[0].GetYaxis().GetTitle())
            minima = []
            for h in hist:
                #h.SetLineColor(colors[i])
                mg.Add(h)
                minima.append(h.GetMinimum())
                i += 1
            mg.SetMinimum(min(minima))
            mg.Draw(option)
            Low = hist[0].GetXaxis().GetBinLowEdge(1)
            Nbin = hist[0].GetXaxis().GetNbins()
            High = hist[0].GetXaxis().GetBinUpEdge(Nbin)
            mg.GetXaxis().Set(Nbin, Low, High)
            '''
            for i in range(hist[0].GetXaxis().GetNbins()):
                u = i + 1
                mg.GetXaxis().SetBinLabel(u, hist[0].GetXaxis().GetBinLabel(u))
            '''
        elif isinstance(hist[0], ROOT.TEfficiency):
            i = 0
            mg = ROOT.TMultiGraph('mg', hist[0].GetTitle()+';'+hist[0].CreateGraph().GetXaxis().GetTitle()+';'+hist[0].CreateGraph().GetYaxis().GetTitle())

            for h in hist:
                print( h)
                h.SetLineColor(colors[i])
                mg.Add(h.CreateGraph())
                i += 1
            mg.SetMaximum(1.1)
            mg.SetMinimum(0.001)
            mg.Draw(option)
            
        elif isinstance(hist[0], ROOT.TH1F):
            mg = ROOT.THStack()
            i = 0
            print(hist[0].GetTitle(), hist[0].GetXaxis().GetTitle(), hist[0].GetYaxis().GetTitle())
            for h in hist:
                #h.SetLineColor(colors[i])
                if stack:
                    #h.SetFillColor(colors[i])
                    mg.Add(h)
                    i += 1
                else:
                  for h in hist:
                    h.Draw(option+'SAME')
            mg.Draw(option)
            mg.GetXaxis().SetTitle(hist[0].GetXaxis().GetTitle())
            mg.GetYaxis().SetTitle(hist[0].GetYaxis().GetTitle())
            if title == "":
                mg.SetTitle(hist[0].GetTitle()) 
            else:
                mg.SetTitle(title)
        if log:
            c1.SetLogy(1)
        c1.Pad().Modified()
        c1.Pad().Update()
        c1.BuildLegend(0.7, 0.65, 0.95, 0.9)
        c1.Pad().Modified()
        c1.Pad().Update()
        
        c1.Print(plotpath + "/" + str(name) + '.png')
        c1.Print(plotpath + "/" + str(name) + '.root')

def save_hist(infile, plotpath, hist, option = "HIST"):
     fout = ROOT.TFile.Open(plotpath + "/" + infile +".root", "UPDATE")
     fout.cd()
     hist.Write("", ROOT.TObject.kOverwrite)
     fout.Close()

def make_graph(entries, x_array, y_array, name, title, x_title, y_title, color, style = 20):
    graph = ROOT.TGraph(entries, x_array, y_array)
    graph.SetNameTitle(name, title)
    graph.GetXaxis().SetTitle(x_title)
    graph.GetYaxis().SetTitle(y_title)
    graph.SetMarkerColor(color)
    graph.SetMarkerStyle(style)
    return graph

def make_hist(tree, variable, title, nbins, xmin, xmax):
    histoname = variable
    th1f = ROOT.TH1F(histoname, title, nbins, xmin, xmax)
    tree.Project(histoname, variable)
    return th1f

def get_timepeak_arrays(peak_array, time_array, full_array):
    peak_to_draw = array('f', len(peak_array)*[0])
    time_to_draw = array('f', len(peak_array)*[0])
    for i in range(len(peak_array)):
        peak_to_draw[i] = full_array[peak_array[i]]
        time_to_draw[i] = time_array[peak_array[i]]
    return time_to_draw, peak_to_draw
