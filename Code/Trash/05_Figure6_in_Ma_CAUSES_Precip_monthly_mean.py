'''
Function: analysis for WRF 2011 May-Aug outputs, as in Ma CAUSES paper Figure 8.
Date: 20200325
'''

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import pandas

ds_WRF = xr.open_dataset('/home/qin5/Data/WRF.postprocessing.extract.hourly.nc')
ds_WRF_Thom = xr.open_dataset('/home/qin5/Data/WRF.postprocessing.extract.hourly.Thom.05678.nc')

ds_NOAA = xr.open_dataset('/home/qin5/Data/CAUSES_obs/noaa_conus_T2M_temperature_1p0deg_hourly_2011_MAMJJA.nc')

ds_ARMBE2D_05 = xr.open_dataset('/home/qin5/Data/ARMBE2DGRID/sgparmbe2dgridX1.c1.20110501.000000.nc')
ds_ARMBE2D_06 = xr.open_dataset('/home/qin5/Data/ARMBE2DGRID/sgparmbe2dgridX1.c1.20110601.000000.nc')
ds_ARMBE2D_07 = xr.open_dataset('/home/qin5/Data/ARMBE2DGRID/sgparmbe2dgridX1.c1.20110701.000000.nc')
ds_ARMBE2D_08 = xr.open_dataset('/home/qin5/Data/ARMBE2DGRID/sgparmbe2dgridX1.c1.20110801.000000.nc')

## Figure 8 in Ma et al 2018, average over 35-38N, 99-96W, consistent with ARMBE2D from Qi Tang
lat_1 = 35.0
lat_2 = 38.0
lon_1 = -99.0
lon_2 = -96.0

# for 360 longitude
lon_1_360 = 261.0
lon_2_360 = 264.0

### WRF  at ARM SGP site 
RAIN_regrid = ds_WRF['RAIN_tot_regrid']

RAIN_WRF_month = RAIN_regrid.resample(time='MS').mean(dim='time')
RAIN_WRF_May = RAIN_WRF_month[0,:,:]
RAIN_WRF_Jun = RAIN_WRF_month[1,:,:]
RAIN_WRF_Jul = RAIN_WRF_month[2,:,:]
RAIN_WRF_Aug = RAIN_WRF_month[3,:,:]
RAIN_WRF_JJA = (RAIN_WRF_Jun + RAIN_WRF_Jul + RAIN_WRF_Aug)/3.0
RAIN_WRF_MJJA = (RAIN_WRF_May + RAIN_WRF_Jun + RAIN_WRF_Jul + RAIN_WRF_Aug)/4.0

WRF_May = RAIN_WRF_May.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
WRF_Jun = RAIN_WRF_Jun.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
WRF_Jul = RAIN_WRF_Jul.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
WRF_Aug = RAIN_WRF_Aug.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
WRF_JJA = RAIN_WRF_JJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
WRF_MJJA = RAIN_WRF_MJJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')

### WRF_Thom 
RAIN_regrid_Thom = ds_WRF_Thom['RAIN_regrid']

RAIN_WRF_Thom_month = RAIN_regrid_Thom.resample(time='MS').mean(dim='time')
RAIN_WRF_Thom_May = RAIN_WRF_Thom_month[0,:,:]
RAIN_WRF_Thom_Jun = RAIN_WRF_Thom_month[1,:,:]
RAIN_WRF_Thom_Jul = RAIN_WRF_Thom_month[2,:,:]
RAIN_WRF_Thom_Aug = RAIN_WRF_Thom_month[3,:,:]
RAIN_WRF_Thom_JJA = (RAIN_WRF_Thom_Jun + RAIN_WRF_Thom_Jul + RAIN_WRF_Thom_Aug)/3.0
RAIN_WRF_Thom_MJJA = (RAIN_WRF_Thom_May + RAIN_WRF_Thom_Jun + RAIN_WRF_Thom_Jul + RAIN_WRF_Thom_Aug)/4.0

WRF_Thom_May = RAIN_WRF_Thom_May.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
WRF_Thom_Jun = RAIN_WRF_Thom_Jun.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
WRF_Thom_Jul = RAIN_WRF_Thom_Jul.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
WRF_Thom_Aug = RAIN_WRF_Thom_Aug.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
WRF_Thom_JJA = RAIN_WRF_Thom_JJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
WRF_Thom_MJJA = RAIN_WRF_Thom_MJJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')

### ------ NOAA obs T2m -----
t2m = ds_NOAA['t2m']
t2m = t2m.rename({'t':'time'}).rename({'y':'lat'}).rename({'x':'lon'})
t2m['lon'] = ds_NOAA['Longitude'].values
t2m['lat'] = ds_NOAA['Latitude'].values

## In the original file, the time is not properly encoded (units not conformed to CF standard?)
##  datetime type is required for the monthly resmaple calculation.
values_time = ds_NOAA['Time'].values
attrs_time = {'units': 'hours since 2011-04-01 00:00:00'}
ds_time = xr.Dataset({'time': ('time', values_time, attrs_time) })
dt_format_time = xr.decode_cf(ds_time)

t2m.coords['time'] = dt_format_time['time']
t2m = t2m + 273.15
t2m.attrs['units'] = "K"
T2_NOAA_month = t2m.resample(time='MS').mean(dim='time')

T2_NOAA_May = T2_NOAA_month[1,:,:]
T2_NOAA_Jun = T2_NOAA_month[2,:,:]
T2_NOAA_Jul = T2_NOAA_month[3,:,:]
T2_NOAA_Aug = T2_NOAA_month[4,:,:]
T2_NOAA_JJA = (T2_NOAA_Jun + T2_NOAA_Jul + T2_NOAA_Aug)/3.0
T2_NOAA_MJJA = (T2_NOAA_May + T2_NOAA_Jun + T2_NOAA_Jul + T2_NOAA_Aug)/4.0

NOAA_May = T2_NOAA_May.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1_360, lon_2_360)).mean(dim='lat').mean(dim='lon')
NOAA_Jun = T2_NOAA_Jun.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1_360, lon_2_360)).mean(dim='lat').mean(dim='lon')
NOAA_Jul = T2_NOAA_Jul.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1_360, lon_2_360)).mean(dim='lat').mean(dim='lon')
NOAA_Aug = T2_NOAA_Aug.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1_360, lon_2_360)).mean(dim='lat').mean(dim='lon')
NOAA_JJA = T2_NOAA_JJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1_360, lon_2_360)).mean(dim='lat').mean(dim='lon')
NOAA_MJJA = T2_NOAA_MJJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1_360, lon_2_360)).mean(dim='lat').mean(dim='lon')

### ARM SGP obs: ARMBE2DGRID from Qi Tang

temp05 = ds_ARMBE2D_05['temp']
temp06 = ds_ARMBE2D_06['temp']
temp07 = ds_ARMBE2D_07['temp']
temp08 = ds_ARMBE2D_08['temp']

temp_05678 = xr.concat([temp05, temp06, temp07, temp08], dim='time')
temp_05678 = temp_05678.resample(time='MS').mean(dim='time')
temp_May = temp_05678[0,:,:]
temp_Jun = temp_05678[1,:,:]
temp_Jul = temp_05678[2,:,:]
temp_Aug = temp_05678[3,:,:]
temp_JJA = (temp_Jun + temp_Jul + temp_Aug)/3.0
temp_MJJA = (temp_May + temp_Jun + temp_Jul + temp_Aug)/4.0

ARM_May = temp_May.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
ARM_Jun = temp_Jun.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
ARM_Jul = temp_Jul.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
ARM_Aug = temp_Aug.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
ARM_JJA = temp_JJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
ARM_MJJA = temp_MJJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')

### Plot ###
x_axis = ['May','Jun','Jul','Aug','JJA','MJJA']

fig = plt.figure()
fontsize = 7
pos_adjust1 = 0.04

ax1 = fig.add_subplot(1,1,1)
ax1.text(s='T2m, K', x=0, y=1.02, ha='left', va='bottom', \
        fontsize=fontsize, transform=ax1.transAxes)
ax1.scatter(x_axis, [WRF_May, WRF_Jun, WRF_Jul, WRF_Aug, WRF_JJA, WRF_MJJA], c='b',marker='s', label='WRF_Morr')
ax1.scatter(x_axis, [WRF_Thom_May, WRF_Thom_Jun, WRF_Thom_Jul, WRF_Thom_Aug, WRF_Thom_JJA, WRF_Thom_MJJA], c='g',marker='s', label='WRF_Thom')
#-------

ax1.scatter(x_axis, [ARM_May, ARM_Jun, ARM_Jul, ARM_Aug, ARM_JJA, ARM_MJJA], c='r', marker='d', label='ARM obs')
ax1.scatter(x_axis, [NOAA_May, NOAA_Jun, NOAA_Jul, NOAA_Aug, NOAA_JJA, NOAA_MJJA], c='b', marker='d', label='NOAA obs')
#ax1.set_yticks(np.arange(0.0,4.6,0.5))
#ax1.set_xticks(np.arange(0.0,24.1,3.0))
ax1.set(xlabel='month category', ylabel='T2m, K', title='T2m, WRF vs ARM SGP')
ax1.grid()
ax1.legend(loc='lower right')

fig.savefig("../Figure/Figure6.T2m.WRF_Morri_Thom_vs_ARM_SGP.png",dpi=600)
plt.show()








