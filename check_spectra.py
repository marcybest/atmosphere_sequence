#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 14:10:23 2025

@author: simonpetrus

A black body law is considered to fit VHS 1256 b spectrum.
The data have been observed at medium resolution (R~8000) with VLT/X-Shooter
More details about the data and the objects are given in Petrus et al. 2025, Petrus et al. 2024, Miles et al. 2023

"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


# Definition of the black body law
# Physical constants
h = 6.62607015e-34   # Planck constant (J.s)
c = 2.99792458e8     # Speed of light (m/s)
k = 1.380649e-23     # Boltzmann constant (J/K)

# -------------------------------------

# --> NEED TO BE ADAPTED : Path where the data are stored
data_path = './VHS1256b/DATA/VHS1256b_spectrum.npz'

open_npz = np.load(data_path)
wav = open_npz['wav']
flx = open_npz['flx']
err = open_npz['err']

# Plot of the data
for plot_range in [[1.00, 1.35], [1.4, 1.8], [1.95, 2.5]]:
    ind_plot = np.where((wav >= plot_range[0]) & (wav <= plot_range[1]))
    plt.errorbar(wav[ind_plot], flx[ind_plot], yerr=err[ind_plot],c='tab:red',alpha= 0.5, zorder=1)
    plt.plot(wav[ind_plot], flx[ind_plot], c='tab:red', zorder=2)



# --> NEED TO BE ADAPTED : Path where the data are stored
data_path = './PSO318/PSO318.npz'

open_npz = np.load(data_path)

wav = open_npz['wl']
flx = open_npz['flx']
err = open_npz['err']

# Plot of the data
for plot_range in [[1.00, 1.35], [1.4, 1.8], [1.95, 2.5]]:
    ind_plot = np.where((wav >= plot_range[0]) & (wav <= plot_range[1]))
    plt.errorbar(wav[ind_plot], flx[ind_plot], yerr=err[ind_plot], c='tab:blue',alpha= 0.5, zorder=1)
    plt.plot(wav[ind_plot], flx[ind_plot], c='tab:blue', zorder=2)

# Definition of the axis labels
plt.xlabel(r'Wavelength ($\rm \mu$m)')
plt.ylabel(r'Flux (W.m$\rm ^{-2}.\mu m^{-1}$)')
# Definition of the legend
plt.errorbar([], [], yerr=[], c='0.7', zorder=1, label='Errors')
plt.plot([], [], c='tab:red', zorder=2, label='VHS 1256 b')
plt.plot([], [], c='tab:blue', zorder=3, label='PSO 318')
plt.legend()
#plt.yscale('log')
#plt.xlim(1.2,1.3)
plt.show()







#
