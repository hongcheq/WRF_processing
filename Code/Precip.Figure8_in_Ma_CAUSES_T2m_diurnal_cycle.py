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
RAIN_regrid = ds_WRF['RAIN_tot_regrid']
RAIN_regrid = RAIN_regrid * 24.0 # from mm/hr to mm/day
RAIN_regrid.attrs['units'] = "mm/day"

#RAIN_May = RAIN_regrid[:738,:,:]
#RAIN_JJA = RAIN_regrid[738:,:,:]
RAIN_MJJA = RAIN_regrid

#RAIN_WRF_May = RAIN_May.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
#RAIN_WRF_JJA = RAIN_JJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
RAIN_WRF_MJJA = RAIN_MJJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')

#WRF_May = RAIN_WRF_May.groupby('time.hour').mean()
#WRF_JJA = RAIN_WRF_JJA.groupby('time.hour').mean()
WRF_MJJA = RAIN_WRF_MJJA.groupby('time.hour').mean()

### ARM SGP obs: ARMBE2DGRID from Qi Tang

precip05 = ds_ARMBE2D_05['precip_rate']
precip06 = ds_ARMBE2D_06['precip_rate']
precip07 = ds_ARMBE2D_07['precip_rate']
precip08 = ds_ARMBE2D_08['precip_rate']

precip_05678 = xr.concat([precip05, precip06, precip07, precip08], dim='time')
precip_05678 = precip_05678 * 24.0 # from mm/hr to mm/day
precip_05678.attrs['units'] = "mm/day"

#precip_May = precip05.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
#precip_JJA = precip_0678.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
precip_MJJA = precip_05678.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')

### the time variable in ARMBE2DGRID is not-so-regular, 
### using groupby('time.hour').mean() may entail issues, just use for loop
###ARM_May = precip_May.groupby('time.hour').mean()
###ARM_JJA = precip_JJA.groupby('time.hour').mean()

#ARM_May = np.zeros(24)
#ARM_JJA = np.zeros(24)
ARM_MJJA = np.zeros(24)

#for i in np.arange(0,31,1):
#    ARM_May = ARM_May + precip_May[i*24:i*24+24].values
#ARM_May = ARM_May / 31.0
#
#for i in np.arange(0,92,1):
#    ARM_JJA = ARM_JJA + precip_JJA[i*24:i*24+24].values
#ARM_JJA = ARM_JJA / 92.0
#
for i in np.arange(0,92,1):
    ARM_MJJA = ARM_MJJA + precip_MJJA[i*24:i*24+24].values
ARM_MJJA = ARM_MJJA / (31.0 + 92.0)
print(ARM_MJJA)
#print(ARM_JJA)

### WRF bias in May, and JJA ###
#bias_May = WRF_May - ARM_May
#bias_JJA = WRF_JJA - ARM_JJA
bias_MJJA = WRF_MJJA - ARM_MJJA

### Plot ###
#x_axis = WRF_May.coords['hour']
x_axis = WRF_MJJA.coords['hour']

fig = plt.figure(figsize=(9,10))
fontsize = 7
pos_adjust1 = 0.04

ax1 = fig.add_subplot(3,1,1)
ax1.text(s='Precip bias, WRF-ARMBE2D', x=0, y=1.02, ha='left', va='bottom', \
        fontsize=fontsize, transform=ax1.transAxes)
#ax1.plot(x_axis, bias_May.values, 'r-', label='precip,May')
ax1.plot(x_axis, bias_MJJA.values, 'r--', label='precip,MJJA')
#ax1.set_yticks(np.arange(-2.0,9.1,1.0))
ax1.axhline(linewidth=1.5, color='k')
ax1.set_xticks(np.arange(0.0,24.1,3.0))
ax1.set(xlabel='UTC(hr)', ylabel='WRF precip bias, mm/day', title='Precip, WRF vs ARM SGP')
ax1.grid()
ax1.legend(loc='upper right')

ax2 = fig.add_subplot(3,1,2)
ax2.text(s='Precip, WRF', x=0, y=1.02, ha='left', va='bottom', \
        fontsize=fontsize, transform=ax2.transAxes)
#ax2.plot(x_axis, WRF_May.values, 'b-', label='precip,May')
ax2.plot(x_axis, WRF_MJJA.values, 'b--', label='precip,MJJA')
#ax2.set_yticks(np.arange(0.0,9.1,1.0))
ax2.set_xticks(np.arange(0.0,24.1,3.0))
ax2.set(xlabel='UTC(hr)', ylabel='WRF precip, mm/day')
ax2.grid()
ax2.legend(loc='upper right')

ax3 = fig.add_subplot(3,1,3)
ax3.text(s='precip,SGP,ARMBE2D', x=0, y=1.02, ha='left', va='bottom', \
        fontsize=fontsize, transform=ax3.transAxes)
#ax3.plot(x_axis, ARM_May, 'k-', label='precip,May')
ax3.plot(x_axis, ARM_MJJA, 'k--', label='precip,MJJA')
#ax3.set_yticks(np.arange(0.0,9.1,1.0))
ax3.set_xticks(np.arange(0.0,24.1,3.0))
ax3.set(xlabel='UTC(hr)', ylabel='precip SGP obs, mm/day')
ax3.grid()
ax3.legend(loc='upper right')

fig.savefig("../Figure/Precip.Diurnal.WRF_vs_ARM_SGP.png",dpi=600)
plt.show()








