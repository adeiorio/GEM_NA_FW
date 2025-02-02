#include <iostream>
#include "TFile.h"
#include "TTree.h"
#include <fstream>

using namespace std;

// run 50-54 - Variazione su E-field su induction 
// run 55-70 - Variazione su E-field su transfer 2 
// run 21-43 - Variazione su E-field su GEM1 

void GEM_intermediate_extraction(int run_start, int run_stop) {

  //const Int_t   run_size      = 5;
  //const Int_t   run_size      = 16;
  const Int_t   run_size      = 18; //23;
  
  const Int_t   electrodes    =  7;
  const Float_t gap_drift     =  0.3; //cm
  const Float_t gap_transfer1 =  0.1; //cm
  const Float_t gap_transfer2 =  0.2; //cm
  const Float_t gap_induction =  0.1; //cm
  
  Double_t mean[electrodes][run_size], meanErr[electrodes][run_size], rms[electrodes][run_size], rmsErr[electrodes][run_size], chi2[electrodes][run_size], E_drift[run_size], E_GEM1[run_size], E_transfer1[run_size], E_GEM2[run_size], E_transfer2[run_size], E_GEM3[run_size], E_induction[run_size], E_driftErr[run_size], E_GEM1Err[run_size], E_GEM2Err[run_size], E_GEM3Err[run_size], E_transfer2Err[run_size], E_transfer1Err[run_size],  E_inductionErr[run_size], RUN[run_size]; 
   
  ifstream ifile;
  char ifile_name[128];
  for(Int_t run=run_start; run<=run_stop; run++){

    sprintf(ifile_name, "./AnaOutput/Output_Run_%.4i.txt", run);
    cout << ifile_name << endl;
    ifile.open (ifile_name);
    for(Int_t i=0; i<electrodes; i++){
      ifile >> RUN[run-run_start] >> mean[i][run-run_start] >> meanErr[i][run-run_start] >> rms[i][run-run_start] >> rmsErr[i][run-run_start] >> chi2[i][run-run_start] >> E_induction[run-run_start] >> E_GEM3[run-run_start] >> E_transfer2[run-run_start] >> E_GEM2[run-run_start] >> E_transfer1[run-run_start] >> E_GEM1[run-run_start] >> E_drift[run-run_start];
      
      cout<<  "RUN:" <<RUN[run-run_start] << "  " << "  " <<mean[i][run-run_start] << "  " << meanErr[i][run-run_start] << "  "<< rms[i][run-run_start]<< " " << rmsErr[i][run-run_start] << "  " << chi2[i][run-run_start] << "  E_GEM3:" << E_GEM3[run-run_start] <<  "  E_induction:" << E_induction[run-run_start] <<"  E_drift:" << E_drift[run-run_start] <<endl;
    // cout << "Run:"<< run << " Mean:"<<mean << " MeanErr:" << meanErr << "  rms:"<< rms<< "  rmsErr:" << rmsErr << "  chi/ndf:" << chi2 << endl;
   
      // if(i==1)mean[1][run-run_start] = mean[0][run-run_start]+mean[1][run-run_start];
      // if(i==3)mean[3][run-run_start] = mean[2][run-run_start]+mean[3][run-run_start];
      // if(i==5)mean[5][run-run_start] = mean[4][run-run_start]+mean[5][run-run_start];
    }

    E_induction[run-run_start]    = (E_induction[run-run_start]/1000.)/gap_induction;
    E_transfer1[run-run_start]    = (E_transfer1[run-run_start]/1000.)/gap_transfer1;
    E_transfer2[run-run_start]    = (E_transfer2[run-run_start]/1000.)/gap_transfer2;
    E_drift[run-run_start]        = (E_drift[run-run_start]/1000.)/gap_drift; // Trasform Volt in Efield
    E_transfer1Err[run-run_start] = (3/1000.)/gap_transfer1;
    E_transfer2Err[run-run_start] = (3/1000.)/gap_transfer2;
    E_driftErr[run-run_start]     = (3/1000.)/gap_drift;
    E_inductionErr[run-run_start] = (3/1000.); //gap_induction;
    ifile.close();
  }
  TCanvas *c1 = new TCanvas("c1","Electron Collection", 600, 600);
  c1->Divide(3,3);
  TGraphErrors* gr[run_size];
  for(Int_t i=0; i<electrodes;i++){
    gr[i]= new TGraphErrors(run_size, E_GEM3, mean[i], E_GEM3Err, meanErr[i]);
    gr[i]->SetTitle("Electron Collection from Transfer 1 ");
    if(i==0)gr[i]->GetYaxis()->SetTitle("GEM 3 Bottom Current (nA)");
    if(i==1)gr[i]->GetYaxis()->SetTitle("GEM 3 Top Current (nA)");
    if(i==2)gr[i]->GetYaxis()->SetTitle("GEM 2 Bottom Current (nA)");
    if(i==3)gr[i]->GetYaxis()->SetTitle("GEM 2 Top Current (nA)");
    if(i==4)gr[i]->GetYaxis()->SetTitle("GEM 1 Bottom Current (nA)");
    if(i==5)gr[i]->GetYaxis()->SetTitle("GEM 1 Top Current (nA)");
    if(i==6)gr[i]->GetYaxis()->SetTitle("Drift(Cathode) Current (nA)");
    gr[i]->GetXaxis()->SetTitle("Transfer 1 E-Field (kV/cm)");
    c1->cd(i+1);
    c1->SetGridx();
    c1->SetGridy();
    gr[i]->Draw("APE");
  }    
  
  //t1->Close();
}
