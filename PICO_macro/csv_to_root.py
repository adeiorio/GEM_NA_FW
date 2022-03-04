import ROOT
import pandas as pd
import root_pandas
import optparse

usage = 'csv_to_root.py' #-p PICO1
parser = optparse.OptionParser(usage)

parser.add_option('-p', '--pico', dest='pico', type='string', default = 'PICO1', help="Enter PICO number")
(opt, args) = parser.parse_args()

pico = opt.pico

folder = "/eos/home-a/acagnott/GEM_plot/"
data = 'LABGEM_scariche/12_01_22/'
filecsv = pico+"discharges_event.csv"

df = pd.read_csv(folder+data+filecsv)

df.to_root(folder+data+pico+"discharges_event.root", key="t1")
