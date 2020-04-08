##############################################################################
#  Copyright (c) 2018 by Paul Scherrer Institute, Switzerland
#  All rights reserved.
#  Authors: Oliver Bruendler
##############################################################################

import sys
sys.path.append("../..")

from SignalProcessing.Filters.Fir import *
from SignalProcessing.Filters.Cic import FreqResp as CicResp
from SignalProcessing.General.Conversions import *
from SignalProcessing.Plots.Filters import *

import numpy as np
from matplotlib import pyplot as plt
from scipy import signal as sps

def TestCicComp():
    FS = 100e3
    CIC_R = 5
    CIC_O = 3
    FIR_O = 500
    FIR_R = 4

    fig, ax = plt.subplots(3)

    f = np.linspace(0, FS/2, 10000)
    respCic = CicResp(f, FS, CIC_R, CIC_O, True, diffDelay=2)
    ax[0].plot(f, Lin2dB(respCic))
    ax[0].set_title("CIC Gain")
    ax[0].set_ylabel("Gain [dB]")

    coef = CicComp(1.5e3, 2e3, FS/CIC_R, CIC_O, FIR_O, FIR_R, cic_diffDel=2, minPhase=True)
    g = GainAtFreq(coef, f, FS/CIC_R)
    respFir = np.abs(g)
    ax[1].plot(f, Lin2dB(respFir))
    ax[1].set_title("FIR Gain")
    ax[1].set_ylabel("Gain [dB]")

    respComp = respCic*respFir
    ax[2].plot(f, Lin2dB(respComp))
    ax[2].set_title("Compound Gain")
    ax[2].set_ylabel("Gain [dB]")

    fig.subplots_adjust(hspace=0.5)

    plt.show()

def TestMinPhase():
    FS = 100e3
    ORDER = 63
    coef = sps.firwin(ORDER+1, 0.25)
    Bode(coef, fs=FS, show=False)
    ImpStepResp(coef, show=False)
    coef_minPhase = MinPhaseFromLinPhase(coef)
    Bode(coef_minPhase, fs=FS, show=False)
    ImpStepResp(coef_minPhase, show=True)

print("Test CIC Compensation Filter")
TestCicComp()
print("Test Minimum Phase Filter")
TestMinPhase()


