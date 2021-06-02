#include "analysis_suite/Analyzer/interface/ScaleFactors.h"

#include "analysis_suite/Analyzer/interface/CommonEnums.h"
#include <filesystem>

ScaleFactors::ScaleFactors(Year year)
    : year_(year)
{
    std::string scaleDir = getenv("CMSSW_BASE");
    scaleDir += "/src/analysis_suite/data/scale_factors/";

    std::string strYear;
    if (year == Year::yr2016) {
        calib = BTagCalibration("deepcsv", scaleDir + "btag_2016.csv");
        strYear = "2016";
    } else if (year == Year::yr2017) {
        calib = BTagCalibration("deepcsv", scaleDir + "btag_2017.csv");
        strYear = "2017";
    } else {
        calib = BTagCalibration("deepcsv", scaleDir + "btag_2018.csv");
        strYear = "2018";
    }
    btag_reader = BTagCalibrationReader(BTagEntry::OP_MEDIUM, "central");
    btag_reader.load(calib, BTagEntry::FLAV_B, "comb");
    btag_reader.load(calib, BTagEntry::FLAV_C, "comb");
    btag_reader.load(calib, BTagEntry::FLAV_UDSG, "incl");

    std::cout << scaleDir + "event_scalefactors.root" << std::endl;
    TFile* f_scale_factors = new TFile((scaleDir + "event_scalefactors.root").c_str());
    f_scale_factors->cd(strYear.c_str());
    pileupSF = (TH1D*)gDirectory->Get("pileupSF");
    h_btag_eff_b = (TH2D*)gDirectory->Get("btagEff_b");
    h_btag_eff_c = (TH2D*)gDirectory->Get("btagEff_c");
    h_btag_eff_udsg = (TH2D*)gDirectory->Get("btagEff_udsg");
}

float ScaleFactors::getBJetSF(const Jet& jets)
{

    float weight = 1.;
    const auto goodBJets = jets.list(Level::Bottom);
    BTagEntry::JetFlavor flav;

    for (auto bidx : goodBJets) {
        int pdgId = std::abs(jets.hadronFlavour->At(bidx));
        if (pdgId == static_cast<Int_t>(PID::Bottom))
            flav = BTagEntry::FLAV_B;
        else if (pdgId == static_cast<Int_t>(PID::Charm))
            flav = BTagEntry::FLAV_C;
        else
            flav = BTagEntry::FLAV_UDSG;
        weight *= btag_reader.eval_auto_bounds("central", flav, jets.eta(bidx), jets.pt(bidx));
    }
    for (auto jidx : jets.list(Level::Tight)) {
        if (std::find(goodBJets.begin(), goodBJets.end(), jidx) != goodBJets.end()) {
            continue; // is a bjet, weighting already taken care of
        }
        int pdgId = std::abs(jets.hadronFlavour->At(jidx));
        float pt = jets.pt(jidx);
        float eta = fabs(jets.eta(jidx));
        float eff = 1;
        if (pdgId == static_cast<Int_t>(PID::Bottom)) {
            flav = BTagEntry::FLAV_B;
            eff = getWeight(h_btag_eff_b, pt, eta);
        } else if (pdgId == static_cast<Int_t>(PID::Charm)) {
            flav = BTagEntry::FLAV_C;
            eff = getWeight(h_btag_eff_c, pt, eta);
        } else {
            flav = BTagEntry::FLAV_UDSG;
            eff = getWeight(h_btag_eff_udsg, pt, eta);
        }
        double bSF = btag_reader.eval_auto_bounds("central", flav, jets.eta(jidx), jets.pt(jidx));
        weight *= (1 - bSF * eff) / (1 - eff);
    }

    return weight;
}

float ScaleFactors::getPileupSF(int nPU)
{
    return getWeight(pileupSF, nPU);
}
