##############################################################################
#  Copyright (c) 2018 by Paul Scherrer Institute, Switzerland
#  All rights reserved.
#  Authors: Oliver Bruendler
##############################################################################

#######################################################################################################################
# Import Statements
#######################################################################################################################
from scipy import signal as sps
from .Cic import FreqResp as CicFreqResp
from SignalProcessing.General.Conversions import *

#######################################################################################################################
# Public Functions
#######################################################################################################################
def GainAtFreq(coefs, f, fs):
    """
    Calculate the FIR response at a given frequency
    :param coefs: FIR coefficients
    :param f: Frequency to calculate the gain at. Alternatively an array of frequencies can be passed.
    :param fs: Sampling frequency
    :return: Response at the given frequency
    """
    w = f/fs*2*np.pi
    res = 0
    idx = 0
    for x in coefs:
        res += x * np.e**(-idx * 1j * w)
        idx += 1
    return res

def CicComp(fc : float, fstop : float, fs_cicout : float,
            cic_order : int,
            fir_order : int, fir_ratio : int,
            cic_diffDel: int = 1, window: str = None, suppressionDb: float = 80.0, minPhase: bool = False) -> np.ndarray:
    """
    Design CIC compensation filter. The compensatio filter does additional decimation since this is the most common
    approach to build compound filters.

    :param fc: Cutoff frequency in Hz
    :param fstop: Start frequency of the stop-band in Hz
    :param fs_cicout: Sampling frequency at the CIC output in Hz
    :param cic_order: Order of the CIC filter
    :param fir_order: Order of the FIR filter
    :param fir_ratio: Decimation ratio of the FIR filter
    :param cic_diffDel: Differential delay of CIC filter (optional, default = 1)
    :param window: Window type as string (e.g. "flattop", "hamming", "blackman")
    :param suppressionDb: Stopband suppression in dB
    :param minPhase: True = Design a minimum phase FIR, False = design a linear phase FIR
    :return: FIR coefficients
    """
    #Derived parameters
    fsFirOut = fs_cicout/fir_ratio
    fsCicIn = fs_cicout #We assume a CIC ratio=1 since the CIC ratio does not have any impact on the results
    if window is None:
        window = "flattop"
    POINTS = 16384
    gainStop = 1/dB2Lin(suppressionDb)

    #Check parameters
    if fc >= fstop: raise ValueError("fc must be < fstop")
    if fstop >= fsFirOut/2: raise ValueError("fstop must be < FIR output sample rate / 2")

    #Calculate Parameters
    fCicCorr = np.linspace(0, fs_cicout/2, POINTS)
    cicResp = CicFreqResp(fCicCorr, fsCicIn, 1, cic_order, normalize=True, diffDelay=cic_diffDel)
    hCicCorr = 1/cicResp
    fFir = []
    hFir = []
    addedFstop = False
    for f, h in zip(fCicCorr, hCicCorr):
        if f < fc:
            fFir.append(f)
            hFir.append(h)
        elif f > fstop:
            fFir.append(f)
            hFir.append(gainStop)
        elif not addedFstop:
            fFir.append(fstop)
            hFir.append(gainStop)
            addedFstop = True
    fFirNorm = np.array(fFir) / (fs_cicout/2)
    firCoefs = sps.firwin2(fir_order+1, fFirNorm, hFir, window=window)
    #Correct DC gain has priority
    firCoefs = firCoefs / np.sum(firCoefs)
    #Convert to minimum phase if required
    if minPhase:
        return MinPhaseFromLinPhase(firCoefs)
    return firCoefs

def MinPhaseFromLinPhase(coefs : np.ndarray) -> np.ndarray:
    """
    Calculate minimum phase FIR filter from linear phase FIR filter coefficients
    :param coefs: Linear phase FIR filter coefficients
    :return: Minimum phase FIR filter coefficients
    """
    fftSize = len(coefs)*25
    maxphaseFilter = np.real(np.fft.ifft(np.exp(sps.hilbert(np.real(np.log(np.fft.fft(coefs + 1e-12, fftSize) + 1e-12)) + 1e-12))))
    minphaseFilter = maxphaseFilter[::-1]  # reverse
    return minphaseFilter[0:len(coefs)-1]