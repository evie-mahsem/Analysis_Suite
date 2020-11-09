#!/usr/bin/env python3

import uproot4 as uproot
import awkward1 as ak
import numpy as np
import numba
import math

from Analyzer import AnalyzeTask
from Analyzer.Common import deltaR, jetRel, in_zmass, cartes
from commons.configs import pre

class Muon(AnalyzeTask):
    def __init__(self, task, *args, **kwargs):
        super().__init__(task, *args, **kwargs)

        self.add_job("loose_mask", outmask = "Muon_looseMask",
                     invars = Muon.loose)

        self.add_job("looseIdx", outmask = "Muon_looseIndex",
                     inmask = "Muon_looseMask", invars = ["Muon_pt"])

        self.add_job("fake_mask", outmask = "Muon_basicFakeMask",
                     inmask = "Muon_looseMask", invars = Muon.fake)
        self.add_job("closeJet", outmask = ["Muon_closeJetIndex", "Muon_closeJetDR"],
                     inmask = "Muon_basicFakeMask", invars = Muon.close_jet)
        self.add_job("fullIso", outmask = "Muon_fakeMask",
                     inmask = "Muon_basicFakeMask", invars = Muon.v_fullIso,
                     addvals = [(None, "Muon_closeJetIndex")])

        self.add_job("tight_mask", outmask = "Muon_finalMask",
                     inmask = "Muon_fakeMask", invars = Muon.tight)

        self.add_job("pass_zveto", outmask = "Muon_ZVeto",
                     inmask = "Muon_looseMask", invars = Muon.muon_part,
                     addvals = [("Muon_finalMask", "Muon_looseIndex")])

        self.add_job("lep_sf", outmask = "Muon_scale", inmask = "Muon_looseMask",
                     invars = pre("Muon", ["pt", "eta"]))
        self.add_job("lep_tracking_sf", outmask = "Muon_trackingScale",
                     inmask = "Muon_looseMask", invars = ["Muon_eta"])
    # Numba methods

    loose = pre("Muon", ["pt", "eta", "isGlobal", "isTracker", "isPFcand",
                         'miniPFRelIso_all', 'dz', 'dxy'])
    @staticmethod
    @numba.vectorize('b1(f4,f4,b1,b1,b1,f4,f4,f4)')
    def loose_mask(pt, eta, isGlobal, isTracker, isPFcand, iso, dz, dxy):
        return (pt > 5 and
           abs(eta) < 2.4 and
           (isGlobal or isTracker) and
           isPFcand and
           iso < 0.4 and
           abs(dz) < 0.1 and
           abs(dxy) < 0.05
           )


    fake = pre("Muon", ["pt", "tightCharge", "mediumId", "sip3d"])
    @staticmethod
    @numba.vectorize('b1(f4,i4,b1,f4)')
    def fake_mask(pt, tightCharge, mediumId, sip3d):
        return (
            pt > 10 and
            tightCharge == 2 and
            mediumId and
            sip3d < 4
           )

    tight = pre("Muon", ["pt", 'eta', 'miniPFRelIso_all'])
    @staticmethod
    @numba.vectorize('b1(f4,f4,f4)')
    def tight_mask(pt, eta, iso):
        return (
            #pt > 20 and
            pt > 15 and
            iso < 0.16
           )
    
    @staticmethod
    @numba.jit(nopython=True)
    def looseIdx(events, builder):
        for event in events:
            builder.begin_list()
            for midx in range(len(event.Muon_pt)):
                builder.integer(midx)
            builder.end_list()

    close_jet = ["Muon_eta", "Muon_phi", "Jet_eta", "Jet_phi"]
    @staticmethod
    def closeJet(events):
        leta, jeta = cartes(events.Muon_eta, events.Jet_eta)
        lphi, jphi = cartes(events.Muon_phi, events.Jet_phi)
        dr = (jeta-leta)**2 + (jphi-lphi)**2
        dr_idx = ak.argmin(dr, axis=-1) % ak.count(events.Jet_eta, axis=-1)
        dr_min = ak.min(dr, axis=-1)
        return ak.zip((dr_idx, dr_min))

    
    v_fullIso = pre("Muon", ["pt", "eta", "phi"]) + pre("Jet", ["pt", "eta", "phi"])
    @staticmethod
    def fullIso(events):
        I2 = 0.8
        I3_pow2 = 7.2**2

        closeJet_pt = events.Jet_pt[events.Muon_closeJetIndex]
        closeJet_eta = events.Jet_eta[events.Muon_closeJetIndex]
        closeJet_phi = events.Jet_phi[events.Muon_closeJetIndex]
        jetrel = jetRel(events.Muon_pt, events.Muon_eta,
                        events.Muon_phi, closeJet_pt,
                        closeJet_eta, closeJet_phi)
        pass_I2 = (events.Muon_pt/closeJet_pt) > I2
        pass_I3 = jetrel > I3_pow2
        return pass_I2 or pass_I3


    muon_part = pre("Muon", ["pt", "eta", "phi", "charge"])
    @staticmethod
    def pass_zveto(events):
        tpt, lpt = cartes(events.Muon_pt[events.Muon_looseIndex], events.Muon_pt)
        teta, leta = cartes(events.Muon_eta[events.Muon_looseIndex], events.Muon_eta)
        tphi, lphi = cartes(events.Muon_phi[events.Muon_looseIndex], events.Muon_phi)
        tq, lq = cartes(events.Muon_charge[events.Muon_looseIndex], events.Muon_charge)

        isOS = lq*tq < 0
        zmass = in_zmass(tpt[isOS], teta[isOS], tphi[isOS],
                         lpt[isOS], leta[isOS], lphi[isOS])
        return ak.sum(zmass, axis=-1) != 0


    @staticmethod
    @numba.vectorize('f4(f4,f4)')
    def lep_sf(pt, eta):
        sf = np.array([[0.9047, 0.8860, 0.8916, 0.8394],
                       [0.9430, 0.9685, 0.9741, 0.8917],
                       [0.9707, 0.9724, 0.9777, 0.9180],
                       [0.9821, 0.9850, 0.9934, 0.9389],
                       [0.9854, 0.9861, 0.9968, 0.9453],
                       [0.9813, 0.9819, 0.9964, 0.9410],
                       [0.9830, 0.9861, 0.9994, 0.9525]])
        pt_edges = np.array([20, 25, 30, 40, 50, 60, 14000])
        eta_edges = np.array([0.9, 1.2, 2.1, 2.4])

        return sf[np.argmax(pt <= pt_edges), np.argmax(abs(eta) <= eta_edges)]



    @staticmethod
    @numba.vectorize('f4(f4)')
    def lep_tracking_sf(eta):
        sf = np.array([0.9879, 0.9939, 0.9970, 0.9954, 0.9937, 0.9959, 0.9976,
                       0.9961, 0.9930, 0.9819])
        eta_edges = np.array([-2.1, -1.6, -1.1, -0.6, 0.0, 0.6, 1.1, 1.6,
                              2.1, 2.4])
        return sf[np.argmax(eta <= eta_edges)]