#ifndef __JET_H_
#define __JET_H_

#include <unordered_map>

#include "analysis_suite/Analyzer/interface/Particle.h"

class Jet : public Particle {
public:
    void setup(TTreeReader& fReader, int year);

    float getHT(int name, size_t syst) { return getHT(list(name, syst)); };
    float getHT(int name) { return getHT(*list(name)); };

    float getCentrality(int name, size_t syst) { return getCentrality(list(name, syst)); };
    float getCentrality(int name) { return getCentrality(*list(name)); };

    virtual void setGoodParticles(size_t syst) override
    {
        Particle::setGoodParticles(syst);
        n_loose_bjet.push_back(0);
        n_medium_bjet.push_back(0);
        n_tight_bjet.push_back(0);

        createLooseList();
        createBJetList();
        createTightList();

        fill_bitmap();
    }

    virtual void clear() override
    {
        Particle::clear();
        closeJetDr_by_index.clear();
        n_loose_bjet.clear();
        n_medium_bjet.clear();
        n_tight_bjet.clear();
    }

    std::unordered_map<size_t, size_t> closeJetDr_by_index;

    std::vector<Int_t> n_loose_bjet, n_medium_bjet, n_tight_bjet;

    TTRArray<Int_t>* jetId;
    TTRArray<Int_t>* hadronFlavour;
    TTRArray<Float_t>* btag;

private:
    float loose_bjet_cut, medium_bjet_cut, tight_bjet_cut;
    int looseId = 0b11;

    void createLooseList();
    void createBJetList();
    void createTightList();

    float getHT(std::vector<size_t> jet_list);
    float getCentrality(std::vector<size_t> jet_list);
};

#endif // __JET_H_