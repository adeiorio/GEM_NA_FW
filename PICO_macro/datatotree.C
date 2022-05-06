#include <iostream>
#include "TFile.h"
#include "TTree.h"
#include <fstream>

using namespace std;

void datatotree(TString filename) {

  ifstream in;
  Double_t time = 0.; 
  Float_t v1 = 0, v2 = 0, v3 = 0, v4 = 0, v5 = 0, v6 = 0, v7 = 0, i1 = 0, i2 = 0, i3 = 0, i4 = 0, i5 = 0, i6 = 0, i7 = 0;
  Int_t nlines = 0;
  in.open(filename+".txt");
  TFile *f = new TFile(filename+".root","RECREATE");

  TTree* t1 = new TTree("t1", "t1");
  t1->Branch("Time",    &time, "Time/D");
  t1->Branch("V_G3B",   &v1,   "V_G3B/F");
  t1->Branch("I_G3B",   &i1,   "I_G3B/F");
  t1->Branch("V_G3T",   &v2,   "V_G3T/F");
  t1->Branch("I_G3T",   &i2,   "I_G3T/F");
  t1->Branch("V_G2B",   &v3,   "V_G2B/F");
  t1->Branch("I_G2B",   &i3,   "I_G2B/F");
  t1->Branch("V_G2T",   &v4,   "V_G2T/F");
  t1->Branch("I_G2T",   &i4,   "I_G2T/F");
  t1->Branch("V_G1B",   &v5,   "V_G1B/F");
  t1->Branch("I_G1B",   &i5,   "I_G1B/F");
  t1->Branch("V_G1T",   &v6,   "V_G1T/F");
  t1->Branch("I_G1T",   &i6,   "I_G1T/F");
  t1->Branch("V_drift", &v7,   "V_drift/F");
  t1->Branch("I_drift", &i7,   "I_drift/F");


  while(1){
    //cout << "Is the file good? " << in.good() << endl;
    if (!in.good()) break;
    //cout << "ciao" << endl;
    in >> time >> v1 >> v2 >> v3 >> v4 >> v5 >> v6 >> v7;
    //cout << time << "||" << v1 << "||" << v2 << "||" << v3 << "||" << v4 << "||" << v5 << "||" << v6 << "||" << v7 << "||" << endl;
    //nlines++;
    in >> i1 >> i2 >> i3 >> i4 >> i5 >> i6 >> i7;
    //cout << i1 << "||" << i2 << "||" << i3 << "||" << i4 << "||" << i5 << "||" << i6 << "||" << i7 << endl;
    t1->Fill();//time, v1, v2, v3, v4, v5, v6, v7, i1, i2, i3, i4, i5, i6, i7);
    //nlines++;
  }

  //t1->Close();
   f->Write();
   f->Close();
}
