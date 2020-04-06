##############################################################################
#  Copyright (c) 2018 by Paul Scherrer Institute, Switzerland
#  All rights reserved.
#  Authors: Oliver Bruendler
##############################################################################

#######################################################################################################################
# Import Statements
#######################################################################################################################
import numpy as np
from matplotlib import pyplot as plt
from scipy import signal as sps
from matplotlib.ticker import EngFormatter
from SignalProcessing.General.Conversions import Lin2dB

#######################################################################################################################
# Public Functions
#######################################################################################################################
def Bode(b : np.ndarray, a : np.ndarray = [1], fs : float = 1.0, points : int = 1000, show : bool = True):
    """
    Plot Bode diagram for a given filter

    :param b: Numerator coefficients
    :param a: Denominator coefficients
    :param fs: Sampling frequency in Hz
    :param points: Number of points to plot
    :param show: True = show plot immediately, False = show() must be called externally
    """
    #Calculate
    w, h = sps.freqz(b, a, points)
    f = w/(2*np.pi)*fs
    amp = Lin2dB(np.abs(h))
    ang = np.unwrap(np.angle(h))/(2*np.pi)*360
    #Plot
    hzFormatter = EngFormatter(unit="Hz")
    fig, ax = plt.subplots(2)
    fig.suptitle("Bode Plot")
    ax[0].plot(f, amp)
    ax[0].set_ylabel("Gain [dB]")
    ax[0].set_xlabel("Frequency [Hz]")
    ax[0].xaxis.set_major_formatter(hzFormatter)
    ax[1].plot(f, ang)
    ax[1].set_ylabel("Angle [°]")
    ax[1].set_xlabel("Frequency [Hz]")
    ax[1].xaxis.set_major_formatter(hzFormatter)
    fig.subplots_adjust(hspace=0.5)
    if show:
        plt.show()

def ImpStepResp(b : np.ndarray, a : np.ndarray = [1], points : int = None, show : bool = True):
    """
    Plot impulse and step resonse of a filter

    :param b: Numerator coefficients
    :param a: Denominator coefficients
    :param points: Number of points to plot (optional, by default number of points is equal to number of b-coefficients)
    :param show: True = show plot immediately, False = show() must be called externally
    """
    #By default use the size of the numberator (as used for FIR filters)
    if points is None:
        points = len(b)
    #Calculate impulse response
    inpPulse = np.zeros(points)
    inpPulse[0] = 1.0
    outpPulse = sps.lfilter(b, a, inpPulse)
    outpStep = sps.lfilter(b, a, np.ones(points))
    #plot
    fig, ax = plt.subplots(2)
    ax[0].plot(outpPulse)
    ax[0].set_title("Impulse Response")
    ax[1].plot(outpStep)
    ax[1].set_title("Step Response")
    fig.subplots_adjust(hspace=0.5)
    if show:
        plt.show()



