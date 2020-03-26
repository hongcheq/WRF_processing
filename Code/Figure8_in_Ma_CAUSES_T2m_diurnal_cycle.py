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
T2_regrid = ds_WRF['T2_regrid']

T2_May = T2_regrid[:738,:,:]
T2_JJA = T2_regrid[738:,:,:]

T2_WRF_May = T2_May.groupby('time.hour').mean()
T2_WRF_JJA = T2_JJA.groupby('time.hour').mean()

WRF_May = T2_WRF_May.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
WRF_JJA = T2_WRF_JJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')

### ARM SGP obs: ARMBE2DGRID from Qi Tang

temp05 = ds_ARMBE2D_05['temp']
temp06 = ds_ARMBE2D_06['temp']
temp07 = ds_ARMBE2D_07['temp']
temp08 = ds_ARMBE2D_08['temp']

temp_0678 = xr.concat([temp06, temp07, temp08], dim='time')

temp_May = temp05.groupby('time.hour').mean()
temp_JJA = temp_0678.groupby('time.hour').mean()

ARM_May = temp_May.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
ARM_JJA = temp_JJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')

### WRF bias in May, and JJA ###
bias_May = WRF_May - ARM_May
bias_JJA = WRF_JJA - ARM_JJA
#print(bias_May)
#print(bias_JJA)

### Plot ###
x_axis = WRF_May.coords['hour']

fig = plt.figure()
fontsize = 7
pos_adjust1 = 0.04

ax1 = fig.add_subplot(2,1,1)
ax1.text(s='T2m bias, WRF-ARMBE2D', x=0, y=1.02, ha='left', va='bottom', \
        fontsize=fontsize, transform=ax1.transAxes)
ax1.plot(x_axis, bias_May.values, 'r-', label='T2m,May')
ax1.plot(x_axis, bias_JJA.values, 'r--', label='T2m,JJA')
ax1.set_yticks(np.arange(0.0,4.6,0.5))
ax1.set_xticks(np.arange(0.0,24.1,3.0))
ax1.set(xlabel='UTC(hr)', ylabel='WRF T2m bias, K', title='T2m, WRF vs ARM SGP')
ax1.grid()
ax1.legend(loc='lower right')

ax2 = fig.add_subplot(2,1,2)
ax2.text(s='T2m,SGP,ARMBE2D', x=0, y=1.02, ha='left', va='bottom', \
        fontsize=fontsize, transform=ax2.transAxes)
ax2.plot(x_axis, ARM_May.values, 'k-', label='T2m,May')
ax2.plot(x_axis, ARM_JJA.values, 'k--', label='T2m,JJA')
ax2.set_yticks(np.arange(285.0,311.0,3.0))
ax2.set_xticks(np.arange(0.0,24.1,3.0))
ax2.set(xlabel='UTC(hr)', ylabel='T2m SGP obs, K')
ax2.grid()
ax2.legend(loc='lower right')

fig.savefig("../Figure/T2m.WRF_vs_ARM_SGP.png",dpi=600)
plt.show()








