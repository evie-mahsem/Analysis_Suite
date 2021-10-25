#include "analysis_suite/Analyzer/interface/Particle.h"

void GenericParticle::setup(std::string name, TTreeReader& fReader)
{
    m_pt = new TTreeReaderArray<Float_t>(fReader, (name + "_pt").c_str());
    m_eta = new TTreeReaderArray<Float_t>(fReader, (name + "_eta").c_str());
    m_phi = new TTreeReaderArray<Float_t>(fReader, (name + "_phi").c_str());
    m_mass = new TTreeReaderArray<Float_t>(fReader, (name + "_mass").c_str());
}

void GenericParticle::clear() {
    for (auto& [key, plist] : m_partList) {
        plist->clear();
    }
}

void GenericParticle::setup_map(Level level) {
    m_partList[level] = new std::vector<size_t>(); // maybe try for virtual soon?
}

void Particle::clear()
{
    for (auto& [key, plist] : m_partArray) {
        m_bitArray[key].clear();
        for (size_t i = 0; i < nSyst; ++i) {
            plist[i].clear();
        }
    }
}

void Particle::setup_map(Level level)
{
    m_partArray[level] = PartList(nSyst);
    m_partList[level] = nullptr;
    m_bitArray[level] = std::vector<size_t>();
}

void Particle::moveLevel(Level level_start, Level level_end)
{
    m_partList[level_end] = m_partList[level_start];
    m_bitArray[level_end] = m_bitArray[level_start];
}
