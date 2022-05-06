import os
import optparse
import ROOT

usage = 'prepare_txt.py' #-m "format rename convert store"
parser = optparse.OptionParser(usage)
parser.add_option('-f', '--folder', dest='folder', type='string', default = '/eos/home-a/acagnott/GEMData/CERN_P5', help='Default folder is ../GEMData/CERN_P5')
parser.add_option('-i', '--input', dest='input', type='string', default = 'PICO1_run0000', help="Enter an input root file")
parser.add_option('-m', '--mode', dest='mode', type='string', default = 'format', help="Enter the mode") #'format' 'rename' ' publish'
(opt, args) = parser.parse_args()

ROOT.gStyle.SetOptStat(0000)
ROOT.gStyle.SetOptFit(1111)
ROOT.gROOT.SetBatch()

folder = opt.folder
input = opt.input
mode = opt.mode

file = input+".txt"

if 'format' in mode:
    fin = open(folder+file,"rt")
    print fin
    fileout = file.replace(".txt","_.txt")
    fout = open(folder+fileout,"wt")
    print fout
    for line in fin:
        #read replace the string and write to output file
        fout.write(line.replace(',', '.'))
        #close input and output files
    fin.close()
    print file+" done!"
if 'rename'in mode:
    print 'rename mode'
    fileout = file.replace(".txt","_.txt")

    if (os.path.exists(folder+fileout)):
        print 'from'+ folder+fileout+" to "+folder+file
        os.rename(folder+fileout, folder+file)

if 'convert' in mode:
    print 'convert mode'
    rootcommand="root -l -b -q '"+folder+"../datatotree.C(\""+folder+"/"+file.replace(".txt","")+"\")'"
    print ("executing root macro with ",rootcommand)
    os.system(rootcommand)

if 'publish' in mode:
    print 'publishing files'
    command= ' python peak_finder.py -f '+folder+' -i '+ input
    os.system(command)
