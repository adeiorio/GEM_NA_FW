import ROOT
import pandas as pd
import root_pandas
import optparse

usage = 'csv_to_root.py' #-p PICO1
parser = optparse.OptionParser(usage)

parser.add_option('-p', '--pico', dest='pico', type='string', default = 'PICO1', help="Enter PICO number")
parser.add_option('-f', '--folder', dest='folder', type='string', default= '/eos/home-a/acagnott/GEM_plot/CERN_P5/', help='csv folder')
parser.add_option('-i', '--input', dest='input', type='string', default= 'PICO1_run0001', help='run name')
(opt, args) = parser.parse_args()

pico = opt.pico
folder = opt.folder
input = opt.input

#folder = "/eos/home-a/acagnott/GEM_plot/"
data = 'LABGEM_scariche/12_01_22/'
if 'CERN_P5' in folder : data = ''
filecsv = input+"discharges_event.csv"

print folder+data+filecsv
df = pd.read_csv(folder+data+filecsv)

print folder+data+filecsv
df.to_root(folder+data+input+'discharges_event.root',key="t1")
