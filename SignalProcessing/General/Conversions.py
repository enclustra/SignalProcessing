##############################################################################
#  Copyright (c) 2018 by Paul Scherrer Institute, Switzerland
#  All rights reserved.
#  Authors: Oliver Bruendler
##############################################################################

#######################################################################################################################
# Import Statements
#######################################################################################################################
from enum import Enum
import numpy as np

#######################################################################################################################
# Types
#######################################################################################################################
class DbConvType(Enum):
    """
    Type of Linear <-> dB conversion
    Amplitude: db=20*log10(x)
    Power: dB = 10*log10(x)
    """
    Amplitude = 0
    Power = 1

#######################################################################################################################
# Public Functions
#######################################################################################################################
def Lin2dB(lin, type : DbConvType = DbConvType.Amplitude):
    """
    Linear gain to dB conversion
    :param lin: Linear gain value (scalar or numpy array)
    :param type: Type of the conversion (amplitude or power9
    :return: dB value
    """
    return _DbConvFactor(type)*np.log10(lin)

def dB2Lin(dB, type : DbConvType = DbConvType.Amplitude):
    """
    dB to linear gain conversion
    :param dB: dB gain value (scalar or numpy array)
    :param type: Type of the conversion (amplitude or power9
    :return: linear gain value
    """
    return 10.0**(dB/_DbConvFactor(type))

#######################################################################################################################
# Private Functions
#######################################################################################################################
def _DbConvFactor(type : DbConvType) -> float:
    if type is DbConvType.Amplitude:
        return 20.0
    else:
        return 10.0