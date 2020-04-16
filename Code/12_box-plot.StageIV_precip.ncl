;Function: box plot analysis

load "/home/qin5/Programming/NCL/my_funcs_and_procs/Calendar.ncl"

begin

dir_WRF = "/home/qin5/Data/WRF.postprocessing.extract.hourly.nc"
dir_WRF_Thom = "/home/qin5/Data/WRF.postprocessing.extract.hourly.Thom.nc"

f_WRF = addfile(dir_WRF,"r")
f_WRF_Thom = addfile(dir_WRF_Thom,"r")

obs_file = "/home/qin5/Data/Precip_StageIV/Precip_Stage_IV.2011045678.postprocessing.extract.hourly.nc"
obs_f = addfile(obs_file,"r")

lat_1 = 35.0
lat_2 = 38.0
lon_1 = -99.0
lon_2 = -96.0

;;========= WRF areal average 
RAIN_tot_regrid = f_WRF->RAIN_tot_regrid
;printVarSummary(RAIN_tot_regrid)

RAIN_WRF_SGP = dim_avg_n_Wrap(dim_avg_n_Wrap(RAIN_tot_regrid(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)
RAIN_WRF_SGP = RAIN_WRF_SGP * 24.0
RAIN_WRF_SGP@units = "mm/day"
printVarSummary(RAIN_WRF_SGP)

RAIN_WRF_SGP_May = RAIN_WRF_SGP(0:737)
RAIN_WRF_SGP_Jun = RAIN_WRF_SGP(738:1457)
RAIN_WRF_SGP_Jul = RAIN_WRF_SGP(1458:2201)
RAIN_WRF_SGP_Aug = RAIN_WRF_SGP(2202:)

;;--------;;;========= WRF_Thom
RAIN_tot_regrid_Thom = f_WRF_Thom->RAIN_tot_regrid

RAIN_WRF_Thom_SGP = dim_avg_n_Wrap(dim_avg_n_Wrap(RAIN_tot_regrid_Thom(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)
RAIN_WRF_Thom_SGP = RAIN_WRF_Thom_SGP * 24.0
RAIN_WRF_Thom_SGP@units = "mm/day"
printVarSummary(RAIN_WRF_Thom_SGP)

RAIN_WRF_Thom_SGP_May = RAIN_WRF_Thom_SGP(:) ; the test .nc only contains a few days.
;------- uncomment
;RAIN_WRF_Thom_SGP_May = RAIN_WRF_Thom_SGP(0:737)
;RAIN_WRF_Thom_SGP_Jun = RAIN_WRF_Thom_SGP(738:1457)
;RAIN_WRF_Thom_SGP_Jul = RAIN_WRF_Thom_SGP(1458:2201)
;RAIN_WRF_Thom_SGP_Aug = RAIN_WRF_Thom_SGP(2202:)
;-------

;;----------Stage IV areal average----------------
precip_st4 = obs_f->precip_st4_regrid(:,:,:)  

;; NaN values
if (any(isnan_ieee(precip_st4))) then
      value = 1.e20
      replace_ieeenan (precip_st4, value, 0)
      precip_st4@_FillValue = value
end if
printVarSummary(precip_st4)

precip_st4 = precip_st4 * 24.0 ; from mm accumulated per hour, i.e. mm/hour to mm/day
precip_st4@units = "mm/day"

precip_st4_SGP_May = dim_avg_n_Wrap(dim_avg_n_Wrap(precip_st4(718:1461,{lat_1:lat_2},{lon_1:lon_2}),1),1)

precip_st4_SGP_Jun = dim_avg_n_Wrap(dim_avg_n_Wrap(precip_st4(1462:2181,{lat_1:lat_2},{lon_1:lon_2}),1),1)

precip_st4_SGP_Jul = dim_avg_n_Wrap(dim_avg_n_Wrap(precip_st4(2180:2922,{lat_1:lat_2},{lon_1:lon_2}),1),1)

precip_st4_SGP_Aug = dim_avg_n_Wrap(dim_avg_n_Wrap(precip_st4(2923:,{lat_1:lat_2},{lon_1:lon_2}),1),1)

;;----------------- Calculate box-plot stats of WRF
May_box_val = new((/3,5/),double)
Jun_box_val = new((/3,5/),double)
Jul_box_val = new((/3,5/),double)
Aug_box_val = new((/3,5/),double)

WRF_stats_temp = stat_dispersion(RAIN_WRF_SGP_May,False)
WRF_IQR =  WRF_stats_temp(10) - WRF_stats_temp(6)
May_box_val(0,0) = WRF_stats_temp(6) - 1.5 * WRF_IQR ; 1.5 interquartile range between the end of the whiskers and the lower quartile
May_box_val(0,1) = WRF_stats_temp(6) ; lower quartile
May_box_val(0,2) = WRF_stats_temp(8) ; median
May_box_val(0,3) = WRF_stats_temp(10) ; upper quartile
May_box_val(0,4) = WRF_stats_temp(10) + 1.5 * WRF_IQR

WRF_stats_temp = stat_dispersion(RAIN_WRF_SGP_Jun,False)
WRF_IQR =  WRF_stats_temp(10) - WRF_stats_temp(6)
Jun_box_val(0,0) = WRF_stats_temp(6) - 1.5 * WRF_IQR ; 1.5 interquartile range between the end of the whiskers and the lower quartile
Jun_box_val(0,1) = WRF_stats_temp(6) ; lower quartile
Jun_box_val(0,2) = WRF_stats_temp(8) ; median
Jun_box_val(0,3) = WRF_stats_temp(10) ; upper quartile
Jun_box_val(0,4) = WRF_stats_temp(10) + 1.5 * WRF_IQR

WRF_stats_temp = stat_dispersion(RAIN_WRF_SGP_Jul,False)
WRF_IQR =  WRF_stats_temp(10) - WRF_stats_temp(6)
Jul_box_val(0,0) = WRF_stats_temp(6) - 1.5 * WRF_IQR ; 1.5 interquartile range between the end of the whiskers and the lower quartile
Jul_box_val(0,1) = WRF_stats_temp(6) ; lower quartile
Jul_box_val(0,2) = WRF_stats_temp(8) ; median
Jul_box_val(0,3) = WRF_stats_temp(10) ; upper quartile
Jul_box_val(0,4) = WRF_stats_temp(10) + 1.5 * WRF_IQR

WRF_stats_temp = stat_dispersion(RAIN_WRF_SGP_Aug,False)
WRF_IQR =  WRF_stats_temp(10) - WRF_stats_temp(6)
Aug_box_val(0,0) = WRF_stats_temp(6) - 1.5 * WRF_IQR ; 1.5 interquartile range between the end of the whiskers and the lower quartile
Aug_box_val(0,1) = WRF_stats_temp(6) ; lower quartile
Aug_box_val(0,2) = WRF_stats_temp(8) ; median
Aug_box_val(0,3) = WRF_stats_temp(10) ; upper quartile
Aug_box_val(0,4) = WRF_stats_temp(10) + 1.5 * WRF_IQR

;---------------- Calculate box-plot stas of WRF_Thom
WRF_stats_temp = stat_dispersion(RAIN_WRF_Thom_SGP_May,False)
WRF_IQR =  WRF_stats_temp(10) - WRF_stats_temp(6)
May_box_val(1,0) = WRF_stats_temp(6) - 1.5 * WRF_IQR ; 1.5 interquartile range between the end of the whiskers and the lower quartile
May_box_val(1,1) = WRF_stats_temp(6) ; lower quartile
May_box_val(1,2) = WRF_stats_temp(8) ; median
May_box_val(1,3) = WRF_stats_temp(10) ; upper quartile
May_box_val(1,4) = WRF_stats_temp(10) + 1.5 * WRF_IQR

;;---------- uncomment
;WRF_stats_temp = stat_dispersion(RAIN_WRF_Thom_SGP_Jun,False)
;WRF_IQR =  WRF_stats_temp(10) - WRF_stats_temp(6)
;Jun_box_val(1,0) = WRF_stats_temp(6) - 1.5 * WRF_IQR ; 1.5 interquartile range between the end of the whiskers and the lower quartile
;Jun_box_val(1,1) = WRF_stats_temp(6) ; lower quartile
;Jun_box_val(1,2) = WRF_stats_temp(8) ; median
;Jun_box_val(1,3) = WRF_stats_temp(10) ; upper quartile
;Jun_box_val(1,4) = WRF_stats_temp(10) + 1.5 * WRF_IQR
;
;WRF_stats_temp = stat_dispersion(RAIN_WRF_Thom_SGP_Jul,False)
;WRF_IQR =  WRF_stats_temp(10) - WRF_stats_temp(6)
;Jul_box_val(1,0) = WRF_stats_temp(6) - 1.5 * WRF_IQR ; 1.5 interquartile range between the end of the whiskers and the lower quartile
;Jul_box_val(1,1) = WRF_stats_temp(6) ; lower quartile
;Jul_box_val(1,2) = WRF_stats_temp(8) ; median
;Jul_box_val(1,3) = WRF_stats_temp(10) ; upper quartile
;Jul_box_val(1,4) = WRF_stats_temp(10) + 1.5 * WRF_IQR
;
;WRF_stats_temp = stat_dispersion(RAIN_WRF_Thom_SGP_Aug,False)
;WRF_IQR =  WRF_stats_temp(10) - WRF_stats_temp(6)
;Aug_box_val(1,0) = WRF_stats_temp(6) - 1.5 * WRF_IQR ; 1.5 interquartile range between the end of the whiskers and the lower quartile
;Aug_box_val(1,1) = WRF_stats_temp(6) ; lower quartile
;Aug_box_val(1,2) = WRF_stats_temp(8) ; median
;Aug_box_val(1,3) = WRF_stats_temp(10) ; upper quartile
;Aug_box_val(1,4) = WRF_stats_temp(10) + 1.5 * WRF_IQR
;----------------------------;


;;---------------- Calculate box-plot stats of ARMBE

st4_stats_temp = stat_dispersion(precip_st4_SGP_May,False)
st4_IQR =  st4_stats_temp(10) - st4_stats_temp(6)
May_box_val(2,0) = st4_stats_temp(6) - 1.5 * st4_IQR ; 1.5 interquartile range between the end of the whiskers and the lower quartile
May_box_val(2,1) = st4_stats_temp(6) ; lower quartile
May_box_val(2,2) = st4_stats_temp(8) ; median
May_box_val(2,3) = st4_stats_temp(10) ; upper quartile
May_box_val(2,4) = st4_stats_temp(10) + 1.5 * st4_IQR

st4_stats_temp = stat_dispersion(precip_st4_SGP_Jun,False)
st4_IQR =  st4_stats_temp(10) - st4_stats_temp(6)
Jun_box_val(2,0) = st4_stats_temp(6) - 1.5 * st4_IQR ; 1.5 interquartile range between the end of the whiskers and the lower quartile
Jun_box_val(2,1) = st4_stats_temp(6) ; lower quartile
Jun_box_val(2,2) = st4_stats_temp(8) ; median
Jun_box_val(2,3) = st4_stats_temp(10) ; upper quartile
Jun_box_val(2,4) = st4_stats_temp(10) + 1.5 * st4_IQR

st4_stats_temp = stat_dispersion(precip_st4_SGP_Jul,False)
st4_IQR =  st4_stats_temp(10) - st4_stats_temp(6)
Jul_box_val(2,0) = st4_stats_temp(6) - 1.5 * st4_IQR ; 1.5 interquartile range between the end of the whiskers and the lower quartile
Jul_box_val(2,1) = st4_stats_temp(6) ; lower quartile
Jul_box_val(2,2) = st4_stats_temp(8) ; median
Jul_box_val(2,3) = st4_stats_temp(10) ; upper quartile
Jul_box_val(2,4) = st4_stats_temp(10) + 1.5 * st4_IQR

st4_stats_temp = stat_dispersion(precip_st4_SGP_Aug,False)
st4_IQR =  st4_stats_temp(10) - st4_stats_temp(6)
Aug_box_val(2,0) = st4_stats_temp(6) - 1.5 * st4_IQR ; 1.5 interquartile range between the end of the whiskers and the lower quartile
Aug_box_val(2,1) = st4_stats_temp(6) ; lower quartile
Aug_box_val(2,2) = st4_stats_temp(8) ; median
Aug_box_val(2,3) = st4_stats_temp(10) ; upper quartile
Aug_box_val(2,4) = st4_stats_temp(10) + 1.5 * st4_IQR

;;--------------plot ------------
wks = gsn_open_wks("x11","../Figure/box-plot.precip_StageIV")

plot = new(4,graphic)

res = True
res@tiMainString = "Precip box plot, May"
res@tiYAxisString = "mm/day"

res@trYMinF = 0.0
res@trYMaxF = 3.0

res@tmXBLabels = (/"WRF_Morri","WRF_Thom","StageIV"/) ; labels for each box

x_axis = (/1.0, 2.0, 3.0/)

yval_May = May_box_val

opti = True
opti@boxWidth = 0.40
opti@boxColors = (/"blue","green","black"/)

plot(0) = boxplot(wks,x_axis,yval_May,opti,res,False)

;;--------- uncomment
;yval_Jun = Jun_box_val
;res@tiMainString = "Precip box plot, Jun"
;plot(1) = boxplot(wks,x_axis,yval_Jun,opti,res,False)
;
;yval_Jul = Jul_box_val
;res@tiMainString = "Precip box plot, Jul"
;plot(2) = boxplot(wks,x_axis,yval_Jul,opti,res,False)
;
;yval_Aug = Aug_box_val
;res@tiMainString = "Precip box plot, Aug"
;plot(3) = boxplot(wks,x_axis,yval_Aug,opti,res,False)
;
;------------------------

resP = True

resP@amJust = "TopRight"
gsn_panel(wks,plot,(/1,4/),resP)


end
