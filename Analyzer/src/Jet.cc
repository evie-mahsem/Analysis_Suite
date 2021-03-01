#include "analysis_suite/Analyzer/interface/Jet.h"

void Jet::setup(TTreeReader& fReader, int year) {
    Particle::setup("Jet", fReader, year);
    jetId = new TTRArray<Int_t>(fReader, "Jet_jetId");
    hadronFlavour  = new TTRArray<Int_t>(fReader, "Jet_hadronFlavour");
    btag  = new TTRArray<Float_t>(fReader, "Jet_btagDeepB");


    if(year_ == yr2016) {
        loose_bjet_cut = 0.2219;
        medium_bjet_cut = 0.6324;
        tight_bjet_cut = 0.8958;
    } else if(year_ == yr2017) {
        loose_bjet_cut = 0.1522;
        medium_bjet_cut = 0.4941;
        tight_bjet_cut = 0.8001;
    } else if(year_ == yr2018) {
        loose_bjet_cut = 0.1241;
        medium_bjet_cut = 0.4184;
        tight_bjet_cut = 0.7527;
    }
}

void Jet::createLooseList() {
    for (size_t i = 0; i < pt->GetSize(); i++) {
        if (pt->At(i) > 5 &&
            abs(eta->At(i)) < 2.4 &&
            (jetId->At(i) & looseId) != 0 &&
            (closeJetDr_by_index.find(i) == closeJetDr_by_index.end() ||
             closeJetDr_by_index.at(i) >= pow(0.4, 2))
        )
            looseList.push_back(i);
    }
}

void Jet::createBJetList() {
    for(auto i: looseList) {
        if (btag->At(i) > medium_bjet_cut)
            bjetList.push_back(i);
        n_loose_bjet += (btag->At(i) > loose_bjet_cut) ? 1 : 0;
        n_medium_bjet += (btag->At(i) > medium_bjet_cut) ? 1 : 0;
        n_tight_bjet += (btag->At(i) > tight_bjet_cut) ? 1 : 0;
    }
}

void Jet::createTightList() {
    for(auto i: looseList) {
        if (pt->At(i) > 40)
            tightList.push_back(i);
    }
}

float Jet::getHT(std::vector<size_t> jet_list) {
    float ht = 0;
    for (auto i: jet_list) {
        ht += pt->At(i);
    }
    return ht;
}

float Jet::getCentrality(std::vector<size_t> jet_list) {
    float etot = 0;
    for (auto i: jet_list) {
        LorentzVector jet(pt->At(i), eta->At(i), phi->At(i), mass->At(i));
        etot += jet.E();
    }
    return getHT(jet_list)/etot;
}

void Jet::fillBJet(std::vector<size_t>& fillList, BJetOut& fillObject) {
    fillObject.n_loose = n_loose_bjet;
    fillObject.n_medium = n_medium_bjet;
    fillObject.n_tight = n_tight_bjet;
    for(auto midx: fillList) {
        fillObject.pt.push_back(pt->At(midx));
        fillObject.eta.push_back(eta->At(midx));
        fillObject.phi.push_back(phi->At(midx));
        fillObject.mass.push_back(mass->At(midx));
        fillObject.discriminator.push_back(btag->At(midx));
    }
}