##############################################################################
#  Copyright (c) 2020 by Oliver Bründler, Switzerland
#  All rights reserved.
#  Authors: Oliver Bruendler
##############################################################################

#######################################################################################################################
# Import Statements
#######################################################################################################################
import numpy as np
from matplotlib import pyplot as plt
from scipy import signal as sps

#######################################################################################################################
# Public Functions
#######################################################################################################################
def CalcSpectrum(sig : np.ndarray, fs : float, win : callable):
    """
    Calculate power spectrum
    :param sig: Signal
    :param fs: Sample frequency
    :param win: Window to apply
    :return: Tuple (frequencies, power in dB)
    """
    win = win(sig.size, sym=False)
    inWin = sig * win
    linSpecIn = np.abs(np.fft.fft(inWin)) / (sig.size * np.average(win))
    logSpecIn = 20 * np.log10(linSpecIn)
    freqs = np.fft.fftfreq(sig.size, 1 / fs)
    idx = np.argsort(freqs)
    return freqs[idx], logSpecIn[idx]

def PlotSpectrumToAx(sig : np.ndarray, fs : float, win : callable, ax : plt.Axes, title : str = None):
    """
    Plot a spectrum into an axes object
    :param sig: Signal
    :param fs: Sample frequency
    :param win: Window to apply
    :param ax: Axes object to plot into
    :param title: Plot title (optional)
    :return:
    """
    if title is not None:
        ax.set_title(title)
    f, a = CalcSpectrum(sig, fs, win)
    ax.plot(f, a)
    ax.set_xlabel("Frequency")
    ax.set_ylabel("Gain [dB]")

def PlotSpectrum(sig : np.ndarray, fs : float, win : callable = None, title : str = None, show : bool = True):
    """
    Create a spectrum plot
    :param sig: Signal to plot the spectrum for
    :param fs: Sampling frequency
    :param win: Window to apply
    :param title: Plot title
    :param show: True = show plot immediately, False = show() must be called externally
    """
    winToUse = win
    if winToUse is None:
        winToUse = sps.windows.blackman
    fig, ax = plt.subplots(1,1)
    PlotSpectrumToAx(sig, fs, winToUse, ax, title)
    if show:
        plt.show()