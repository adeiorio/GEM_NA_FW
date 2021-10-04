#include "TFile.h"
#include "TH1.h"
#include "TF1.h"
#include "TGraph.h"
#include "TChain.h"
#include "TCanvas.h"
#include "TMath.h"
#include "iostream"
#include "LOESS1.h"
#include "FFT.h"
#include "TApplication.h"
#include "TStyle.h"
#include <TSystem.h>

using namespace std;

void write(TString foutput, TObject *obj){
  TFile *fout = TFile::Open(foutput, "UPDATE");
  fout->cd();
  obj->Write("",TObject::kOverwrite);
  fout->Close();
}

void print(TString canvasname, TObject *obj, TString option, int logy){
  TCanvas *c1 = new TCanvas(canvasname,"c1",50,50,700,600);
  c1->SetFillColor(0);
  c1->SetBorderMode(0);
  c1->SetFrameFillStyle(0);
  c1->SetFrameBorderMode(0);
  c1->SetLeftMargin( 0.12 );
  c1->SetRightMargin( 0.9 );
  c1->SetTopMargin( 1 );
  c1->SetBottomMargin(-1);
  c1->SetTickx(1);
  c1->SetTicky(1);
  c1->cd();
  obj->Draw(option);
  if(logy)
    c1->SetLogy(1);
  c1->Update();
  c1->Print(canvasname+".png");
  c1->Close(); 
  gSystem->ProcessEvents(); 
  delete c1; 
  c1 = 0;
}


float * low_pass_filter(int n, float data[], float highcut, float dt){
  float alpha = 2*TMath::Pi()*dt*highcut/(2*TMath::Pi()*dt*highcut+1);
  cout << "alpha parameter in the low pass filter is " << alpha << endl;
  cout << "Cutting frequencies higher than " << highcut << endl;
  float y[n] = {0.};
  y[0] = alpha*data[0];
  for(int i = 1; i < n; i++){
    y[i] = y[i-1]+ alpha*(data[i]-y[i-1]);
  }
  return y;
}

float * high_pass_filter(int n, float data[], float lowcut, float dt){
  float alpha = 1/(2*TMath::Pi()*dt*lowcut+1);
  cout << "alpha parameter in the high pass filter is " << alpha << endl;
  cout << "Cutting frequencies lower than " << lowcut << endl;
  float y[n] = {0.};
  y[0] = data[0];
  for(int i = 1; i < n; i++){
    y[i] =  alpha*(y[i-1] + data[i] - data[i-1]);
  }
  return y;
}

float * band_pass_filter(int n, float data[], float lowcut, float highcut, float dt){
  //float *y;
  float *z;
  z = high_pass_filter(n, low_pass_filter(n, data, highcut, dt), lowcut, dt);
  return z;
}


void ana_compass(TString path, TString run_number){
  cout << path << run_number << endl;
  TChain *chain = new TChain("Data_F");
  chain->Add(path + "run_"+run_number+"/FILTERED/compassF_run_"+run_number+".root");
  chain->Add(path + "run_"+run_number+"/FILTERED/compassF_run_"+run_number+"_*.root");
  cout << "Number of events " << chain->GetEntries() << endl;
  TH1F *h_waveform = new TH1F("waveform", "", 5240, 0, 5239);
  TH1F *h_baseline = new TH1F("ch_baseline", "", 20001, 0, 20000);

  // Settings for the histograms
  int integral_min = 88, integral_max = 200, range_baseline = 65; 
  int nbins_charge = 5000, nbins_peak = 1200, nbins_basedistr = 10001, nbins_sigmabasedistr = 125;
  float xmin_charge = -100, xmin_peak = 500, xmin_basedistr = 0, xmin_sigmabasedistr = 1;
  float xmax_charge = 50000000, xmax_peak = 15000, xmax_basedistr = 20000, xmax_sigmabasedistr = 500;
  bool Debug = false;

  // Channel 0 initialization
  TH1F *ch0_charge = new TH1F("ch0_charge", "Charge integral for channel 0", nbins_charge, xmin_charge, xmax_charge);
  TH1F *ch0_peak = new TH1F("ch0_peak", "Distribution of signal peak", nbins_peak, xmin_peak, xmax_peak);
  TH1F *ch0_basedistr = new TH1F("ch0_basedistr", "Baseline mean distribution",  nbins_basedistr, xmin_basedistr, xmax_basedistr);
  TH1F *ch0_sigmabasedistr = new TH1F("ch0_sigmabasedistr", "Baseline RMS distribution", nbins_sigmabasedistr, xmin_sigmabasedistr, xmax_sigmabasedistr);
  TGraph *ch0_base_evt = new TGraph();
  ch0_base_evt->SetNameTitle("ch0_base_evt", "Baseline mean vs event number");
  TGraph *ch0_sigmabase_evt = new TGraph();
  ch0_sigmabase_evt->SetNameTitle("ch0_base_evt", "Baseline RMS vs event number");
  TGraph *ch0_peak_evt = new TGraph();
  ch0_peak_evt->SetNameTitle("ch0_peak_evt", "Signal peak vs event number");
  TGraph *ch0_charge_evt = new TGraph();
  ch0_charge_evt->SetNameTitle("ch0_charge_evt", "Charge integral vs event number");

  // Channel 1 initialization
  TH1F *ch1_charge = new TH1F("ch1_charge", "Charge integral for channel 1", nbins_charge, xmin_charge, xmax_charge);
  TH1F *ch1_peak = new TH1F("ch1_peak", "Distribution of signal peak", nbins_peak, xmin_peak, xmax_peak);
  TH1F *ch1_basedistr = new TH1F("ch1_basedistr", "Baseline mean distribution",  nbins_basedistr, xmin_basedistr, xmax_basedistr);
  TH1F *ch1_sigmabasedistr = new TH1F("ch1_sigmabasedistr", "Baseline RMS distribution", nbins_sigmabasedistr, xmin_sigmabasedistr, xmax_sigmabasedistr);
  TGraph *ch1_base_evt = new TGraph();
  ch1_base_evt->SetNameTitle("ch1_base_evt", "Baseline mean vs event number");
  TGraph *ch1_sigmabase_evt = new TGraph();
  ch1_sigmabase_evt->SetNameTitle("ch1_base_evt", "Baseline RMS vs event number");
  TGraph *ch1_peak_evt = new TGraph();
  ch1_peak_evt->SetNameTitle("ch1_peak_evt", "Signal peak vs event number");
  TGraph *ch1_charge_evt = new TGraph();
  ch1_charge_evt->SetNameTitle("ch1_charge_evt", "Charge integral vs event number");

  // Channel 2 initialization
  TH1F *ch2_charge = new TH1F("ch2_charge", "Charge integral for channel 2", nbins_charge, xmin_charge, xmax_charge);
  TH1F *ch2_peak = new TH1F("ch2_peak", "Distribution of signal peak", nbins_peak, xmin_peak, xmax_peak);
  TH1F *ch2_basedistr = new TH1F("ch2_basedistr", "Baseline mean distribution",  nbins_basedistr, xmin_basedistr, xmax_basedistr);
  TH1F *ch2_sigmabasedistr = new TH1F("ch2_sigmabasedistr", "Baseline RMS distribution", nbins_sigmabasedistr, xmin_sigmabasedistr, xmax_sigmabasedistr);
  TGraph *ch2_base_evt = new TGraph();
  ch2_base_evt->SetNameTitle("ch2_base_evt", "Baseline mean vs event number");
  TGraph *ch2_sigmabase_evt = new TGraph();
  ch2_sigmabase_evt->SetNameTitle("ch2_base_evt", "Baseline RMS vs event number");
  TGraph *ch2_peak_evt = new TGraph();
  ch2_peak_evt->SetNameTitle("ch2_peak_evt", "Signal peak vs event number");
  TGraph *ch2_charge_evt = new TGraph();
  ch2_charge_evt->SetNameTitle("ch2_charge_evt", "Charge integral vs event number");

  // Channel 3 initialization
  TH1F *ch3_charge = new TH1F("ch3_charge", "Charge integral for channel 3", nbins_charge, xmin_charge, xmax_charge);
  TH1F *ch3_peak = new TH1F("ch3_peak", "Distribution of signal peak", nbins_peak, xmin_peak, xmax_peak);
  TH1F *ch3_basedistr = new TH1F("ch3_basedistr", "Baseline mean distribution",  nbins_basedistr, xmin_basedistr, xmax_basedistr);
  TH1F *ch3_sigmabasedistr = new TH1F("ch3_sigmabasedistr", "Baseline RMS distribution", nbins_sigmabasedistr, xmin_sigmabasedistr, xmax_sigmabasedistr);
  TGraph *ch3_base_evt = new TGraph();
  ch3_base_evt->SetNameTitle("ch3_base_evt", "Baseline mean vs event number");
  TGraph *ch3_sigmabase_evt = new TGraph();
  ch3_sigmabase_evt->SetNameTitle("ch3_base_evt", "Baseline RMS vs event number");
  TGraph *ch3_peak_evt = new TGraph();
  ch3_peak_evt->SetNameTitle("ch3_peak_evt", "Signal peak vs event number");
  TGraph *ch3_charge_evt = new TGraph();
  ch3_charge_evt->SetNameTitle("ch3_charge_evt", "Charge integral vs event number");

  UShort_t mChannel;
  TArrayS Waveform;
  TArrayS *mWaveformPnt = &Waveform;
  chain->SetBranchAddress("Samples", &mWaveformPnt);
  chain->SetBranchAddress("Channel", &mChannel);

  int count_ch0 = 0;
  int count_ch1 = 0;
  int count_ch2 = 0;
  int count_ch3 = 0;

  TCanvas *temp = new TCanvas("temp","temp",50,50,700,600);
  temp->SetFillColor(0);
  temp->SetBorderMode(0);
  temp->SetFrameFillStyle(0);
  temp->SetFrameBorderMode(0);
  temp->SetLeftMargin( 0.12 );
  temp->SetRightMargin( 0.9 );
  temp->SetTopMargin( 1 );
  temp->SetBottomMargin(-1);
  temp->SetTickx(1);
  temp->SetTicky(1);

  int lastevt = 5001;
  if(!Debug)
    lastevt = chain->GetEntries();
  for(Int_t evt = 0; evt < lastevt; evt++){
    chain->GetEvent(evt);
    h_waveform->Reset("ICES");
    h_baseline->Reset("ICES");
    int wfsize = Waveform.GetSize();
    for(Int_t i=0; i < wfsize; i++){
      h_waveform->SetBinContent(i, Waveform[i]);
    }

    if(evt%1000 == 0)
      cout << "Processing event " << evt << " out of " << chain->GetEntries() << endl;

    float data_array[wfsize] = {0.};
    float data_array_nobas[wfsize] = {0.};
    float time_array[wfsize] = {0.};
    float dt = 4E-9; 
    float baseline, sigma_baseline;

    for(int j = 0; j < range_baseline; j++){
      h_baseline->Fill(Waveform[j]);
      baseline = h_baseline->GetMean();
      sigma_baseline = h_baseline->GetRMS();
    }

    for(int j = 0; j < wfsize; j++){
      data_array[j] = Waveform[j];
      data_array_nobas[j] = Waveform[j] - baseline;
      h_waveform->SetBinContent(j, data_array_nobas[j]);
      time_array[j] = j*dt;
    }

    // Ricerca del massimo della forma d'onda
    float max_signal = 0.;
    for(int l = integral_min; l < integral_max; l++){
      if(max_signal < data_array_nobas[l])
	  max_signal = data_array_nobas[l];
    }
    
    /*    TGraph *c = new TGraph();
    ch2_peak_evt->SetNameTitle("ch2_peak_evt", "Signal peak vs event number");

    LOESS1(float x[], float y[], int N = 10)*/

    if(mChannel==0){
      ch0_charge->Fill(h_waveform->Integral(integral_min,integral_max));
      ch0_peak->Fill(max_signal);
      ch0_basedistr->Fill(baseline);
      ch0_sigmabasedistr->Fill(sigma_baseline);
      ch0_base_evt->SetPoint(count_ch0, count_ch0, baseline);
      ch0_sigmabase_evt->SetPoint(count_ch0, count_ch0, sigma_baseline);
      ch0_peak_evt->SetPoint(count_ch0, count_ch0, max_signal);
      ch0_charge_evt->SetPoint(count_ch0, count_ch0, h_waveform->Integral(integral_min,integral_max));
      count_ch0++;
    }

    if(mChannel==1){
      ch1_charge->Fill(h_waveform->Integral(integral_min,integral_max));
      ch1_peak->Fill(max_signal);
      ch1_basedistr->Fill(baseline);
      ch1_sigmabasedistr->Fill(sigma_baseline);
      ch1_base_evt->SetPoint(count_ch1, count_ch1, baseline);
      ch1_sigmabase_evt->SetPoint(count_ch1, count_ch1, sigma_baseline);
      ch1_peak_evt->SetPoint(count_ch1, count_ch1, max_signal);
      ch1_charge_evt->SetPoint(count_ch1, count_ch1, h_waveform->Integral(integral_min,integral_max));
      count_ch1++;
    }
    if(mChannel==2){
      ch2_charge->Fill(h_waveform->Integral(integral_min,integral_max));
      ch2_peak->Fill(max_signal);
      ch2_basedistr->Fill(baseline);
      ch2_sigmabasedistr->Fill(sigma_baseline);
      ch2_base_evt->SetPoint(count_ch2, count_ch2, baseline);
      ch2_sigmabase_evt->SetPoint(count_ch2, count_ch2, sigma_baseline);
      ch2_peak_evt->SetPoint(count_ch2, count_ch2, max_signal);
      ch2_charge_evt->SetPoint(count_ch2, count_ch2, h_waveform->Integral(integral_min,integral_max));
      count_ch2++;
    }
    if(mChannel==3){
      ch3_charge->Fill(h_waveform->Integral(integral_min,integral_max));
      ch3_peak->Fill(max_signal);
      ch3_basedistr->Fill(baseline);
      ch3_sigmabasedistr->Fill(sigma_baseline);
      ch3_base_evt->SetPoint(count_ch3, count_ch3, baseline);
      ch3_sigmabase_evt->SetPoint(count_ch3, count_ch3, sigma_baseline);
      ch3_peak_evt->SetPoint(count_ch3, count_ch3, max_signal);
      ch3_charge_evt->SetPoint(count_ch3, count_ch3, h_waveform->Integral(integral_min,integral_max));
      count_ch3++;
    }

    if(evt==lastevt){
      TCanvas *wave = new TCanvas("wave","wave",50,50,700,600);
      wave->SetFillColor(0);
      wave->SetBorderMode(0);
      wave->SetFrameFillStyle(0);
      wave->SetFrameBorderMode(0);
      wave->SetLeftMargin( 0.12 );
      wave->SetRightMargin( 0.9 );
      wave->SetTopMargin( 1 );
      wave->SetBottomMargin(-1);
      wave->SetTickx(1);
      wave->SetTicky(1);
      wave->cd();
      h_waveform->Draw();
    }
      
  } //This closes the loop over the events

  TF1 *gaus = new TF1("gaus", "gaus");//, 1500, 4500);
  TF1 *gaus_sigmabase = new TF1("gaus", "gaus");//, 1500, 4500);
  float ch0_basedistr_mean, ch0_basedistr_mean_err, ch0_basedistr_sigma, ch0_basedistr_sigma_err, ch0_sigmabasedistr_mean, ch0_sigmabasedistr_mean_err, ch0_sigmabasedistr_sigma, ch0_sigmabasedistr_sigma_err;

  TString fout = "Results_run_" + run_number + ".root";
  if(count_ch0 > 0){ 
    write(fout, ch0_charge);
    write(fout, ch0_peak);
    write(fout, ch0_basedistr);
    temp->cd();
    ch0_basedistr->Fit(gaus, "Q");
    ch0_basedistr_mean = gaus->GetParameter(1);
    ch0_basedistr_mean_err = gaus->GetParError(1);
    ch0_basedistr_sigma = gaus->GetParameter(2);
    ch0_basedistr_sigma_err = gaus->GetParError(2);
    write(fout, ch0_sigmabasedistr);
    gaus_sigmabase->SetRange(ch0_sigmabasedistr->GetMean()-ch0_sigmabasedistr->GetMean()/1.5, ch0_sigmabasedistr->GetMean()+ch0_sigmabasedistr->GetMean()/1.5);
    temp->cd();
    ch0_sigmabasedistr->Fit(gaus_sigmabase, "QR");
    ch0_sigmabasedistr_mean = gaus_sigmabase->GetParameter(1);
    ch0_sigmabasedistr_mean_err = gaus_sigmabase->GetParError(1);
    ch0_sigmabasedistr_sigma = gaus_sigmabase->GetParameter(2);
    ch0_sigmabasedistr_sigma_err = gaus_sigmabase->GetParError(2);
    write(fout, ch0_base_evt);
    write(fout, ch0_sigmabase_evt);
    write(fout, ch0_peak_evt);
    write(fout, ch0_charge_evt);
    TCanvas *c0 = new TCanvas("c0_ch0","c0",50,50,700,600);
    c0->SetFillColor(0);
    c0->SetBorderMode(0);
    c0->SetFrameFillStyle(0);
    c0->SetFrameBorderMode(0);
    c0->SetLeftMargin( 0.12 );
    c0->SetRightMargin( 0.9 );
    c0->SetTopMargin( 1 );
    c0->SetBottomMargin(-1);
    c0->SetTickx(1);
    c0->SetTicky(1);
    c0->Divide(4,2);
    c0->cd(1);
    ch0_charge->Draw();
    c0->cd(2);
    ch0_peak->Draw();
    c0->cd(3);
    ch0_basedistr->Draw();
    c0->cd(4);
    ch0_sigmabasedistr->Draw();
    c0->cd(5);
    ch0_charge_evt->Draw("AP");
    c0->cd(6);
    ch0_peak_evt->Draw("AP");
    c0->cd(7);
    ch0_base_evt->Draw("AP");
    c0->cd(8);
    ch0_sigmabase_evt->Draw("AP");
  }

  if(count_ch1 > 0){ 
    write(fout, ch1_charge);
    write(fout, ch1_peak);
    write(fout, ch1_basedistr);
    write(fout, ch1_sigmabasedistr);
    write(fout, ch1_base_evt);
    write(fout, ch1_sigmabase_evt);
    write(fout, ch1_peak_evt);
    write(fout, ch1_charge_evt);
    TCanvas *c1 = new TCanvas("c1_ch1","c1",50,50,700,600);
    c1->SetFillColor(0);
    c1->SetBorderMode(0);
    c1->SetFrameFillStyle(0);
    c1->SetFrameBorderMode(0);
    c1->SetLeftMargin( 0.12 );
    c1->SetRightMargin( 0.9 );
    c1->SetTopMargin( 1 );
    c1->SetBottomMargin(-1);
    c1->SetTickx(1);
    c1->SetTicky(1);
    c1->Divide(4,2);
    c1->cd(1);
    ch1_charge->Draw();
    c1->cd(2);
    ch1_peak->Draw();
    c1->cd(3);
    ch1_basedistr->Draw();
    c1->cd(4);
    ch1_sigmabasedistr->Draw();
    c1->cd(5);
    ch1_charge_evt->Draw("AP");
    c1->cd(6);
    ch1_peak_evt->Draw("AP");
    c1->cd(7);
    ch1_base_evt->Draw("AP");
    c1->cd(8);
    ch1_sigmabase_evt->Draw("AP");
  }

  if(count_ch2 > 0){ 
    write(fout, ch2_charge);
    write(fout, ch2_peak);
    write(fout, ch2_basedistr);
    write(fout, ch2_sigmabasedistr);
    write(fout, ch2_base_evt);
    write(fout, ch2_sigmabase_evt);
    write(fout, ch2_peak_evt);
    write(fout, ch2_charge_evt);
    TCanvas *c2 = new TCanvas("c2_ch2","c2",50,50,700,600);
    c2->SetFillColor(0);
    c2->SetBorderMode(0);
    c2->SetFrameFillStyle(0);
    c2->SetFrameBorderMode(0);
    c2->SetLeftMargin( 0.12 );
    c2->SetRightMargin( 0.9 );
    c2->SetTopMargin( 1 );
    c2->SetBottomMargin(-1);
    c2->SetTickx(1);
    c2->SetTicky(1);
    c2->Divide(4,2);
    c2->cd(1);
    ch2_charge->Draw();
    c2->cd(2);
    ch2_peak->Draw();
    c2->cd(3);
    ch2_basedistr->Draw();
    c2->cd(4);
    ch2_sigmabasedistr->Draw();
    c2->cd(5);
    ch2_charge_evt->Draw("AP");
    c2->cd(6);
    ch2_peak_evt->Draw("AP");
    c2->cd(7);
    ch2_base_evt->Draw("AP");
    c2->cd(8);
    ch2_sigmabase_evt->Draw("AP");
  }

  if(count_ch3 > 0){ 
    write(fout, ch3_charge);
    write(fout, ch3_peak);
    write(fout, ch3_basedistr);
    write(fout, ch3_sigmabasedistr);
    write(fout, ch3_base_evt);
    write(fout, ch3_sigmabase_evt);
    write(fout, ch3_peak_evt);
    write(fout, ch3_charge_evt);
    TCanvas *c3 = new TCanvas("c3_ch3","c3",50,50,700,600);
    c3->SetFillColor(0);
    c3->SetBorderMode(0);
    c3->SetFrameFillStyle(0);
    c3->SetFrameBorderMode(0);
    c3->SetLeftMargin( 0.12 );
    c3->SetRightMargin( 0.9 );
    c3->SetTopMargin( 1 );
    c3->SetBottomMargin(-1);
    c3->SetTickx(1);
    c3->SetTicky(1);
    c3->Divide(4,2);
    c3->cd(1);
    ch3_charge->Draw();
    c3->cd(2);
    ch3_peak->Draw();
    c3->cd(3);
    ch3_basedistr->Draw();
    c3->cd(4);
    ch3_sigmabasedistr->Draw();
    c3->cd(5);
    ch3_charge_evt->Draw("AP");
    c3->cd(6);
    ch3_peak_evt->Draw("AP");
    c3->cd(7);
    ch3_base_evt->Draw("AP");
    c3->cd(8);
    ch3_sigmabase_evt->Draw("AP");
  }

  //Here the information for the analysis are available

  // Channel 0 initialization
  TH1F *ch0_charge_clean = new TH1F("ch0_charge_clean", "Charge integral for channel 0", nbins_charge, xmin_charge, xmax_charge);
  TH1F *ch0_peak_clean = new TH1F("ch0_peak_clean", "Distribution of signal peak", nbins_peak, xmin_peak, xmax_peak);
  TH1F *ch0_basedistr_clean = new TH1F("ch0_basedistr_clean", "Baseline mean distribution",  nbins_basedistr, xmin_basedistr, xmax_basedistr);
  TH1F *ch0_sigmabasedistr_clean = new TH1F("ch0_sigmabasedistr_clean", "Baseline RMS distribution", nbins_sigmabasedistr, xmin_sigmabasedistr, xmax_sigmabasedistr);
  TGraph *ch0_base_evt_clean = new TGraph();
  ch0_base_evt_clean->SetNameTitle("ch0_base_evt_clean", "Baseline mean vs event number");
  TGraph *ch0_sigmabase_evt_clean = new TGraph();
  ch0_sigmabase_evt_clean->SetNameTitle("ch0_base_evt_clean", "Baseline RMS vs event number");
  TGraph *ch0_peak_evt_clean = new TGraph();
  ch0_peak_evt_clean->SetNameTitle("ch0_peak_evt_clean", "Signal peak vs event number");
  TGraph *ch0_charge_evt_clean = new TGraph();
  ch0_charge_evt_clean->SetNameTitle("ch0_charge_evt_clean", "Charge integral vs event number");

  // Channel 1 initialization
  TH1F *ch1_charge_clean = new TH1F("ch1_charge_clean", "Charge integral for channel 1", nbins_charge, xmin_charge, xmax_charge);
  TH1F *ch1_peak_clean = new TH1F("ch1_peak_clean", "Distribution of signal peak", nbins_peak, xmin_peak, xmax_peak);
  TH1F *ch1_basedistr_clean = new TH1F("ch1_basedistr_clean", "Baseline mean distribution",  nbins_basedistr, xmin_basedistr, xmax_basedistr);
  TH1F *ch1_sigmabasedistr_clean = new TH1F("ch1_sigmabasedistr_clean", "Baseline RMS distribution", nbins_sigmabasedistr, xmin_sigmabasedistr, xmax_sigmabasedistr);
  TGraph *ch1_base_evt_clean = new TGraph();
  ch1_base_evt_clean->SetNameTitle("ch1_base_evt_clean", "Baseline mean vs event number");
  TGraph *ch1_sigmabase_evt_clean = new TGraph();
  ch1_sigmabase_evt_clean->SetNameTitle("ch1_base_evt_clean", "Baseline RMS vs event number");
  TGraph *ch1_peak_evt_clean = new TGraph();
  ch1_peak_evt_clean->SetNameTitle("ch1_peak_evt_clean", "Signal peak vs event number");
  TGraph *ch1_charge_evt_clean = new TGraph();
  ch1_charge_evt_clean->SetNameTitle("ch1_charge_evt_clean", "Charge integral vs event number");

  // Channel 2 initialization
  TH1F *ch2_charge_clean = new TH1F("ch2_charge_clean", "Charge integral for channel 2", nbins_charge, xmin_charge, xmax_charge);
  TH1F *ch2_peak_clean = new TH1F("ch2_peak_clean", "Distribution of signal peak", nbins_peak, xmin_peak, xmax_peak);
  TH1F *ch2_basedistr_clean = new TH1F("ch2_basedistr_clean", "Baseline mean distribution",  nbins_basedistr, xmin_basedistr, xmax_basedistr);
  TH1F *ch2_sigmabasedistr_clean = new TH1F("ch2_sigmabasedistr_clean", "Baseline RMS distribution", nbins_sigmabasedistr, xmin_sigmabasedistr, xmax_sigmabasedistr);
  TGraph *ch2_base_evt_clean = new TGraph();
  ch2_base_evt_clean->SetNameTitle("ch2_base_evt_clean", "Baseline mean vs event number");
  TGraph *ch2_sigmabase_evt_clean = new TGraph();
  ch2_sigmabase_evt_clean->SetNameTitle("ch2_base_evt_clean", "Baseline RMS vs event number");
  TGraph *ch2_peak_evt_clean = new TGraph();
  ch2_peak_evt_clean->SetNameTitle("ch2_peak_evt_clean", "Signal peak vs event number");
  TGraph *ch2_charge_evt_clean = new TGraph();
  ch2_charge_evt_clean->SetNameTitle("ch2_charge_evt_clean", "Charge integral vs event number");

  // Channel 3 initialization
  TH1F *ch3_charge_clean = new TH1F("ch3_charge_clean", "Charge integral for channel 3", nbins_charge, xmin_charge, xmax_charge);
  TH1F *ch3_peak_clean = new TH1F("ch3_peak_clean", "Distribution of signal peak", nbins_peak, xmin_peak, xmax_peak);
  TH1F *ch3_basedistr_clean = new TH1F("ch3_basedistr_clean", "Baseline mean distribution",  nbins_basedistr, xmin_basedistr, xmax_basedistr);
  TH1F *ch3_sigmabasedistr_clean = new TH1F("ch3_sigmabasedistr_clean", "Baseline RMS distribution", nbins_sigmabasedistr, xmin_sigmabasedistr, xmax_sigmabasedistr);
  TGraph *ch3_base_evt_clean = new TGraph();
  ch3_base_evt_clean->SetNameTitle("ch3_base_evt_clean", "Baseline mean vs event number");
  TGraph *ch3_sigmabase_evt_clean = new TGraph();
  ch3_sigmabase_evt_clean->SetNameTitle("ch3_base_evt_clean", "Baseline RMS vs event number");
  TGraph *ch3_peak_evt_clean = new TGraph();
  ch3_peak_evt_clean->SetNameTitle("ch3_peak_evt_clean", "Signal peak vs event number");
  TGraph *ch3_charge_evt_clean = new TGraph();
  ch3_charge_evt_clean->SetNameTitle("ch3_charge_evt_clean", "Charge integral vs event number");

  count_ch0 = 0;
  count_ch1 = 0;
  count_ch2 = 0;
  count_ch3 = 0;


  for(Int_t evt=0; evt<lastevt; evt++){
    chain->GetEvent(evt);
    int wfsize = Waveform.GetSize();
    for(Int_t i=0; i < wfsize; i++){
      h_waveform->SetBinContent(i, Waveform[i]);
    }

    if(evt%1000 == 0)
      cout << "Processing event " << evt << " out of " << chain->GetEntries() << endl;

    float data_array[wfsize] = {0.};
    float data_array_nobas[wfsize] = {0.};
    float time_array[wfsize] = {0.};
    float dt = 4E-9; 
    float baseline, sigma_baseline;

    for(int j = 0; j < range_baseline; j++){
      h_baseline->Fill(Waveform[j]);
      // TF1 *gaus = new TF1("gaus", "gaus");//, 1500, 4500);
      //h_baseline->Fit(gaus, "Q");
      //baseline = gaus->GetParameter(1);
      //sigma_baseline = gaus->GetParameter(2);
      baseline = h_baseline->GetMean();
      sigma_baseline = h_baseline->GetRMS();
    }

    for(int j = 0; j < wfsize; j++){
      data_array[j] = Waveform[j];
      data_array_nobas[j] = Waveform[j] - baseline;
      h_waveform->SetBinContent(j, data_array_nobas[j]);
      time_array[j] = j*dt;
    }

    // Ricerca del massimo della forma d'onda
    float max_signal = 0.;
    for(int l = integral_min; l < integral_max; l++){
      if(max_signal < data_array_nobas[l])
	  max_signal = data_array_nobas[l];
    }
    
    /*    TGraph *c = new TGraph();
    ch2_peak_evt_clean->SetNameTitle("ch2_peak_evt_clean", "Signal peak vs event number");

    LOESS1(float x[], float y[], int N = 10)*/
    float n_sigma_base_ch0 = 2.5;
    float n_sigma_sigmabase_ch0 = 2.5;
    if(mChannel==0){
      if(((baseline < ch0_basedistr_mean + n_sigma_base_ch0*ch0_basedistr_sigma) && (baseline > ch0_basedistr_mean - n_sigma_base_ch0*ch0_basedistr_sigma)) && ((sigma_baseline < ch0_sigmabasedistr_mean + n_sigma_sigmabase_ch0*ch0_sigmabasedistr_sigma) && (sigma_baseline > ch0_sigmabasedistr_mean - n_sigma_sigmabase_ch0*ch0_sigmabasedistr_sigma)) && (h_waveform->Integral(integral_min,integral_max)>10000)){
	ch0_charge_clean->Fill(h_waveform->Integral(integral_min,integral_max));
	ch0_peak_clean->Fill(max_signal);
	ch0_basedistr_clean->Fill(baseline);
	ch0_sigmabasedistr_clean->Fill(sigma_baseline);
	ch0_base_evt_clean->SetPoint(count_ch0, count_ch0, baseline);
	ch0_sigmabase_evt_clean->SetPoint(count_ch0, count_ch0, sigma_baseline);
	ch0_peak_evt_clean->SetPoint(count_ch0, count_ch0, max_signal);
	ch0_charge_evt_clean->SetPoint(count_ch0, count_ch0, h_waveform->Integral(integral_min,integral_max));
	count_ch0++;
      }
    }

    if(mChannel==1){
      ch1_charge_clean->Fill(h_waveform->Integral(integral_min,integral_max));
      ch1_peak_clean->Fill(max_signal);
      ch1_basedistr_clean->Fill(baseline);
      ch1_sigmabasedistr_clean->Fill(sigma_baseline);
      ch1_base_evt_clean->SetPoint(count_ch1, count_ch1, baseline);
      ch1_sigmabase_evt_clean->SetPoint(count_ch1, count_ch1, sigma_baseline);
      ch1_peak_evt_clean->SetPoint(count_ch1, count_ch1, max_signal);
      ch1_charge_evt_clean->SetPoint(count_ch1, count_ch1, h_waveform->Integral(integral_min,integral_max));
      count_ch1++;
    }

    if(mChannel==2){
      ch2_charge_clean->Fill(h_waveform->Integral(integral_min,integral_max));
      ch2_peak_clean->Fill(max_signal);
      ch2_basedistr_clean->Fill(baseline);
      ch2_sigmabasedistr_clean->Fill(sigma_baseline);
      ch2_base_evt_clean->SetPoint(count_ch2, count_ch2, baseline);
      ch2_sigmabase_evt_clean->SetPoint(count_ch2, count_ch2, sigma_baseline);
      ch2_peak_evt_clean->SetPoint(count_ch2, count_ch2, max_signal);
      ch2_charge_evt_clean->SetPoint(count_ch2, count_ch2, h_waveform->Integral(integral_min,integral_max));
      count_ch2++;
    }

    if(mChannel==3){
      ch3_charge_clean->Fill(h_waveform->Integral(integral_min,integral_max));
      ch3_peak_clean->Fill(max_signal);
      ch3_basedistr_clean->Fill(baseline);
      ch3_sigmabasedistr_clean->Fill(sigma_baseline);
      ch3_base_evt_clean->SetPoint(count_ch3, count_ch3, baseline);
      ch3_sigmabase_evt_clean->SetPoint(count_ch3, count_ch3, sigma_baseline);
      ch3_peak_evt_clean->SetPoint(count_ch3, count_ch3, max_signal);
      ch3_charge_evt_clean->SetPoint(count_ch3, count_ch3, h_waveform->Integral(integral_min,integral_max));
      count_ch3++;
    }

    h_waveform->Reset("ICES");
    h_baseline->Reset("ICES");
  }

  TF1 *gaus_leadpeak_peak_ch0 = new TF1("gaus", "gaus");//, 1500, 4500);
  TF1 *gaus_subleadpeak_peak_ch0 = new TF1("gaus", "gaus");//, 1500, 4500);

  if(count_ch0 > 0){ 
    write(fout, ch0_charge_clean);
    write(fout, ch0_peak_clean);
    ch0_peak_clean->GetXaxis()->SetRange(ch0_peak_clean->GetXaxis()->FindBin(1500),ch0_peak_clean->GetXaxis()->FindBin(20000));
    float max_ch0 = ch0_peak_clean->GetMaximumBin();
    ch0_peak_clean->GetXaxis()->SetRange(1,ch0_peak_clean->GetNbinsX());
    float x_peak = ch0_peak_clean->GetXaxis()->GetBinCenter(max_ch0);
    gaus_leadpeak_peak_ch0->SetRange(x_peak-x_peak/5, x_peak+x_peak/5);
    temp->cd();
    ch0_peak_clean->Fit(gaus_leadpeak_peak_ch0, "QR+");
    cout << "Parameter mu of the leading peak of the Pulse height " << gaus_leadpeak_peak_ch0->GetParameter(1) << "+/-" << gaus_leadpeak_peak_ch0->GetParError(1) << endl;
    cout << "Parameter sigma of the leading peak of the Pulse height " << gaus_leadpeak_peak_ch0->GetParameter(2) << "+/-" << gaus_leadpeak_peak_ch0->GetParError(2) << endl;
    gaus_subleadpeak_peak_ch0->SetRange(gaus_leadpeak_peak_ch0->GetParameter(1)/2-gaus_leadpeak_peak_ch0->GetParameter(1)/14, gaus_leadpeak_peak_ch0->GetParameter(1)/2+gaus_leadpeak_peak_ch0->GetParameter(1)/14);
    gaus_subleadpeak_peak_ch0->SetParameter(1, gaus_leadpeak_peak_ch0->GetParameter(1)/2);
    cout << "Range leading peak " << x_peak-x_peak/5 << " " << x_peak+x_peak/5 << endl;
    cout << "Range sub leading peak " << gaus_leadpeak_peak_ch0->GetParameter(1)/2-gaus_leadpeak_peak_ch0->GetParameter(1)/10 << " " << gaus_leadpeak_peak_ch0->GetParameter(1)/2+gaus_leadpeak_peak_ch0->GetParameter(1)/10 << endl;
    temp->cd();
    ch0_peak_clean->Fit(gaus_subleadpeak_peak_ch0, "QR+");
    cout << "Parameter mu of the subleading peak of the Pulse height " << gaus_subleadpeak_peak_ch0->GetParameter(1) << "+/-" << gaus_subleadpeak_peak_ch0->GetParError(1) << endl;
    cout << "Parameter sigma of the subleading peak of the Pulse height " << gaus_subleadpeak_peak_ch0->GetParameter(2) << "+/-" << gaus_subleadpeak_peak_ch0->GetParError(2) << endl;
    write(fout, ch0_basedistr_clean);
    write(fout, ch0_sigmabasedistr_clean);
    write(fout, ch0_base_evt_clean);
    write(fout, ch0_sigmabase_evt_clean);
    write(fout, ch0_peak_evt_clean);
    write(fout, ch0_charge_evt_clean);
    TCanvas *c4 = new TCanvas("c4_ch0","c4",50,50,700,600);
    c4->SetFillColor(0);
    c4->SetBorderMode(0);
    c4->SetFrameFillStyle(0);
    c4->SetFrameBorderMode(0);
    c4->SetLeftMargin( 0.12 );
    c4->SetRightMargin( 0.9 );
    c4->SetTopMargin( 1 );
    c4->SetBottomMargin(-1);
    c4->SetTickx(1);
    c4->SetTicky(1);
    c4->Divide(4,2);
    c4->cd(1);
    ch0_charge_clean->Draw();
    c4->cd(2);
    ch0_peak_clean->Draw();
    c4->cd(3);
    ch0_basedistr_clean->Draw();
    c4->cd(4);
    ch0_sigmabasedistr_clean->Draw();
    c4->cd(5);
    ch0_charge_evt_clean->Draw("AP");
    c4->cd(6);
    ch0_peak_evt_clean->Draw("AP");
    c4->cd(7);
    ch0_base_evt_clean->Draw("AP");
    c4->cd(8);
    ch0_sigmabase_evt_clean->Draw("AP");
  }

  if(count_ch1 > 0){ 
    write(fout, ch1_charge_clean);

    write(fout, ch1_peak_clean);
    write(fout, ch1_basedistr_clean);
    write(fout, ch1_sigmabasedistr_clean);
    write(fout, ch1_base_evt_clean);
    write(fout, ch1_sigmabase_evt_clean);
    write(fout, ch1_peak_evt_clean);
    write(fout, ch1_charge_evt_clean);
    TCanvas *c5 = new TCanvas("c5_ch1","c5",50,50,700,600);
    c5->SetFillColor(0);
    c5->SetBorderMode(0);
    c5->SetFrameFillStyle(0);
    c5->SetFrameBorderMode(0);
    c5->SetLeftMargin( 0.12 );
    c5->SetRightMargin( 0.9 );
    c5->SetTopMargin( 1 );
    c5->SetBottomMargin(-1);
    c5->SetTickx(1);
    c5->SetTicky(1);
    c5->Divide(4,2);
    c5->cd(1);
    ch1_charge_clean->Draw();
    c5->cd(2);
    ch1_peak_clean->Draw();
    c5->cd(3);
    ch1_basedistr_clean->Draw();
    c5->cd(4);
    ch1_sigmabasedistr_clean->Draw();
    c5->cd(5);
    ch1_charge_evt_clean->Draw("AP");
    c5->cd(6);
    ch1_peak_evt_clean->Draw("AP");
    c5->cd(7);
    ch1_base_evt_clean->Draw("AP");
    c5->cd(8);
    ch1_sigmabase_evt_clean->Draw("AP");
  }

  if(count_ch2 > 0){ 
    write(fout, ch2_charge_clean);
    write(fout, ch2_peak_clean);
    write(fout, ch2_basedistr_clean);
    write(fout, ch2_sigmabasedistr_clean);
    write(fout, ch2_base_evt_clean);
    write(fout, ch2_sigmabase_evt_clean);
    write(fout, ch2_peak_evt_clean);
    write(fout, ch2_charge_evt_clean);
    TCanvas *c6 = new TCanvas("c6_ch2","c6",50,50,700,600);
    c6->SetFillColor(0);
    c6->SetBorderMode(0);
    c6->SetFrameFillStyle(0);
    c6->SetFrameBorderMode(0);
    c6->SetLeftMargin( 0.12 );
    c6->SetRightMargin( 0.9 );
    c6->SetTopMargin( 1 );
    c6->SetBottomMargin(-1);
    c6->SetTickx(1);
    c6->SetTicky(1);
    c6->Divide(4,2);
    c6->cd(1);
    ch2_charge_clean->Draw();
    c6->cd(2);
    ch2_peak_clean->Draw();
    c6->cd(3);
    ch2_basedistr_clean->Draw();
    c6->cd(4);
    ch2_sigmabasedistr_clean->Draw();
    c6->cd(5);
    ch2_charge_evt_clean->Draw("AP");
    c6->cd(6);
    ch2_peak_evt_clean->Draw("AP");
    c6->cd(7);
    ch2_base_evt_clean->Draw("AP");
    c6->cd(8);
    ch2_sigmabase_evt_clean->Draw("AP");
  }

  if(count_ch3 > 0){ 
    write(fout, ch3_charge_clean);
    write(fout, ch3_peak_clean);
    write(fout, ch3_basedistr_clean);
    write(fout, ch3_sigmabasedistr_clean);
    write(fout, ch3_base_evt_clean);
    write(fout, ch3_sigmabase_evt_clean);
    write(fout, ch3_peak_evt_clean);
    write(fout, ch3_charge_evt_clean);
    TCanvas *c7 = new TCanvas("c7_ch3","c7",50,50,700,600);
    c7->SetFillColor(0);
    c7->SetBorderMode(0);
    c7->SetFrameFillStyle(0);
    c7->SetFrameBorderMode(0);
    c7->SetLeftMargin( 0.12 );
    c7->SetRightMargin( 0.9 );
    c7->SetTopMargin( 1 );
    c7->SetBottomMargin(-1);
    c7->SetTickx(1);
    c7->SetTicky(1);
    c7->Divide(4,2);
    c7->cd(1);
    ch3_charge_clean->Draw();
    c7->cd(2);
    ch3_peak_clean->Draw();
    c7->cd(3);
    ch3_basedistr_clean->Draw();
    c7->cd(4);
    ch3_sigmabasedistr_clean->Draw();
    c7->cd(5);
    ch3_charge_evt_clean->Draw("AP");
    c7->cd(6);
    ch3_peak_evt_clean->Draw("AP");
    c7->cd(7);
    ch3_base_evt_clean->Draw("AP");
    c7->cd(8);
    ch3_sigmabase_evt_clean->Draw("AP");
  }


}


int main(int argc, char** argv){
  TString path = argv[1];
  TString run = argv[2];
  cout << "Path to the data " << argv[1] << endl;
  cout << "Analysing compass run " << argv[2] << endl;
  TApplication theApp("h1Thread", &argc, argv);
  ana_compass(path, run);
  theApp.Run(kTRUE);
  return 0;
}
