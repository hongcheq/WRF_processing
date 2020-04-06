'''
Function: analysis for WRF 2011 May-Aug outputs, as in Ma CAUSES paper Figure 15.
Date: 20200325
'''

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import pandas
import matplotlib.dates as mdates

ds_WRF = xr.open_dataset('/home/qin5/Data/WRF.postprocessing.extract.hourly.nc')
ds_SM_WRF = xr.open_dataset('/home/qin5/Data/WRF.postprocessing.extract.hourly.SMOIS.nc')

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
RAIN_tot_regrid = ds_WRF['RAIN_tot_regrid']
RAIN_WRF_daily = RAIN_tot_regrid.resample(time='1D').mean(dim='time')
RAIN_WRF_SGP = RAIN_WRF_daily.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
RAIN_WRF_SGP = RAIN_WRF_SGP * 24.0 # from mm/hr to mm/day
RAIN_WRF_SGP.attrs['units'] = "mm/day"
#print(RAIN_WRF_SGP)

#### accumulative rain
RAIN_WRF_ACC = np.asarray([RAIN_WRF_SGP[0:i].values.sum() for i in np.arange(0,122,1)])
RAIN_WRF_ACC = xr.DataArray(RAIN_WRF_ACC, dims=('time'), coords = {'time':RAIN_WRF_SGP.coords['time'] })
RAIN_WRF_ACC.attrs['units'] = "mm"
RAIN_WRF_ACC.attrs['long_name'] = "accumulated total precip"
#print(RAIN_WRF_ACC)

### -------- calculate evaporation from latent heat
Lv_water = 2264705.0 # J/kg

LH_regrid = ds_WRF['LH_regrid']
LH_WRF_daily = LH_regrid.resample(time='1D').mean(dim='time')
LH_WRF_SGP = LH_WRF_daily.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
LH_WRF_SGP_W_m2 = LH_WRF_SGP
LH_WRF_SGP = LH_WRF_SGP * 3600.0*24.0/Lv_water # from W/m2 to mm/day
LH_WRF_SGP.attrs['units'] = "mm/day"
LH_WRF_SGP.attrs['long_name'] = "ET converted from latent heat flux, mm/day"
#print(LH_WRF_SGP)

#### accumulative evaporation
evap_WRF_ACC = np.asarray([LH_WRF_SGP[0:i].values.sum() for i in np.arange(0,122,1)])
evap_WRF_ACC = xr.DataArray(evap_WRF_ACC, dims=('time'), coords = {'time':LH_WRF_SGP.coords['time'] })
evap_WRF_ACC.attrs['units'] = "mm"
evap_WRF_ACC.attrs['long_name'] = "accumulated ET, converted from latent heat flux"
#print(evap_WRF_ACC)

### soil moisture at 5cm depth 
SMOIS_regrid = ds_SM_WRF['SMOIS_regrid'][:,0,:,:]   # depth 0 is 5-cm
SMOIS_WRF_daily = SMOIS_regrid.resample(time='1D').mean(dim='time')
SMOIS_WRF_SGP = SMOIS_WRF_daily.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
SMOIS_WRF_SGP.attrs['units'] = "m3/m3"
#print(SMOIS_WRF_SGP)

### soil moisture at 0.25 depth
SMOIS25_regrid = ds_SM_WRF['SMOIS_regrid'][:,1,:,:]   # depth 0 is 25-cm
SMOIS25_WRF_daily = SMOIS25_regrid.resample(time='1D').mean(dim='time')
SMOIS25_WRF_SGP = SMOIS25_WRF_daily.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
SMOIS25_WRF_SGP.attrs['units'] = "m3/m3"
#print(SMOIS25_WRF_SGP)

### evaporative fraction LH/(SH+LH)
HFX_regrid = ds_WRF['HFX_regrid']
EF_regrid = LH_regrid / (HFX_regrid+LH_regrid)
EF_regrid = EF_regrid.where( (HFX_regrid+LH_regrid) > 10.0)  # to avoid unrealistic values when denominator is too small 

EF_WRF_daily = EF_regrid.resample(time='1D').mean(dim='time')
EF_WRF_SGP = EF_WRF_daily.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
EF_WRF_SGP.attrs['units'] = "unitless"
#print(EF_WRF_SGP)

### Sensible heat flux
HFX_WRF_daily = HFX_regrid.resample(time='1D').mean(dim='time')
HFX_WRF_SGP = HFX_WRF_daily.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
HFX_WRF_SGP.attrs['units'] = "unitless"
#print(EF_WRF_SGP)

### T2m
T2_regrid = ds_WRF['T2_regrid']
T2_WRF_daily = T2_regrid.resample(time='1D').mean(dim='time')
T2_WRF_SGP = T2_WRF_daily.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
#print(T2_WRF_SGP)

### ---------------------------
### ARM SGP obs: ARMBE2DGRID from Qi Tang

precip05 = ds_ARMBE2D_05['precip_rate']
precip06 = ds_ARMBE2D_06['precip_rate']
precip07 = ds_ARMBE2D_07['precip_rate']
precip08 = ds_ARMBE2D_08['precip_rate']
precip_05678 = xr.concat([precip05, precip06, precip07, precip08], dim='time')
precip_daily = precip_05678.resample(time='1D').mean('time')
precip_ARM_SGP = precip_daily.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
precip_ARM_SGP = precip_ARM_SGP * 24.0 # from mm/hr to mm/day
precip_ARM_SGP.attrs['units'] = "mm/day"
#print(precip_ARM_SGP)

### accumulative rain
precip_ARM_ACC = np.asarray([precip_ARM_SGP[0:i].values.sum() for i in np.arange(0,123,1)])
precip_ARM_ACC = xr.DataArray(precip_ARM_ACC, dims=('time'), coords = {'time':precip_ARM_SGP.coords['time'] })
precip_ARM_ACC.attrs['units'] = "mm"
precip_ARM_ACC.attrs['long_name'] = "accumulated total precip"
#print(precip_ARM_ACC)

### evaporation converted from latent heat flux
latent05 = -ds_ARMBE2D_05['latent_heat_flux'] # upward means positive
latent06 = -ds_ARMBE2D_06['latent_heat_flux']
latent07 = -ds_ARMBE2D_07['latent_heat_flux']
latent08 = -ds_ARMBE2D_08['latent_heat_flux']
latent_05678 = xr.concat([latent05, latent06, latent07, latent08], dim='time')
latent_daily = latent_05678.resample(time='1D').mean('time')
latent_ARM_SGP = latent_daily.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
latent_ARM_SGP_W_m2 = latent_ARM_SGP
latent_ARM_SGP = latent_ARM_SGP * 3600.0*24.0/Lv_water # from W/m2 to mm/day 
latent_ARM_SGP.attrs['units'] = "mm/day"
#print(latent_ARM_SGP)

### accumulative ET
evap_ARM_ACC = np.asarray([latent_ARM_SGP[0:i].values.sum() for i in np.arange(0,123,1)])
evap_ARM_ACC = xr.DataArray(evap_ARM_ACC, dims=('time'), coords = {'time':latent_ARM_SGP.coords['time'] })
evap_ARM_ACC.attrs['units'] = "mm"
evap_ARM_ACC.attrs['long_name'] = "accumulated total ET, converted from latent heat flux"
#print(evap_ARM_ACC)

### soil moisture at 5-cm
SM05 = ds_ARMBE2D_05['soil_moisture_swats'][:,0,:,:] # 0 layer is 5-cm
SM06 = ds_ARMBE2D_06['soil_moisture_swats'][:,0,:,:]
SM07 = ds_ARMBE2D_07['soil_moisture_swats'][:,0,:,:]
SM08 = ds_ARMBE2D_08['soil_moisture_swats'][:,0,:,:]
SM_05678 = xr.concat([SM05, SM06, SM07, SM08], dim='time')
SM_daily = SM_05678.resample(time='1D').mean('time')
SM_ARM_SGP = SM_daily.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
SM_ARM_SGP.attrs['units'] = "m3/m3"
#print(SM_ARM_SGP)

### soil moisture at 25-cm
SM25_05 = ds_ARMBE2D_05['soil_moisture_swats'][:,2,:,:] # 2 layer is 25-cm
SM25_06 = ds_ARMBE2D_06['soil_moisture_swats'][:,2,:,:]
SM25_07 = ds_ARMBE2D_07['soil_moisture_swats'][:,2,:,:]
SM25_08 = ds_ARMBE2D_08['soil_moisture_swats'][:,2,:,:]
SM25_05678 = xr.concat([SM25_05, SM25_06, SM25_07, SM25_08], dim='time')
SM25_daily = SM25_05678.resample(time='1D').mean('time')
SM25_ARM_SGP = SM25_daily.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
SM25_ARM_SGP.attrs['units'] = "m3/m3"
#print(SM_ARM_SGP)

### soil moisture from ebbr measurements (only 2.5cm)
SM05_ebbr = ds_ARMBE2D_05['soil_moisture_ebbr']
SM06_ebbr = ds_ARMBE2D_06['soil_moisture_ebbr']
SM07_ebbr = ds_ARMBE2D_07['soil_moisture_ebbr']
SM08_ebbr = ds_ARMBE2D_08['soil_moisture_ebbr']
SM_05678_ebbr = xr.concat([SM05_ebbr, SM06_ebbr, SM07_ebbr, SM08_ebbr], dim='time')
SM_daily_ebbr = SM_05678_ebbr.resample(time='1D').mean('time')
SM_ARM_SGP_ebbr = SM_daily_ebbr.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
SM_ARM_SGP_ebbr.attrs['units'] = "m3/m3"

### evaporative fraction = LH/(SH+LH)
sensible05 = -ds_ARMBE2D_05['sensible_heat_flux'] # upward means positive
sensible06 = -ds_ARMBE2D_06['sensible_heat_flux']
sensible07 = -ds_ARMBE2D_07['sensible_heat_flux']
sensible08 = -ds_ARMBE2D_08['sensible_heat_flux']
sensible_05678 = xr.concat([sensible05, sensible06, sensible07, sensible08], dim='time')
EF_obs = latent_05678/(latent_05678+sensible_05678)
EF_obs = EF_obs.where( (latent_05678+sensible_05678) > 10.0)  # to avoid unrealistic values when denominator is too small. 

EF_daily = EF_obs.resample(time='1D').mean('time')
EF_ARM_SGP = EF_daily.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
EF_ARM_SGP.attrs['units'] = "unitless"

### Sensible heat flux
sensible_daily = sensible_05678.resample(time='1D').mean('time')
sensible_ARM_SGP = sensible_daily.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
sensible_ARM_SGP.attrs['units'] = "unitless"

### 2m air temperature 
temp05 = ds_ARMBE2D_05['temp'] 
temp06 = ds_ARMBE2D_06['temp']
temp07 = ds_ARMBE2D_07['temp']
temp08 = ds_ARMBE2D_08['temp']
temp_05678 = xr.concat([temp05, temp06, temp07, temp08], dim='time')
temp_daily = temp_05678.resample(time='1D').mean('time')
temp_ARM_SGP = temp_daily.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
#print(temp_ARM_SGP)

### ---------------------------
### Plot ###
x_axis = RAIN_WRF_ACC.coords['time']

### x-axis for datetime64
years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
days = mdates.DayLocator()
#dates_fmt = mdates.DateFormatter('%Y-%m-%d')
dates_fmt = mdates.DateFormatter('%m-%d')

fig = plt.figure(figsize=(10,10))
fontsize = 6
pos_adjust1 = 0.02

ax1 = fig.add_subplot(3,3,1)
ax1.text(s='Accumulated precip, mm', x=0, y=1.02, ha='left', va='bottom', \
        fontsize=fontsize, transform=ax1.transAxes)
ax1.plot(x_axis, RAIN_WRF_ACC.values, 'b-', label='precip, WRF')
## Note that WRF simulation does not have 08-31 data, only 122 values;
## Therefore, also omit 08-31 data in ARMBE when plotting.
ax1.plot(x_axis, precip_ARM_ACC[0:122].values, 'k-', label='precip, ARMBE2D')
ax1.grid()
ax1.legend(loc='upper left',fontsize=fontsize)
## format the ticks
ax1.xaxis.set_major_locator(months)
ax1.xaxis.set_major_formatter(dates_fmt)

### subplot (3,3,2)
ax2 = fig.add_subplot(3,3,2)
ax2.text(s='Accumulated ET (converted from LatentHeatFlux), mm', x=0, y=1.02, ha='left', va='bottom', \
        fontsize=fontsize, transform=ax2.transAxes)
ax2.plot(x_axis, evap_WRF_ACC.values, 'b-', label='ET, WRF')
ax2.plot(x_axis, evap_ARM_ACC[0:122].values, 'k-', label='ET, ARMBE2D')
ax2.grid()
ax2.legend(loc='upper left',fontsize=fontsize)
# format the ticks
ax2.xaxis.set_major_locator(months)
ax2.xaxis.set_major_formatter(dates_fmt)

### subplot (3,3,5)
ax3 = fig.add_subplot(3,3,3)
ax3.text(s='P-E (Accumulated), mm', x=0, y=1.02, ha='left', va='bottom', \
        fontsize=fontsize, transform=ax3.transAxes)
ax3.plot(x_axis, (RAIN_WRF_ACC.values - evap_WRF_ACC.values), 'b-', label='P-E, WRF')
ax3.plot(x_axis, (precip_ARM_ACC[0:122].values - evap_ARM_ACC[0:122].values), 'k-', label='P-E, ARMBE2D')
ax3.grid()
ax3.legend(loc='lower left',fontsize=fontsize)
# format the ticks
ax3.xaxis.set_major_locator(months)
ax3.xaxis.set_major_formatter(dates_fmt)

### subplot(3,3,4)
ax4 = fig.add_subplot(3,3,4)
ax4.text(s='soil moisture, m3/m3', x=0, y=1.02, ha='left', va='bottom', \
        fontsize=fontsize, transform=ax4.transAxes)
ax4.plot(x_axis, SMOIS_WRF_SGP.values, 'b-', label='SMOIS,5cm,WRF')
ax4.plot(x_axis, SM_ARM_SGP[0:122].values, 'k-', label='SM_swats,5cm,ARMBE2D')
ax4.plot(x_axis, SMOIS25_WRF_SGP.values, 'b+', label='SMOIS,25cm,WRF')
ax4.plot(x_axis, SM25_ARM_SGP[0:122].values, 'k+', label='SM_swats,25cm,ARMBE2D')
ax4.plot(x_axis, SM_ARM_SGP_ebbr[0:122].values, 'k--', label='SM_ebbr,2.5cm,ARMBE2D')
#ax4.set_ylim(0,0.4)
#ax4.set_yticks([0.0,0.1,0.2,0.3,0.4])
ax4.grid()
ax4.legend(loc='lower left',fontsize=fontsize)
# format the ticks
ax4.xaxis.set_major_locator(months)
ax4.xaxis.set_major_formatter(dates_fmt)

### subplot(3,3,4)
ax5 = fig.add_subplot(3,3,5)
ax5.text(s='EF bias, WRF-obs, (EF=LH/(SH+LH)), unitless', x=0, y=1.02, ha='left', va='bottom', \
        fontsize=fontsize, transform=ax5.transAxes)
ax5.plot(x_axis, (EF_WRF_SGP.values - EF_ARM_SGP[0:122].values) , 'g-', label='EF bias')
#ax5.plot(x_axis, EF_WRF_SGP.values , 'b-', label='EF WRF')
#ax5.plot(x_axis, EF_ARM_SGP[0:122].values, 'k-', label='EF obs')
ax5.grid()
ax5.legend(loc='lower left',fontsize=fontsize)
# format the ticks
ax5.xaxis.set_major_locator(months)
ax5.xaxis.set_major_formatter(dates_fmt)
ax5.axhline(linewidth=1.5, color='k')

### suplot(3,3,6)
ax6 = fig.add_subplot(3,3,6)
ax6.text(s='T2 bias, WRF-obs, K', x=0, y=1.02, ha='left', va='bottom', \
        fontsize=fontsize, transform=ax6.transAxes)
ax6.plot(x_axis, (T2_WRF_SGP.values - temp_ARM_SGP[0:122].values) , 'r-', label='T2m bias')
ax6.grid()
ax6.legend(loc='lower left',fontsize=fontsize)
# format the ticks
ax6.xaxis.set_major_locator(months)
ax6.xaxis.set_major_formatter(dates_fmt)
ax6.axhline(linewidth=1.5, color='k')

### Add precipitation rate
ax7 = fig.add_subplot(3,3,7)
ax7.text(s='Precip rate bias, mm/day', x=0, y=1.02, ha='left', va='bottom', \
        fontsize=fontsize, transform=ax7.transAxes)
ax7.plot(x_axis, RAIN_WRF_SGP.values - precip_ARM_SGP[0:122].values, 'k-', label='precip rate, WRF-ARMBE2D')
#ax7.plot(x_axis, precip_ARM_SGP[0:122].values, 'k-', label='precip rate, ARMBE2D')
ax7.grid()
ax7.legend(loc='upper left',fontsize=fontsize)
## format the ticks
ax7.xaxis.set_major_locator(months)
ax7.xaxis.set_major_formatter(dates_fmt)
ax7.axhline(linewidth=1.5, color='k')

### Add latent heat flux
ax8 = fig.add_subplot(3,3,8)
ax8.text(s='Latent heat flux bias, W/m2', x=0, y=1.02, ha='left', va='bottom', \
        fontsize=fontsize, transform=ax8.transAxes)
ax8.plot(x_axis, LH_WRF_SGP_W_m2.values - latent_ARM_SGP_W_m2[0:122].values , 'k-', label='LH, WRF-ARMBE2D')
#ax8.plot(x_axis, latent_ARM_SGP_W_m2[0:122].values, 'k-', label='LH, ARMBE2D')
ax8.grid()
ax8.legend(loc='upper left',fontsize=fontsize)
## format the ticks
ax8.xaxis.set_major_locator(months)
ax8.xaxis.set_major_formatter(dates_fmt)
ax8.axhline(linewidth=1.5, color='k')

### Add sensible heat flux
ax9 = fig.add_subplot(3,3,9)
ax9.text(s='Sensible heat flux bias, W/m2', x=0, y=1.02, ha='left', va='bottom', \
        fontsize=fontsize, transform=ax9.transAxes)
ax9.plot(x_axis, HFX_WRF_SGP.values - sensible_ARM_SGP[0:122].values , 'k-', label='SH, WRF-ARMBE2D')
#ax9.plot(x_axis, sensible_ARM_SGP[0:122].values, 'k-', label='SH, ARMBE2D')
ax9.grid()
ax9.legend(loc='upper left',fontsize=fontsize)
## format the ticks
ax9.xaxis.set_major_locator(months)
ax9.xaxis.set_major_formatter(dates_fmt)
ax9.axhline(linewidth=1.5, color='k')



###
#fig.savefig("../Figure/Figure15.WRF_vs_ARM_SGP.png",dpi=600, bbox_inches='tight')
fig.savefig("../Figure/Figure15.WRF_vs_ARM_SGP.png",dpi=600)
plt.show()








