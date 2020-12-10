#!/usr/bin/env python3
import awkward1 as ak
import numpy as np
import numba
from types import MethodType

from analysis_suite.Analyzer.ThreeTop import Jet, Electron, EventWide


setattr(Electron, "mva_vars", ["Electron_mvaFall17V1noIso"])

@staticmethod
@numba.vectorize('b1(f4,f4,f4,f4)')
def mva_loose(pt, eCorr, eta, mva):
    A = np.array([0.488, -0.045, 0.176])
    B = np.array([-0.64, -0.775, -0.733])
    C = np.array([0.148, 0.075, 0.077])
    if pt/eCorr < 5: return False
    elif pt/eCorr < 10:  mvaVec = A
    elif pt/eCorr < 25:  mvaVec = B - C*(1 - (pt/eCorr-10)/15)
    else:                mvaVec = B

    if abs(eta) < 0.8:     mvaCut = mvaVec[0]
    elif abs(eta) < 1.479: mvaCut = mvaVec[1]
    elif abs(eta) < 2.5:   mvaCut = mvaVec[2]

    return mva > mvaCut
setattr(Electron, "mva_loose", mva_loose)


@staticmethod
@numba.vectorize('b1(f4,f4,f4,f4)')
def mva_tight(pt, eCorr, eta, mva):
    B = np.array([0.68, 0.475, 0.32])
    C = np.array([0.48 , 0.375, 0.42])
    if pt/eCorr < 10: return False
    elif pt/eCorr < 25:  mvaVec = B - C*(1 - (pt/eCorr-10)/15)
    else:                mvaVec = B

    if abs(eta) < 0.8:     mvaCut = mvaVec[0]
    elif abs(eta) < 1.479: mvaCut = mvaVec[1]
    elif abs(eta) < 2.5:   mvaCut = mvaVec[2]

    return mva > mvaCut
setattr(Electron, "mva_tight", mva_tight)


setattr(Jet, "btag", ["Jet_btagDeepB"])

@numba.vectorize('b1(f4)')
def loose_bjet_mask(btag):
    return btag > 0.1522
setattr(Jet, "loose_bjet_mask", loose_bjet_mask)

@numba.vectorize('b1(f4)')
def bjet_mask(btag):
    return (btag > 0.4941)
setattr(Jet, "bjet_mask", bjet_mask)

@numba.vectorize('b1(f4)')
def tight_bjet_mask(btag):
    return (btag > 0.8001)
setattr(Jet, "tight_bjet_mask", tight_bjet_mask)


triggers_vars = ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8",
                 "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",
                 "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ",
                 "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL"]
setattr(EventWide, "triggers_vars", triggers_vars)
@staticmethod
@numba.vectorize('b1(b1,b1,b1,b1,i8)')
def trigger_2lep(mm_trig, em_trig1, em_trig2, ee_trig, chan):
    return (
        (abs(chan) <= 1) or
        ((abs(chan) == 20 and ee_trig) or
         ((abs(chan)-21)//2 == 0  and (em_trig1 or em_trig2)) or
         (abs(chan) == 23 and mm_trig))
    )
setattr(EventWide, "trigger_2lep", trigger_2lep)


#reusing 2016 for now

@numba.vectorize('f4(f4,f4,i4)')
def get_eff(pt, eta, flav):
    pt_bins = np.array([ 20.,25.,30.,35.,40.,45.,50.,60.,70.,80.,90., 100.,
                         120., 150., 200., 300., 400.,600.00001])
    eta_bins = np.array([0.,0.4,0.8,1.2,1.6,2.,2.4,2.80001])
    beff = np.array(
        [[0.,0.,0.,0.,0.,0.,0.],
         [0.41398005,0.55588727,0.61965316,0.65848032,0.68257666,0.69821823,0.70871995],
         [0.73255498,0.73647957,0.73747648,0.73899761,0.73867302,0.72925876,0.70192552],
         [0.,0.4193679,0.56195701,0.62679134,0.66609534,0.68992415,0.70587103],
         [0.73503713,0.73999806,0.74403387,0.74532109,0.74566087,0.74365821,0.73273753],
         [0.60052583,0.,0.4108313,0.55213561,0.61519638,0.65325901,0.6757757],
         [0.71092268,0.71817402,0.72304025,0.72517578,0.72606662,0.72493386,0.72182742],
         [0.6226428,0.57429372,0.,0.38088279,0.52725437,0.58735835,0.62354587],
         [0.66814147,0.67650933,0.68232424,0.68549007,0.6861546,0.6843152,0.68023263],
         [0.61825041,0.58487348,0.55704951,0.,0.36727572,0.51866208,0.57288085],
         [0.63809814,0.6438944,0.64879239,0.65105793,0.65022993,0.6477851,0.64366503],
         [0.60408685,0.56224321,0.52647918,0.51515618,0.,0.30399818,0.44724396],
         [0.54809753,0.55754159,0.56281068,0.56491298,0.56443807,0.55909425,0.55421188],
         [0.52819869,0.49943524,0.45419927,0.43113976,0.42315369,0.,0.0870582],
         [0.1741395,0.18299451,0.18721013,0.18674717,0.18533283,0.17804836,0.17241213],
         [0.15786974,0.14962066,0.14280494,0.13499271,0.13724089,0.17142857,0.],
         [0.,0.,0.,0.,0.,0.,0.]])

    ceff = np.array(
        [[0.,0.,0.,0.,0.,0.,0.],
         [0.09605581,0.12410384,0.12922657,0.13003449,0.12713233,0.12349516,0.11992575],
         [0.11077503,0.11290275,0.11418996,0.11694229,0.1228226,0.12803157,0.13353377],
         [0.,0.09769354,0.12782521,0.13562521,0.13614974,0.13475622,0.13103418],
         [0.11955391,0.11931815,0.12080788,0.12211066,0.12442252,0.13013958,0.1336838],
         [0.15290434,0.,0.09386869,0.12526362,0.13330156,0.13620229,0.13387709],
         [0.12403051,0.12166882,0.12033651,0.12213164,0.12210498,0.12331598,0.12795951],
         [0.1396926,0.15268153,0.,0.08410784,0.12118319,0.13137186,0.13429759],
         [0.1272108,0.12518141,0.12222271,0.12144273,0.12181173,0.12322879,0.12523763],
         [0.13454179,0.15027482,0.16276056,0.,0.08142199,0.12066179,0.12976008],
         [0.1299197,0.12717505,0.1237424,0.12124234,0.11974666,0.11923736,0.12014573],
         [0.12881077,0.12776468,0.13442361,0.14039512,0.,0.0680127,0.10547481],
         [0.11739374,0.11558625,0.11366165,0.11125208,0.10721674,0.10475925,0.10587145],
         [0.10896039,0.10879443,0.09395944,0.1106383,0.11741935,0.,0.01783546],
         [0.0377829,0.03943053,0.03991925,0.03793149,0.03720793,0.0354333,0.03502522],
         [0.03249954,0.0341295,0.03190705,0.0311245,0.0392638,0.04481793,0.],
         [0.,0.,0.,0.,0.,0.,0.]])

    udsgeff = np.array(
        [[0.,0.,0.,0.,0.,0.,0.],
         [0.01028227,0.01377282,0.01404542,0.01285212,0.01125089,0.00984283,0.00886976],
         [0.00742326,0.00740213,0.00743306,0.00781097,0.00841655,0.00941328,0.01176253],
         [0.,0.01141693,0.0156972,0.01635897,0.01513036,0.0135414,0.01193933],
         [0.00922866,0.00903339,0.00907098,0.00912464,0.00934741,0.00972857,0.01061892],
         [0.02813613,0.,0.0118528,0.0169082,0.01760006,0.01645718,0.01474649],
         [0.01078179,0.0100911,0.00989137,0.00967994,0.00963295,0.00977745,0.01057892],
         [0.02103948,0.02887109,0.,0.01206342,0.01908405,0.02065739,0.01952669],
         [0.0144558,0.01341292,0.01266643,0.01231569,0.01242357,0.0123856,0.01279626],
         [0.02247174,0.03444328,0.04886468,0.,0.01362941,0.02137496,0.02207748],
         [0.01748953,0.01611835,0.01503661,0.01409539,0.01377884,0.01380135,0.01388992],
         [0.01987808,0.02277699,0.02942324,0.03396428,0.,0.01378709,0.02185348],
         [0.02054229,0.01920641,0.01807032,0.01668022,0.01592929,0.01576353,0.01586111],
         [0.01849175,0.01928662,0.01969277,0.02268445,0.02348822,0.,0.00417874],
         [0.00880346,0.00911839,0.00912211,0.0089739,0.0085578,0.00798211,0.0078915],
         [0.00772069,0.00771858,0.00708935,0.00755066,0.00776725,0.00821618,0.],
         [0.,0.,0.,0.,0.,0.,0.]])

    ptbin = np.argmax(pt < pt_bins) - 1
    etabin = np.argmax(eta < eta_bins) - 1
    if abs(flav) == 5:
        return beff[ptbin][etabin]
    elif abs(flav) == 4:
        return ceff[ptbin][etabin]
    else:
        return udsgeff[ptbin][etabin]
setattr(Jet, "get_eff", get_eff)

@numba.vectorize('f4(f4,i4)')
def get_sf(x, flav):
    if abs(flav) == 5:
        return 0.637301*((1.+(0.479205*x))/(1.+(0.311514*x)))
    elif abs(flav) == 4:
        return 0.637301*((1.+(0.479205*x))/(1.+(0.311514*x)))
    else:
        return 1.03216+0.000504744*x+2.12276e-08*x*x+-2.27663e-10*x*x*x
setattr(Jet, "get_sf", get_sf)

@numba.vectorize('f4(f4,i4)')
def get_loose_sf(x, flav):
    if abs(flav) == 5:
        return 0.733112*((1.+(0.336449*x))/(1.+(0.246914*x)))
    elif abs(flav) == 4:
        return 0.733112*((1.+(0.336449*x))/(1.+(0.246914*x)))
    else:
        return 1.06765+0.000317422*x+-4.61732e-07*x*x+2.03608e-10*x*x*x
setattr(Jet, "get_loose_sf", get_loose_sf)

@numba.vectorize('f4(f4,i4)')
def get_tight_sf(x, flav):
    if abs(flav) == 5:
        return 0.506673*((1.+(0.464958*x))/(1.+(0.239689*x)))
    elif abs(flav) == 4:
        return 0.506673*((1.+(0.464958*x))/(1.+(0.239689*x)))
    else:
        return 1.00762+51.6984/(x*x)+0.000370519*x
setattr(Jet, "get_tight_sf", get_tight_sf)
