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

label_str = "SH_LH"
### WRF calculate diurnal cycle at ARM SGP site 
HFX_regrid = ds_WRF['HFX_regrid']
LH_regrid = ds_WRF['LH_regrid']

HFX_May = HFX_regrid[:738,:,:]
HFX_JJA = HFX_regrid[738:,:,:]
LH_May = LH_regrid[:738,:,:]
LH_JJA = LH_regrid[738:,:,:]

HFX_WRF_May = HFX_May.groupby('time.hour').mean()
HFX_WRF_JJA = HFX_JJA.groupby('time.hour').mean()
LH_WRF_May = LH_May.groupby('time.hour').mean()
LH_WRF_JJA = LH_JJA.groupby('time.hour').mean()

WRF_May_SH = HFX_WRF_May.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
WRF_JJA_SH = HFX_WRF_JJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
WRF_May_LH = LH_WRF_May.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
WRF_JJA_LH = LH_WRF_JJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')

### ARM SGP obs: ARMBE2DGRID from Qi Tang

SH05 = -ds_ARMBE2D_05['sensible_heat_flux'] # make it positive when going upward
SH06 = -ds_ARMBE2D_06['sensible_heat_flux']
SH07 = -ds_ARMBE2D_07['sensible_heat_flux']
SH08 = -ds_ARMBE2D_08['sensible_heat_flux']

LH05 = -ds_ARMBE2D_05['latent_heat_flux'] # make it positive when going upward
LH06 = -ds_ARMBE2D_06['latent_heat_flux']
LH07 = -ds_ARMBE2D_07['latent_heat_flux']
LH08 = -ds_ARMBE2D_08['latent_heat_flux']

SH_0678 = xr.concat([SH06, SH07, SH08], dim='time')
LH_0678 = xr.concat([LH06, LH07, LH08], dim='time')

SH_May = SH05.groupby('time.hour').mean()
SH_JJA = SH_0678.groupby('time.hour').mean()
LH_May = LH05.groupby('time.hour').mean()
LH_JJA = LH_0678.groupby('time.hour').mean()

ARM_May_SH = SH_May.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
ARM_JJA_SH = SH_JJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
ARM_May_LH = LH_May.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
ARM_JJA_LH = LH_JJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')

### WRF bias in May, and JJA ###
bias_May_SH = WRF_May_SH - ARM_May_SH
bias_JJA_SH = WRF_JJA_SH - ARM_JJA_SH
bias_May_LH = WRF_May_LH - ARM_May_LH
bias_JJA_LH = WRF_JJA_LH - ARM_JJA_LH

### Plot ###
x_axis = WRF_May_SH.coords['hour']

fig = plt.figure()
fontsize = 7
pos_adjust1 = 0.04

ax1 = fig.add_subplot(2,1,1)
#ax1.text(s='SensibleHeatFlux bias, WRF-ARMBE2D', x=0, y=1.02, ha='left', va='bottom', \
#        fontsize=fontsize, transform=ax1.transAxes)
ax1.plot(x_axis, bias_May_SH.values, 'r-', label='SH,May')
ax1.plot(x_axis, bias_JJA_SH.values, 'r--', label='SH,JJA')
ax1.plot(x_axis, bias_May_LH.values, 'b-', label='LH,May')
ax1.plot(x_axis, bias_JJA_LH.values, 'b--', label='LH,JJA')
ax1.set_yticks(np.arange(-200.0,201.0,50.0))
ax1.set_xticks(np.arange(0.0,24.1,3.0))
ax1.set(xlabel='UTC(hr)', ylabel='WRF bias, W/m2', title='Sensible/Latent heat flux, WRF vs ARM SGP')
ax1.grid()
#ax1.legend(loc='lower right')

ax2 = fig.add_subplot(2,1,2)
#ax2.text(s='SensibleHeatFlux,SGP,ARMBE2D', x=0, y=1.02, ha='left', va='bottom', \
#        fontsize=fontsize, transform=ax2.transAxes)
ax2.plot(x_axis, ARM_May_SH.values,'r-', label='SH,May')
ax2.plot(x_axis, ARM_JJA_SH.values, 'r--',  label='SH,JJA')
ax2.plot(x_axis, ARM_May_LH.values,'b-', label='LH,May')
ax2.plot(x_axis, ARM_JJA_LH.values, 'b--',  label='LH,JJA')
ax2.set_yticks(np.arange(-100.0,501.0,100.0))
ax2.set_xticks(np.arange(0.0,24.1,3.0))
ax2.set(xlabel='UTC(hr)', ylabel='SGP obs, W/m2')
ax2.grid()
ax2.legend(loc='upper left')

fig.savefig("../Figure/"+label_str+".WRF_vs_ARM_SGP.png",dpi=600)
plt.show()







