#ifndef __COMMONENUMS_H_
#define __COMMONENUMS_H_

#include <unordered_map>
#include <vector>

const size_t MAX_PARTICLES = 65535;

enum class Year {
    yr2016,
    yr2017,
    yr2018,
    yrDefault,
};

static const std::unordered_map<Year, std::string> yearMap = {
    { Year::yr2016, "2016" },
    { Year::yr2017, "2017" },
    { Year::yr2018, "2018" }
};

enum class PID {
    Muon = 13,
    Electron = 11,
    Top = 6,
    Bottom = 5,
    Charm = 4,
    Jet = 0
};

enum class Level {
    Loose,
    Fake,
    Tight,
    Top,
    Bottom,
    Jet,
};

enum class Systematic {
    Nominal,
    LHE_muF,
    LHE_muR,

    BJet_BTagging,
    BJet_Eff,
    BJet_Shape_hf,
    BJet_Shape_hfstats1,
    BJet_Shape_hfstats2,
    BJet_Shape_lf,
    BJet_Shape_lfstats1,
    BJet_Shape_lfstats2,
    BJet_Shape_cferr1,
    BJet_Shape_cferr2,

    Muon_ID,
    Muon_Iso,
    Electron_SF,
    Electron_Susy,
    Top_SF,
    Pileup,
    Jet_JER,
    Jet_JES,
};

enum class eVar {
    Nominal,
    Up,
    Down,
};

static const std::unordered_map<std::string, Systematic> syst_by_name = {
    { "LHE_muF", Systematic::LHE_muF },
    { "LHE_muR", Systematic::LHE_muR },

    { "BJet_BTagging", Systematic::BJet_BTagging },
    { "BJet_Eff", Systematic::BJet_Eff },
    { "BJet_Shape_lf", Systematic::BJet_Shape_lf },
    { "BJet_Shape_lfstats1", Systematic::BJet_Shape_lfstats1 },
    { "BJet_Shape_lfstats2", Systematic::BJet_Shape_lfstats2 },
    { "BJet_Shape_hf", Systematic::BJet_Shape_hf },
    { "BJet_Shape_hfstats1", Systematic::BJet_Shape_hfstats1 },
    { "BJet_Shape_hfstats2", Systematic::BJet_Shape_hfstats2 },
    { "BJet_Shape_cferr1", Systematic::BJet_Shape_cferr1 },
    { "BJet_Shape_cferr2", Systematic::BJet_Shape_cferr2 },

    { "Muon_ID", Systematic::Muon_ID },
    { "Muon_Iso", Systematic::Muon_Iso },
    { "Electron_SF", Systematic::Electron_SF },
    { "Electron_Susy", Systematic::Electron_Susy },
    { "Top_SF", Systematic::Top_SF },
    { "Pileup", Systematic::Pileup },
    { "Jet_JER", Systematic::Jet_JER },
    { "Jet_JES", Systematic::Jet_JES },
};

static const std::vector<eVar> syst_vars = { eVar::Up, eVar::Down };
static const std::vector<eVar> nominal_var = { eVar::Nominal };

static const std::unordered_map<eVar, std::string> varName_by_var = {
    { eVar::Nominal, "central" },
    { eVar::Up, "up" },
    { eVar::Down, "down" },
};

#endif // __COMMONENUMS_H_
