'''
Function: analysis for WRF 2011 May-Aug outputs, as in Ma CAUSES paper Figure 8.
Date: 20200325
'''

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import pandas

ds_WRF = xr.open_dataset('/home/qin5/Data/WRF.postprocessing.extract.hourly.nc')

ds_ARMBE2D_05 = xr.open_dataset('/home/qin5/Data/ARMBE2DGRID/sgparmbe2dgridX1.c1.20110501.000000.nc')
ds_ARMBE2D_06 = xr.open_dataset('/home/qin5/Data/ARMBE2DGRID/sgparmbe2dgridX1.c1.20110601.000000.nc')
ds_ARMBE2D_07 = xr.open_dataset('/home/qin5/Data/ARMBE2DGRID/sgparmbe2dgridX1.c1.20110701.000000.nc')
ds_ARMBE2D_08 = xr.open_dataset('/home/qin5/Data/ARMBE2DGRID/sgparmbe2dgridX1.c1.20110801.000000.nc')

## Figure 8 in Ma et al 2018, average over 35-38N, 99-96W, consistent with ARMBE2D from Qi Tang
lat_1 = 35.0
lat_2 = 38.0
lon_1 = -99.0
lon_2 = -96.0

### WRF calculate diurnal cycle at ARM SGP site 
LH_regrid = ds_WRF['LH_regrid']
HFX_regrid = ds_WRF['HFX_regrid']

LH_WRF_month = LH_regrid.resample(time='MS').mean(dim='time')
LH_WRF_May = LH_WRF_month[0,:,:]
LH_WRF_Jun = LH_WRF_month[1,:,:]
LH_WRF_Jul = LH_WRF_month[2,:,:]
LH_WRF_Aug = LH_WRF_month[3,:,:]
LH_WRF_JJA = (LH_WRF_Jun + LH_WRF_Jul + LH_WRF_Aug)/3.0
LH_WRF_MJJA = (LH_WRF_May + LH_WRF_Jun + LH_WRF_Jul + LH_WRF_Aug)/4.0

HFX_WRF_month = HFX_regrid.resample(time='MS').mean(dim='time')
HFX_WRF_May = HFX_WRF_month[0,:,:]
HFX_WRF_Jun = HFX_WRF_month[1,:,:]
HFX_WRF_Jul = HFX_WRF_month[2,:,:]
HFX_WRF_Aug = HFX_WRF_month[3,:,:]
HFX_WRF_JJA = (HFX_WRF_Jun + HFX_WRF_Jul + HFX_WRF_Aug)/3.0
HFX_WRF_MJJA = (HFX_WRF_May + HFX_WRF_Jun + HFX_WRF_Jul + HFX_WRF_Aug)/4.0

L_WRF_May = LH_WRF_May.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
L_WRF_Jun = LH_WRF_Jun.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
L_WRF_Jul = LH_WRF_Jul.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
L_WRF_Aug = LH_WRF_Aug.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
L_WRF_JJA = LH_WRF_JJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
L_WRF_MJJA = LH_WRF_MJJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')

SH_WRF_May = HFX_WRF_May.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
SH_WRF_Jun = HFX_WRF_Jun.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
SH_WRF_Jul = HFX_WRF_Jul.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
SH_WRF_Aug = HFX_WRF_Aug.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
SH_WRF_JJA = HFX_WRF_JJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
SH_WRF_MJJA = HFX_WRF_MJJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')

### ARM SGP obs: ARMBE2DGRID from Qi Tang

latent05 = -ds_ARMBE2D_05['latent_heat_flux'] # make it positive going upward
latent06 = -ds_ARMBE2D_06['latent_heat_flux']
latent07 = -ds_ARMBE2D_07['latent_heat_flux']
latent08 = -ds_ARMBE2D_08['latent_heat_flux']

sensible05 = -ds_ARMBE2D_05['sensible_heat_flux'] # make it positive going upward
sensible06 = -ds_ARMBE2D_06['sensible_heat_flux']
sensible07 = -ds_ARMBE2D_07['sensible_heat_flux']
sensible08 = -ds_ARMBE2D_08['sensible_heat_flux']

latent_05678 = xr.concat([latent05, latent06, latent07, latent08], dim='time')
latent_05678 = latent_05678.resample(time='MS').mean(dim='time')
latent_May = latent_05678[0,:,:]
latent_Jun = latent_05678[1,:,:]
latent_Jul = latent_05678[2,:,:]
latent_Aug = latent_05678[3,:,:]
latent_JJA = (latent_Jun + latent_Jul + latent_Aug)/3.0
latent_MJJA = (latent_May + latent_Jun + latent_Jul + latent_Aug)/4.0

sensible_05678 = xr.concat([sensible05, sensible06, sensible07, sensible08], dim='time')
sensible_05678 = sensible_05678.resample(time='MS').mean(dim='time')
sensible_May = sensible_05678[0,:,:]
sensible_Jun = sensible_05678[1,:,:]
sensible_Jul = sensible_05678[2,:,:]
sensible_Aug = sensible_05678[3,:,:]
sensible_JJA = (sensible_Jun + sensible_Jul + sensible_Aug)/3.0
sensible_MJJA = (sensible_May + sensible_Jun + sensible_Jul + sensible_Aug)/4.0

L_ARM_May = latent_May.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
L_ARM_Jun = latent_Jun.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
L_ARM_Jul = latent_Jul.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
L_ARM_Aug = latent_Aug.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
L_ARM_JJA = latent_JJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
L_ARM_MJJA = latent_MJJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')

SH_ARM_May = sensible_May.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
SH_ARM_Jun = sensible_Jun.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
SH_ARM_Jul = sensible_Jul.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
SH_ARM_Aug = sensible_Aug.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
SH_ARM_JJA = sensible_JJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
SH_ARM_MJJA = sensible_MJJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')

### Plot ###
x_axis = ['May','Jun','Jul','Aug','JJA','MJJA']

fig = plt.figure()
fontsize = 7
pos_adjust1 = 0.04

ax1 = fig.add_subplot(2,1,1)
ax1.text(s='Latent Heat Flux, W/m2', x=0, y=1.02, ha='left', va='bottom', \
        fontsize=fontsize, transform=ax1.transAxes)
ax1.scatter(x_axis, [L_WRF_May, L_WRF_Jun, L_WRF_Jul, L_WRF_Aug, L_WRF_JJA, L_WRF_MJJA], c='k',marker='s', label='WRF')
ax1.scatter(x_axis, [L_ARM_May, L_ARM_Jun, L_ARM_Jul, L_ARM_Aug, L_ARM_JJA, L_ARM_MJJA], c='r', marker='d', label='ARM obs')
#ax1.set_yticks(np.arange(0.0,4.6,0.5))
#ax1.set_xticks(np.arange(0.0,24.1,3.0))
ax1.set(xlabel='month category', ylabel='Latent heat flux, W/m2', title='WRF vs ARM SGP')
ax1.grid()
ax1.legend(loc='lower right')

ax2 = fig.add_subplot(2,1,2)
ax2.text(s='Sensible Heat Flux, W/m2', x=0, y=1.02, ha='left', va='bottom', \
        fontsize=fontsize, transform=ax2.transAxes)
ax2.scatter(x_axis, [SH_WRF_May, SH_WRF_Jun, SH_WRF_Jul, SH_WRF_Aug, SH_WRF_JJA, SH_WRF_MJJA], c='k',marker='s', label='WRF')
ax2.scatter(x_axis, [SH_ARM_May, SH_ARM_Jun, SH_ARM_Jul, SH_ARM_Aug, SH_ARM_JJA, SH_ARM_MJJA], c='r', marker='d', label='ARM obs')
ax2.set(xlabel='month category', ylabel='Sensible heat flux, W/m2')
ax2.grid()
ax2.legend(loc='lower right')


fig.savefig("../Figure/Figure7.SH.LH,WRF_vs_ARM_SGP.png",dpi=600)
plt.show()








