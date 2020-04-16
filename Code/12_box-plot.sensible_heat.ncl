;Function: box plot analysis

load "/home/qin5/Programming/NCL/my_funcs_and_procs/Calendar.ncl"

begin

dir_WRF = "/home/qin5/Data/WRF.postprocessing.extract.hourly.nc"
dir_WRF_Thom = "/home/qin5/Data/WRF.postprocessing.extract.hourly.Thom.nc"

f_WRF = addfile(dir_WRF,"r")
f_WRF_Thom = addfile(dir_WRF_Thom,"r")

dir_ARMBE2D_05 = "/home/qin5/Data/ARMBE2DGRID/sgparmbe2dgridX1.c1.20110501.000000.nc"
dir_ARMBE2D_06 = "/home/qin5/Data/ARMBE2DGRID/sgparmbe2dgridX1.c1.20110601.000000.nc"
dir_ARMBE2D_07 = "/home/qin5/Data/ARMBE2DGRID/sgparmbe2dgridX1.c1.20110701.000000.nc"
dir_ARMBE2D_08 = "/home/qin5/Data/ARMBE2DGRID/sgparmbe2dgridX1.c1.20110801.000000.nc"
f_ARM_05 = addfile(dir_ARMBE2D_05,"r")
f_ARM_06 = addfile(dir_ARMBE2D_06,"r")
f_ARM_07 = addfile(dir_ARMBE2D_07,"r")
f_ARM_08 = addfile(dir_ARMBE2D_08,"r")

lat_1 = 35.0
lat_2 = 38.0
lon_1 = -99.0
lon_2 = -96.0

;;========= WRF areal average 
HFX_regrid = f_WRF->HFX_regrid

HFX_WRF_SGP = dim_avg_n_Wrap(dim_avg_n_Wrap(HFX_regrid(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)

HFX_WRF_SGP_May = HFX_WRF_SGP(0:737)
HFX_WRF_SGP_Jun = HFX_WRF_SGP(738:1457)
HFX_WRF_SGP_Jul = HFX_WRF_SGP(1458:2201)
HFX_WRF_SGP_Aug = HFX_WRF_SGP(2202:)

;--------- WRF_Thom areal average
HFX_regrid_Thom = f_WRF_Thom->HFX_regrid

HFX_WRF_Thom_SGP = dim_avg_n_Wrap(dim_avg_n_Wrap(HFX_regrid_Thom(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)

HFX_WRF_Thom_SGP_May = HFX_WRF_Thom_SGP(:)
;---------- uncomment
;HFX_WRF_Thom_SGP_May = HFX_WRF_Thom_SGP(0:737)
;HFX_WRF_Thom_SGP_Jun = HFX_WRF_Thom_SGP(738:1457)
;HFX_WRF_Thom_SGP_Jul = HFX_WRF_Thom_SGP(1458:2201)
;HFX_WRF_Thom_SGP_Aug = HFX_WRF_Thom_SGP(2202:)
;-------

;;----------ARMBE2DGRID areal average----------------
sh05 = f_ARM_05->sensible_heat_flux
sh06 = f_ARM_06->sensible_heat_flux
sh07 = f_ARM_07->sensible_heat_flux
sh08 = f_ARM_08->sensible_heat_flux

sh05 = -sh05
sh06 = -sh06
sh07 = -sh07
sh08 = -sh08

sh_ARM_SGP_May = dim_avg_n_Wrap(dim_avg_n_Wrap(sh05(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)
sh_ARM_SGP_Jun = dim_avg_n_Wrap(dim_avg_n_Wrap(sh06(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)
sh_ARM_SGP_Jul = dim_avg_n_Wrap(dim_avg_n_Wrap(sh07(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)
sh_ARM_SGP_Aug = dim_avg_n_Wrap(dim_avg_n_Wrap(sh08(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)

;;----------------- Calculate box-plot stats of WRF
May_box_val = new((/3,5/),double)
Jun_box_val = new((/3,5/),double)
Jul_box_val = new((/3,5/),double)
Aug_box_val = new((/3,5/),double)

WRF_stats_temp = stat_dispersion(HFX_WRF_SGP_May,False)
WRF_IQR =  WRF_stats_temp(10) - WRF_stats_temp(6)
May_box_val(0,0) = WRF_stats_temp(6) - 1.5 * WRF_IQR ; 1.5 interquartile range between the end of the whiskers and the lower quartile
May_box_val(0,1) = WRF_stats_temp(6) ; lower quartile
May_box_val(0,2) = WRF_stats_temp(8) ; median
May_box_val(0,3) = WRF_stats_temp(10) ; upper quartile
May_box_val(0,4) = WRF_stats_temp(10) + 1.5 * WRF_IQR

WRF_stats_temp = stat_dispersion(HFX_WRF_SGP_Jun,False)
WRF_IQR =  WRF_stats_temp(10) - WRF_stats_temp(6)
Jun_box_val(0,0) = WRF_stats_temp(6) - 1.5 * WRF_IQR ; 1.5 interquartile range between the end of the whiskers and the lower quartile
Jun_box_val(0,1) = WRF_stats_temp(6) ; lower quartile
Jun_box_val(0,2) = WRF_stats_temp(8) ; median
Jun_box_val(0,3) = WRF_stats_temp(10) ; upper quartile
Jun_box_val(0,4) = WRF_stats_temp(10) + 1.5 * WRF_IQR

WRF_stats_temp = stat_dispersion(HFX_WRF_SGP_Jul,False)
WRF_IQR =  WRF_stats_temp(10) - WRF_stats_temp(6)
Jul_box_val(0,0) = WRF_stats_temp(6) - 1.5 * WRF_IQR ; 1.5 interquartile range between the end of the whiskers and the lower quartile
Jul_box_val(0,1) = WRF_stats_temp(6) ; lower quartile
Jul_box_val(0,2) = WRF_stats_temp(8) ; median
Jul_box_val(0,3) = WRF_stats_temp(10) ; upper quartile
Jul_box_val(0,4) = WRF_stats_temp(10) + 1.5 * WRF_IQR

WRF_stats_temp = stat_dispersion(HFX_WRF_SGP_Aug,False)
WRF_IQR =  WRF_stats_temp(10) - WRF_stats_temp(6)
Aug_box_val(0,0) = WRF_stats_temp(6) - 1.5 * WRF_IQR ; 1.5 interquartile range between the end of the whiskers and the lower quartile
Aug_box_val(0,1) = WRF_stats_temp(6) ; lower quartile
Aug_box_val(0,2) = WRF_stats_temp(8) ; median
Aug_box_val(0,3) = WRF_stats_temp(10) ; upper quartile
Aug_box_val(0,4) = WRF_stats_temp(10) + 1.5 * WRF_IQR

;------------------- calculate box-plot stats of WRF_Thom
WRF_stats_temp = stat_dispersion(HFX_WRF_Thom_SGP_May,False)
WRF_IQR =  WRF_stats_temp(10) - WRF_stats_temp(6)
May_box_val(1,0) = WRF_stats_temp(6) - 1.5 * WRF_IQR ; 1.5 interquartile range between the end of the whiskers and the lower quartile
May_box_val(1,1) = WRF_stats_temp(6) ; lower quartile
May_box_val(1,2) = WRF_stats_temp(8) ; median
May_box_val(1,3) = WRF_stats_temp(10) ; upper quartile
May_box_val(1,4) = WRF_stats_temp(10) + 1.5 * WRF_IQR

;--------- uncomment
;WRF_stats_temp = stat_dispersion(HFX_WRF_Thom_SGP_Jun,False)
;WRF_IQR =  WRF_stats_temp(10) - WRF_stats_temp(6)
;Jun_box_val(1,0) = WRF_stats_temp(6) - 1.5 * WRF_IQR ; 1.5 interquartile range between the end of the whiskers and the lower quartile
;Jun_box_val(1,1) = WRF_stats_temp(6) ; lower quartile
;Jun_box_val(1,2) = WRF_stats_temp(8) ; median
;Jun_box_val(1,3) = WRF_stats_temp(10) ; upper quartile
;Jun_box_val(1,4) = WRF_stats_temp(10) + 1.5 * WRF_IQR
;
;WRF_stats_temp = stat_dispersion(HFX_WRF_Thom_SGP_Jul,False)
;WRF_IQR =  WRF_stats_temp(10) - WRF_stats_temp(6)
;Jul_box_val(1,0) = WRF_stats_temp(6) - 1.5 * WRF_IQR ; 1.5 interquartile range between the end of the whiskers and the lower quartile
;Jul_box_val(1,1) = WRF_stats_temp(6) ; lower quartile
;Jul_box_val(1,2) = WRF_stats_temp(8) ; median
;Jul_box_val(1,3) = WRF_stats_temp(10) ; upper quartile
;Jul_box_val(1,4) = WRF_stats_temp(10) + 1.5 * WRF_IQR
;
;WRF_stats_temp = stat_dispersion(HFX_WRF_Thom_SGP_Aug,False)
;WRF_IQR =  WRF_stats_temp(10) - WRF_stats_temp(6)
;Aug_box_val(1,0) = WRF_stats_temp(6) - 1.5 * WRF_IQR ; 1.5 interquartile range between the end of the whiskers and the lower quartile
;Aug_box_val(1,1) = WRF_stats_temp(6) ; lower quartile
;Aug_box_val(1,2) = WRF_stats_temp(8) ; median
;Aug_box_val(1,3) = WRF_stats_temp(10) ; upper quartile
;Aug_box_val(1,4) = WRF_stats_temp(10) + 1.5 * WRF_IQR

;;---------------- Calculate box-plot stats of ARMBE

ARM_stats_temp = stat_dispersion(sh_ARM_SGP_May,False)
ARM_IQR =  ARM_stats_temp(10) - ARM_stats_temp(6)
May_box_val(2,0) = ARM_stats_temp(6) - 1.5 * ARM_IQR ; 1.5 interquartile range between the end of the whiskers and the lower quartile
May_box_val(2,1) = ARM_stats_temp(6) ; lower quartile
May_box_val(2,2) = ARM_stats_temp(8) ; median
May_box_val(2,3) = ARM_stats_temp(10) ; upper quartile
May_box_val(2,4) = ARM_stats_temp(10) + 1.5 * ARM_IQR

ARM_stats_temp = stat_dispersion(sh_ARM_SGP_Jun,False)
ARM_IQR =  ARM_stats_temp(10) - ARM_stats_temp(6)
Jun_box_val(2,0) = ARM_stats_temp(6) - 1.5 * ARM_IQR ; 1.5 interquartile range between the end of the whiskers and the lower quartile
Jun_box_val(2,1) = ARM_stats_temp(6) ; lower quartile
Jun_box_val(2,2) = ARM_stats_temp(8) ; median
Jun_box_val(2,3) = ARM_stats_temp(10) ; upper quartile
Jun_box_val(2,4) = ARM_stats_temp(10) + 1.5 * ARM_IQR

ARM_stats_temp = stat_dispersion(sh_ARM_SGP_Jul,False)
ARM_IQR =  ARM_stats_temp(10) - ARM_stats_temp(6)
Jul_box_val(2,0) = ARM_stats_temp(6) - 1.5 * ARM_IQR ; 1.5 interquartile range between the end of the whiskers and the lower quartile
Jul_box_val(2,1) = ARM_stats_temp(6) ; lower quartile
Jul_box_val(2,2) = ARM_stats_temp(8) ; median
Jul_box_val(2,3) = ARM_stats_temp(10) ; upper quartile
Jul_box_val(2,4) = ARM_stats_temp(10) + 1.5 * ARM_IQR

ARM_stats_temp = stat_dispersion(sh_ARM_SGP_Aug,False)
ARM_IQR =  ARM_stats_temp(10) - ARM_stats_temp(6)
Aug_box_val(2,0) = ARM_stats_temp(6) - 1.5 * ARM_IQR ; 1.5 interquartile range between the end of the whiskers and the lower quartile
Aug_box_val(2,1) = ARM_stats_temp(6) ; lower quartile
Aug_box_val(2,2) = ARM_stats_temp(8) ; median
Aug_box_val(2,3) = ARM_stats_temp(10) ; upper quartile
Aug_box_val(2,4) = ARM_stats_temp(10) + 1.5 * ARM_IQR

;;--------------plot ------------
wks = gsn_open_wks("x11","../Figure/box-plot.sensible_heat_flux")

plot = new(4,graphic)

res = True
res@tiMainString = "Sensible heat flux box plot, May"
res@tiYAxisString = "W/m2"

res@trYMinF = -500.0
res@trYMaxF = 700.0

res@tmXBLabels = (/"WRF_Morri","WRF_Thom","ARMBE2D"/) ; labels for each box

x_axis = (/1.0, 2.0, 3.0/)

yval_May = May_box_val

opti = True
opti@boxWidth = 0.40
opti@boxColors = (/"blue","green","black"/)

plot(0) = boxplot(wks,x_axis,yval_May,opti,res,False)

;----------- uncomment
;yval_Jun = Jun_box_val
;res@tiMainString = "Sensible heat flux box plot, Jun"
;plot(1) = boxplot(wks,x_axis,yval_Jun,opti,res,False)
;
;yval_Jul = Jul_box_val
;res@tiMainString = "Sensible heat flux box plot, Jul"
;plot(2) = boxplot(wks,x_axis,yval_Jul,opti,res,False)
;
;yval_Aug = Aug_box_val
;res@tiMainString = "Sensible heat flux box plot, Aug"
;plot(3) = boxplot(wks,x_axis,yval_Aug,opti,res,False)

;------------------------

resP = True

resP@amJust = "TopRight"
gsn_panel(wks,plot,(/1,4/),resP)


end
