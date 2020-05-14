'''
Function: analysis for WRF 2011 May-Aug outputs, as in VanWeverberg CAUSES paper Figure 13.
Date: 20200325
'''

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import pandas

label_string = "_Morr"

ds_WRF = xr.open_dataset('/home/qin5/Data/WRF.postprocessing.extract.hourly.nc')
ds_WRF_Thom = xr.open_dataset('/home/qin5/Data/WRF.postprocessing.extract.hourly.Thom.05678.nc')

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

RAIN_regrid_Thom = ds_WRF_Thom['RAIN_tot_regrid']
RAIN_regrid_Thom = RAIN_regrid_Thom * 24.0 # from mm/hr to mm/day
RAIN_regrid_Thom.attrs['units'] = "mm/day"

RAIN_JJA = RAIN_regrid[738:,:,:]
RAIN_JJA_Thom = RAIN_regrid_Thom[738:,:,:]


RAIN_WRF_JJA = RAIN_JJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
RAIN_WRF_JJA_Thom = RAIN_JJA_Thom.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')

### Why RAIN_WRF_JJA_Thom minimum values is smaller than zero? shouldn't that >= zero?
### Is it due to regridding?
### But the regridding also done for Morrison, it doesn't have negative rainfall. smallest value == 0.
### What make the _Thompson simulation different?
#print(np.amin(RAIN_WRF_JJA))
#print(np.amin(RAIN_WRF_JJA_Thom))
#print(np.where(RAIN_WRF_JJA_Thom == np.amin(RAIN_WRF_JJA_Thom)))
#print(ds_WRF_Thom['time'][2009])
#print(RAIN_WRF_JJA.coords['time'][0:24])

### workaround set RAIN_WRF_JJA_Thom to zero where values < 0
print(RAIN_WRF_JJA_Thom)
RAIN_WRF_JJA_Thom = RAIN_WRF_JJA_Thom.where(RAIN_WRF_JJA_Thom > 0.0, 0.0)
#----------

WRF_JJA = RAIN_WRF_JJA.groupby('time.hour').mean()
WRF_JJA_Thom = RAIN_WRF_JJA_Thom.groupby('time.hour').mean()
print(WRF_JJA_Thom)


### ARM SGP obs: ARMBE2DGRID from Qi Tang

precip05 = ds_ARMBE2D_05['precip_rate']
precip06 = ds_ARMBE2D_06['precip_rate']
precip07 = ds_ARMBE2D_07['precip_rate']
precip08 = ds_ARMBE2D_08['precip_rate']

##precip05 = precip05 * 24.0
##precip05.attrs['umits'] = "mm/day"

precip_0678 = xr.concat([precip06, precip07, precip08], dim='time')
precip_0678 = precip_0678 * 24.0 # from mm/hr to mm/day
precip_0678.attrs['units'] = "mm/day"

precip_JJA = precip_0678.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')

### the time variable in ARMBE2DGRID is not-so-regular, 
### using groupby('time.hour').mean() may entail issues, just use for loop
###ARM_May = precip_May.groupby('time.hour').mean()
###ARM_JJA = precip_JJA.groupby('time.hour').mean()

#ARM_May = np.zeros(24)
ARM_JJA = np.zeros(24)
#ARM_MJJA = np.zeros(24)

#for i in np.arange(0,31,1):
#    ARM_May = ARM_May + precip_May[i*24:i*24+24].values
#ARM_May = ARM_May / 31.0

for i in np.arange(0,92,1):
    ARM_JJA = ARM_JJA + precip_JJA[i*24:i*24+24].values
ARM_JJA = ARM_JJA / 92.0

#for i in np.arange(0,31+92,1):
#    ARM_MJJA = ARM_MJJA + precip_MJJA[i*24:i*24+24].values
#ARM_MJJA = ARM_MJJA / (31.0 + 92.0)
#print(ARM_MJJA)
print(ARM_JJA)

### WRF bias in May, and JJA ###
#bias_May = WRF_May - ARM_May
#bias_JJA = WRF_JJA - ARM_JJA
#bias_MJJA = WRF_MJJA - ARM_MJJA

### Plot ###
#x_axis = WRF_May.coords['hour']
x_axis = WRF_JJA.coords['hour']

fig = plt.figure(figsize=(9,6))
fontsize = 7
pos_adjust1 = 0.04

ax1 = fig.add_subplot(1,1,1)
ax1.text(s='Precip, WRF vs ARMBE2D', x=0, y=1.02, ha='left', va='bottom', \
        fontsize=fontsize, transform=ax1.transAxes)
#ax1.plot(x_axis, bias_May.values, 'r-', label='precip,May')
ax1.plot(x_axis, WRF_JJA.values, 'b-', label='JJA,WRF_Morri')
ax1.plot(x_axis, WRF_JJA_Thom.values, 'g-', label='JJA,WRF_Thom')
ax1.plot(x_axis, ARM_JJA, 'k-', label='JJA,ARMBE2D')

#ax1.set_yticks(np.arange(-2.0,9.1,1.0))
ax1.axhline(linewidth=1.5, color='k')
ax1.set_xticks(np.arange(0.0,24.,3.0))
ax1.set_xticklabels(np.arange(0+24-6,24+24-6,3) % 24 )
ax1.set(xlabel='LST(hr), UTC-6', ylabel='precip, mm/day', title='Precip, WRF vs ARM SGP')
ax1.grid()
ax1.legend(loc='upper right')

#ax2 = fig.add_subplot(3,1,2)
#ax2.text(s='Precip, WRF', x=0, y=1.02, ha='left', va='bottom', \
#        fontsize=fontsize, transform=ax2.transAxes)
##ax2.plot(x_axis, WRF_May.values, 'b-', label='precip,May')
#ax2.plot(x_axis, WRF_JJA.values, 'b--', label='precip,JJA')
##ax2.set_yticks(np.arange(0.0,9.1,1.0))
#ax2.set_xticks(np.arange(0.0,24.,3.0))
#ax2.set_xticklabels(np.arange(0+24-6,24+24-6,3) % 24 )
#ax2.set(xlabel='LST(hr), UTC-6', ylabel='WRF precip, mm/day')
#ax2.grid()
#ax2.legend(loc='upper right')
#
#ax3 = fig.add_subplot(3,1,3)
#ax3.text(s='precip,SGP,ARMBE2D', x=0, y=1.02, ha='left', va='bottom', \
#        fontsize=fontsize, transform=ax3.transAxes)
##ax3.plot(x_axis, ARM_May, 'k-', label='precip,May')
#ax3.plot(x_axis, ARM_JJA, 'k--', label='precip,JJA')
##ax3.set_yticks(np.arange(0.0,9.1,1.0))
#ax3.set_xticks(np.arange(0.0,24.,3.0))
#ax3.set_xticklabels(np.arange(0+24-6,24+24-6,3) % 24 )
#ax3.set(xlabel='LST(hr), UTC-6', ylabel='precip SGP obs, mm/day')
#ax3.grid()
#ax3.legend(loc='upper right')
#
fig.savefig("../Figure/Precip.Diurnal.JJA.WRF_vs_ARM_SGP.Morri_Thom.png",dpi=600)
plt.show()








