#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 15:31:03 2025

@author: simonpetrus
"""
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt


# --> NEED TO BE ADAPTED : Path where the data are stored
data_path = './VHS1256b/DATA/VHS1256b_spectrum.npz'

open_npz = np.load(data_path)
wav_obs = open_npz['wav']
flx_obs = open_npz['flx']
err_obs = open_npz['err']

# Plot of the data
for plot_range in [[1.00, 1.35], [1.4, 1.8], [1.95, 2.5]]:
    ind_plot = np.where((wav_obs >= plot_range[0]) & (wav_obs <= plot_range[1]))
    plt.errorbar(wav_obs[ind_plot], flx_obs[ind_plot], yerr=err_obs[ind_plot], c='0.7', zorder=1)
    plt.plot(wav_obs[ind_plot], flx_obs[ind_plot], c='k', zorder=2)


for config in ['cloudy', 'cloudless']:

    # --> NEED TO BE ADAPTED : Path where the models grids are stored
    model_path = './VHS1256b/MODELS_GRID/model_sonora_diamondback_'+config+'.nc'

    # The grid is open
    ds = xr.open_dataset(model_path, decode_cf=False, engine='netcdf4')

    # Extraction of the parameter space
    teff_mod = ds['par1'].values
    logg_mod = ds['par2'].values
    mh_mod = ds['par3'].values

    # Extraction of the model spectrum for each set of parameters

    print(teff_mod)

    chi2_test = 1e100
    for p1_i, p1 in enumerate(teff_mod):
        for p2_i, p2 in enumerate(logg_mod):
            for p3_i, p3 in enumerate(mh_mod):
                # Extraction of the flux from the grid
                flx_mod = np.asarray(ds['grid'].sel(par1=p1, par2=p2, par3=p3))
                # Normalization of the model flux to the data flux
                ck_top = np.sum((flx_mod * flx_obs) / (err_obs * err_obs))
                ck_bot = np.sum((flx_mod / err_obs)**2)
                ck = ck_top / ck_bot
                flx_mod *= ck

                # Calculation of the chi2
                chi2 = np.sum((flx_mod-flx_obs)**2 / err_obs**2)

                # If the calculated chi2 is lower than the previous one we keep the parameters set
                if chi2 < chi2_test:
                    chi2_test = chi2
                    flx_test = flx_mod
                    teff = p1
                    logg = p2
                    mh = p3

    print()
    print('For the '+config+' configuration:')
    print('   Teff = ' + str(teff))
    print('   log(g) = ' + str(logg))
    print('   [M/H] = ' + str(mh))


    # Plot of the best model
    if config == 'cloudy':
        plt.plot(wav_obs, flx_test, c='forestgreen', zorder=3)
    elif config == 'cloudless':
        plt.plot(wav_obs, flx_test, c='dodgerblue', zorder=3)


# Definition of the axis labels
plt.xlabel(r'Wavelength ($\rm \mu$m)')
plt.ylabel(r'Flux (W.m$\rm ^{-2}.\mu m^{-1}$)')
# Definition of the legend
plt.plot([], [], c='k', zorder=2, label='Obs. data')
plt.errorbar([], [], yerr=[], c='0.7', zorder=1, label='Errors')
plt.plot([], [], c='forestgreen', zorder=3, label='Best cloudy model')
plt.plot([], [], c='dodgerblue', zorder=3, label='Best cloudless model')
plt.legend()
plt.show()














#
