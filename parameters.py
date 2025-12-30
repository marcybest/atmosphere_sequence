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





# --> NEED TO BE ADAPTED : Path where the models grids are stored
model_path = './VHS1256b/MODELS_GRID/model_sonora_diamondback_cloudy.nc'

# The grid is open
ds = xr.open_dataset(model_path, decode_cf=False, engine='netcdf4')

# Extraction of the parameter space
teff_mod = ds['par1'].values
logg_mod = ds['par2'].values
mh_mod = ds['par3'].values

print(teff_mod)
print(logg_mod)
print(mh_mod)

colors = ['tab:red','tab:blue']

j=0
for i in [0,4]:#[0,int(len(teff_mod)/2),int(len(teff_mod))-1]:
    flx_mod = np.asarray(ds['grid'].sel(par1=teff_mod[3], par2=logg_mod[i], par3=mh_mod[-1]))

    # Normalization of the model flux to the data flux
    ck_top = np.sum((flx_mod * flx_obs) / (err_obs * err_obs))
    ck_bot = np.sum((flx_mod / err_obs)**2)
    ck = ck_top / ck_bot
    flx_mod *= ck
    plt.plot(wav_obs, flx_mod, c=colors[j], zorder=3,label='log(g)='+str(logg_mod[i]))
    j+=1


plt.yscale('log')
plt.legend()

plt.show()
