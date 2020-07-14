'''
Function: 
    1. OBS: distribution of (fraction of MCS grids to total grids). One hour is one sample, one snapshot of \
            MCS grids/total SGP grids is one data point.
    2. OBS: distribution of (MCS frequency on different hour of the day). Check the 3x3 SGP grids,\
            MCS cases / total MCS cases, inspect this over different hour of the day.
    3. WRF_Morrison: similar to 1 
    4. WRF_Morrison: similar to 2
'''

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd

ds_OBS = xr.open_dataset('/home/qin5/Data/WRF_postprocessing/OBS/mcstrack_20110501-0831.ncrcat.nc')
ds_WRF_MCS = xr.open_dataset('/home/qin5/Data/WRF_postprocessing/WRF_Morri/WRF.mask.postprocessing.extract.hourly.0.04.nc')

## Figure 8 in Ma et al 2018, average over 35-38N, 99-96W, consistent with ARMBE2D from Qi Tang
lat_1 = 35.0
lat_2 = 38.0
lon_1 = -99.0
lon_2 = -96.0

### OBS of MCS masks
### MCS masks
#OBS_MCS_mask = ds_OBS['pcptracknumber']

### Convert all MCS track number to 1 for summation purpose
pcpnumber_OBS = ds_OBS.pcptracknumber.values
pcpnumber_OBS[pcpnumber_OBS > 0] = 1

# Convert numpy array to DataArray
mcspcpmask_OBS = xr.DataArray(pcpnumber_OBS, coords={'time':ds_OBS.time, 'lat':ds_OBS.lat, 'lon':ds_OBS.lon}, dims=['time','lat','lon'])

# slice over SGP 3x3 grid box
mcspcpmask_OBS_SGP = mcspcpmask_OBS.sel(lat=slice(lat_1,lat_2),lon=slice(lon_1,lon_2))
print(mcspcpmask_OBS_SGP)

# total points at SGP box
lat_count = len(ds_OBS['lat'].sel(lat=slice(lat_1, lat_2)).values)
lon_count = len(ds_OBS['lon'].sel(lon=slice(lon_1, lon_2)).values)
total_count = lat_count * lon_count # 82x82

# Calculate MCS grid point fraction for different hours
mcspcpmask_OBS_SGP_MCS_points = mcspcpmask_OBS_SGP.sum(dim='lat').sum(dim='lon')
#print(mcspcpmask_OBS_SGP_MCS_points)

mcspcpmask_OBS_SGP_MCS_fraction = mcspcpmask_OBS_SGP_MCS_points / total_count
#print(mcspcpmask_OBS_SGP_MCS_fraction.values)

##### MCS mask at different hour of the day
mcspcpmask_OBS_SGP_MCS_points_diurnal = mcspcpmask_OBS_SGP_MCS_points.groupby('time.hour').sum()
#print(mcspcpmask_OBS_SGP_MCS_points_diurnal)

mcspcpmask_OBS_SGP_MCS_points_diurnal_total = mcspcpmask_OBS_SGP_MCS_points_diurnal.sum(dim='hour')
#print(mcspcpmask_OBS_SGP_MCS_points_diurnal_total)

mcspcpmask_OBS_SGP_MCS_points_diurnal_fraction = mcspcpmask_OBS_SGP_MCS_points_diurnal / mcspcpmask_OBS_SGP_MCS_points_diurnal_total
#print(mcspcpmask_OBS_SGP_MCS_points_diurnal_fraction)

#### WRF_Morrison
### MCS masks
#WRF_MCS_mask = ds_WRF_MCS['pcptracknumber_regrid']

pcpnumber_WRF = ds_WRF_MCS.pcptracknumber_regrid.values
pcpnumber_WRF[pcpnumber_WRF > 0] = 1

# Convert numpy array to DataArray
mcspcpmask_WRF = xr.DataArray(pcpnumber_WRF, coords={'time':ds_WRF_MCS.time, 'lat':ds_WRF_MCS.lat, 'lon':ds_WRF_MCS.lon}, dims=['time','lat','lon'])

# slice over SGP 3x3 grid box
mcspcpmask_WRF_SGP = mcspcpmask_WRF.sel(lat=slice(lat_1,lat_2),lon=slice(lon_1,lon_2))
print(mcspcpmask_WRF_SGP)

# total points at SGP box
lat_count_WRF = len(ds_WRF_MCS['lat'].sel(lat=slice(lat_1, lat_2)).values)
lon_count_WRF = len(ds_WRF_MCS['lon'].sel(lon=slice(lon_1, lon_2)).values)
total_count_WRF = lat_count_WRF * lon_count_WRF  # 76x76
print(total_count_WRF)  # 5776

# Calculate MCS grid point fraction for different hours
mcspcpmask_WRF_SGP_MCS_points = mcspcpmask_WRF_SGP.sum(dim='lat').sum(dim='lon')
print(mcspcpmask_WRF_SGP_MCS_points)

mcspcpmask_WRF_SGP_MCS_fraction = mcspcpmask_WRF_SGP_MCS_points / total_count_WRF
print(mcspcpmask_WRF_SGP_MCS_fraction.values)

##### MCS mask at different hour of the day
mcspcpmask_WRF_SGP_MCS_points_diurnal = mcspcpmask_WRF_SGP_MCS_points.groupby('time.hour').sum()
print(mcspcpmask_WRF_SGP_MCS_points_diurnal)

mcspcpmask_WRF_SGP_MCS_points_diurnal_total = mcspcpmask_WRF_SGP_MCS_points_diurnal.sum(dim='hour')
print(mcspcpmask_WRF_SGP_MCS_points_diurnal_total)

mcspcpmask_WRF_SGP_MCS_points_diurnal_fraction = mcspcpmask_WRF_SGP_MCS_points_diurnal / mcspcpmask_WRF_SGP_MCS_points_diurnal_total
print(mcspcpmask_WRF_SGP_MCS_points_diurnal_fraction)

######
### Plot 
fig = plt.figure(figsize=(12,12))
fontsize = 7

ax1 = fig.add_subplot(2,2,1)
num_bins1 = 20
n, bins, patches = ax1.hist(mcspcpmask_OBS_SGP_MCS_fraction.values, num_bins1)
ax1.set(xlabel='MCS grids/total grids', ylabel='# of hours',title='OBS, MCS grids fraction, histogram')
ax1.grid()

ax2 = fig.add_subplot(2,2,2)
ax2.set_xticks(np.arange(0,24,1))
x_labels = ['18','19','20','21','22','23','00','01','02','03','04','05','06','07',\
        '08','09','10','11','12','13','14','15','16','17']
ax2.set_xticklabels(x_labels)
ax2.bar(np.arange(0,24,1),mcspcpmask_OBS_SGP_MCS_points_diurnal_fraction)
ax2.set(xlabel='hour of the day (LST=UTC-6)', ylabel='MCS fraction',title='OBS, MCS occurrence fraction(space+time)')
ax2.grid()

ax3 = fig.add_subplot(2,2,3)
num_bins3 = 20
n, bins, patches = ax3.hist(mcspcpmask_WRF_SGP_MCS_fraction.values, num_bins3)
ax3.set(xlabel='MCS grids/total grids', ylabel='# of hours',title='WRF_Morri, MCS grids fraction, histogram')
ax3.grid()

ax4 = fig.add_subplot(2,2,4)
ax4.set_xticks(np.arange(0,24,1))
x_labels_ax4 = ['18','19','20','21','22','23','00','01','02','03','04','05','06','07',\
        '08','09','10','11','12','13','14','15','16','17']
ax4.set_xticklabels(x_labels_ax4)
ax4.bar(np.arange(0,24,1),mcspcpmask_WRF_SGP_MCS_points_diurnal_fraction)
ax4.set(xlabel='hour of the day (LST=UTC-6)', ylabel='MCS fraction',title='WRF_Morri, MCS occurrence fraction(space+time)')
ax4.grid()


fig.savefig("../Figure_MCS_mask/MCS_distribution.png",dpi=200)
plt.tight_layout()
plt.show()




