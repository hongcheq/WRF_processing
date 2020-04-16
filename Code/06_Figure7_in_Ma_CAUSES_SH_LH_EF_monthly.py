'''
Function: analysis for WRF 2011 May-Aug outputs, as in Ma CAUSES paper Figure 8.
Date: 20200325
'''

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import pandas

ds_WRF = xr.open_dataset('/home/qin5/Data/WRF.postprocessing.extract.hourly.nc')
ds_WRF_Thom = xr.open_dataset('/home/qin5/Data/WRF.postprocessing.extract.hourly.Thom.nc')

ds_FLUXNET = xr.open_dataset('/home/qin5/Data/CAUSES_obs/LE_H_FLUXNET_2011_conus_1dgrid.nc',\
        decode_times=False)

ds_GLEAM = xr.open_dataset('/home/qin5/Data/GLEAM/E_2011_GLEAM.processed.daily.nc')

ds_ARMBE2D_05 = xr.open_dataset('/home/qin5/Data/ARMBE2DGRID/sgparmbe2dgridX1.c1.20110501.000000.nc')
ds_ARMBE2D_06 = xr.open_dataset('/home/qin5/Data/ARMBE2DGRID/sgparmbe2dgridX1.c1.20110601.000000.nc')
ds_ARMBE2D_07 = xr.open_dataset('/home/qin5/Data/ARMBE2DGRID/sgparmbe2dgridX1.c1.20110701.000000.nc')
ds_ARMBE2D_08 = xr.open_dataset('/home/qin5/Data/ARMBE2DGRID/sgparmbe2dgridX1.c1.20110801.000000.nc')

## Figure 8 in Ma et al 2018, average over 35-38N, 99-96W, consistent with ARMBE2D from Qi Tang
lat_1 = 35.0
lat_2 = 38.0
lon_1 = -99.0
lon_2 = -96.0

### WRF  at ARM SGP site 
LH_regrid = ds_WRF['LH_regrid']
HFX_regrid = ds_WRF['HFX_regrid']

LH_WRF_month = LH_regrid.resample(time='MS').mean(dim='time')
LH_WRF_May = LH_WRF_month[0,:,:]
LH_WRF_Jun = LH_WRF_month[1,:,:]
LH_WRF_Jul = LH_WRF_month[2,:,:]
LH_WRF_Aug = LH_WRF_month[3,:,:]
LH_WRF_JJA = (LH_WRF_Jun + LH_WRF_Jul + LH_WRF_Aug)/3.0
LH_WRF_MJJA = (LH_WRF_May + LH_WRF_Jun + LH_WRF_Jul + LH_WRF_Aug)/4.0

HFX_WRF_month = HFX_regrid.resample(time='MS').mean(dim='time')
HFX_WRF_May = HFX_WRF_month[0,:,:]
HFX_WRF_Jun = HFX_WRF_month[1,:,:]
HFX_WRF_Jul = HFX_WRF_month[2,:,:]
HFX_WRF_Aug = HFX_WRF_month[3,:,:]
HFX_WRF_JJA = (HFX_WRF_Jun + HFX_WRF_Jul + HFX_WRF_Aug)/3.0
HFX_WRF_MJJA = (HFX_WRF_May + HFX_WRF_Jun + HFX_WRF_Jul + HFX_WRF_Aug)/4.0

L_WRF_May = LH_WRF_May.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
L_WRF_Jun = LH_WRF_Jun.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
L_WRF_Jul = LH_WRF_Jul.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
L_WRF_Aug = LH_WRF_Aug.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
L_WRF_JJA = LH_WRF_JJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
L_WRF_MJJA = LH_WRF_MJJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')

SH_WRF_May = HFX_WRF_May.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
SH_WRF_Jun = HFX_WRF_Jun.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
SH_WRF_Jul = HFX_WRF_Jul.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
SH_WRF_Aug = HFX_WRF_Aug.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
SH_WRF_JJA = HFX_WRF_JJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
SH_WRF_MJJA = HFX_WRF_MJJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')

### Add evaporative fraction here 
EF_WRF_May = L_WRF_May / (L_WRF_May + SH_WRF_May)
EF_WRF_Jun = L_WRF_Jun / (L_WRF_Jun + SH_WRF_Jun)
EF_WRF_Jul = L_WRF_Jul / (L_WRF_Jul + SH_WRF_Jul)
EF_WRF_Aug = L_WRF_Aug / (L_WRF_Aug + SH_WRF_Aug)
EF_WRF_JJA = L_WRF_JJA / (L_WRF_JJA + SH_WRF_JJA)
EF_WRF_MJJA = L_WRF_MJJA / (L_WRF_MJJA + SH_WRF_MJJA)

###### WRF_Thom
LH_regrid_Thom = ds_WRF_Thom['LH_regrid']
HFX_regrid_Thom = ds_WRF_Thom['HFX_regrid']

LH_WRF_Thom_month = LH_regrid_Thom.resample(time='MS').mean(dim='time')
LH_WRF_Thom_May = LH_WRF_Thom_month[0,:,:]
LH_WRF_Thom_Jun = LH_WRF_Thom_month[1,:,:]
LH_WRF_Thom_Jul = LH_WRF_Thom_month[2,:,:]
LH_WRF_Thom_Aug = LH_WRF_Thom_month[3,:,:]
LH_WRF_Thom_JJA = (LH_WRF_Thom_Jun + LH_WRF_Thom_Jul + LH_WRF_Thom_Aug)/3.0
LH_WRF_Thom_MJJA = (LH_WRF_Thom_May + LH_WRF_Thom_Jun + LH_WRF_Thom_Jul + LH_WRF_Thom_Aug)/4.0

HFX_WRF_Thom_month = HFX_regrid_Thom.resample(time='MS').mean(dim='time')
HFX_WRF_Thom_May = HFX_WRF_Thom_month[0,:,:]
HFX_WRF_Thom_Jun = HFX_WRF_Thom_month[1,:,:]
HFX_WRF_Thom_Jul = HFX_WRF_Thom_month[2,:,:]
HFX_WRF_Thom_Aug = HFX_WRF_Thom_month[3,:,:]
HFX_WRF_Thom_JJA = (HFX_WRF_Thom_Jun + HFX_WRF_Thom_Jul + HFX_WRF_Thom_Aug)/3.0
HFX_WRF_Thom_MJJA = (HFX_WRF_Thom_May + HFX_WRF_Thom_Jun + HFX_WRF_Thom_Jul + HFX_WRF_Thom_Aug)/4.0

L_WRF_Thom_May = LH_WRF_Thom_May.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
L_WRF_Thom_Jun = LH_WRF_Thom_Jun.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
L_WRF_Thom_Jul = LH_WRF_Thom_Jul.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
L_WRF_Thom_Aug = LH_WRF_Thom_Aug.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
L_WRF_Thom_JJA = LH_WRF_Thom_JJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
L_WRF_Thom_MJJA = LH_WRF_Thom_MJJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')

SH_WRF_Thom_May = HFX_WRF_Thom_May.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
SH_WRF_Thom_Jun = HFX_WRF_Thom_Jun.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
SH_WRF_Thom_Jul = HFX_WRF_Thom_Jul.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
SH_WRF_Thom_Aug = HFX_WRF_Thom_Aug.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
SH_WRF_Thom_JJA = HFX_WRF_Thom_JJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
SH_WRF_Thom_MJJA = HFX_WRF_Thom_MJJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')

### Add evaporative fraction here 
EF_WRF_Thom_May = L_WRF_Thom_May / (L_WRF_Thom_May + SH_WRF_Thom_May)
EF_WRF_Thom_Jun = L_WRF_Thom_Jun / (L_WRF_Thom_Jun + SH_WRF_Thom_Jun)
EF_WRF_Thom_Jul = L_WRF_Thom_Jul / (L_WRF_Thom_Jul + SH_WRF_Thom_Jul)
EF_WRF_Thom_Aug = L_WRF_Thom_Aug / (L_WRF_Thom_Aug + SH_WRF_Thom_Aug)
EF_WRF_Thom_JJA = L_WRF_Thom_JJA / (L_WRF_Thom_JJA + SH_WRF_Thom_JJA)
EF_WRF_Thom_MJJA = L_WRF_Thom_MJJA / (L_WRF_Thom_MJJA + SH_WRF_Thom_MJJA)


### -----Add FLUXNET to reveal the observational uncertainties------------- ###
hfls = ds_FLUXNET['hfls']
hfss = ds_FLUXNET['hfss']

hfls = hfls.rename({'latitude':'lat'})
hfls = hfls.rename({'longitude':'lon'})
hfss = hfss.rename({'latitude':'lat'})
hfss = hfss.rename({'longitude':'lon'})

LH_FLUX_May = hfls[4,:,:]
LH_FLUX_Jun = hfls[5,:,:]
LH_FLUX_Jul = hfls[6,:,:]
LH_FLUX_Aug = hfls[7,:,:]
LH_FLUX_JJA = (LH_FLUX_Jun + LH_FLUX_Jul + LH_FLUX_Aug)/3.0
LH_FLUX_MJJA = (LH_FLUX_May + LH_FLUX_Jun + LH_FLUX_Jul + LH_FLUX_Aug)/4.0

HFX_FLUX_May = hfss[4,:,:]
HFX_FLUX_Jun = hfss[5,:,:]
HFX_FLUX_Jul = hfss[6,:,:]
HFX_FLUX_Aug = hfss[7,:,:]
HFX_FLUX_JJA = (HFX_FLUX_Jun + HFX_FLUX_Jul + HFX_FLUX_Aug)/3.0
HFX_FLUX_MJJA = (HFX_FLUX_May + HFX_FLUX_Jun + HFX_FLUX_Jul + HFX_FLUX_Aug)/4.0

L_FLUX_May = LH_FLUX_May.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
L_FLUX_Jun = LH_FLUX_Jun.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
L_FLUX_Jul = LH_FLUX_Jul.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
L_FLUX_Aug = LH_FLUX_Aug.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
L_FLUX_JJA = LH_FLUX_JJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
L_FLUX_MJJA = LH_FLUX_MJJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')

SH_FLUX_May = HFX_FLUX_May.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
SH_FLUX_Jun = HFX_FLUX_Jun.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
SH_FLUX_Jul = HFX_FLUX_Jul.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
SH_FLUX_Aug = HFX_FLUX_Aug.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
SH_FLUX_JJA = HFX_FLUX_JJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
SH_FLUX_MJJA = HFX_FLUX_MJJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')

### Add evaporative fraction here 
EF_FLUX_May = L_FLUX_May / (L_FLUX_May + SH_FLUX_May)
EF_FLUX_Jun = L_FLUX_Jun / (L_FLUX_Jun + SH_FLUX_Jun)
EF_FLUX_Jul = L_FLUX_Jul / (L_FLUX_Jul + SH_FLUX_Jul)
EF_FLUX_Aug = L_FLUX_Aug / (L_FLUX_Aug + SH_FLUX_Aug)
EF_FLUX_JJA = L_FLUX_JJA / (L_FLUX_JJA + SH_FLUX_JJA)
EF_FLUX_MJJA = L_FLUX_MJJA / (L_FLUX_MJJA + SH_FLUX_MJJA)

### add GLEAM model evaporation for LH to constain the uncertainties
E_a_regrid = ds_GLEAM['E_a_regrid']
E_b_regrid = ds_GLEAM['E_b_regrid']

E_a_regrid = E_a_regrid * 2265000.0 / (3600*24) # from mm/hr to W/m2
E_a_regrid.attrs['units'] = "W/m2"
E_b_regrid = E_b_regrid * 2265000.0 / (3600*24) # from mm/hr to W/m2
E_b_regrid.attrs['units'] = "W/m2"

E_a_month = E_a_regrid.resample(time='MS').mean(dim='time')
E_b_month = E_b_regrid.resample(time='MS').mean(dim='time')

E_a_May = E_a_month[4,:,:]
E_a_Jun = E_a_month[5,:,:]
E_a_Jul = E_a_month[6,:,:]
E_a_Aug = E_a_month[7,:,:]
E_a_JJA = (E_a_Jun + E_a_Jul + E_a_Aug)/3.0
E_a_MJJA = (E_a_May + E_a_Jun + E_a_Jul + E_a_Aug)/4.0

E_b_May = E_b_month[4,:,:]
E_b_Jun = E_b_month[5,:,:]
E_b_Jul = E_b_month[6,:,:]
E_b_Aug = E_b_month[7,:,:]
E_b_JJA = (E_b_Jun + E_b_Jul + E_b_Aug)/3.0
E_b_MJJA = (E_b_May + E_b_Jun + E_b_Jul + E_b_Aug)/4.0

Ea_GLEAM_May = E_a_May.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
Ea_GLEAM_Jun = E_a_Jun.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
Ea_GLEAM_Jul = E_a_Jul.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
Ea_GLEAM_Aug = E_a_Aug.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
Ea_GLEAM_JJA = E_a_JJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
Ea_GLEAM_MJJA = E_a_MJJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')

Eb_GLEAM_May = E_b_May.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
Eb_GLEAM_Jun = E_b_Jun.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
Eb_GLEAM_Jul = E_b_Jul.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
Eb_GLEAM_Aug = E_b_Aug.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
Eb_GLEAM_JJA = E_b_JJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
Eb_GLEAM_MJJA = E_b_MJJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')

### ---------------------
### ARM SGP obs: ARMBE2DGRID from Qi Tang

latent05 = -ds_ARMBE2D_05['latent_heat_flux'] # make it positive going upward
latent06 = -ds_ARMBE2D_06['latent_heat_flux']
latent07 = -ds_ARMBE2D_07['latent_heat_flux']
latent08 = -ds_ARMBE2D_08['latent_heat_flux']

sensible05 = -ds_ARMBE2D_05['sensible_heat_flux'] # make it positive going upward
sensible06 = -ds_ARMBE2D_06['sensible_heat_flux']
sensible07 = -ds_ARMBE2D_07['sensible_heat_flux']
sensible08 = -ds_ARMBE2D_08['sensible_heat_flux']

latent_05678 = xr.concat([latent05, latent06, latent07, latent08], dim='time')
latent_05678 = latent_05678.resample(time='MS').mean(dim='time')
latent_May = latent_05678[0,:,:]
latent_Jun = latent_05678[1,:,:]
latent_Jul = latent_05678[2,:,:]
latent_Aug = latent_05678[3,:,:]
latent_JJA = (latent_Jun + latent_Jul + latent_Aug)/3.0
latent_MJJA = (latent_May + latent_Jun + latent_Jul + latent_Aug)/4.0

sensible_05678 = xr.concat([sensible05, sensible06, sensible07, sensible08], dim='time')
sensible_05678 = sensible_05678.resample(time='MS').mean(dim='time')
sensible_May = sensible_05678[0,:,:]
sensible_Jun = sensible_05678[1,:,:]
sensible_Jul = sensible_05678[2,:,:]
sensible_Aug = sensible_05678[3,:,:]
sensible_JJA = (sensible_Jun + sensible_Jul + sensible_Aug)/3.0
sensible_MJJA = (sensible_May + sensible_Jun + sensible_Jul + sensible_Aug)/4.0

L_ARM_May = latent_May.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
L_ARM_Jun = latent_Jun.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
L_ARM_Jul = latent_Jul.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
L_ARM_Aug = latent_Aug.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
L_ARM_JJA = latent_JJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
L_ARM_MJJA = latent_MJJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')

SH_ARM_May = sensible_May.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
SH_ARM_Jun = sensible_Jun.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
SH_ARM_Jul = sensible_Jul.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
SH_ARM_Aug = sensible_Aug.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
SH_ARM_JJA = sensible_JJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
SH_ARM_MJJA = sensible_MJJA.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')

### Add evaporative fraction here ###
EF_ARM_May = L_ARM_May / (L_ARM_May + SH_ARM_May)
EF_ARM_Jun = L_ARM_Jun / (L_ARM_Jun + SH_ARM_Jun)
EF_ARM_Jul = L_ARM_Jul / (L_ARM_Jul + SH_ARM_Jul)
EF_ARM_Aug = L_ARM_Aug / (L_ARM_Aug + SH_ARM_Aug)
EF_ARM_JJA = L_ARM_JJA / (L_ARM_JJA + SH_ARM_JJA)
EF_ARM_MJJA = L_ARM_MJJA / (L_ARM_MJJA + SH_ARM_MJJA)

### Plot ###
x_axis = ['May','Jun','Jul','Aug','JJA','MJJA']

fig = plt.figure(figsize=(7,9))
fontsize = 6
pos_adjust1 = 0.04

ax1 = fig.add_subplot(3,1,1)
ax1.text(s='Latent Heat Flux, W/m2', x=0, y=1.02, ha='left', va='bottom', \
        fontsize=fontsize, transform=ax1.transAxes)
ax1.scatter(x_axis, [L_WRF_May, L_WRF_Jun, L_WRF_Jul, L_WRF_Aug, L_WRF_JJA, L_WRF_MJJA], c='b',marker='s', label='WRF_Morr')
ax1.scatter(x_axis, [L_WRF_Thom_May, L_WRF_Thom_Jun, L_WRF_Thom_Jul, L_WRF_Thom_Aug, L_WRF_Thom_JJA, L_WRF_Thom_MJJA], c='g',marker='s', label='WRF_Thom')
ax1.scatter(x_axis, [L_ARM_May, L_ARM_Jun, L_ARM_Jul, L_ARM_Aug, L_ARM_JJA, L_ARM_MJJA], c='r', marker='d', label='ARM obs')
ax1.scatter(x_axis, [L_FLUX_May, L_FLUX_Jun, L_FLUX_Jul, L_FLUX_Aug, L_FLUX_JJA, L_FLUX_MJJA], c='b', marker='d', label='FLUXNET obs')
ax1.scatter(x_axis, [Ea_GLEAM_May, Ea_GLEAM_Jun, Ea_GLEAM_Jul, Ea_GLEAM_Aug, Ea_GLEAM_JJA, Ea_GLEAM_MJJA], c='y', marker='d', label='GLEAM E_va')
ax1.scatter(x_axis, [Eb_GLEAM_May, Eb_GLEAM_Jun, Eb_GLEAM_Jul, Eb_GLEAM_Aug, Eb_GLEAM_JJA, Eb_GLEAM_MJJA], c='g', marker='d', label='GLEAM E_vb')
ax1.set_yticks(np.arange(40.0,170,20))
#ax1.set_xticks(np.arange(0.0,24.1,3.0))
ax1.set(xlabel='month category', ylabel='Latent heat flux, W/m2', title='WRF vs ARM SGP')
ax1.grid()
ax1.legend(loc='upper center')

ax2 = fig.add_subplot(3,1,2)
ax2.text(s='Sensible Heat Flux, W/m2', x=0, y=1.02, ha='left', va='bottom', \
        fontsize=fontsize, transform=ax2.transAxes)
ax2.scatter(x_axis, [SH_WRF_May, SH_WRF_Jun, SH_WRF_Jul, SH_WRF_Aug, SH_WRF_JJA, SH_WRF_MJJA], c='b',marker='s', label='WRF_Morr')
ax2.scatter(x_axis, [SH_WRF_Thom_May, SH_WRF_Thom_Jun, SH_WRF_Thom_Jul, SH_WRF_Thom_Aug, SH_WRF_Thom_JJA, SH_WRF_Thom_MJJA], c='g',marker='s', label='WRF_Thom')
ax2.scatter(x_axis, [SH_ARM_May, SH_ARM_Jun, SH_ARM_Jul, SH_ARM_Aug, SH_ARM_JJA, SH_ARM_MJJA], c='r', marker='d', label='ARM obs')
ax2.scatter(x_axis, [SH_FLUX_May, SH_FLUX_Jun, SH_FLUX_Jul, SH_FLUX_Aug, SH_FLUX_JJA, SH_FLUX_MJJA], c='b', marker='d', label='FLUXNET obs')
ax2.set(xlabel='month category', ylabel='Sensible heat flux, W/m2')
ax2.grid()
ax2.legend(loc='upper left')

ax3 = fig.add_subplot(3,1,3)
ax3.text(s='Evaporative Fraction, unitless', x=0, y=1.02, ha='left', va='bottom', \
        fontsize=fontsize, transform=ax3.transAxes)
ax3.scatter(x_axis, [EF_WRF_May, EF_WRF_Jun, EF_WRF_Jul, EF_WRF_Aug, EF_WRF_JJA, EF_WRF_MJJA], c='b',marker='s', label='WRF_Morr')
ax3.scatter(x_axis, [EF_WRF_Thom_May, EF_WRF_Thom_Jun, EF_WRF_Thom_Jul, EF_WRF_Thom_Aug, EF_WRF_Thom_JJA, EF_WRF_Thom_MJJA], c='g',marker='s', label='WRF_Thom')
ax3.scatter(x_axis, [EF_ARM_May, EF_ARM_Jun, EF_ARM_Jul, EF_ARM_Aug, EF_ARM_JJA, EF_ARM_MJJA], c='r', marker='d', label='ARM obs')
ax3.scatter(x_axis, [EF_FLUX_May, EF_FLUX_Jun, EF_FLUX_Jul, EF_FLUX_Aug, EF_FLUX_JJA, EF_FLUX_MJJA], c='b', marker='d', label='FLUXNET obs')
ax3.set(xlabel='month category', ylabel='Evaporative Fraction, unitless')
ax3.grid()
ax3.legend(loc='lower left')

fig.savefig("../Figure/Figure7.SH.LH.EF.WRF_Morri_Thom_vs_ARM_SGP_FLUXNET_GLEAM.png",dpi=600)
plt.show()








