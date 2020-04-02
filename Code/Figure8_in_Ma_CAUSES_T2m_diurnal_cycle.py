'''
Function: analysis for WRF 2011 May-Aug outputs, as in Ma CAUSES paper Figure 8.
Date: 20200325
'''

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import pandas

ds_WRF = xr.open_dataset('/home/qin5/Data/WRF.postprocessing.extract.hourly.nc')


ds_ARMBE2D_01 = xr.open_dataset('/home/qin5/Data/ARMBE2DGRID/sgparmbe2dgridX1.c1.20110101.000000.nc')
ds_ARMBE2D_02 = xr.open_dataset('/home/qin5/Data/ARMBE2DGRID/sgparmbe2dgridX1.c1.20110201.000000.nc')
ds_ARMBE2D_03 = xr.open_dataset('/home/qin5/Data/ARMBE2DGRID/sgparmbe2dgridX1.c1.20110301.000000.nc')
ds_ARMBE2D_04 = xr.open_dataset('/home/qin5/Data/ARMBE2DGRID/sgparmbe2dgridX1.c1.20110401.000000.nc')

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

T2_WRF_May = T2_May.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
T2_WRF_JJA = T2_JJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')

WRF_May = T2_WRF_May.groupby('time.hour').mean()
WRF_JJA = T2_WRF_JJA.groupby('time.hour').mean()

### ARM SGP obs: ARMBE2DGRID from Qi Tang

temp01 = ds_ARMBE2D_01['temp']
temp02 = ds_ARMBE2D_02['temp']
temp03 = ds_ARMBE2D_03['temp']
temp04 = ds_ARMBE2D_04['temp']

#temp05 = ds_ARMBE2D_05['temp']
temp05 = ds_ARMBE2D_05['temp'][48:,:,:]  # remove the first 48 hours, debug testing, the first 48-hours erroneous?
temp06 = ds_ARMBE2D_06['temp']
temp07 = ds_ARMBE2D_07['temp']
temp08 = ds_ARMBE2D_08['temp']

temp_0678 = xr.concat([temp06, temp07, temp08], dim='time')

temp_Jan = temp01.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
temp_Feb = temp02.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
temp_Mar = temp03.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
temp_Apr = temp04.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')

temp_May = temp05.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
temp_Jun = temp06.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
temp_Jul = temp07.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
temp_Aug = temp08.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')

temp_JJA = temp_0678.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')

ARM_Jan = temp_Jan.groupby('time.hour').mean()
ARM_Feb = temp_Feb.groupby('time.hour').mean()
ARM_Mar = temp_Mar.groupby('time.hour').mean()
ARM_Apr = temp_Apr.groupby('time.hour').mean()

ARM_May = temp_May.groupby('time.hour').mean()
ARM_Jun = temp_Jun.groupby('time.hour').mean()
ARM_Jul = temp_Jul.groupby('time.hour').mean()
ARM_Aug = temp_Aug.groupby('time.hour').mean()

ARM_JJA = temp_JJA.groupby('time.hour').mean()

### WRF bias in May, and JJA ###
bias_May = WRF_May - ARM_May
bias_JJA = WRF_JJA - ARM_JJA
#print(bias_May)
#print(bias_JJA)

### Plot ###
x_axis = WRF_May.coords['hour']

fig = plt.figure(figsize=(8,9))
fontsize = 7
pos_adjust1 = 0.04

ax1 = fig.add_subplot(3,1,1)
ax1.text(s='T2m bias, WRF-ARMBE2D', x=0, y=1.02, ha='left', va='bottom', \
        fontsize=fontsize, transform=ax1.transAxes)
ax1.plot(x_axis, bias_May.values, 'r-', label='T2m,May')
ax1.plot(x_axis, bias_JJA.values, 'r--', label='T2m,JJA')
ax1.set_yticks(np.arange(0.0,4.6,0.5))
ax1.set_xticks(np.arange(0.0,24.1,3.0))
ax1.set(xlabel='UTC(hr)', ylabel='WRF T2m bias, K', title='T2m, WRF vs ARM SGP')
ax1.grid()
ax1.legend(loc='lower right')

ax2 = fig.add_subplot(3,1,2)
ax2.text(s='T2m,SGP,ARMBE2D', x=0, y=1.02, ha='left', va='bottom', \
        fontsize=fontsize, transform=ax2.transAxes)
### debug
ax2.plot(x_axis, ARM_Jan.values, 'b-', label='T2m,Jan')
ax2.plot(x_axis, ARM_Feb.values, 'g-', label='T2m,Feb')
ax2.plot(x_axis, ARM_Mar.values, 'r-', label='T2m,Mar')
ax2.plot(x_axis, ARM_Apr.values, 'c-', label='T2m,Apr')
ax2.plot(x_axis, ARM_May.values, 'm-', label='T2m,May')
ax2.plot(x_axis, ARM_Jun.values, 'y-', label='T2m,Jun')
ax2.plot(x_axis, ARM_Jul.values, 'k-', label='T2m,Jul')
ax2.plot(x_axis, ARM_Aug.values, 'k--', label='T2m,Aug')

ax2.plot(x_axis, ARM_JJA.values, 'k+', label='T2m,JJA')

#ax2.set_yticks(np.arange(285.0,311.0,3.0))
#ax2.set_xticks(np.arange(0.0,24.1,3.0))
ax2.set_xticks(np.arange(0.0,27.1,3.0))
ax2.set(xlabel='UTC(hr)', ylabel='T2m SGP obs, K')
ax2.grid()
ax2.legend(loc='lower right')

ax3 = fig.add_subplot(3,1,3)
ax3.text(s='T2m, WRF', x=0, y=1.02, ha='left', va='bottom', \
        fontsize=fontsize, transform=ax3.transAxes)
ax3.plot(x_axis, WRF_May.values, 'k-', label='T2m,May')
ax3.plot(x_axis, WRF_JJA.values, 'k--', label='T2m,JJA')
ax3.set_yticks(np.arange(285.0,311.0,3.0))
ax3.set_xticks(np.arange(0.0,24.1,3.0))
ax3.set(xlabel='UTC(hr)', ylabel='T2m WRF, K')
ax3.grid()
ax3.legend(loc='lower right')

fig.savefig("../Figure/T2m.WRF_vs_ARM_SGP.May_first_few_days_removed.png",dpi=600)
plt.show()








