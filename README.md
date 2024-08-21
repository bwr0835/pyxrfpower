# PyXRFPower

PyXRFPower is a graphical user interface (GUI) designed to allow one to quickly estimate element-dependent spatial resolutions of scanning fluorescence X-ray microscopy (SFXM) images acquired at synchrotron light source beamlines via power spectral density (PSD) analysis [1].

# GUI Features

- Elemental image and 2D PSD visualization
- Tunable number of radial frequency bins
- Tunable signal-to-noise ratio (SNR) cutoffs
- Isotropic and anisotropic (i.e. $x$ and $y$) spatial resolutions $\delta_{\mathrm{res}}$ and $\delta_{\mathrm{res},x}$ and $\delta_{\mathrm{res},y}$, respectively
- A plot window capable of displaying azimuthally averaged PSD profiles for up to **ten** different elements simultaneously

# OS and File Requirements

Mac, Linux, and Windows systems are all supported.

Currently, HDF5 and Matlab files are supported; <ins>**however**</ins>, because synchrotron light sources can have different file structures, if the synchrotron of interest is not available, please contact <benjaminroter2026@u.northwestern.edu>.

# Introduction

The 2D PSD for a particular element can be found via

```math
\text{2D PSD} \equiv S\left(u_{x}, u_{y}\right) = \mathcal{F}\left\{\sqrt{I\left(x, y\right)}\right\}^{*}\mathcal{F}\left\{\sqrt{I\left(x, y\right)}\right\} = \left|\mathcal{F}\left\{\sqrt{I\left(x, y\right)}\right\}\right|^{2}.
```
- $u_{x}, u_{y} \equiv x$, $y$ spatial frequencies extending out to $1/\left(2\Delta_{x}\right)$, $1/\left(2\Delta_{y}\right)$
  - $\Delta_{x}$, $\Delta_{y} \equiv x$, $y$ pixel sizes
- $I \equiv$ fluorescence intensity

2D PSDs can be averaged over an arbitrary number of circles to produce azimuthally averaged PSDs $S\left(u_{r}\right).$
 - $u_{r} \equiv$ radial spatial frequency

Spatial resolution can be estimated by fitting power law signal decays and noise floors relative to the frequency $u_{\mathrm{res}}$ at which the signal and noise meet ("knee frequency" $u_{\mathrm{knee}}$); however, because there is approximately equal mixing of signal and noise at $u_{r}$, finding $u_{\mathrm{res}}$ corresponding to an SNR greater than one, i.e. corresponding to a multiplicative factor greater than one, is will dilute the contributions to resolution from noise.

Half-pitch/half-period spatial resolution $\delta_{\mathrm{res}}$ for an isotropic beam can be estimated as

```math
\delta_{\mathrm{res}} = \frac{1}{2u_{\mathrm{res}}}.
```

For an anisotropic beam, $u_{\mathrm{res}} \rightarrow u_{\mathrm{res},x}, u_{\mathrm{res},y} \therefore \delta_{\mathrm{res}} \rightarrow \delta_{\mathrm{res},x}, \delta_{\mathrm{res},y}$.

More details about this analysis can be found in a manuscript currently being drafted.

# Installation

1. Install [Anaconda](http://continuum.io/downloads)
2. Clone this repository
3. Create an appropriate `conda` environment in a command line and activate it:

```
$ cd <path to PyXRFPower directory>
$ conda env create -f base_env.yml --name pyxrfpower
$ conda activate pyxrfpower
```

4. Invoke PyXRFPower:

```
$ python pyxrfpower_launcher.py
```

# References

[1] J. Deng, D. J. Vine, S. Chen, Q. Jin., Y. S. G. Nashed, T. Peterka, S. Vogt, and C. Jacobsen, Sci. Rep. **7**, 445 (2017).
