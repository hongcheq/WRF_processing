'''
Function: analysis for WRF 2011 May-Aug outputs, as in VanWeverberg CAUSES paper Figure 13.
Date: 20200325
'''

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import pandas

#label_string = "_Morr"
label_string = "_Thom"

ds_WRF = xr.open_dataset('/home/qin5/Data/WRF.postprocessing.extract.hourly.Thom.nc')

ds_pr_stage4 = xr.open_dataset('/home/qin5/Data/Precip_StageIV/Precip_Stage_IV.2011045678.postprocessing.extract.hourly.nc')

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

print(RAIN_WRF_MJJA.coords['time'][0:24])
#print(RAIN_WRF_JJA.coords['time'][0:24])

#WRF_May = RAIN_WRF_May.groupby('time.hour').mean()
#WRF_JJA = RAIN_WRF_JJA.groupby('time.hour').mean()
WRF_MJJA = RAIN_WRF_MJJA.groupby('time.hour').mean()
print(WRF_MJJA)

### Stage IV precip obs

pr_st4 = ds_pr_stage4['precip_st4_regrid'][718:,:,:]  # skip Apr values, only retain May 1st - Aug 31st
pr_st4 = pr_st4 * 24.0 # from mm/hr to mm/day
pr_st4.attrs['units'] = "mm/day"

pr_st4_MJJA = pr_st4.sel(lat=slice(lat_1, lat_2), lon=slice(lon_1, lon_2)).mean(dim='lat').mean(dim='lon')
print(pr_st4_MJJA)

### the time variable in this stage IV precip is -regular, 
### so using groupby('time.hour').mean() should not entail issues
### the Apr 01 - Aug 31 have 2943 values, can't be divided by 24, (contain missing values?) 
### as a result using for loop over that 24 hour may encouter issues
pr_st4_MJJA_diurnal = pr_st4_MJJA.groupby('time.hour').mean()
###ARM_JJA = precip_JJA.groupby('time.hour').mean()
print(pr_st4_MJJA_diurnal)

####pr_st4_SGP_MJJA = np.zeros(24)

#for i in np.arange(0,92,1):
#    ARM_JJA = ARM_JJA + precip_JJA[i*24:i*24+24].values
#ARM_JJA = ARM_JJA / 92.0

##for i in np.arange(0,31+92,1):
##    pr_st4_SGP_MJJA = pr_st4_SGP_MJJA + pr_st4_MJJA[i*24:i*24+24].values
##pr_st4_SGP_MJJA = pr_st4_SGP_MJJA / (31.0 + 92.0)
##print(pr_st4_SGP_MJJA)

### WRF bias in May, and JJA ###
bias_MJJA = WRF_MJJA - pr_st4_MJJA_diurnal

### Plot ###
#x_axis = WRF_May.coords['hour']
x_axis = WRF_MJJA.coords['hour']

fig = plt.figure(figsize=(9,10))
fontsize = 7
pos_adjust1 = 0.04

ax1 = fig.add_subplot(3,1,1)
ax1.text(s='Precip bias, WRF - StageIV_precip', x=0, y=1.02, ha='left', va='bottom', \
        fontsize=fontsize, transform=ax1.transAxes)
#ax1.plot(x_axis, bias_May.values, 'r-', label='precip,May')
ax1.plot(x_axis, bias_MJJA.values, 'r--', label='precip,MJJA')
#ax1.set_yticks(np.arange(-2.0,9.1,1.0))
ax1.axhline(linewidth=1.5, color='k')
ax1.set_xticks(np.arange(0.0,24.,3.0))
ax1.set_xticklabels(np.arange(0+24-6,24+24-6,3) % 24 )
ax1.set(xlabel='LST(hr), UTC-6', ylabel='WRF precip bias, mm/day', title='Precip, WRF'+label_string+' vs StageIV')
ax1.grid()
ax1.legend(loc='upper right')

ax2 = fig.add_subplot(3,1,2)
ax2.text(s='Precip, WRF', x=0, y=1.02, ha='left', va='bottom', \
        fontsize=fontsize, transform=ax2.transAxes)
#ax2.plot(x_axis, WRF_May.values, 'b-', label='precip,May')
ax2.plot(x_axis, WRF_MJJA.values, 'b--', label='precip,MJJA')
#ax2.set_yticks(np.arange(0.0,9.1,1.0))
ax2.set_xticks(np.arange(0.0,24.,3.0))
ax2.set_xticklabels(np.arange(0+24-6,24+24-6,3) % 24 )
ax2.set(xlabel='LST(hr), UTC-6', ylabel='WRF precip, mm/day')
ax2.grid()
ax2.legend(loc='upper right')

ax3 = fig.add_subplot(3,1,3)
ax3.text(s='precip,StageIV@SGP', x=0, y=1.02, ha='left', va='bottom', \
        fontsize=fontsize, transform=ax3.transAxes)
#ax3.plot(x_axis, ARM_May, 'k-', label='precip,May')
ax3.plot(x_axis, pr_st4_MJJA_diurnal, 'k--', label='precip,MJJA')
#ax3.set_yticks(np.arange(0.0,9.1,1.0))
ax3.set_xticks(np.arange(0.0,24.,3.0))
ax3.set_xticklabels(np.arange(0+24-6,24+24-6,3) % 24 )
ax3.set(xlabel='LST(hr), UTC-6', ylabel='precip Stage IV @SGP, mm/day')
ax3.grid()
ax3.legend(loc='upper right')

fig.savefig("../Figure/Precip.Diurnal.MJJA.StageIV.WRF_vs_ARM_SGP."+label_string+".png",dpi=600)
plt.show()








