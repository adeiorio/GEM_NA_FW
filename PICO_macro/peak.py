from array import array
import math
import ROOT

def mean(array):
    sum=0
    for arr in array: sum+= arr
    return sum/len(array)

def mean_dev(array, mean):
    sum = 0
    for arr in array: sum += (arr-mean)**2
    dev = math.sqrt(sum)/len(array)
    return dev

def rms(array):
    sum =0
    for arr in array: sum += arr*arr
    m = sum/len(array)
    rms = math.sqrt(m)
    sum = 0
    for arr in array: sum+= (arr-rms)**2
    dev_rms = math.sqrt(sum/len(array))
    return rms, dev_rms


point_tot = 10000  # numero di punti considerati per le medie 
point_discharge = 600 # numero di punti successivi al picco per studiare la scarica, sono +2secondi
to_no_consider = 50


class peak:
    def __init__(self, entry, t_array, height, i_array, v_array, prominence = None, right_threshold=None, left_threshold=None):

        self.entry = entry
        self.time = t_array[entry]
        self.t_peak = (int)(t_array[entry])
        self.height = height
        self.prominence = prominence
        self.right_threshold = right_threshold
        self.left_threshold = left_threshold
        self.i_array = i_array
        self.t_array = t_array
        self.v_array = v_array
        
    def runtime_mean(self, pnt_tot = 10000 , step = 1000, to_drop = 0):
        values = self.i_array[self.entry - (pnt_tot + to_drop): self.entry - to_drop ]
        if self.entry<(pnt_tot+to_drop): print "*****Something went wrong-> peak_entry is smaller than (pnt_tot+to_drop)" 
        mean_tot = mean(values)
        mean_tot_dev = mean_dev(values, mean_tot)
        rms_, rms_dev = rms(values)
        if type(len(values)/step)!= int: print "***Warning: step is not compatible with the # of point considered" 
        n_means = (int)(len(values)/step)
        means = array("f", n_means*[0.])
        means_dev = array("f", n_means*[0.])
        rms__, rms__dev = array("f", n_means*[0.]), array("f", n_means*[0.]) 
        for i in range(n_means):
            means[i] = mean(values[i*step: i*step+(step)])
            means_dev[i] = mean_dev(values[i*step: i*step+step], means[i])
            rms__[i], rms__dev[i] = rms(values[i*step: i*step+step])
        return mean_tot, mean_tot_dev, means, means_dev, rms_, rms_dev, rms__, rms__dev
    
    def graph_peak(self, pnt_to_plot = 500):
        i_to_plot = self.i_array[self.entry - (int)(0.5*pnt_to_plot): self.entry + (int)(0.5*pnt_to_plot)]
        t_to_plot = self.t_array[self.entry - (int)(0.5*pnt_to_plot): self.entry + (int)(0.5*pnt_to_plot)]
        times = t_to_plot
        currents = i_to_plot
        #print("point to plot: "+str(pnt_to_plot))
        #print(times)
        #print(currents)
        gr_it = ROOT.TGraph(pnt_to_plot, times, currents)
        gr_it.SetName("peak")
        gr_it.SetMarkerStyle(20)
        gr_it.GetXaxis().SetTitle("time (ms)")
        gr_it.GetYaxis().SetTitle("current (#mu A)")
        gr_it_clone = gr_it.Clone()
        #gr_itClone = gr_it.Clone()
        #exp = ROOT.TF1("exp", "expo", times[0], times[-1])
        #gr_itClone.Fit("exp")
        #tau = exp.GetParameter(1)
        return gr_it_clone
        #return gr_it, tau
    
    def graph_voltage(self, pnt_to_plot = 100):
        v_to_plot = self.v_array[self.entry-(int)(0.5*pnt_to_plot): self.entry+(int)(0.5*pnt_to_plot)]
        t_to_plot = self.t_array[self.entry - (int)(0.5*pnt_to_plot): self.entry + (int)(0.5*pnt_to_plot)]
        gr_volt = ROOT.TGraph(pnt_to_plot, t_to_plot, v_to_plot)
        gr_volt.SetMarkerStyle(20)
        gr_volt.GetXaxis().SetTitle("time (ms)")
        gr_volt.GetYaxis().SetTitle("Voltage (V)")
        gr_volt_clone = gr_volt.Clone()
        return gr_volt_clone
        
    
        
