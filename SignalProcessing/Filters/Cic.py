##############################################################################
#  Copyright (c) 2018 by Paul Scherrer Institute, Switzerland
#  All rights reserved.
#  Authors: Oliver Bruendler
##############################################################################

#######################################################################################################################
# Import Statements
#######################################################################################################################
import numpy as np

#######################################################################################################################
# Public Functions
#######################################################################################################################
def Gain(ratio : int, order : int, diff_delay : int = 1) -> int:
    """
    Calculate CIC Gain (for differential delay = 1)

    :param ratio: CIC decimation ratio
    :param order: CIC order
    :param diff_delay: Differential delay (optional, default = 1)
    :return: CIC gain (linear)
    """
    return (ratio*diff_delay)**order

def FreqResp(f : np.ndarray, fs : float, ratio : int, order : int, normalize : bool = False, diffDelay = 1) -> np.ndarray:
    """
    Calculate the frequency response of a CIC filter (for differential delay = 1)

    :param f: Frequency (in Hz)
    :param fs: Input Sampling Frequency (in Hz)
    :param ratio: CIC decimation ratio
    :param order: CIC order
    :param normalize: True = Normalize gain to 1, do not normalize gain
    :param diffDelay: Differential delay taps (optional, default = 1)
    :return: Gain at frequencies f
    """
    g = Gain(ratio, order, diff_delay=diffDelay)
    f = f/fs*ratio
    respUncomp =  abs((np.sin(f * diffDelay * 1.0 * np.pi)+1e-16) / (np.sin(f * np.pi / ratio)+1e-16)) ** order
    respUncomp[f==0] = g
    if normalize:
        return respUncomp / g
    else:
        return respUncomp