# PyXRFPower

PyXRFPower is a graphical user interface (GUI) designed to allow one to quickly estimate element-dependent spatial resolutions of scanning fluorescence X-ray microscopy (SFXM) images acquired at synchrotron light source beamlines via power spectral density (PSD) analysis [1].

# Introduction

2D PSD $\left(u_{x}, u_{y}\right)$ can be found via

```math
S\left(u_{x}, u_{y}\right) = \mathcal{F}\left\{\sqrt{I}\right\}^{*}\mathcal{F}\left\{\sqrt{I}\right\},
```

where 

- $u_{x}, u_{y} \equiv x$, $y$ spatial frequencies
- $I \equiv$ intensity

# Features

- Elemental image visualization
- Tunable number of radial frequency bins
- Tunable signal-to-noise ratio (SNR) cutoffs
- Isotropic and anisotropic (i.e. $x$ and $y$) spatial resolutions
- A plot window capable of displaying azimuthally averaged PSD profiles for up to **ten** different elements simultaneously

# OS Requirements

Mac, Linux, and Windows systems are all supported.

# Installation

1. Install [Anaconda](http://continuum.io/downloads)
2. Clone this repository
3. Create an appropriate `conda` environment in a command line and activate it:

```
$ cd <path to PyXRFPower directory>
$ conda env create -f base_env.yml --name <anything other than ones containing base, env, or base_env>
$ conda activate <renamed virtual environment>
```

4. Invoke PyXRFPower:

```
$ python xrfpower_launcher
```
