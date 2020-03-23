'''
Function: WRF output vs obs
Date: 20200322
'''

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy
import pandas
import datetime

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
VAR_WRF = VAR_WRF - 273.15 # from Kelvin to degree C
VAR_WRF.attrs['units'] = "degree Celsius"
print(VAR_WRF)

VAR_obs = obs_ds[VAR_obs_str]

print(VAR_obs)
