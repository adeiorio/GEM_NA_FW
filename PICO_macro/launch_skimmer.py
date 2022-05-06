import os
import optparse

usage = 'launch_skimmer.py' # -m "skim makeplot"
parser = optparse.OptionParser(usage)
parser.add_option('-m', '--mode', dest='mode', type='string', default = 'skim', help ='which step do you want to run?')
(opt, args) = parser.parse_args()

mode = opt.mode

data_folder = '/eos/home-a/acagnott/GEMData/'

data = 'CERNdata_dischargesfiltertest'#'CERN_P5'#CERN_dischargefiltertest

rootfile_folder = data_folder+data

macro_py = 'dis_skimmer_v3.py'


options = '-w' #'-w -a'  w==write csv and a=append to apply to attach discharges from more files

last_run = 0
run_analyzed = ["PICO1_run"+str(i).zfill(4)+"_skim.root" for i in range(last_run+1)]
run_analyzed = []

dryrun=False#True

for file in os.listdir(rootfile_folder):

        
    if ('skim' in mode and file.endswith(".root") and not 'skim' in file):
        if os.path.exists(rootfile_folder+"/"+file.replace(".root", "_skim.root")): continue
        command = 'python '+macro_py+' -f '+rootfile_folder +" -i "+ file.replace('.root', '')+" &"
        print command
        if not dryrun: os.system(command)

    if ('makeplot'in mode and file.endswith("_skim.root")):
        if file not in run_analyzed:#os.path.exists(rootfile_folder+"/"+file.replace(".root", "_skim.root")):
            command_mp = 'python dis_makeplot.py -f '+rootfile_folder+' -i '+ file.replace('_skim.root', '')+" "+options
            print command_mp
            options = '-w '
            if not dryrun: os.system(command_mp)
            
