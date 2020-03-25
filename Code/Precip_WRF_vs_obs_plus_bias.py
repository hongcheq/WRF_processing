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

VAR_WRF_str = "RAIN_tot_regrid"
VAR_obs_str = "prect"
VAR_label = "precip"

WRF_file = "/home/qin5/Data/WRF.postprocessing.extract.nc"
obs_file = "/home/qin5/Data/CAUSES_obs/prect_gpcp_2011_daily.nc"

#WRF_ds = xr.open_dataset(WRF_file, decode_times=False)
WRF_ds = xr.open_dataset(WRF_file)
obs_ds = xr.open_dataset(obs_file)
print(WRF_ds)
print(obs_ds)

VAR_WRF = WRF_ds[VAR_WRF_str]
print(VAR_WRF)
VAR_obs = obs_ds[VAR_obs_str]
print(VAR_obs)

### Note that the lat, lon dimension name must be the same when subtracting using xarray
### Otherwise, 2D - 2D produces a 4D data array with (lat,lon, latitude, longitude)
VAR_obs = VAR_obs.rename({'longitude':'lon'})
#VAR_obs['lon'] = WRF_ds['lon']
VAR_obs = VAR_obs.rename({'latitude':'lat'})
#VAR_obs['lat'] = WRF_ds['lat']
print(VAR_obs)

# Calculate monthly values 
VAR_WRF_month = VAR_WRF.resample(Time='MS').mean(dim='Time')
VAR_obs_month = VAR_obs.resample(time='MS').mean(dim='time')
print(VAR_WRF_month)
print(VAR_obs_month)

# --------------- May, Jun, Jul, Aug -----
VAR_WRF_May = VAR_WRF_month[0,:,:]
VAR_WRF_Jun = VAR_WRF_month[1,:,:]
VAR_WRF_Jul = VAR_WRF_month[2,:,:]
VAR_WRF_Aug = VAR_WRF_month[3,:,:]
print(VAR_WRF_May)

VAR_obs_May = VAR_obs_month[4,:,:]
VAR_obs_Jun = VAR_obs_month[5,:,:]
VAR_obs_Jul = VAR_obs_month[6,:,:]
VAR_obs_Aug = VAR_obs_month[7,:,:]
print(VAR_obs_May)

VAR_bias_May = VAR_WRF_May - VAR_obs_May 
VAR_bias_Jun = VAR_WRF_Jun - VAR_obs_Jun
VAR_bias_Jul = VAR_WRF_Jul - VAR_obs_Jul
VAR_bias_Aug = VAR_WRF_Aug - VAR_obs_Aug

print(VAR_WRF_May.shape)
print(VAR_obs_May.shape)
print(VAR_bias_May)

# ------ panel plot ---------
map_crs = cartopy.crs.PlateCarree()
data_crs = cartopy.crs.PlateCarree()

fig = plt.figure()
fontsize = 5
pos_adjust1 = 0.04
cmap_str_op1 = 'YlGnBu'
cmap_str_op2 = 'RdBu'

levels_op1 = np.arange(0.0,7.1,0.5)
levels_op2 = np.arange(-4,4.1,0.25)

units_str = 'mm/day'

obs_source = 'GPCP'

####

ax1 = fig.add_subplot(3, 4, 1, projection=map_crs)
ax1.set_extent([233,292,18,57], crs=map_crs)
# add country borders (110m resolution defaults)
ax1.add_feature(cartopy.feature.BORDERS)
# add states/provinces by first importing the shape file from Natural Earth
states_provinces = cartopy.feature.NaturalEarthFeature(category='cultural',\
                    name='admin_1_states_provinces_lakes_shp',scale='110m', facecolor='none')
ax1.add_feature(states_provinces, edgecolor='0')
ax1.coastlines()

ax1.text(s='WRF, May', x=0, y=1.02, ha='left', va='bottom', fontsize=fontsize, transform=ax1.transAxes)
ax1.text(s=VAR_label, x=0.98, y=1.02, ha='right', va='bottom', fontsize=fontsize, transform=ax1.transAxes)

contourf_plot1 = ax1.contourf(VAR_WRF_May['lon'],VAR_WRF_May['lat'],VAR_WRF_May,\
        levels=levels_op1,cmap=cmap_str_op1, transform=data_crs, extend='both')

ax1_pos = ax1.get_position()
cbar1_ax = fig.add_axes([ax1_pos.x0,ax1_pos.y0-pos_adjust1,ax1_pos.width,0.03])
cbar1 = plt.colorbar(contourf_plot1, cax=cbar1_ax, orientation='horizontal')
cbar1_ax.tick_params(labelsize=fontsize)
cbar1.set_label(units_str, fontsize=fontsize)

########## subplot(3,4,2) #####
ax2 = fig.add_subplot(3, 4, 2, projection=map_crs)

ax2.set_extent([233,292,18,57], crs=map_crs)
# add country borders (110m resolution defaults)
ax2.add_feature(cartopy.feature.BORDERS)
ax2.add_feature(states_provinces, edgecolor='0')
ax2.coastlines()

ax2.text(s='WRF, Jun', x=0, y=1.02, ha='left', va='bottom', fontsize=fontsize, transform=ax2.transAxes)
ax2.text(s=VAR_label, x=0.98, y=1.02, ha='right', va='bottom', fontsize=fontsize, transform=ax2.transAxes)
contourf_plot2 = ax2.contourf(VAR_WRF_Jun['lon'],VAR_WRF_Jun['lat'],VAR_WRF_Jun,\
        levels=levels_op1,cmap=cmap_str_op1, transform=data_crs, extend='both')

ax2_pos = ax2.get_position()
cbar2_ax = fig.add_axes([ax2_pos.x0,ax2_pos.y0-pos_adjust1,ax2_pos.width,0.03])
cbar2 = plt.colorbar(contourf_plot2, cax=cbar2_ax, orientation='horizontal')
cbar2_ax.tick_params(labelsize=fontsize)
cbar2.set_label(units_str, fontsize=fontsize)

########### subplot(3,4,3) ######
ax3 = fig.add_subplot(3, 4, 3, projection=map_crs)

ax3.set_extent([233,292,18,57], crs=map_crs)
# add country borders (110m resolution defaults)
ax3.add_feature(cartopy.feature.BORDERS)
ax3.add_feature(states_provinces, edgecolor='0')
ax3.coastlines()

ax3.text(s='WRF, Jul', x=0, y=1.02, ha='left', va='bottom', fontsize=fontsize, transform=ax3.transAxes)
ax3.text(s=VAR_label, x=0.98, y=1.02, ha='right', va='bottom', fontsize=fontsize, transform=ax3.transAxes)
contourf_plot3 = ax3.contourf(VAR_WRF_Jul['lon'],VAR_WRF_Jul['lat'],VAR_WRF_Jul,\
        levels=levels_op1,cmap=cmap_str_op1, transform=data_crs, extend='both')

ax3_pos = ax3.get_position()
cbar3_ax = fig.add_axes([ax3_pos.x0,ax3_pos.y0-pos_adjust1,ax3_pos.width,0.03])
cbar3 = plt.colorbar(contourf_plot3, cax=cbar3_ax, orientation='horizontal')
cbar3_ax.tick_params(labelsize=fontsize)
cbar3.set_label(units_str, fontsize=fontsize)

########### subplot(3,4,4) ######
ax4 = fig.add_subplot(3, 4, 4, projection=map_crs)

ax4.set_extent([233,292,18,57], crs=map_crs)
# add country borders (110m resolution defaults)
ax4.add_feature(cartopy.feature.BORDERS)
ax4.add_feature(states_provinces, edgecolor='0')
ax4.coastlines()

ax4.text(s='WRF, Aug', x=0, y=1.02, ha='left', va='bottom', fontsize=fontsize, transform=ax4.transAxes)
ax4.text(s=VAR_label, x=0.98, y=1.02, ha='right', va='bottom', fontsize=fontsize, transform=ax4.transAxes)
contourf_plot4 = ax4.contourf(VAR_WRF_Aug['lon'],VAR_WRF_Aug['lat'],VAR_WRF_Aug,\
        levels=levels_op1,cmap=cmap_str_op1, transform=data_crs, extend='both')

ax4_pos = ax4.get_position()
cbar4_ax = fig.add_axes([ax4_pos.x0,ax4_pos.y0-pos_adjust1,ax4_pos.width,0.03])
cbar4 = plt.colorbar(contourf_plot4, cax=cbar4_ax, orientation='horizontal')
cbar4_ax.tick_params(labelsize=fontsize)
cbar4.set_label(units_str, fontsize=fontsize)

######## subplot(3,4,5) ########
ax5 = fig.add_subplot(3, 4, 5, projection=map_crs)

ax5.set_extent([233,292,18,57], crs=map_crs)
# add country borders (110m resolution defaults)
ax5.add_feature(cartopy.feature.BORDERS)
ax5.add_feature(states_provinces, edgecolor='0')
ax5.coastlines()

ax5.text(s=obs_source+', May', x=0, y=1.02, ha='left', va='bottom', fontsize=fontsize, transform=ax5.transAxes)
ax5.text(s=VAR_label, x=0.98, y=1.02, ha='right', va='bottom', fontsize=fontsize, transform=ax5.transAxes)
contourf_plot5 = ax5.contourf(VAR_obs_May['lon'],VAR_obs_May['lat'],VAR_obs_May,\
        levels=levels_op1,cmap=cmap_str_op1, transform=data_crs, extend='both')

ax5_pos = ax5.get_position()
cbar5_ax = fig.add_axes([ax5_pos.x0,ax5_pos.y0-pos_adjust1,ax5_pos.width,0.03])
cbar5 = plt.colorbar(contourf_plot5, cax=cbar5_ax, orientation='horizontal')
cbar5_ax.tick_params(labelsize=fontsize)
cbar5.set_label(units_str, fontsize=fontsize)

### subplot(3,4,6) #####
ax6 = fig.add_subplot(3, 4, 6, projection=map_crs)

ax6.set_extent([233,292,18,57], crs=map_crs)
# add country borders (110m resolution defaults)
ax6.add_feature(cartopy.feature.BORDERS)
ax6.add_feature(states_provinces, edgecolor='0')
ax6.coastlines()

ax6.text(s=obs_source+', Jun', x=0, y=1.02, ha='left', va='bottom', fontsize=fontsize, transform=ax6.transAxes)
ax6.text(s=VAR_label, x=0.98, y=1.02, ha='right', va='bottom', fontsize=fontsize, transform=ax6.transAxes)
contourf_plot6 = ax6.contourf(VAR_obs_Jun['lon'],VAR_obs_Jun['lat'],VAR_obs_Jun,\
        levels=levels_op1,cmap=cmap_str_op1, transform=data_crs, extend='both')

ax6_pos = ax6.get_position()
cbar6_ax = fig.add_axes([ax6_pos.x0,ax6_pos.y0-pos_adjust1,ax6_pos.width,0.03])
cbar6 = plt.colorbar(contourf_plot6, cax=cbar6_ax, orientation='horizontal')
cbar6_ax.tick_params(labelsize=fontsize)
cbar6.set_label(units_str, fontsize=fontsize)

### subplot(3,4,7) #####
ax7 = fig.add_subplot(3, 4, 7, projection=map_crs)

ax7.set_extent([233,292,18,57], crs=map_crs)
# add country borders (110m resolution defaults)
ax7.add_feature(cartopy.feature.BORDERS)
ax7.add_feature(states_provinces, edgecolor='0')
ax7.coastlines()

ax7.text(s=obs_source+', Jul', x=0, y=1.02, ha='left', va='bottom', fontsize=fontsize, transform=ax7.transAxes)
ax7.text(s=VAR_label, x=0.98, y=1.02, ha='right', va='bottom', fontsize=fontsize, transform=ax7.transAxes)
contourf_plot7 = ax7.contourf(VAR_obs_Jul['lon'],VAR_obs_Jul['lat'],VAR_obs_Jul,\
        levels=levels_op1,cmap=cmap_str_op1, transform=data_crs, extend='both')

ax7_pos = ax7.get_position()
cbar7_ax = fig.add_axes([ax7_pos.x0,ax7_pos.y0-pos_adjust1,ax7_pos.width,0.03])
cbar7 = plt.colorbar(contourf_plot7, cax=cbar7_ax, orientation='horizontal')
cbar7_ax.tick_params(labelsize=fontsize)
cbar7.set_label(units_str, fontsize=fontsize)

### subplot (3,4,8) ###
ax8 = fig.add_subplot(3, 4, 8, projection=map_crs)

ax8.set_extent([233,292,18,57], crs=map_crs)
# add country borders (110m resolution defaults)
ax8.add_feature(cartopy.feature.BORDERS)
ax8.add_feature(states_provinces, edgecolor='0')
ax8.coastlines()

ax8.text(s=obs_source+', Aug', x=0, y=1.02, ha='left', va='bottom', fontsize=fontsize, transform=ax8.transAxes)
ax8.text(s=VAR_label, x=0.98, y=1.02, ha='right', va='bottom', fontsize=fontsize, transform=ax8.transAxes)
contourf_plot8 = ax8.contourf(VAR_obs_Aug['lon'],VAR_obs_Aug['lat'],VAR_obs_Aug,\
        levels=levels_op1,cmap=cmap_str_op1, transform=data_crs, extend='both')

ax8_pos = ax8.get_position()
cbar8_ax = fig.add_axes([ax8_pos.x0,ax8_pos.y0-pos_adjust1,ax8_pos.width,0.03])
cbar8 = plt.colorbar(contourf_plot8, cax=cbar8_ax, orientation='horizontal')
cbar8_ax.tick_params(labelsize=fontsize)
cbar8.set_label(units_str, fontsize=fontsize)

### subplot(3,4,9) ###
ax9 = fig.add_subplot(3, 4, 9, projection=map_crs)

ax9.set_extent([233,292,18,57], crs=map_crs)
# add country borders (110m resolution defaults)
ax9.add_feature(cartopy.feature.BORDERS)
ax9.add_feature(states_provinces, edgecolor='0')
ax9.coastlines()


ax9.text(s='WRF-'+obs_source+', May', x=0, y=1.02, ha='left', va='bottom', fontsize=fontsize, transform=ax9.transAxes)
ax9.text(s=VAR_label, x=0.98, y=1.02, ha='right', va='bottom', fontsize=fontsize, transform=ax9.transAxes)
print(VAR_bias_May)
contourf_plot9 = ax9.contourf(VAR_bias_May['lon'],VAR_bias_May['lat'],VAR_bias_May,\
        levels=levels_op2,cmap=cmap_str_op2, transform=data_crs, extend='both')

ax9_pos = ax9.get_position()
cbar9_ax = fig.add_axes([ax9_pos.x0,ax9_pos.y0-pos_adjust1,ax9_pos.width,0.03])
cbar9 = plt.colorbar(contourf_plot9, cax=cbar9_ax, orientation='horizontal')
cbar9_ax.tick_params(labelsize=fontsize)
cbar9.set_label(units_str, fontsize=fontsize)

### subplot(3,4,10) ###
ax10 = fig.add_subplot(3, 4, 10, projection=map_crs)

ax10.set_extent([233,292,18,57], crs=map_crs)
ax10.add_feature(cartopy.feature.BORDERS)
ax10.add_feature(states_provinces, edgecolor='0')
ax10.coastlines()

ax10.text(s='WRF-'+obs_source+', Jun', x=0, y=1.02, ha='left', va='bottom', fontsize=fontsize, transform=ax10.transAxes)
ax10.text(s=VAR_label, x=0.98, y=1.02, ha='right', va='bottom', fontsize=fontsize, transform=ax10.transAxes)
contourf_plot10 = ax10.contourf(VAR_bias_Jun['lon'],VAR_bias_Jun['lat'],VAR_bias_Jun,\
        levels=levels_op2,cmap=cmap_str_op2, transform=data_crs, extend='both')

ax10_pos = ax10.get_position()
cbar10_ax = fig.add_axes([ax10_pos.x0,ax10_pos.y0-pos_adjust1,ax10_pos.width,0.03])
cbar10 = plt.colorbar(contourf_plot10, cax=cbar10_ax, orientation='horizontal')
cbar10_ax.tick_params(labelsize=fontsize)
cbar10.set_label(units_str, fontsize=fontsize)

### subplot(3,4,11) ###
ax11 = fig.add_subplot(3, 4, 11, projection=map_crs)

ax11.set_extent([233,292,18,57], crs=map_crs)
ax11.add_feature(cartopy.feature.BORDERS)
ax11.add_feature(states_provinces, edgecolor='0')
ax11.coastlines()

ax11.text(s='WRF-'+obs_source+', Jul', x=0, y=1.02, ha='left', va='bottom', fontsize=fontsize, transform=ax11.transAxes)
ax11.text(s=VAR_label, x=0.98, y=1.02, ha='right', va='bottom', fontsize=fontsize, transform=ax11.transAxes)
contourf_plot11 = ax11.contourf(VAR_bias_Jul['lon'],VAR_bias_Jul['lat'],VAR_bias_Jul,\
        levels=levels_op2,cmap=cmap_str_op2, transform=data_crs, extend='both')

ax11_pos = ax11.get_position()
cbar11_ax = fig.add_axes([ax11_pos.x0,ax11_pos.y0-pos_adjust1,ax11_pos.width,0.03])
cbar11 = plt.colorbar(contourf_plot11, cax=cbar11_ax, orientation='horizontal')
cbar11_ax.tick_params(labelsize=fontsize)
cbar11.set_label(units_str, fontsize=fontsize)

### subplot(3,4,12) ###
ax12 = fig.add_subplot(3, 4, 12, projection=map_crs)

ax12.set_extent([233,292,18,57], crs=map_crs)
ax12.add_feature(cartopy.feature.BORDERS)
ax12.add_feature(states_provinces, edgecolor='0')
ax12.coastlines()

ax12.text(s='WRF-'+obs_source+', Aug', x=0, y=1.02, ha='left', va='bottom', fontsize=fontsize, transform=ax12.transAxes)
ax12.text(s=VAR_label, x=0.98, y=1.02, ha='right', va='bottom', fontsize=fontsize, transform=ax12.transAxes)
contourf_plot12 = ax12.contourf(VAR_bias_Aug['lon'],VAR_bias_Aug['lat'],VAR_bias_Aug,\
        levels=levels_op2,cmap=cmap_str_op2, transform=data_crs, extend='both')

ax12_pos = ax12.get_position()
cbar12_ax = fig.add_axes([ax12_pos.x0,ax12_pos.y0-pos_adjust1,ax12_pos.width,0.03])
cbar12 = plt.colorbar(contourf_plot12, cax=cbar12_ax, orientation='horizontal')
cbar12_ax.tick_params(labelsize=fontsize)
cbar12.set_label(units_str, fontsize=fontsize)


#plt.show()
#fig.savefig('../Figure/'+VAR_WRF_str+'.png', dpi=600, bbox_inches='tight')
fig.savefig('../Figure/'+VAR_WRF_str+'.pdf', bbox_inches='tight')




