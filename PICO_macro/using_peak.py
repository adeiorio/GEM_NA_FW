from peak import *
import ROOT
from scipy.signal import find_peaks

#-f 20191212 -i CERN_20191212_0000.root
infile = ROOT.TFile.Open("20191212/CERN_20191212_0000.root")
tree = infile.Get("t1")
entries = tree.GetEntries()

frequency_data =  (1./280.)*10**3 #ms

ig3t = array('f', entries*[0])

for i in range(entries):
    tree.GetEntry(i)
    ig3t[i] = -tree.I_G3T

trig_entry_current = (int)(0.3*10**6/ frequency_data)

ig3t = ig3t[trig_entry_current:]
#ig3b = ig3b[trig_entry_current:]
#time_current = time_current[trig_entry_current:]  


#Find_peaks(x, height=None, threshold=None, distance=None, prominence=None, width=None, wlen=None, rel_height=0.5, plateau_size=None)                                                    
peak_high = 2 #10                                                                                                                                                                            
threshold_peak = .5
prominence_peak = None#.01                                                                                                                                                                   
distance = 2000
#peaks_ig1t, properties_ig1t = find_peaks(ig1t, height = peak_high, threshold = threshold_peak, prominence = prominence_peak)                                                     
#peaks_ig1b, properties_ig1b = find_peaks(ig1b, height = peak_high, threshold = threshold_peak, prominence = prominence_peak)                                                   
#peaks_ig2t, properties_ig2t = find_peaks(ig2t, height = peak_high, threshold = threshold_peak, prominence = prominence_peak)                                                         
#peaks_ig2b, properties_ig2b = find_peaks(ig2b, height = peak_high, threshold = threshold_peak, prominence = prominence_peak)                                                 
#peaks_ig3t, properties_ig3t = find_peaks(ig3t, height = peak_high, threshold = threshold_peak, prominence = prominence_peak)  
peaks_ig3t, properties_ig3t = find_peaks(ig3t, height = peak_high, distance= distance)

print("G3B ", peaks_ig3t, properties_ig3t)

n_points = 10000
i_array = ig3t[peaks_ig3t[0]-n_points-9:peaks_ig3t[0]-10]
peak1 = peak(entry = peaks_ig3t[0], time=5000,  height = ig3t[peaks_ig3t[0]], i_array= i_array)

print(peak1.entry)
print(peak1.height)

mean_tot1, means1 = peak1.runtime_mean(1000)
print(mean_tot1, means1)
