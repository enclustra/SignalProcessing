# General Information

## Maintainer
Radoslaw Rybaniec [radoslaw.rybaniec@psi.ch]

## Authors
Oliver Bründler [oli.bruendler@gmx.ch]

## License
This library is published under [PSI HDL Library License](License.txt), which is [LGPL](LGPL2_1.txt) plus some additional exceptions to clarify the LGPL terms in the context of firmware development.

## Changelog
See [Changelog](Changelog.md)

## What belongs into this Library
Any python functions for signal processing that are commonly used and non-project-specifc but not directly available from the scipy package. This can include calculations, plots, etc. Do not include functionality that is project specific or already available from the scipy package.

Examples for things that belong into this library:
* CIC frequency response calculation
* CIC compensation filter coefficient calculation

Examples for things that do not belong into this library:
* Calculation of filter parameters to suppress a project-specific set of frequencies (project-specific)
* Calculate an FIR filter with a given cutoff frequency (available from scipy.signal)

# Installation
to install, use the command below

```
pip install <root>\dist\SignalProcessing-<version>.tar.gz
``` 

# Packaing
To package the project after making changes, update the version number in *setup.py* and run

```
python3 setup.py sdist
```




 
