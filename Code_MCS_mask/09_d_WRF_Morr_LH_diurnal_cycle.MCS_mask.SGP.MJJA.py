'''
Function: analysis for WRF_Morri 2011 May-Aug outputs, as in Feng 2018 paper Figure 5.
Date: 20200709
'''
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import pandas

label_string = "_Morr"

#ds_WRF = xr.open_dataset('/home/qin5/Data/WRF.postprocessing.extract.hourly.nc')
##ds_WRF = xr.open_dataset('/home/qin5/Data/WRF_postprocessing/WRF_Morri/WRF.postprocessing.extract.hourly.0.04.RAIN_tot.ncrcat.nc')
ds_WRF = xr.open_dataset('/home/qin5/Data/WRF_postprocessing/WRF_Morri/WRF.postprocessing.extract.hourly.0.04.LH.time_revise.nc')
ds_WRF_MCS = xr.open_dataset('/home/qin5/Data/WRF_postprocessing/WRF_Morri/WRF.mask.postprocessing.extract.hourly.0.04.nc')

ds_OBS = xr.open_dataset('/home/qin5/Data/WRF_postprocessing/OBS/mcstrack_20110501-0831.ncrcat.nc')

ds_ARMBE2D_var = xr.open_dataset('/home/qin5/Data/ARMBE2DGRID/OBS_MCS_mask_consistency/sgparmbe2dgridX1.c1.201105_08.time_revise.latent_heat_flux.nc')

##ds_WRF_Thom = xr.open_dataset('/home/qin5/Data/WRF.postprocessing.extract.hourly.Thom.05678.nc')

##ds_ARMBE2D_01 = xr.open_dataset('/home/qin5/Data/ARMBE2DGRID/sgparmbe2dgridX1.c1.20110101.000000.nc')
##ds_ARMBE2D_02 = xr.open_dataset('/home/qin5/Data/ARMBE2DGRID/sgparmbe2dgridX1.c1.20110201.000000.nc')
##ds_ARMBE2D_03 = xr.open_dataset('/home/qin5/Data/ARMBE2DGRID/sgparmbe2dgridX1.c1.20110301.000000.nc')
##ds_ARMBE2D_04 = xr.open_dataset('/home/qin5/Data/ARMBE2DGRID/sgparmbe2dgridX1.c1.20110401.000000.nc')

#ds_ARMBE2D_05 = xr.open_dataset('/scratch/CAUSES/CAUSES/obs/ARMBE2DGRID/OLD/2011_old/sgparmbe2dgridX1.c1.20110501.000000.nc')
#ds_ARMBE2D_05 = xr.open_dataset('/home/qin5/Data/ARMBE2DGRID/sgparmbe2dgridX1.c1.20110501.000000.nc')
#ds_ARMBE2D_06 = xr.open_dataset('/home/qin5/Data/ARMBE2DGRID/sgparmbe2dgridX1.c1.20110601.000000.nc')
#ds_ARMBE2D_07 = xr.open_dataset('/home/qin5/Data/ARMBE2DGRID/sgparmbe2dgridX1.c1.20110701.000000.nc')
#ds_ARMBE2D_08 = xr.open_dataset('/home/qin5/Data/ARMBE2DGRID/sgparmbe2dgridX1.c1.20110801.000000.nc')

## Figure 8 in Ma et al 2018, average over 35-38N, 99-96W, consistent with ARMBE2D from Qi Tang
lat_1 = 35.0
lat_2 = 38.0
lon_1 = -99.0
lon_2 = -96.0

### WRF calculate diurnal cycle
### MCS masks
WRF_MCS_mask = ds_WRF_MCS['pcptracknumber_regrid']

### Convert all MCS track number to 1 for summation purpose
pcpnumber_WRF = ds_WRF_MCS.pcptracknumber_regrid.values
pcpnumber_WRF[pcpnumber_WRF > 0] = 1

# Convert numpy array to DataArray
mcspcpmask_WRF = xr.DataArray(pcpnumber_WRF, coords={'time':ds_WRF_MCS.time, 'lat':ds_WRF_MCS.lat, 'lon':ds_WRF_MCS.lon}, dims=['time','lat','lon'])

# Sum MCS PF counts overtime to get number of hours
mcspcpct_WRF = mcspcpmask_WRF.sum(dim='time')
print(mcspcpct_WRF)

# Total number of time frames selected
ntimes = np.zeros(1, dtype=int)
ntimes[0] = len(ds_WRF_MCS['time'])

##### Note: RAIN_tot_regrid and WRF_MCS_mask, the time dimension of these two variable needs to be the same!
var_regrid_yes_MCS = ds_WRF['LH_regrid'].where(WRF_MCS_mask > 0)
var_regrid_no_MCS = ds_WRF['LH_regrid'].where(np.isnan(WRF_MCS_mask))

### In Feng et al [2018], Figure 7, MCS precip is adjusted by * (MCS hours / total hours) ?
###                                 non-MCS precip is adjusted by * (non-MCS hours / total hours )?
#var_regrid_yes_MCS = var_regrid_yes_MCS * mcspcpct_WRF / ntimes[0]
#var_regrid_no_MCS = var_regrid_no_MCS * (ntimes[0] - mcspcpct_WRF) / ntimes[0]

###
var_WRF_yes_MCS = var_regrid_yes_MCS.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
var_WRF_no_MCS = var_regrid_no_MCS.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')

### Lessons learned: the groupby('time.hour') command requires the time has regular values, just check
print(var_WRF_yes_MCS.coords['time'][0:24])
print(ds_WRF_MCS['time'][0:24])
print(ds_OBS['time'][0:24])

### skip the first 17 values from 05-01 07:00:00 - 05-01 23:00:00
#var_WRF_yes_MCS2 = var_WRF_yes_MCS[17:]
#var_WRF_no_MCS2 = var_WRF_no_MCS[17:]
#print(var_WRF_yes_MCS2)
#print(var_WRF_no_MCS2)

### the time has regular values, so you can use the following command
WRF_yes_MCS = var_WRF_yes_MCS.groupby('time.hour').mean()
WRF_no_MCS = var_WRF_no_MCS.groupby('time.hour').mean()

## change units
#WRF_yes_MCS = WRF_yes_MCS * 24.0  # from mm/hour to mm/day
#WRF_yes_MCS.attrs['units'] = "mm/day"
#WRF_no_MCS = WRF_no_MCS * 24.0  # from mm/hour to mm/day
#WRF_no_MCS.attrs['units'] = "mm/day"
####

### OBS of MCS masks
### MCS masks
OBS_MCS_mask = ds_OBS['pcptracknumber']
ARMBE_var = -ds_ARMBE2D_var['latent_heat_flux']
str_var_plt = "LH"
str_var_plt_units = "W/m2"

### Convert all MCS track number to 1 for summation purpose
pcpnumber_OBS = ds_OBS.pcptracknumber.values
pcpnumber_OBS[pcpnumber_OBS > 0] = 1

# Convert numpy array to DataArray
mcspcpmask_OBS = xr.DataArray(pcpnumber_OBS, coords={'time':ds_OBS.time, 'lat':ds_OBS.lat, 'lon':ds_OBS.lon}, dims=['time','lat','lon'])

# Sum MCS PF counts overtime to get number of hours
mcspcpct_OBS = mcspcpmask_OBS.sum(dim='time')
print(mcspcpct_OBS)

# Total number of time frames selected
ntimes_OBS = np.zeros(1, dtype=int)
ntimes_OBS[0] = len(ds_OBS['time'])

### Steve: you may want to allow some leeway in the MCS tracking at SGP box
lee_way = 0.10   # If the OBS MCS tracking have at least 50% of pixels say this hour has MCS
                  # then total total SGP box will be regarded as MCS present.
# total points at SGP box
lat_count = len(ds_OBS['lat'].sel(lat=slice(lat_1, lat_2)).values)
lon_count = len(ds_OBS['lon'].sel(lon=slice(lon_1, lon_2)).values)
total_count = lat_count * lon_count # 82x82
threshold = total_count * lee_way # if 82*82*lee_way points have MCS, then deem the whole SGP box MCS present

# subset the MCS mask at SGP box
var_ARMBE_SGP_mean =  ARMBE_var.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')

mcspcpmask_OBS_SGP = mcspcpmask_OBS.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2))

mcspcpmask_OBS_SGP_MCS_points = mcspcpmask_OBS_SGP.sum(dim='lat').sum(dim='lon')

#####
#var_regrid_yes_MCS_obs = ds_OBS['precipitation'].where(OBS_MCS_mask > 0)
#var_regrid_no_MCS_obs = ds_OBS['precipitation'].where(np.isnan(OBS_MCS_mask))

var_ARMBE_SGP_mean.coords['time'] = mcspcpmask_OBS_SGP_MCS_points.coords['time']
print(var_ARMBE_SGP_mean.coords['time'])
print(mcspcpmask_OBS_SGP_MCS_points.coords['time'])

var_regrid_yes_MCS_obs = var_ARMBE_SGP_mean.where(mcspcpmask_OBS_SGP_MCS_points > threshold)
var_regrid_no_MCS_obs = var_ARMBE_SGP_mean.where(mcspcpmask_OBS_SGP_MCS_points <= threshold)

print(var_regrid_yes_MCS_obs)
print(var_regrid_no_MCS_obs)

### In Feng et al [2018], Figure 7, MCS precip is adjusted by * (MCS hours / total hours) ?
###                                 non-MCS precip is adjusted by * (non-MCS hours / total hours )?
#mcspcpct_OBS_tmp = mcspcpct_OBS.sel(lat=slice(lat_1,lat_2),lon=slice(lon_1,lon_2)).mean(dim='lat').mean(dim='lon')

#var_regrid_yes_MCS_obs = var_regrid_yes_MCS_obs * mcspcpct_OBS_tmp / ntimes_OBS[0]
#var_regrid_no_MCS_obs = var_regrid_no_MCS_obs * (ntimes_OBS[0] - mcspcpct_OBS_tmp) / ntimes_OBS[0]

###
#var_OBS_yes_MCS = var_regrid_yes_MCS_obs.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
#var_OBS_no_MCS = var_regrid_no_MCS_obs.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
var_OBS_yes_MCS = var_regrid_yes_MCS_obs
var_OBS_no_MCS = var_regrid_no_MCS_obs


### Lessons learned: the groupby('time.hour') command requires the time has regular values, just check
print(var_OBS_yes_MCS.coords['time'][0:24])
print(var_OBS_yes_MCS.coords['time'][0:24])

### the time has regular values, so you can use the following command
OBS_yes_MCS = var_OBS_yes_MCS.groupby('time.hour').mean()
OBS_no_MCS = var_OBS_no_MCS.groupby('time.hour').mean()

## change units
#OBS_yes_MCS = OBS_yes_MCS * 24.0  # from mm/hour to mm/day
#OBS_yes_MCS.attrs['units'] = "mm/day"
#OBS_no_MCS = OBS_no_MCS * 24.0  # from mm/hour to mm/day
#OBS_no_MCS.attrs['units'] = "mm/day"
####


### ARM SGP obs: ARMBE2DGRID from Qi Tang
#temp05 = ds_ARMBE2D_05['temp']
#temp06 = ds_ARMBE2D_06['temp']
#temp07 = ds_ARMBE2D_07['temp']
#temp08 = ds_ARMBE2D_08['temp']

#temp_0678 = xr.concat([temp06, temp07, temp08], dim='time')

#temp_May = temp05.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
#temp_JJA = temp_0678.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')

### the time coords values are irregular, so you cannot use groupby('time.hour').mean() to 
### calculate diurnal cycle, just use for loops
#print(temp_JJA['time'][0:24])

#ARM_May = np.zeros(24)
#ARM_JJA = np.zeros(24)
#
#for i in np.arange(0,31,1):
#    ARM_May = ARM_May + temp_May[0+i*24:i*24+24].values
#
#ARM_May = ARM_May / 31.0
#
#for i in np.arange(0,92,1):
#    ARM_JJA = ARM_JJA + temp_JJA[0+i*24:i*24+24].values
#
#ARM_JJA = ARM_JJA / 92.0
#print(ARM_May)
#print(ARM_JJA)

### do not use the groupby('time.hour').mean() command since the time values is not regular.
##ARM_Jan = temp_Jan.groupby('time.hour').mean()
#ARM_Feb = temp_Feb.groupby('time.hour').mean()
#ARM_Mar = temp_Mar.groupby('time.hour').mean()
#ARM_Apr = temp_Apr.groupby('time.hour').mean()

#ARM_May = temp_May.groupby('time.hour').mean()
#ARM_Jun = temp_Jun.groupby('time.hour').mean()
#ARM_Jul = temp_Jul.groupby('time.hour').mean()
#ARM_Aug = temp_Aug.groupby('time.hour').mean()
#ARM_JJA = temp_JJA.groupby('time.hour').mean()

### WRF bias in May, and JJA ###
#bias_May = WRF_May - ARM_May
#bias_JJA = WRF_JJA - ARM_JJA

#print(WRF_May)
#print(bias_JJA)

### Plot ###
x_axis = WRF_yes_MCS.coords['hour']

fig = plt.figure(figsize=(8,6))
fontsize = 7
pos_adjust1 = 0.04

ax1 = fig.add_subplot(1,1,1)
ax1.text(s=str_var_plt+', WRF vs ARMBE2D', x=0, y=1.02, ha='left', va='bottom', \
        fontsize=fontsize, transform=ax1.transAxes)
ax1.plot(x_axis, OBS_yes_MCS.values, 'k-', label='ARMBE2D_yes_MCS')
ax1.plot(x_axis, OBS_no_MCS.values, 'k--', label='ARMBE2D_no_MCS')
#ax1.plot(x_axis, ARM_JJA, 'k-', label='ARM, JJA')
ax1.plot(x_axis, WRF_yes_MCS, 'r-', label='WRF_Morri_yes_MCS')
ax1.plot(x_axis, WRF_no_MCS, 'r--', label='WRF_Morri_no_MCS')
#ax1.plot(x_axis, WRF_JJA_Thom, 'g--', label='WRF_Thom, JJA')

#ax1.set_yticks(np.arange(0.0,3.2,0.5))
ax1.set_xticks(np.arange(0.0,24.1,3.0))
#ax1.set_xticks(np.arange(0.0,24.1,3.0),["18", "21", "24", "3", "6", "9", "12", "15"])
ax1.set(xlabel='UTC(LST+6hr)',ylabel=str_var_plt+', '+str_var_plt_units,title=str_var_plt+', ARMBE2D, 2011 May-Aug')
#ax1.set(xlabel='LST(hr)', ylabel='Precip, mm/day', title='Precip, 2011 May-Aug')
ax1.grid()
ax1.legend(loc='upper left')

#ax2 = fig.add_subplot(2,1,2)
#ax2.text(s='T2m, ARM SGP', x=0, y=1.02, ha='left', va='bottom', \
#        fontsize=fontsize, transform=ax2.transAxes)
##ax2.plot(x_axis, ARM_May, 'k-', label='May')
#ax2.plot(x_axis, ARM_JJA, 'k--', label='JJA')
#ax2.set_yticks(np.arange(285.0,311.0,3.0))
#ax2.set_xticks(np.arange(0.0,24.1,3.0))
#ax2.set(xlabel='UTC(hr)', ylabel='T2m ARM SGP, K')
#ax2.grid()
#ax2.legend(loc='lower right')

fig.savefig("../Figure_MCS_mask/09_d_"+str_var_plt+".OBS_vs_WRF_Morri"+label_string+".MCS_masks.png",dpi=600,bbox_inches="tight")
plt.show()



