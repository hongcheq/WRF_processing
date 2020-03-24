'''
Function: WRF output vs obs
Date: 20200322
'''

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy
import pandas as pd
import datetime

### workaround for the "urlopen error [SSL: CERTIFICATE_VERIFY_FAILED]" error message
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context
### 


VAR_WRF_str = "T2_regrid"
VAR_obs_str = "t2m"

WRF_file = "/home/qin5/Data/WRF.postprocessing.extract.nc"
obs_file = "/home/qin5/Data/CAUSES_obs/noaa_conus_T2M_temperature_1p0deg_hourly_2011_MAMJJA.nc"

#WRF_ds = xr.open_dataset(WRF_file, decode_times=False)
WRF_ds = xr.open_dataset(WRF_file)
obs_ds = xr.open_dataset(obs_file)
print(WRF_ds)
print(obs_ds)

VAR_WRF = WRF_ds[VAR_WRF_str]
attrs_temp = VAR_WRF.attrs
VAR_WRF = VAR_WRF - 273.15 # from Kelvin to degree C
VAR_WRF.attrs = attrs_temp
VAR_WRF.attrs['units'] = "degree Celsius"
print(VAR_WRF)

VAR_obs = obs_ds[VAR_obs_str]

## In the original file, the time is not properly encoded (units not conformed to CF standard?)
##  datetime type is required for the monthly resmaple calculation.
values_time = obs_ds['Time'].values
attrs_time = {'units': 'hours since 2011-04-01 00:00:00'}
ds_time = xr.Dataset({'time': ('time', values_time, attrs_time) })
dt_format_time = xr.decode_cf(ds_time)
print(dt_format_time)

VAR_obs = VAR_obs.rename({'t': 'Time'})
VAR_obs.coords['Time'] = dt_format_time['time'].values
print(VAR_obs.coords['Time'])

VAR_obs = VAR_obs.rename({'x':'lon'})
VAR_obs['lon'] = WRF_ds['lon']
VAR_obs = VAR_obs.rename({'y':'lat'})
VAR_obs['lat'] = WRF_ds['lat']
print(VAR_obs)

### this NOAA t2m has NaN values, needs to be taken care of ##
## VAR_WRF shows nan values for many _FillValues, does this suggest it handles _FillValues
## and NaN values automatically? Put aside for now ##

# Calculate monthly values 
VAR_WRF_month = VAR_WRF.resample(Time='MS').mean(dim='Time')
VAR_obs_month = VAR_obs.resample(Time='MS').mean(dim='Time')
print(VAR_WRF_month)
print(VAR_obs_month)

# --------------- May, Jun, Jul, Aug -----
VAR_WRF_May = VAR_WRF_month[0,:,:]
VAR_WRF_Jun = VAR_WRF_month[1,:,:]
VAR_WRF_Jul = VAR_WRF_month[2,:,:]
VAR_WRF_Aug = VAR_WRF_month[3,:,:]
print(VAR_WRF_May)

VAR_obs_May = VAR_obs_month[1,:,:]
VAR_obs_Jun = VAR_obs_month[2,:,:]
VAR_obs_Jul = VAR_obs_month[3,:,:]
VAR_obs_Aug = VAR_obs_month[4,:,:]
print(VAR_obs_May)

VAR_bias_May = VAR_WRF_May - VAR_obs_May
VAR_bias_Jun = VAR_WRF_Jun - VAR_obs_Jun
VAR_bias_Jul = VAR_WRF_Jul - VAR_obs_Jul
VAR_bias_Aug = VAR_WRF_Aug - VAR_obs_Aug
print(VAR_bias_May)

# ------ panel plot ---------
map_crs = cartopy.crs.PlateCarree()
data_crs = cartopy.crs.PlateCarree()

fig = plt.figure()


ax = fig.add_subplot(3, 4, 1, projection=map_crs)
ax.set_extent([233,292,18,57], crs=map_crs)
ax.coastlines()
ax.set_title('WRF, May')
ax.contourf(VAR_WRF_May['lon'], VAR_WRF_May['lat'], VAR_WRF_May, transform=data_crs) 

plt.show()
#fig.savefig('test.png', dpi=600, bbox_inches='tight')




