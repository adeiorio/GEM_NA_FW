#source launch_P5publish.sh PICO1_run0000
python launch_P5publish.py -f /eos/home-a/acagnott/GEMData/CERN_P5/ -i $1 -m 'format'
python launch_P5publish.py -f /eos/home-a/acagnott/GEMData/CERN_P5/ -i $1 -m 'rename'
python launch_P5publish.py -f /eos/home-a/acagnott/GEMData/CERN_P5/ -i $1 -m 'convert'
python launch_P5publish.py -f /eos/home-a/acagnott/GEMData/CERN_P5/ -i $1 -m 'publish'
