import ROOT
import optparse
from array import array

usage = 'python zoom_graph.py'
parser= optparse.OptionParser(usage)

parser.add_option('-f', '--folder', dest='folder', type='string', default = 'CERN_20191213_0008', help='Default folder is 20191212')
parser.add_option('-i', '--input', dest='input', type='string', default = 'CERN_20191213_0008_allGraph.root', help="Enter an input root file")
parser.add_option('-c', '--channel', dest='channel', type='string', default = 'all', help='channels to plot')
parser.add_option('-t', '--time0', dest='time0', type='string', default = '0', help='x minimum')
parser.add_option('-y', '--time1', dest='time1', type='string', default = '600000', help='x maximum')
(opt, args) = parser.parse_args()

folder = opt.folder
infile = ROOT.TFile.Open(folder+'/'+opt.input)
print('input file:', infile)
t_min = float(opt.time0)
t_max = float(opt.time1)
ch_volt = ['DRIFT', 'G3T', 'G3B', 'G2T', 'G2B', 'G1T', 'G1B']
outfile = ROOT.TFile.Open(folder+'/gr_test.root','RECREATE')

dic_range = {'DRIFT' :  (-3320, -3290), 
             'G1T': (-2535, -2510), 
             'G1B': (-2125, -2105), 
             'G2T': (-1810, -1795), 
             'G2B': (-1411, -1409), 
             'G3T': (-860, -800), 
             'G3B':(-434, -433)
             }

if opt.channel != 'all' : ch_volt = [opt.channel]
     

n_zeros=0

for ch in ch_volt:
    gr = infile.Get('Voltage_'+ch)
    gr.GetXaxis().SetRangeUser(t_min, t_max)
    gr.SetTitle(ch)
    outfile.cd()
    gr.Write()
